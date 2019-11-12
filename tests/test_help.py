import unittest

from unittest.mock import Mock
from help import formatting_command

class TestCommands(unittest.TestCase):

    def test_formatting_command(self):
        info = (None, ["<arg1>", "<arg2>", "(arg3)"], "this is the description")

        # Test with default values (add_params=False, separator=- and escape=False)
        actual_cmd = formatting_command("/foobar", info)
        expected_cmd = "/foobar - this is the description"
        self.assertEqual(expected_cmd, actual_cmd)

        # Test with add_params=True, separator=- and escape=False
        actual_cmd = formatting_command("/foobar", info, add_params=True)
        expected_cmd = "/foobar <arg1>, <arg2>, (arg3) - this is the description"
        self.assertEqual(expected_cmd, actual_cmd)

        # Test with add_params=True, separator=+ and escape=False
        actual_cmd = formatting_command("/foobar", info, add_params=True, separator="+")
        expected_cmd = "/foobar <arg1>, <arg2>, (arg3) + this is the description"
        self.assertEqual(expected_cmd, actual_cmd)

        # Test with add_params=True, separator=+ and escape=True
        info = (None, ["<arg1>", "<arg2|arg3>", "(arg4)"], "this is the description")
        actual_cmd = formatting_command("/foobar", info, add_params=True, separator="|", escape=True)
        expected_cmd = "/foobar \<arg1\>, \<arg2\|arg3\>, (arg4) | this is the description"
        self.assertEqual(expected_cmd, actual_cmd)
