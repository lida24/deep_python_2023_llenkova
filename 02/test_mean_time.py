import time
from io import StringIO
import unittest
from unittest import mock
from mean_time import mean, foo


class MeanTest(unittest.TestCase):
    def setUp(self) -> None:
        self.time_to_sleep = 0.1
        self.mock_foo = mock.patch("mean_time.foo").start()
        self.mock_foo.side_effect = lambda arg: time.sleep(self.time_to_sleep)

    def tearDown(self) -> None:
        mock.patch.stopall()

    def test_mean_time_with_one_call(self) -> None:
        last_k_calls = 7
        with mock.patch("sys.stdout", new=StringIO()) as mock_print:
            decorated_foo = mean(last_k_calls)(self.mock_foo)
            decorated_foo(5)
            self.assertEqual(
                mock_print.getvalue().split()[-2][:3], f"{self.time_to_sleep:.1f}"
            )
        self.mock_foo.assert_called_once_with(5)

    def test_mean_time_with_hundred_calls(self) -> None:
        last_k_calls = 10
        with mock.patch("sys.stdout", new=StringIO()) as mock_print:
            decorated_foo = mean(last_k_calls)(self.mock_foo)
            for i in range(100):
                decorated_foo(i)
                self.assertEqual(
                    mock_print.getvalue().split()[-2][:3], f"{self.time_to_sleep:.1f}"
                )
                self.mock_foo.assert_called_with(i)
            self.assertEqual(self.mock_foo.call_count, 100)

    def test_mean_time_with_less_calls_than_last_k_calls(self) -> None:
        last_k_calls = 5
        with mock.patch("sys.stdout", new=StringIO()) as mock_print:
            decorated_foo = mean(last_k_calls)(self.mock_foo)
            for i in range(3):
                decorated_foo(i)
                self.assertEqual(
                    mock_print.getvalue().split()[-2][:3], f"{self.time_to_sleep:.1f}"
                )
                self.mock_foo.assert_called_with(i)
            self.assertEqual(self.mock_foo.call_count, 3)

    def test_mean_decorator_with_more_calls_than_last_k_calls(self) -> None:
        last_k_calls = 7
        with mock.patch("sys.stdout", new=StringIO()) as mock_print:
            decorated_foo = mean(last_k_calls)(self.mock_foo)
            for i in range(10):
                decorated_foo(i)
                self.assertEqual(
                    mock_print.getvalue().split()[-2][:3], f"{self.time_to_sleep:.1f}"
                )
                self.mock_foo.assert_called_with(i)
            self.assertEqual(self.mock_foo.call_count, 10)

    def test_mean_decorator_with_equal_calls_and_last_k_calls(self) -> None:
        last_k_calls = 8
        with mock.patch("sys.stdout", new=StringIO()) as mock_print:
            decorated_foo = mean(last_k_calls)(self.mock_foo)
            for i in range(8):
                decorated_foo(i)
                self.assertEqual(
                    mock_print.getvalue().split()[-2][:3], f"{self.time_to_sleep:.1f}"
                )
                self.mock_foo.assert_called_with(i)
            self.assertEqual(self.mock_foo.call_count, 8)

    def test_mean_decorator_with_zero_last_k_calls(self) -> None:
        last_k_calls = 0
        with self.assertRaises(ValueError) as err:
            mean(last_k_calls)(self.mock_foo)
        self.assertEqual("last_k_calls must be a positive integer", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))
        self.assertEqual(self.mock_foo.call_count, 0)

    def test_mean_decorator_with_non_positive_integer_last_k_calls(self) -> None:
        last_k_calls = -5
        with self.assertRaises(ValueError) as err:
            mean(last_k_calls)(self.mock_foo)
        self.assertEqual("last_k_calls must be a positive integer", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))
        self.assertEqual(self.mock_foo.call_count, 0)

    def test_mean_decorator_with_non_integer_last_k_calls(self) -> None:
        last_k_calls = 5.5
        with self.assertRaises(TypeError) as err:
            mean(last_k_calls)(self.mock_foo)
        self.assertEqual("last_k_calls must be an integer", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))
        self.assertEqual(self.mock_foo.call_count, 0)

    def test_mean_decorator(self) -> None:
        last_k_calls = 5
        decorated_func = mean(last_k_calls)(foo)
        self.assertEqual(decorated_func.__name__, "inner")

    def test_foo(self) -> None:
        answer = foo(5)
        self.assertEqual(answer, 5)
