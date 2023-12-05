import json
import ujson
import cjson
import time


if __name__ == "__main__":
    with open("large_data.json", "r") as f:
        data = f.read()
    json_data = json.loads(data)
    for dict_obj in json_data:
        start_time = time.time()
        json.dumps(dict_obj)
        end_time = time.time()
        json_execution_time_dumps = end_time - start_time

        start_time = time.time()
        ujson.dumps(dict_obj)
        end_time = time.time()
        ujson_execution_time_dumps = end_time - start_time

        start_time = time.time()
        cjson.dumps(dict_obj)
        end_time = time.time()
        cjson_execution_time_dumps = end_time - start_time

        dict_str = json.dumps(dict_obj)

        start_time = time.time()
        json.loads(dict_str)
        end_time = time.time()
        json_execution_time_loads = end_time - start_time

        start_time = time.time()
        ujson.loads(dict_str)
        end_time = time.time()
        ujson_execution_time_loads = end_time - start_time

        start_time = time.time()
        cjson.loads(dict_str)
        end_time = time.time()
        cjson_execution_time_loads = end_time - start_time

    print(f"{'dumps':=^50}")
    print("Время выполнения для json:", json_execution_time_dumps)
    print("Время выполнения для ujson:", ujson_execution_time_dumps)
    print("Время выполнения для cjson:", cjson_execution_time_dumps)
    print(f"{'loads':=^50}")
    print("Время выполнения для json:", json_execution_time_loads)
    print("Время выполнения для ujson:", ujson_execution_time_loads)
    print("Время выполнения для cjson:", cjson_execution_time_loads)
