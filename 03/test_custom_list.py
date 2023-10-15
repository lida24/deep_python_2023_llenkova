import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_add(self) -> None:
        custom_list_1 = CustomList([5, 1, 3, 7])
        custom_list_2 = CustomList([1, 2, 7])
        self.assertEqual(list(custom_list_1 + custom_list_2), [6, 3, 10, 7])
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))
        self.assertEqual(custom_list_2, CustomList([1, 2, 7]))

        custom_list_3 = CustomList([])
        self.assertEqual(list(custom_list_3 + []), [])
        self.assertEqual(custom_list_3, CustomList([]))

        custom_list_4 = CustomList([2, 5])
        self.assertEqual(list(custom_list_1 + custom_list_4), [7, 6, 3, 7])
        self.assertEqual(custom_list_4, CustomList([2, 5]))

        self.assertEqual(list(custom_list_3 + [2, 5]), [2, 5])
        self.assertEqual(custom_list_3, CustomList([]))

        custom_list_5 = CustomList([2, 9, 15, 84, 9, -3])
        self.assertEqual(
            list(custom_list_5 + custom_list_1),
            [7, 10, 18, 91, 9, -3],
        )
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))
        self.assertEqual(custom_list_5, CustomList([2, 9, 15, 84, 9, -3]))

    def test_radd(self) -> None:
        custom_list_1 = CustomList([5, 1, 3, 7])
        self.assertEqual(list([3, 8, -19, 6, 15] + custom_list_1), [8, 9, -16, 13, 15])
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))

        self.assertEqual(list([5] + custom_list_1), [10, 1, 3, 7])
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))

        self.assertEqual(list([] + custom_list_1), [5, 1, 3, 7])
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))

    def test_sub(self):
        custom_list_1 = CustomList([5, 1, 3, 7])
        custom_list_2 = CustomList([1, 2, 7])
        self.assertEqual(list(custom_list_1 - custom_list_2), [4, -1, -4, 7])
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))
        self.assertEqual(custom_list_2, CustomList([1, 2, 7]))

        custom_list_3 = CustomList([2, 5])
        self.assertEqual(list(custom_list_1 - custom_list_3), [3, -4, 3, 7])
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))
        self.assertEqual(custom_list_3, CustomList([2, 5]))

        custom_list_4 = CustomList([1])
        self.assertEqual(list(custom_list_4 - custom_list_1), [-4, -1, -3, -7])
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))
        self.assertEqual(custom_list_4, CustomList([1]))

        custom_list_5 = CustomList([])
        self.assertEqual(list(custom_list_5 - [3, 9, 1]), [-3, -9, -1])
        self.assertEqual(custom_list_5, CustomList([]))

        self.assertEqual(list(custom_list_5 - []), [])
        self.assertEqual(custom_list_5, CustomList([]))

    def test_rsub(self) -> None:
        custom_list_1 = CustomList([5, 1, 3, 7])
        self.assertEqual(
            list([0, -13, 21, 105, 8, 63] - custom_list_1),
            [-5, -14, 18, 98, 8, 63],
        )
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))

        self.assertEqual(list([3, 8] - custom_list_1), [-2, 7, -3, -7])
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))

        self.assertEqual(list([4] - custom_list_1), [-1, -1, -3, -7])
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))

        self.assertEqual(list([] - custom_list_1), [-5, -1, -3, -7])
        self.assertEqual(custom_list_1, CustomList([5, 1, 3, 7]))

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
