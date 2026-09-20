"""Firestore-backed cache-first helper."""

from datetime import datetime, timedelta, timezone
from typing import Callable, Any

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


def get_or_set(key: str, ttl: int, fn: Callable[[], Any]) -> Any:
    """
    Return a cached value when available and fresh.

    If the cache entry is missing or expired, call fn(), store the result,
    and return it.

    Args:
        key: Cache key. Call sites should provide a SHA-256 key.
        ttl: Cache lifetime in seconds.
        fn: Function used to produce the value on a cache miss.
    """
    client = _get_client()

    # Local development / Firestore disabled:
    # still execute the function normally.
    if client is None:
        return fn()

    doc_ref = client.collection("cache").document(key)
    snapshot = doc_ref.get()

    if snapshot.exists:
        data = snapshot.to_dict() or {}
        expires_at = data.get("expires_at")

        if expires_at and expires_at > datetime.now(timezone.utc):
            return data.get("value")

    value = fn()

    doc_ref.set(
        {
            "value": value,
            "expires_at": datetime.now(timezone.utc) + timedelta(seconds=ttl),
        }
    )

    return value