import unittest
from unittest import mock
from predict_mood import SomeModel, predict_message_mood


class TestPredictMood(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SomeModel()

    def tearDown(self) -> None:
        pass

    def test_predict(self) -> None:
        message = "Test msg"
        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.7
            prediction = self.model.predict(message)
            mock_predict.assert_called_once_with(message)
            self.assertEqual(prediction, 0.7)

    def test_predict_msg_argument(self) -> None:
        message = "Test msg"
        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.6
            predict_message_mood(message, self.model)
            mock_predict.assert_called_with(message)

    def test_predict_called_once(self) -> None:
        message = "Test msg"
        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.3
            predict_message_mood(message, self.model)
            mock_predict.assert_called_once()

    def test_predict_message_mood(self) -> None:
        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.2
            prediction = predict_message_mood("Test msg", self.model)
            self.assertEqual(prediction, "неуд")

        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.9
            prediction = predict_message_mood("Test msg", self.model)
            self.assertEqual(prediction, "отл")

        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.6
            prediction = predict_message_mood("Test msg", self.model)
            self.assertEqual(prediction, "норм")

        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.3
            prediction = predict_message_mood("Test msg", self.model)
            self.assertEqual(prediction, "норм")

        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.8
            prediction = predict_message_mood("Test msg", self.model)
            self.assertEqual(prediction, "норм")

        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.5
            prediction = predict_message_mood(
                "Test msg", self.model, bad_thresholds=0.5, good_thresholds=0.5
            )
            self.assertEqual(prediction, "норм")

    def test_predict_message_mood_custom_thresholds(self) -> None:
        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.4
            prediction = predict_message_mood(
                "Test msg", self.model, bad_thresholds=0.4, good_thresholds=0.6
            )
            self.assertEqual(prediction, "норм")

        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.4
            prediction = predict_message_mood(
                "Test msg", self.model, bad_thresholds=0.5, good_thresholds=0.6
            )
            self.assertEqual(prediction, "неуд")

        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.7
            prediction = predict_message_mood(
                "Test msg", self.model, bad_thresholds=0.5, good_thresholds=0.6
            )
            self.assertEqual(prediction, "отл")

    def test_predict_message_mood_if_error(self) -> None:
        with mock.patch("predict_mood.SomeModel.predict") as mock_predict:
            mock_predict.side_effect = 0.5
            with self.assertRaises(ValueError) as err:
                predict_message_mood("Test msg", self.model, 0.8, 0.3)

        self.assertEqual("Incorrect values of tresholds", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))
        self.assertEqual(mock_predict.call_count, 0)
