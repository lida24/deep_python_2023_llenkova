import unittest
from unittest import mock
from predict_mood import predict_message_mood
from some_model import SomeModel


class TestPredictMood(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SomeModel()
        self.message = "Test msg"

    def tearDown(self) -> None:
        pass

    def test_predict(self) -> None:
        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.7
            prediction = self.model.predict(self.message)
            mock_predict.assert_called_once_with(self.message)
            self.assertEqual(prediction, 0.7)

    def test_predict_msg_argument(self) -> None:
        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.6
            predict_message_mood(self.message, self.model)
            mock_predict.assert_called_with(self.message)

    def test_predict_called_once(self) -> None:
        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.3
            predict_message_mood(self.message, self.model)
            mock_predict.assert_called_once()

    def test_predict_returns_float(self) -> None:
        result = self.model.predict(self.message)
        self.assertIsInstance(result, float)

    def test_predict_returns_value_between_0_and_1(self) -> None:
        result = self.model.predict(self.message)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_predict_message_mood(self) -> None:
        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.2
            prediction = predict_message_mood(self.message, self.model)
            self.assertEqual(prediction, "неуд")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.9
            prediction = predict_message_mood(self.message, self.model)
            self.assertEqual(prediction, "отл")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.6
            prediction = predict_message_mood(self.message, self.model)
            self.assertEqual(prediction, "норм")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.3
            prediction = predict_message_mood(self.message, self.model)
            self.assertEqual(prediction, "норм")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.8
            prediction = predict_message_mood(self.message, self.model)
            self.assertEqual(prediction, "норм")

    def test_predict_message_mood_custom_thresholds(self) -> None:
        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.4
            prediction = predict_message_mood(
                self.message, self.model, bad_thresholds=0.4, good_thresholds=0.6
            )
            self.assertEqual(prediction, "норм")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.4
            prediction = predict_message_mood(
                self.message, self.model, bad_thresholds=0.5, good_thresholds=0.6
            )
            self.assertEqual(prediction, "неуд")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.7
            prediction = predict_message_mood(
                self.message, self.model, bad_thresholds=0.5, good_thresholds=0.6
            )
            self.assertEqual(prediction, "отл")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.4
            prediction = predict_message_mood(
                self.message, self.model, bad_thresholds=0.0, good_thresholds=1.0
            )
            self.assertEqual(prediction, "норм")

    def test_predict_message_mood_if_error(self) -> None:
        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.side_effect = 0.5
            with self.assertRaises(ValueError) as err:
                predict_message_mood(self.message, self.model, 0.8, 0.3)

        self.assertEqual("Incorrect values of tresholds", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))
        self.assertEqual(mock_predict.call_count, 0)

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.4
            with self.assertRaises(ValueError) as err:
                predict_message_mood(self.message, self.model, 1.0, 0.0)

        self.assertEqual("Incorrect values of tresholds", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))
        self.assertEqual(mock_predict.call_count, 0)

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.4
            with self.assertRaises(ValueError) as err:
                predict_message_mood(self.message, self.model, 0.5, 0.5)

        self.assertEqual("Incorrect values of tresholds", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))
        self.assertEqual(mock_predict.call_count, 0)

    def test_predict_message_mood_with_extreme_values(self) -> None:
        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.88888888
            prediction = predict_message_mood(
                self.message,
                self.model,
                bad_thresholds=0.8888888,
                good_thresholds=0.88888889,
            )
            self.assertEqual(prediction, "норм")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.9
            prediction = predict_message_mood(
                self.message,
                self.model,
                bad_thresholds=0.9999998,
                good_thresholds=0.9999999,
            )
            self.assertEqual(prediction, "неуд")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 1
            prediction = predict_message_mood(
                self.message,
                self.model,
                bad_thresholds=0.9999998,
                good_thresholds=0.9999999,
            )
            self.assertEqual(prediction, "отл")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.00001
            prediction = predict_message_mood(
                self.message,
                self.model,
                bad_thresholds=0.0000001,
                good_thresholds=0.9999999,
            )
            self.assertEqual(prediction, "норм")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.98
            prediction = predict_message_mood(
                self.message,
                self.model,
                bad_thresholds=0.0000001,
                good_thresholds=0.9999999,
            )
            self.assertEqual(prediction, "норм")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.98
            prediction = predict_message_mood(
                self.message,
                self.model,
                bad_thresholds=0.9000001,
                good_thresholds=0.9999999,
            )
            self.assertEqual(prediction, "норм")

    def test_predict_message_mood_with_close_values(self) -> None:
        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.0000001
            prediction = predict_message_mood(
                self.message, self.model, bad_thresholds=0.0002, good_thresholds=0.0003
            )
            self.assertEqual(prediction, "неуд")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.000000001
            prediction = predict_message_mood(
                self.message, self.model, bad_thresholds=0.0002, good_thresholds=0.0003
            )
            self.assertEqual(prediction, "неуд")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.0002
            prediction = predict_message_mood(
                self.message, self.model, bad_thresholds=0.0002, good_thresholds=0.0003
            )
            self.assertEqual(prediction, "норм")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.0003
            prediction = predict_message_mood(
                self.message, self.model, bad_thresholds=0.0002, good_thresholds=0.0003
            )
            self.assertEqual(prediction, "норм")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.00003
            prediction = predict_message_mood(
                self.message, self.model, bad_thresholds=0.0002, good_thresholds=0.0003
            )
            self.assertEqual(prediction, "неуд")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.0001
            prediction = predict_message_mood(
                self.message, self.model, bad_thresholds=0.0002, good_thresholds=0.0003
            )
            self.assertEqual(prediction, "неуд")

        with mock.patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.004
            prediction = predict_message_mood(
                self.message, self.model, bad_thresholds=0.0002, good_thresholds=0.0003
            )
            self.assertEqual(prediction, "отл")
