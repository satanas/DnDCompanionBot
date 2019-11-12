import unittest

from unittest.mock import Mock
from commands import parse_command, is_command

class TestCommands(unittest.TestCase):

    def test_parsing_command(self):
        cmd = "/start with other args"
        self.assertEqual('/start', parse_command(cmd))

        cmd = "/start@DnDCompanionBot"
        self.assertEqual('/start', parse_command(cmd))

        cmd = "/start "
        self.assertEqual('/start', parse_command(cmd))

    def test_is_command(self):
        update = Mock()
        update.message = None

        self.assertEqual(False, is_command(update))

        update.message = Mock()
        update.message.text = ""
        self.assertEqual(False, is_command(update))

        update.message.text = "foobar"
        self.assertEqual(False, is_command(update))

