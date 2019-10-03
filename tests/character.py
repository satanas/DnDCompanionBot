import unittest

from character import talk

class TestCharacter(unittest.TestCase):

    def test_talk(self):
        cmd = '/talk Beelzebub What the fuck is wrong with you?'
        result = talk(cmd)
        expected = "```Beelzebub says:\r\n–What the fuck is wrong with you?```"

        self.assertEqual(expected, result)
