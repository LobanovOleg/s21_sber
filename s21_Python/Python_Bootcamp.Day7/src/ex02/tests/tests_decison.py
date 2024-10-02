import pytest
import sys
import os

script_dir = os.path.dirname(__file__)
my_dir = os.path.join(script_dir, "../")
sys.path.append(my_dir)

from src.decison import decision


def test_human():
    """Tests the decision function with human-like input averages."""
    a = (14, 65, 4, 5)
    assert decision(a) == "human"


def test_replicant():
    """Tests the decision function with replicant-like input averages."""
    a = (5, 130, 1, 1)
    assert decision(a) == "replicant"


def test_invalid():
    """Tests the decision function with invalid input averages."""
    a = (14, 70, 4, "invalid")
    with pytest.raises(TypeError):
        decision(a)


if __name__ == "__main__":
    test_human()
    test_invalid()
    test_replicant()
