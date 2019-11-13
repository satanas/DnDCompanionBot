import json
import unittest

from unittest.mock import patch, Mock, PropertyMock

from models.character import Character
from handlers.character import talk, import_character, link_character, get_status, ability_check

CHARACTER_JSON = {
    'character': {
        'id': '123456',
        'name': 'John Wick'
    }
}

class TestCharacter(unittest.TestCase):

    def test_yell(self):
        cmd = '/yell'
        txt_args = 'Beelzebub What the fuck is wrong with you?'
        result = talk(cmd, txt_args)
        expected = "```\r\nBeelzebub says:\r\n–WHAT THE FUCK IS WRONG WITH YOU?\r\n```"

        self.assertEqual(expected, result)

    def test_say(self):
        cmd = '/say'
        txt_args = 'Beelzebub What the fuck is wrong with you?'
        result = talk(cmd, txt_args)
        expected = "```\r\nBeelzebub says:\r\n–What the fuck is wrong with you?\r\n```"

        self.assertEqual(expected, result)

    def test_whisper(self):
        cmd = '/whisper'
        txt_args = 'Beelzebub What the fuck is wrong with you?'
        result = talk(cmd, txt_args)
        expected = "```\r\nBeelzebub says:\r\n–__What the fuck is wrong with you?__\r\n```"

        self.assertEqual(expected, result)

    def test_import_with_invalid_url(self):
        # conditions
        db = Mock()
        get = Mock()

        # execution
        cmd = 'hello_world'
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
        cmd = 'http://example.com/my/character'
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
        cmd = 'http://example.com/my/character'
        rtn = import_character(cmd, db, get)

        # expected
        db.save_character_info.assert_called_with('123456', CHARACTER_JSON)
        self.assertEqual(rtn, 'Character "John Wick" imported successfully!')

    def test_link_character_without_params(self):
        campaign_id = 666
        chat_id = 123456
        username = 'foo'
        db = Mock()
        db.set_character_link = Mock(return_value=True)
        db.get_campaign = Mock(return_value=(campaign_id, None))

        # execution
        args = '987654321'
        rtn = link_character(args, db, chat_id, username)

        # expected
        db.set_character_link.assert_called_with(campaign_id, username, args)
        self.assertEqual('Character with id 987654321 linked to foo successfully!', rtn)

    def test_link_character_with_params(self):
        campaign_id = 666
        chat_id = 123456
        username = 'foo'
        db = Mock()
        db.set_character_link = Mock(return_value=True)
        db.get_campaign = Mock(return_value=(campaign_id, None))

        # execution
        args = '987654321 @foobar'
        rtn = link_character(args, db, chat_id, username)

        # expected
        db.set_character_link.assert_called_with(campaign_id, 'foobar', '987654321')
        self.assertEqual('Character with id 987654321 linked to foobar successfully!', rtn)

    def test_status_without_params(self):
        # conditions
        character_id = 987654321
        campaign_id = 666
        chat_id = 123456
        username = 'foo'
        db = Mock()
        db.get_campaign = Mock(return_value=(campaign_id, None))
        db.get_character_id = Mock(return_value=(character_id))
        db.get_character = Mock(return_value=self.__get_character())

        # execution
        rtn = get_status('', db, chat_id, username)

        # expected
        db.get_character_id.assert_called_with(campaign_id, 'foo')
        self.assertEqual('Amarok Skullsorrow | Human Sorcerer Level 1\r\nHP: 6/6 | XP: 25', rtn)

    def test_status_with_params(self):
        # conditions
        character_id = 987654321
        campaign_id = 666
        chat_id = 123456
        username = 'foo'
        db = Mock()
        db.get_campaign = Mock(return_value=(campaign_id, None))
        db.get_character_id = Mock(return_value=(character_id))
        db.get_character = Mock(return_value=self.__get_character())

        # execution
        rtn = get_status('@foobar', db, chat_id, username)

        # expected
        db.get_character_id.assert_called_with(campaign_id, 'foobar')
        self.assertEqual('Amarok Skullsorrow | Human Sorcerer Level 1\r\nHP: 6/6 | XP: 25', rtn)

    def test_ability_check_with_empty_params(self):
        # conditions
        chat_id = 123456
        username = 'foo'
        db = Mock()

        # execution
        rtn = ability_check('', db, chat_id, username)
        self.assertEqual('Invalid ability. Supported options: str, dex, int, wis, cha', rtn)

    def test_ability_check_with_ability(self):
        # conditions
        character_id = 987654321
        campaign_id = 666
        chat_id = 123456
        username = 'foo'
        db = Mock()
        db.get_campaign = Mock(return_value=(campaign_id, None))
        db.get_character_id = Mock(return_value=(character_id))
        db.get_character = Mock(return_value=self.__get_character())

        # execution
        rtn = ability_check('str', db, chat_id, username)
        self.assertEqual(True, rtn.find("@foo ability check for Amarok Skullsorrow with STR:\r\nFormula: 1d20 + STR(4)\r\n*1d20+4*") == 0)

    def test_ability_check_with_ability_and_skill(self):
        # conditions
        character_id = 987654321
        campaign_id = 666
        chat_id = 123456
        username = 'foo'
        db = Mock()
        db.get_campaign = Mock(return_value=(campaign_id, None))
        db.get_character_id = Mock(return_value=(character_id))
        db.get_character = Mock(return_value=self.__get_character())

        # execution
        rtn = ability_check('wis perception', db, chat_id, username)
        self.assertEqual(True, rtn.find("@foo ability check for Amarok Skullsorrow with WIS (Perception):\r\nFormula: 1d20 + WIS(1) + Perception(1)\r\n*1d20+2*") == 0)

    def test_ability_check_with_ability_and_invalid_skill(self):
        # conditions
        chat_id = 123456
        username = 'foo'
        db = Mock()

        # execution
        rtn = ability_check('str perception', db, chat_id, username)
        self.assertEqual('Invalid skill. Supported options: athletics', rtn)


    def __get_character(self):
        with open('tests/fixtures/character.json', 'r') as jd:
            json_data = json.loads(jd.read())

        with open('tests/fixtures/race_data.json', 'r') as rd:
            race_data = json.loads(rd.read())

        return Character(json_data, race_data, False)
