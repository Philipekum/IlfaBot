import json


def read_json_file(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data
