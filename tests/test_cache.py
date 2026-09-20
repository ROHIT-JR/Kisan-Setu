import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from app.services import cache


class FakeSnapshot:
    def __init__(self, data=None):
        self._data = data
        self.exists = data is not None

    def to_dict(self):
        return self._data


class FakeDocument:
    def __init__(self, store, key):
        self.store = store
        self.key = key

    def get(self):
        return FakeSnapshot(self.store.get(self.key))

    def set(self, data):
        self.store[self.key] = data


class FakeCollection:
    def __init__(self, store):
        self.store = store

    def document(self, key):
        return FakeDocument(self.store, key)


class FakeFirestoreClient:
    def __init__(self):
        self.store = {}

    def collection(self, name):
        return FakeCollection(self.store)


class TestCache(unittest.TestCase):

    def test_cache_miss_calls_function_and_stores_value(self):
        fake_client = FakeFirestoreClient()
        calls = []

        def produce_value():
            calls.append(1)
            return "fresh-value"

        with patch("app.services.cache._get_client", return_value=fake_client):
            result = cache.get_or_set("test-key", 60, produce_value)

        self.assertEqual(result, "fresh-value")
        self.assertEqual(len(calls), 1)
        self.assertIn("test-key", fake_client.store)

    def test_cache_hit_does_not_call_function(self):
        fake_client = FakeFirestoreClient()

        fake_client.store["test-key"] = {
            "value": "cached-value",
            "expires_at": datetime.now(timezone.utc) + timedelta(seconds=60),
        }

        calls = []

        def produce_value():
            calls.append(1)
            return "new-value"

        with patch("app.services.cache._get_client", return_value=fake_client):
            result = cache.get_or_set("test-key", 60, produce_value)

        self.assertEqual(result, "cached-value")
        self.assertEqual(len(calls), 0)

    def test_expired_cache_calls_function_again(self):
        fake_client = FakeFirestoreClient()

        fake_client.store["test-key"] = {
            "value": "old-value",
            "expires_at": datetime.now(timezone.utc) - timedelta(seconds=60),
        }

        calls = []

        def produce_value():
            calls.append(1)
            return "new-value"

        with patch("app.services.cache._get_client", return_value=fake_client):
            result = cache.get_or_set("test-key", 60, produce_value)

        self.assertEqual(result, "new-value")
        self.assertEqual(len(calls), 1)

    def test_firestore_disabled_calls_function(self):
        calls = []

        def produce_value():
            calls.append(1)
            return "local-value"

        with patch("app.services.cache._get_client", return_value=None):
            result = cache.get_or_set("test-key", 60, produce_value)

        self.assertEqual(result, "local-value")
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()