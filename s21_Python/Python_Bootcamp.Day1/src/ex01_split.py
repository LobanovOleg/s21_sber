import ex00_ingot
import unittest


def split_booty(*purses):
    total = sum(purse.get("gold_ingots", 0) for purse in purses)
    for_guys = total // 3
    for_guys_extra = total % 3

    booty = [ex00_ingot.empty({}) for _ in range(3)]
    for i in range(for_guys * 3):
        index = i // for_guys
        booty[index] = ex00_ingot.add_ingot(booty[index])

    for i in range(for_guys_extra):
        booty[i] = ex00_ingot.add_ingot(booty[i])

    return booty


class Test(unittest.TestCase):
    def test_split(self):
        purses = [{"gold_ingots": 9}]
        excepted = [{"gold_ingots": 3}, {"gold_ingots": 3}, {"gold_ingots": 3}]
        self.assertEqual(split_booty(*purses), excepted)

    def test_extra_split(self):
        purses = [{"gold_ingots": 10}, {"gold_ingots": 6}, {"gold_ingots": 3}]
        excepted = [{"gold_ingots": 7}, {"gold_ingots": 6}, {"gold_ingots": 6}]
        self.assertEqual(split_booty(*purses), excepted)

    def test_empty(self):
        purses = [{}]
        excepted = [{}, {}, {}]
        self.assertEqual(split_booty(*purses), excepted)


if __name__ == "__main__":
    unittest.main()
