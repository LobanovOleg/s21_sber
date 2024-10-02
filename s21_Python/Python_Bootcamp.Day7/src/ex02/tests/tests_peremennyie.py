import os
import sys

script_dir = os.path.dirname(__file__)
my_dir = os.path.join(script_dir, "../")
sys.path.append(my_dir)

from src.peremennyie import calculation


def test_calculation():
    """Tests the calculate_averages function with a list of variables and expected output."""
    a = [(10, 60, 3, 4), (12, 65, 4, 5), (8, 70, 2, 3)]
    excepted = (10.0, 65.0, 3.0, 4.0)
    assert calculation(a) == excepted


def test_empty():
    """Tests the calculate_averages function with an empty list of variables and expected output."""
    a = []
    excepted = (0, 0, 0, 0)
    assert calculation(a) == excepted


def test_calculation_1():
    """Tests the calculate_averages function with a single variable and expected output."""
    a = [(10, 60, 3, 4)]
    excepted = (10, 60, 3, 4)
    assert calculation(a) == excepted


if __name__ == "__main__":
    test_calculation()
    test_calculation_1()
    test_empty()
