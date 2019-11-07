import unittest
import tests.utils

from unittest.mock import patch, Mock, PropertyMock
from character import talk, import_character

CHARACTER_JSON = {
    'character': {
        'id': '123456'
    }
}

class TestCharacter(unittest.TestCase):

    def test_talk(self):
        cmd = '/talk Beelzebub What the fuck is wrong with you?'
        result = talk(cmd)
        expected = "```\r\nBeelzebub says:\r\n–What the fuck is wrong with you?\r\n```"

        self.assertEqual(expected, result)


    def test_import_with_invalid_url(self):
        # conditions
        db = Mock()
        get = Mock()

        # execution
        cmd = '/import_char hello_world'
        rtn = import_character(cmd, db, get)

        # expected
        self.assertEqual(rtn, 'hello_world is not a valid URL')

    def test_import_with_request_error(self):
        # conditions
        db = Mock()
        response = Mock()
        response.status_code = 500
        get = Mock(return_value=response)

        # execution
        cmd = '/import_char http://example.com/my/character'
        rtn = import_character(cmd, db, get)

        # expected
        self.assertEqual(rtn, 'Error fetching http://example.com/my/character (status_code: 500)')

    def test_valid_import(self):
        # conditions
        db = Mock()
        db.save_character_info = Mock(return_value=True)
        response = Mock()
        response.status_code = 200
        response.json = Mock(return_value=CHARACTER_JSON)
        get = Mock(return_value=response)

        # execution
        cmd = '/import_char http://example.com/my/character'
        rtn = import_character(cmd, db, get)

        # expected
        self.assertTrue(rtn)
        db.save_character_info.assert_called_with('123456', CHARACTER_JSON)

