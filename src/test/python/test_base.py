import unittest


# from src.main.python.main_base import *


class TestBase(unittest.TestCase):

    def test_create(self):
        self.assertTrue(True)

    def test_measure(self):
        self.assertEqual(2,1+1)


if __name__ == '__main__':
    unittest.main()
