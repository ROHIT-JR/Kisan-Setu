import unittest
from unittest.mock import patch

from app.services import quota


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


class TestQuota(unittest.TestCase):

    def test_first_call_is_allowed(self):
        fake_client = FakeFirestoreClient()

        with patch(
            "app.services.quota._get_client",
            return_value=fake_client,
        ):
            result = quota.check_and_increment("gemini")

        self.assertTrue(result)
        self.assertEqual(len(fake_client.store), 1)

    def test_quota_limit_is_enforced(self):
        fake_client = FakeFirestoreClient()

        with patch(
            "app.services.quota._get_client",
            return_value=fake_client,
        ), patch.object(
            quota.settings,
            "max_gemini_calls_per_day",
            2,
        ):
            first = quota.check_and_increment("gemini")
            second = quota.check_and_increment("gemini")
            third = quota.check_and_increment("gemini")

        self.assertTrue(first)
        self.assertTrue(second)
        self.assertIsNone(third)

    def test_different_services_have_separate_counters(self):
        fake_client = FakeFirestoreClient()

        with patch(
            "app.services.quota._get_client",
            return_value=fake_client,
        ), patch.object(
            quota.settings,
            "max_gemini_calls_per_day",
            1,
        ):
            gemini_result = quota.check_and_increment("gemini")
            weather_result = quota.check_and_increment("weather")

        self.assertTrue(gemini_result)
        self.assertTrue(weather_result)

    def test_firestore_disabled_allows_call(self):
        with patch(
            "app.services.quota._get_client",
            return_value=None,
        ):
            result = quota.check_and_increment("gemini")

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()