import unittest

from unittest.mock import Mock

from handlers.character import handler

class TestCharsheetHandler(unittest.TestCase):
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
        self.db.set_character_link = Mock()

    def test_handler_import(self):
        pass
