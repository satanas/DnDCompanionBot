import unittest

from unittest.mock import Mock
from handlers.dm import add_xp
from tests.helper import get_test_character

class TestDMHandler(unittest.TestCase):
    def setUp(self):
        self.campaign_id = 666
        self.chat_id = 123456
        self.username = 'foo'
        self.character_id = 987654321
        self.campaign = {
            'dm_username': 'foo'
        }

        self.db = Mock()
        self.db.set_character_link = Mock(return_value=True)
        self.db.get_campaign = Mock(return_value=(self.campaign_id, self.campaign))
        self.db.get_character_id = Mock(return_value=(self.character_id))
        self.db.get_character = Mock(return_value=get_test_character())

    def test_set_xp_with_empty_params(self):
        # execution
        rtn = add_xp('/add_xp', '', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual('Invalid command. Usage: /add_xp <username|character> <xp>', rtn)

    def test_set_xp_with_invalid_params(self):
        # execution
        rtn = add_xp('/add_xp', '9 @foobar', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual('Invalid command. Usage: /add_xp <username|character> <xp>', rtn)

    def test_set_xp_with_valid_params(self):
        # execution
        rtn = add_xp('/add_xp', '@foobar 301', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual('Amarok Skullsorrow received 301 pts of experience. XP: 326 | Level: 2', rtn)
