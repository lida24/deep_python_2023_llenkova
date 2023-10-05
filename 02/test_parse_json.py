import unittest
from unittest import mock
from unittest.mock import call
from parse_json import parse_json, keywords_counter, counter


class ParseJsonTest(unittest.TestCase):
    def setUp(self) -> None:
        self.counter = counter
        self.json_str = """
            {
                "key1": "She Other Sense Prepare",
                "key2": "whole production series",
                "key3": "Different expert",
                "key4": "Still discussion light carry full",
                "key5": "town question",
                "key6": "word1",
                "key7": "word4",
                "key8": "she Carry series word5",
                "key9": "different carry"
            }"""

    def tearDown(self) -> None:
        self.counter = {}

    def test_parse_json_with_valid_arguments(self) -> None:
        required_fields = ["key1", "kye3", "key4", "key8"]
        keywords = ["She", "sense", "whole", "carry", "full", "word"]
        expected_results = {"She": 2, "sense": 1, "full": 1, "carry": 2}
        parse_json(
            self.json_str, required_fields, keywords, keyword_callback=keywords_counter
        )
        self.assertEqual(self.counter, expected_results)

    def test_parse_json_with_empty_required_fields(self) -> None:
        required_fields = []
        keywords = ["She", "sense", "whole", "carry", "full", "word"]
        expected_results = {}
        parse_json(
            self.json_str, required_fields, keywords, keyword_callback=keywords_counter
        )
        self.assertEqual(self.counter, expected_results)

    def test_parse_json_with_empty_keywords(self) -> None:
        required_fields = ["key1", "kye3", "key4", "key8"]
        keywords = []
        expected_results = {}
        parse_json(
            self.json_str, required_fields, keywords, keyword_callback=keywords_counter
        )
        self.assertEqual(self.counter, expected_results)

    def test_parse_json_with_none_required_fields(self) -> None:
        required_fields = None
        keywords = ["word2"]

        with self.assertRaises(ValueError) as err:
            parse_json(self.json_str, required_fields, keywords, keyword_callback=None)
        self.assertEqual("required_fields parameter is required", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

    def test_parse_json_with_none_keywords(self) -> None:
        required_fields = ["key1"]
        keywords = None

        with self.assertRaises(ValueError) as err:
            parse_json(self.json_str, required_fields, keywords, keyword_callback=None)
        self.assertEqual("keywords parameter is required", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

    def test_parse_json_with_none_callback(self) -> None:
        required_fields = ["key1"]
        keywords = ["word2"]

        with self.assertRaises(ValueError) as err:
            parse_json(self.json_str, required_fields, keywords, keyword_callback=None)
        self.assertEqual("keyword_callback parameter is required", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

    def test_parse_json_with_missing_required_fields(self) -> None:
        required_fields = ["key10"]
        keywords = ["word2"]
        expected_results = {}
        parse_json(
            self.json_str, required_fields, keywords, keyword_callback=keywords_counter
        )
        self.assertEqual(self.counter, expected_results)

    def test_parse_json_with_missing_keywords(self) -> None:
        required_fields = ["key1", "kye3", "key4", "key8"]
        keywords = ["word1"]
        expected_results = {}
        parse_json(
            self.json_str, required_fields, keywords, keyword_callback=keywords_counter
        )
        self.assertEqual(self.counter, expected_results)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_calls_keyword_callback_correct_number_of_times(
        self, mock_keyword_callback
    ) -> None:
        required_fields = ["key1", "kye3", "key4", "key8"]
        keywords = ["She", "sense", "whole", "carry", "full", "word"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        expected_calls = [
            call("sense"),
            call("She"),
            call("carry"),
            call("full"),
            call("carry"),
            call("She"),
        ]
        for args in mock_keyword_callback.call_args_list:
            self.assertIn(args, expected_calls)
        self.assertEqual(mock_keyword_callback.call_count, 6)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_does_not_call_keyword_callback_when_no_match_found(
        self, mock_keyword_callback
    ) -> None:
        required_fields = ["kye3", "key4", "key8"]
        keywords = ["word7", "word8", "word9"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        mock_keyword_callback.assert_not_called()

    def test_empty_required_fields_and_keywords(self) -> None:
        with mock.patch("parse_json.keywords_counter") as mock_keyword_callback:
            parse_json(self.json_str, [], [], mock_keyword_callback)
            mock_keyword_callback.assert_not_called()

    def test_required_fields_not_in_json(self) -> None:
        required_fields = ["field3", "field4"]
        with mock.patch("parse_json.keywords_counter") as mock_keyword_callback:
            parse_json(self.json_str, required_fields, [], mock_keyword_callback)
            mock_keyword_callback.assert_not_called()
