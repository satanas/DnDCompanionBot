import unittest

from unittest.mock import Mock

from tests.helper import get_test_character
from handlers.turns import handler

class TestTurnHandler(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.bot.send_message = Mock()
        self.update = Mock()
        self.campaign_id = 666
        self.chat_id = 123456
        self.username = 'foo'
        self.character_id = 987654321
        self.campaign = {
            'dm_username': 'foo',
            'turns': ['foo', 'bar', 'baz'],
            'turn_index': 0
        }

        self.db = Mock()
        self.db.set_character_link = Mock(return_value=True)
        self.db.get_campaign = Mock(return_value=(self.campaign_id, self.campaign))
        self.db.get_character_id = Mock(return_value=(self.character_id))
        self.db.get_character = Mock(return_value=get_test_character())
        self.db.set_character_link = Mock()

    def test_roll_handler(self):
        # conditions
        self.db.set_dm = Mock()

        # execution
        rtn = handler(self.bot, self.update, '/turn', '', self.username, self.chat_id, self.db)

        # expected
        self.bot.send_message.assert_called_with(chat_id=self.chat_id, parse_mode="Markdown",
                text="Next in line is foo")
