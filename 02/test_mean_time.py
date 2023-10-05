import time
import unittest
from unittest import mock
from mean_time import mean, foo


class MeanTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @mock.patch("mean_time.foo")
    def test_mean_time_with_one_call(self, mock_foo) -> None:
        mock_foo.side_effect = lambda: time.sleep(1)
        expected_mean = 0.1
        last_k_calls = 5
        with mock.patch("builtins.print") as mock_print:
            decorated_foo = mean(last_k_calls)(foo)
            result = decorated_foo(5)
            mock_print.assert_called_with(
                f"Mean time of last {last_k_calls} calls: {result:.9f} seconds"
            )
            self.assertAlmostEqual(result, expected_mean, delta=0.1)

    @mock.patch("mean_time.foo")
    def test_mean_time_with_hundred_calls(self, mock_foo) -> None:
        mock_foo.side_effect = lambda: time.sleep(1)
        expected_mean = 0.1
        last_k_calls = 10
        with mock.patch("builtins.print") as mock_print:
            decorated_foo = mean(last_k_calls)(foo)
            for i in range(100):
                result = decorated_foo(i)
                mock_print.assert_called_with(
                    f"Mean time of last {last_k_calls} calls: {result:.9f} seconds"
                )
                self.assertAlmostEqual(result, expected_mean, delta=0.1)
            self.assertEqual(mock_print.call_count, 100)

    @mock.patch("mean_time.foo")
    def test_mean_time_with_less_calls_than_last_k_calls(self, mock_foo) -> None:
        mock_foo.side_effect = lambda: time.sleep(1)
        expected_mean = 0.1
        last_k_calls = 5
        with mock.patch("builtins.print") as mock_print:
            decorated_foo = mean(last_k_calls)(foo)
            for i in range(3):
                result = decorated_foo(i)
                mock_print.assert_called_with(
                    f"Mean time of last {last_k_calls} calls: {result:.9f} seconds"
                )
                self.assertAlmostEqual(result, expected_mean, delta=0.1)
            self.assertEqual(mock_print.call_count, 3)

    @mock.patch("mean_time.foo")
    def test_mean_decorator_with_more_calls_than_last_k_calls(self, mock_foo) -> None:
        mock_foo.side_effect = lambda: time.sleep(1)
        expected_mean = 0.1
        last_k_calls = 7
        with mock.patch("builtins.print") as mock_print:
            decorated_foo = mean(last_k_calls)(foo)
            for i in range(10):
                result = decorated_foo(i)
                mock_print.assert_called_with(
                    f"Mean time of last {last_k_calls} calls: {result:.9f} seconds"
                )
                self.assertAlmostEqual(result, expected_mean, delta=0.1)
            self.assertEqual(mock_print.call_count, 10)

    @mock.patch("mean_time.foo")
    def test_mean_decorator_with_equal_calls_and_last_k_calls(self, mock_foo) -> None:
        mock_foo.side_effect = lambda: time.sleep(1)
        expected_mean = 0.1
        last_k_calls = 8
        with mock.patch("builtins.print") as mock_print:
            decorated_foo = mean(last_k_calls)(foo)
            for i in range(8):
                result = decorated_foo(i)
                mock_print.assert_called_with(
                    f"Mean time of last {last_k_calls} calls: {result:.9f} seconds"
                )
                self.assertAlmostEqual(result, expected_mean, delta=0.1)
            self.assertEqual(mock_print.call_count, 8)

    @mock.patch("mean_time.foo")
    def test_mean_decorator_with_zero_last_k_calls(self, mock_foo) -> None:
        mock_foo.side_effect = lambda: time.sleep(1)
        last_k_calls = 0
        with mock.patch("builtins.print") as mock_print:
            with self.assertRaises(ValueError) as err:
                mean(last_k_calls)(foo)
            self.assertEqual(
                "last_k_calls must be a positive integer", str(err.exception)
            )
            self.assertEqual(ValueError, type(err.exception))
            self.assertEqual(mock_print.call_count, 0)

    @mock.patch("mean_time.foo")
    def test_mean_decorator_with_non_positive_integer_last_k_calls(
        self, mock_foo
    ) -> None:
        mock_foo.side_effect = lambda: time.sleep(1)
        last_k_calls = -5
        with mock.patch("builtins.print") as mock_print:
            with self.assertRaises(ValueError) as err:
                mean(last_k_calls)(foo)
            self.assertEqual(
                "last_k_calls must be a positive integer", str(err.exception)
            )
            self.assertEqual(ValueError, type(err.exception))
            self.assertEqual(mock_print.call_count, 0)

    @mock.patch("mean_time.foo")
    def test_mean_decorator_with_non_integer_last_k_calls(self, mock_foo) -> None:
        mock_foo.side_effect = lambda: time.sleep(1)
        last_k_calls = 5.5
        with mock.patch("builtins.print") as mock_print:
            with self.assertRaises(TypeError) as err:
                mean(last_k_calls)(foo)
            self.assertEqual("last_k_calls must be an integer", str(err.exception))
            self.assertEqual(TypeError, type(err.exception))
            self.assertEqual(mock_print.call_count, 0)

    def test_mean_decorator(self) -> None:
        last_k_calls = 5
        decorated_func = mean(last_k_calls)(foo)
        self.assertEqual(decorated_func.__name__, "inner")
