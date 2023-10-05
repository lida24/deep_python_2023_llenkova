import unittest
from unittest import mock
from generator import search_phrases, process_file


class TestGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.test_file = "test_file.txt"

    def tearDown(self) -> None:
        pass

    def test_search_phrases_with_string_file_argument(self) -> None:
        answer = list(search_phrases(self.test_file, ["Rosa"]))
        self.assertEqual(
            answer,
            ["Rosa upala v sadu", "ROSA i AZORA raznye cvety"],
        )

    def test_search_phrases_with_file_object_argument(self) -> None:
        with open(self.test_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, ["v"]))
        self.assertEqual(
            answer,
            ["Rosa upala v sadu", "Azora ischezla v nebe"],
        )

    def test_process_file_strip_and_lower(self) -> None:
        with open(self.test_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, ["ROSA"]))
        self.assertEqual(
            answer,
            ["Rosa upala v sadu", "ROSA i AZORA raznye cvety"],
        )

    def test_process_file_empty_list(self) -> None:
        with open(self.test_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, []))
        self.assertEqual(answer, [])

    def test_process_file_many_words(self) -> None:
        with open(self.test_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, ["azora", "li", "sadu"]))
        self.assertEqual(
            answer,
            [
                "Rosa upala v sadu",
                "Azora uletela vdalake",
                "ROSA i AZORA raznye cvety",
                "Upala li roza",
                "Azora ischezla v nebe",
            ],
        )

    def test_process_file_wrong_words(self) -> None:
        with open(self.test_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, ["rosan", "sad"]))
        self.assertEqual(answer, [])

    def test_process_file_correct_and_wrong_words(self) -> None:
        with open(self.test_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, ["raz", "nebo", "li"]))
        self.assertEqual(answer, ["Upala li roza"])

    def test_process_file_case_insensitive(self) -> None:
        with open(self.test_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, ["rosa", "azora"]))
        self.assertEqual(
            answer,
            [
                "Rosa upala v sadu",
                "Azora uletela vdalake",
                "ROSA i AZORA raznye cvety",
                "Azora ischezla v nebe",
            ],
        )

    def test_process_file_multiple_filters_in_one_str(self) -> None:
        with open(self.test_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, ["v", "azora"]))
        self.assertEqual(
            answer,
            [
                "Rosa upala v sadu",
                "Azora uletela vdalake",
                "ROSA i AZORA raznye cvety",
                "Azora ischezla v nebe",
            ],
        )

    def test_process_file_exact_match_of_filter_and_str(self) -> None:
        with open(self.test_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, ["ROSA i AZORA raznye cvety"]))
        self.assertEqual(
            answer,
            ["ROSA i AZORA raznye cvety"],
        )

    @mock.patch("generator.process_line")
    def test_process_line_called_correctly(self, mock_process_line) -> None:
        with open(self.test_file, "r", encoding="utf-8") as file:
            list(process_file(file, ["v", "azora"]))
        self.assertEqual(mock_process_line.call_count, 6)
