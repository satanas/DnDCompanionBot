import unittest

from unittest.mock import Mock
from handlers.dm import handler, add_xp
from tests.helper import get_test_character
from exceptions import CampaignNotFound

class TestDMHandler(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.bot.send_message = Mock()
        self.update = Mock()
        self.update.message = Mock()
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

    def test_set_dm_with_empty_campaign(self):
        # conditions
        self.db.get_campaign = Mock(return_value=(None, None))

        #execution
        with self.assertRaises(CampaignNotFound) as context:
            handler(self.bot, self.update, '/set_dm', self.username, self.username, self.chat_id, self.db)

    def test_set_dm_with_valid_params(self):
        # conditions
        self.update.message.from_user = Mock()
        self.update.message.from_user.id = '666'
        self.db.set_dm = Mock()

        # execution
        rtn = handler(self.bot, self.update, '/set_dm', self.username, self.username, self.chat_id, self.db)

        # expected
        self.bot.send_message.assert_called_with(chat_id=self.chat_id, text="@foo has been set as DM", parse_mode="Markdown")

