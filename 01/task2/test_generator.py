import unittest
from generator import search_phrases, process_file


class TestGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_file = "temp.txt"

    def tearDown(self) -> None:
        pass

    def test_search_phrases_with_string_file_argument(self) -> None:
        answer = search_phrases(self.temp_file, ["Rosa"])
        self.assertEqual(
            answer,
            ["Rosa upala v sadu", "ROSA i AZORA raznye cvety"],
        )

    def test_search_phrases_with_file_object_argument(self) -> None:
        with open(self.temp_file, "r", encoding="utf-8") as file:
            answer = search_phrases(file, ["v"])
        self.assertEqual(
            answer,
            ["Rosa upala v sadu", "Azora ischezla v nebe"],
        )

    def test_process_file_strip_and_lower(self) -> None:
        with open(self.temp_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, ["ROSA"]))
        self.assertEqual(
            answer,
            ["Rosa upala v sadu", "ROSA i AZORA raznye cvety"],
        )

    def test_process_file_empty_list(self) -> None:
        with open(self.temp_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, []))
        self.assertEqual(answer, [])

    def test_process_file_many_words(self) -> None:
        with open(self.temp_file, "r", encoding="utf-8") as file:
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
        with open(self.temp_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, ["rosan", "sad"]))
        self.assertEqual(answer, [])

    def test_process_file_correct_and_wrong_words(self) -> None:
        with open(self.temp_file, "r", encoding="utf-8") as file:
            answer = list(process_file(file, ["raz", "nebo", "li"]))
        self.assertEqual(answer, ["Upala li roza"])
