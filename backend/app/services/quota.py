"""Daily service quota counter backed by Firestore."""

from datetime import datetime, timezone
from typing import Optional

from google.cloud import firestore

from app.config import settings


_client = None


def _get_client():
    """Create the Firestore client lazily when Firestore is enabled."""
    global _client

    if not settings.firestore_enabled:
        return None

    if _client is None:
        _client = firestore.Client(project=settings.gcp_project_id)

    return _client


def check_and_increment(service_name: str) -> Optional[bool]:
    """
    Check whether a service call is allowed and increment its daily counter.

    Returns:
        True: the call is allowed and the counter was incremented.
        None: the daily quota has already been reached.
    """
    client = _get_client()

    # Local development / Firestore disabled.
    # Keep the service usable without making real Firestore calls.
    if client is None:
        return True

    today = datetime.now(timezone.utc).date().isoformat()
    key = f"{service_name}:{today}"

    doc_ref = client.collection("quota").document(key)
    snapshot = doc_ref.get()

    if snapshot.exists:
        data = snapshot.to_dict() or {}
        count = int(data.get("count", 0))
    else:
        count = 0

    if count >= settings.max_gemini_calls_per_day:
        return None

    doc_ref.set(
        {
            "service": service_name,
            "date": today,
            "count": count + 1,
        }
    )

    return True