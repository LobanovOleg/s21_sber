import json
import os


def read_json(file):
    if os.stat(file).st_size == 0:
        print("Error: json file is empty")
        return None
    with open(file) as f:
        data = json.load(f)
    return data
