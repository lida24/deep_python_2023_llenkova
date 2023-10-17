import unittest
from metaclass import CustomClass


class TestMetaclass(unittest.TestCase):
    def setUp(self) -> None:
        self.inst = CustomClass()

    def tearDown(self) -> None:
        pass

    def test_custom_x(self) -> None:
        self.assertEqual(self.inst.custom_x, 50)

    def test_default_x(self) -> None:
        with self.assertRaises(AttributeError) as err:
            self.inst.x
        self.assertEqual("'CustomClass' object has no attribute 'x'", str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        with self.assertRaises(AttributeError) as err:
            CustomClass.x
        self.assertEqual("type object 'CustomClass' has no attribute 'x'", str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

    def test_custom_val(self) -> None:
        self.assertEqual(self.inst.custom_val, 99)

    def test_custom_line(self) -> None:
        self.assertEqual(self.inst.custom_line(), 100)

    def test_custom_str(self) -> None:
        self.assertEqual(str(self.inst), "Custom_by_metaclass")

    def test_default_val(self) -> None:
        with self.assertRaises(AttributeError) as err:
            self.inst.val
        self.assertEqual("'CustomClass' object has no attribute 'val'", str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

    def test_default_line(self) -> None:
        with self.assertRaises(AttributeError) as err:
            self.inst.line()
        self.assertEqual("'CustomClass' object has no attribute 'line'", str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

    def test_random_attribute(self) -> None:
        with self.assertRaises(AttributeError) as err:
            self.inst.yyy
        self.assertEqual("'CustomClass' object has no attribute 'yyy'", str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

    def test_dynamic_attribute(self) -> None:
        self.inst.dynamic = "added later"
        self.assertEqual(self.inst.custom_dynamic, "added later")

        with self.assertRaises(AttributeError) as err:
            self.inst.dynamic
        self.assertEqual("'CustomClass' object has no attribute 'dynamic'", str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))
