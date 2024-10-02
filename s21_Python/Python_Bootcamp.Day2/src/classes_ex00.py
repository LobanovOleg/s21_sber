import unittest


class Key:
    def __init__(self, phrase):
        self.phrase = phrase

    def __len__(self):
        return 1337

    def __getitem__(self, item):
        if item == 404:
            return 3

    def __gt__(self, other):
        if other == 9000:
            return True

    def __str__(self):
        return "GeneralTsoKeycard"


class TestKey(unittest.TestCase):
    def setUp(self):
        self.key = Key("zax2rulez")

    def test1(self):
        self.assertEqual(len(self.key), 1337)

    def test2(self):
        self.assertEqual(self.key[404], 3)

    def test3(self):
        self.assertEqual(str(self.key), "GeneralTsoKeycard")

    def test4(self):
        self.assertTrue(self.key > 9000)


if __name__ == "__main__":
    unittest.main()
