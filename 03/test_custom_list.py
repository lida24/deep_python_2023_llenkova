import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def setUp(self) -> None:
        self.custom_list = CustomList([5, 1, 3, 7])

    def tearDown(self) -> None:
        pass

    def test_add(self) -> None:
        self.assertListEqual(
            self.custom_list + CustomList([1, 2, 7]), CustomList([6, 3, 10, 7])
        )
        self.assertListEqual(CustomList([]) + [], CustomList([]))
        self.assertListEqual(self.custom_list + [2, 5], CustomList([7, 6, 3, 7]))
        self.assertListEqual(CustomList([]) + [2, 5], CustomList([2, 5]))
        self.assertListEqual(
            CustomList([2, 9, 15, 84, 9, -3]) + self.custom_list,
            CustomList([7, 10, 18, 91, 9, -3]),
        )

    def test_radd(self) -> None:
        self.assertListEqual(
            [3, 8, -19, 6, 15] + self.custom_list, CustomList([8, 9, -16, 13, 15])
        )
        self.assertListEqual([5] + self.custom_list, CustomList([10, 1, 3, 7]))
        self.assertListEqual([] + self.custom_list, CustomList([5, 1, 3, 7]))

    def test_sub(self):
        self.assertListEqual(
            self.custom_list - CustomList([1, 2, 7]), CustomList([4, -1, -4, 7])
        )
        self.assertListEqual(self.custom_list - [2, 5], CustomList([3, -4, 3, 7]))
        self.assertListEqual(
            CustomList([1]) - self.custom_list, CustomList([-4, -1, -3, -7])
        )
        self.assertListEqual(CustomList([]) - [3, 9, 1], CustomList([-3, -9, -1]))
        self.assertListEqual(CustomList([]) - [], CustomList([]))

    def test_rsub(self) -> None:
        self.assertListEqual(
            [0, -13, 21, 105, 8, 63] - self.custom_list,
            CustomList([-5, -14, 18, 98, 8, 63]),
        )
        self.assertListEqual([3, 8] - self.custom_list, CustomList([-2, 7, -3, -7]))
        self.assertListEqual([4] - self.custom_list, CustomList([-1, -1, -3, -7]))
        self.assertListEqual([] - self.custom_list, CustomList([-5, -1, -3, -7]))

    def test_eq(self) -> None:
        self.assertTrue(CustomList([7, 5, 3]) == CustomList([4, 5, 6]))
        self.assertFalse(CustomList([3, 9, 1]) == CustomList([5, 4, 3]))
        self.assertTrue(CustomList([14]) == CustomList([5, 4, 3, 2]))
        self.assertTrue(CustomList([]) == CustomList([]))
        self.assertFalse(CustomList([10, 7, 4]) == CustomList([]))

    def test_ne(self) -> None:
        self.assertTrue(CustomList([11, 32, 8, 10]) != CustomList([9, 7, 4]))
        self.assertTrue(CustomList([9, 5, 3]) != CustomList([4, 5, 5]))
        self.assertFalse(CustomList([9, 9, 1]) != CustomList([5, 4, 10]))
        self.assertTrue(CustomList([14]) != CustomList([9]))
        self.assertFalse(CustomList([]) != CustomList([]))
        self.assertTrue(CustomList([]) != CustomList([90, 76, 45]))

    def test_gt(self):
        self.assertTrue(CustomList([9, 7, 6]) > CustomList([4, 5, 9]))
        self.assertFalse(CustomList([9, 3, 1, 8]) > CustomList([9, 9, 10]))
        self.assertTrue(CustomList([14]) > CustomList([]))
        self.assertFalse(CustomList([]) > CustomList([]))

    def test_ge(self) -> None:
        self.assertTrue(CustomList([3, 1, 10]) >= CustomList([8, 3, 4, -1]))
        self.assertFalse(CustomList([3, 1]) >= CustomList([8, 3, 4, -1]))
        self.assertTrue(CustomList([54]) >= CustomList([10, 9, 3, 6, 4]))
        self.assertTrue(CustomList([]) >= CustomList([]))

    def test_lt(self) -> None:
        self.assertTrue(CustomList([-9, -8, 0, -5]) < CustomList([6, 7, 8]))
        self.assertFalse(CustomList([-7, 6, -1]) < CustomList([-9, -8, 0, -5]))
        self.assertTrue(CustomList([-54]) < CustomList([12, 39, 0, -16, 40]))
        self.assertFalse(CustomList([]) < CustomList([]))

    def test_le(self) -> None:
        self.assertTrue(CustomList([10, 8]) <= CustomList([4, 7, 7]))
        self.assertFalse(CustomList([100, 219, 343, 90]) <= CustomList([78, 12, 90]))
        self.assertTrue(CustomList([-36]) <= CustomList([]))
        self.assertTrue(CustomList([]) <= CustomList([]))

    def test_str(self) -> None:
        custom_list1 = CustomList([13, 97, 23])
        result = str(custom_list1)
        self.assertEqual(result, "Элементы списка: [13, 97, 23], их сумма: 133")

        custom_list2 = CustomList([])
        result = str(custom_list2)
        self.assertEqual(result, "Элементы списка: [], их сумма: 0")

        custom_list3 = CustomList([4, 0, -8, 7, 19])
        result = str(custom_list3)
        self.assertEqual(result, "Элементы списка: [4, 0, -8, 7, 19], их сумма: 22")
