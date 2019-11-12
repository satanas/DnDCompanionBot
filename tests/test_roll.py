import unittest

from handlers.roll import roll, process_notation, roll_one, response

class TestRoll(unittest.TestCase):

    def test_roll(self):
        for i in range(0, 1000):
            result = roll('1d4, 1d6')
            self.assertEqual(len(result.keys()), 2)
            self.assertTrue(list(result.keys())[0] == '1d4')
            self.assertTrue(list(result.keys())[1] == '1d6')
            self.assertTrue(result['1d4'][0] >= 1 and result['1d4'][0] <= 4)
            self.assertTrue(result['1d6'][0] >= 1 and result['1d6'][0] <= 6)

        for i in range(0, 1000):
            result = roll('1d20, 1d20')
            self.assertEqual(len(result.keys()), 1)
            self.assertTrue(list(result.keys())[0] == '1d20')
            self.assertTrue(result['1d20'][0] >= 1 and result['1d20'][0] <= 20)
            self.assertTrue(result['1d20'][1] >= 1 and result['1d20'][1] <= 20)

    def test_process_notation(self):
        for i in range(0, 1000):
            result = process_notation('1d20', '', '')
            self.assertTrue(result >= 1 and result <= 20)

        for i in range(0, 1000):
            result = process_notation('1d20', '+', '5')
            self.assertTrue(result >= 1 and result <= 25)

        for i in range(0, 1000):
            result = process_notation('2d20', '-', '5')
            self.assertTrue(result >= 1 and result <= 35)

        for i in range(0, 1000):
            result = process_notation('1d100', '', '')
            self.assertTrue(result >= 1 and result <= 100)

        for i in range(0, 1000):
            result = process_notation('1d%', '', '')
            self.assertTrue(result >= 1 and result <= 100)

        with self.assertRaises(Exception):
            result = process_notation('2d100', '', '')

    def test_roll_one(self):
        for i in range(0, 1000):
            result = roll_one(20)
            self.assertTrue(result >= 1 and result <= 20)

    def test_response(self):
        pass

