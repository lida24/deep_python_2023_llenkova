import json
import ujson
import cjson
import unittest


class TestCJSON(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_loads(self) -> None:
        json_strs = [
            '{"hello": 10, "world": "value"}',
            '{"name": "John", "age": 30, "city": "New York"}',
            '{"" : "", "": "", "":"", "number": 12345}',
        ]
        for json_str in json_strs:
            self.assertEqual(
                json.loads(json_str), ujson.loads(json_str), cjson.loads(json_str)
            )

    def test_loads_if_error(self) -> None:
        json_strs = [
            '{"hello": 10 "world": "value"}',
            '"name": "John", "age": 30, "city": ""}',
        ]
        for json_str in json_strs:
            with self.assertRaises(TypeError) as err:
                cjson.loads(json_str)
            self.assertEqual(TypeError, type(err.exception))

    def test_dumps(self) -> None:
        dict_objects = [
            {"hello": 10, "world": "value"},
            {"name": "John", "age": 30, "city": "New York"},
            {"": "", "": "", "": "", "number": 12345},
        ]
        for dict_obj in dict_objects:
            self.assertEqual(json.dumps(dict_obj), cjson.dumps(dict_obj))

    def test_dumps_if_error(self) -> None:
        dict_objects = [("a", "b", "c"), [1, 2, 3, 4, 5]]
        for dict_obj in dict_objects:
            with self.assertRaises(TypeError) as err:
                cjson.dumps(dict_obj)
            self.assertEqual(TypeError, type(err.exception))

    def test_dumps_via_loads(self) -> None:
        dict_objects = [
            {"hello": 10, "world": "value"},
            {"name": "John", "age": 30, "city": "New York"},
            {"": "", "": "", "": "", "number": 12345},
        ]
        for dict_obj in dict_objects:
            self.assertEqual(cjson.loads(cjson.dumps(dict_obj)), dict_obj)

    def test_loads_via_dumps(self) -> None:
        json_strs = [
            '{"hello": 10, "world": "value"}',
            '{"name": "John", "age": 30, "city": "New York"}',
        ]
        for json_str in json_strs:
            self.assertEqual(cjson.dumps(cjson.loads(json_str)), json_str)
