import pytest
import sys
import os
import json

script_dir = os.path.dirname(__file__)
my_dir = os.path.join(script_dir, "../")
sys.path.append(my_dir)

from reader import read_json


def test_reader():
    # valid test
    excepted = {"key": "value"}
    with open("test_data.json", "w") as f:
        json.dump(excepted, f)
    assert read_json("test_data.json") == excepted

    # invalid test
    with open("test_data.json", "w") as f:
        f.write("invalid json")
    with pytest.raises(json.JSONDecodeError):
        read_json("test_data.json")

    # not exist
    with pytest.raises(FileNotFoundError):
        read_json("test_file.json")


if __name__ == "__main__":
    test_reader()
