import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_replacement(self) -> None:
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")
        cache.set("k3", "val3")
        self.assertEqual(cache.get("k3"), "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "val1")

    def test_set_and_get(self) -> None:
        cache = LRUCache(2)
        cache.set("k1", "val1")
        self.assertEqual(cache.get("k1"), "val1")
        cache.set("k2", "val2")
        self.assertEqual(cache.get("k2"), "val2")

    def test_update_exist_key(self) -> None:
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k1", "new_val1")
        self.assertEqual(cache.get("k1"), "new_val1")

    def test_lru_cache_behaviour(self) -> None:
        cache = LRUCache(3)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        cache.get("k1")
        cache.set("k4", "val4")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k4"), "val4")

    def test_lru_cache_over_capacity(self) -> None:
        cache = LRUCache(3)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        cache.set("k4", "val4")
        self.assertIsNone(cache.get("k1"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k4"), "val4")

    def test_lru_cache_stability_after_not_existing_key_request(self) -> None:
        cache = LRUCache(1)
        cache.set("k1", "val1")
        value = cache.get("not_existing_key")
        self.assertIsNone(value)
        self.assertEqual(cache.get("k1"), "val1")

    def test_set_same_key_doesnt_increase_size(self) -> None:
        cache = LRUCache(3)
        cache.set("k1", "val1")
        cache.set("k1", "new_val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        self.assertEqual(cache.get("k1"), "new_val1")
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), "val3")

    def test_lru_cache_is_empty_after_creation(self) -> None:
        cache = LRUCache(3)
        self.assertIsNone(cache.get("k1"))

    def test_lru_cache_size_doesnt_increase_size(self) -> None:
        cache = LRUCache(3)
        for i in range(4, 1000):
            cache.set(f"k{i}", f"val{i}")
        self.assertIsNone(cache.get("k1"))
        self.assertEqual(cache.get("k997"), "val997")
        self.assertEqual(cache.get("k998"), "val998")
        self.assertEqual(cache.get("k999"), "val999")

    def test_lru_cache_can_overwrites(self) -> None:
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k2", "new_val2")
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k2"), "new_val2")
        cache.set("k3", "val3")
        self.assertIsNone(cache.get("k1"))
        self.assertEqual(cache.get("k2"), "new_val2")
        self.assertEqual(cache.get("k3"), "val3")

    def test_lru_cache_can_updates(self) -> None:
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        self.assertEqual(cache.get("k1"), "val1")
        cache.set("k3", "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k3"), "val3")

    def test_cache_is_empty(self) -> None:
        cache = LRUCache(0)
        cache.set("k1", "val1")
        self.assertIsNone(cache.get("k1"))
