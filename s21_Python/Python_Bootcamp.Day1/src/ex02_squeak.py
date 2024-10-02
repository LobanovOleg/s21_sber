import unittest


def squeak(func):
    def signal(*a, **b):
        print("SQUEK")
        return func(*a, **b)

    return signal


@squeak
def add_ingot(purse):
    new_purse = dict(purse)
    if "gold_ingots" not in purse:
        new_purse["gold_ingots"] = 1
    else:
        new_purse["gold_ingots"] += 1
    return new_purse


@squeak
def get_ingot(purse):
    new_purse = dict(purse)
    if "gold_ingots" in purse and purse["gold_ingots"] > 0:
        new_purse["gold_ingots"] -= 1
    return new_purse


@squeak
def empty(purse):
    return {}


class Test(unittest.TestCase):
    def test1(self):
        purse = {"gold_ingots": 10}
        excepted = {"gold_ingots": 11}
        self.assertEqual(add_ingot(purse), excepted)

    def test2(self):
        purse = {"gold_ingots": 10}
        excepted = {"gold_ingots": 9}
        self.assertEqual(get_ingot(purse), excepted)

    def test3(self):
        purse = {"gold_ingots": 10}
        excepted = {}
        self.assertEqual(empty(purse), excepted)


if __name__ == "__main__":
    unittest.main()
