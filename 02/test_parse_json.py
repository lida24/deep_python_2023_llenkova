import unittest
from unittest import mock
from unittest.mock import call
from parse_json import parse_json


class ParseJsonTest(unittest.TestCase):
    def setUp(self) -> None:
        self.json_str = """
            {
                "key1": "She Other Sense Prepare",
                "key2": "whole production series",
                "key3": "Different expert",
                "key4": "Still discussion light carry full",
                "key5": "crowd xyz town question xyz",
                "key6": "word1 word1 word1",
                "key7": "word4",
                "key8": "she Carry series word5",
                "key9": "different carry xyz"
            }"""

    def tearDown(self) -> None:
        pass

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_valid_arguments_1(self, mock_keyword_callback) -> None:
        required_fields = ["key1", "key3", "key4", "key8"]
        keywords = ["She", "sense", "whole", "carry", "full", "word", "different"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        expected_calls = [
            call("key1", "sense"),
            call("key1", "She"),
            call("key8", "carry"),
            call("key4", "full"),
            call("key4", "carry"),
            call("key8", "She"),
            call("key3", "different"),
        ]
        for args in mock_keyword_callback.call_args_list:
            self.assertIn(args, expected_calls)
        self.assertEqual(mock_keyword_callback.call_count, 7)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_valid_arguments_2(self, mock_keyword_callback) -> None:
        required_fields = ["key5", "key7", "key4", "key9"]
        keywords = ["town", "word4", "light", "discussion", "carry"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        expected_calls = [
            call("key4", "discussion"),
            call("key7", "word4"),
            call("key9", "carry"),
            call("key4", "carry"),
            call("key5", "town"),
            call("key4", "light"),
        ]
        for args in mock_keyword_callback.call_args_list:
            self.assertIn(args, expected_calls)
        self.assertEqual(mock_keyword_callback.call_count, 6)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_valid_arguments_3(self, mock_keyword_callback) -> None:
        required_fields = ["key2", "key7", "key8", "key9"]
        keywords = ["whole", "production", "series", "she", "different"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        expected_calls = [
            call("key9", "different"),
            call("key2", "production"),
            call("key8", "she"),
            call("key8", "series"),
            call("key2", "series"),
            call("key2", "whole"),
        ]
        for args in mock_keyword_callback.call_args_list:
            self.assertIn(args, expected_calls)
        self.assertEqual(mock_keyword_callback.call_count, 6)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_valid_arguments_4(self, mock_keyword_callback) -> None:
        required_fields = ["key2", "key7", "key9"]
        keywords = ["whole", "production", "series", "she", "different", "word4"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        expected_calls = [
            call("key9", "different"),
            call("key2", "production"),
            call("key7", "word4"),
            call("key2", "series"),
            call("key2", "whole"),
        ]
        for args in mock_keyword_callback.call_args_list:
            self.assertIn(args, expected_calls)
        self.assertEqual(mock_keyword_callback.call_count, 5)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_multiple_keywords_in_one_str_1(
        self, mock_keyword_callback
    ) -> None:
        required_fields = ["key5", "key9"]
        keywords = ["xyz", "crowd", "different"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        expected_calls = [
            call("key9", "different"),
            call("key9", "xyz"),
            call("key5", "xyz"),
            call("key5", "crowd"),
        ]
        for args in mock_keyword_callback.call_args_list:
            self.assertIn(args, expected_calls)
        self.assertEqual(mock_keyword_callback.call_count, 4)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_multiple_keywords_in_one_str_2(
        self, mock_keyword_callback
    ) -> None:
        required_fields = ["key6"]
        keywords = ["word1"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        mock_keyword_callback.assert_called_with("key6", "word1")
        self.assertEqual(mock_keyword_callback.call_count, 1)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_case_insensitive_keywords_1(
        self, mock_keyword_callback
    ) -> None:
        required_fields = ["key1", "key3", "key4", "key8"]
        keywords = ["she", "SENSE", "Whole", "Carry", "FULL"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        expected_calls = [
            call("key1", "SENSE"),
            call("key1", "she"),
            call("key4", "Carry"),
            call("key4", "FULL"),
            call("key8", "Carry"),
            call("key8", "she"),
        ]
        for args in mock_keyword_callback.call_args_list:
            self.assertIn(args, expected_calls)
        self.assertEqual(mock_keyword_callback.call_count, 6)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_case_insensitive_keywords_2(
        self, mock_keyword_callback
    ) -> None:
        required_fields = ["key3", "key8", "key9"]
        keywords = ["xYz", "DiFFerent", "serIES"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        expected_calls = [
            call("key9", "xYz"),
            call("key3", "DiFFerent"),
            call("key8", "serIES"),
            call("key9", "DiFFerent"),
        ]
        for args in mock_keyword_callback.call_args_list:
            self.assertIn(args, expected_calls)
        self.assertEqual(mock_keyword_callback.call_count, 4)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_empty_required_fields(self, mock_keyword_callback) -> None:
        required_fields = []
        keywords = ["She", "sense", "whole", "carry", "full", "word"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        self.assertEqual(mock_keyword_callback.call_count, 0)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_empty_keywords(self, mock_keyword_callback) -> None:
        required_fields = ["key1", "key3", "key4", "key8"]
        keywords = []
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        self.assertEqual(mock_keyword_callback.call_count, 0)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_keyword_not_in_required_fields_1(
        self, mock_keyword_callback
    ) -> None:
        required_fields = ["key1", "key3", "key4", "key8"]
        keywords = ["cash", "empty", "default"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        self.assertEqual(mock_keyword_callback.call_count, 0)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_keyword_not_in_required_fields_2(
        self, mock_keyword_callback
    ) -> None:
        required_fields = ["key2", "key5", "key7", "key9"]
        keywords = ["flat", "slim", "cool"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        self.assertEqual(mock_keyword_callback.call_count, 0)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_none_required_fields(self, mock_keyword_callback) -> None:
        required_fields = None
        keywords = ["word2"]

        with self.assertRaises(ValueError) as err:
            parse_json(
                self.json_str,
                required_fields,
                keywords,
                keyword_callback=mock_keyword_callback,
            )
        self.assertEqual("required_fields parameter is required", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))
        self.assertEqual(mock_keyword_callback.call_count, 0)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_none_keywords(self, mock_keyword_callback) -> None:
        required_fields = ["key1"]
        keywords = None

        with self.assertRaises(ValueError) as err:
            parse_json(
                self.json_str,
                required_fields,
                keywords,
                keyword_callback=mock_keyword_callback,
            )
        self.assertEqual("keywords parameter is required", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))
        self.assertEqual(mock_keyword_callback.call_count, 0)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_none_callback(self, mock_keyword_callback) -> None:
        required_fields = ["key1"]
        keywords = ["word2"]

        with self.assertRaises(ValueError) as err:
            parse_json(self.json_str, required_fields, keywords, keyword_callback=None)
        self.assertEqual("keyword_callback parameter is required", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))
        self.assertEqual(mock_keyword_callback.call_count, 0)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_missing_required_fields(
        self, mock_keyword_callback
    ) -> None:
        required_fields = ["key10"]
        keywords = ["word2"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        self.assertEqual(mock_keyword_callback.call_count, 0)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_with_missing_keywords(self, mock_keyword_callback) -> None:
        required_fields = ["key1", "key3", "key4", "key8"]
        keywords = ["word1"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        self.assertEqual(mock_keyword_callback.call_count, 0)

    @mock.patch("parse_json.keywords_counter")
    def test_parse_json_does_not_call_keyword_callback_when_no_match_found(
        self, mock_keyword_callback
    ) -> None:
        required_fields = ["key3", "key4", "key8"]
        keywords = ["word7", "word8", "word9"]
        parse_json(
            self.json_str,
            required_fields,
            keywords,
            keyword_callback=mock_keyword_callback,
        )
        mock_keyword_callback.assert_not_called()

    def test_parse_json_empty_required_fields_and_keywords(self) -> None:
        required_fields = []
        keywords = []
        with mock.patch("parse_json.keywords_counter") as mock_keyword_callback:
            parse_json(
                self.json_str,
                required_fields,
                keywords,
                keyword_callback=mock_keyword_callback,
            )
            mock_keyword_callback.assert_not_called()

    def test_parse_json_required_fields_not_in_json(self) -> None:
        required_fields = ["field3", "field4"]
        keywords = []
        with mock.patch("parse_json.keywords_counter") as mock_keyword_callback:
            parse_json(
                self.json_str,
                required_fields,
                keywords,
                keyword_callback=mock_keyword_callback,
            )
            mock_keyword_callback.assert_not_called()
