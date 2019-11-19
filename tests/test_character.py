import json
import unittest

from unittest.mock import patch, Mock, PropertyMock

from models.character import Character
from handlers.character import talk, import_character, link_character, get_status, ability_check, get_spells, \
                               initiative_roll, short_rest_roll, get_weapons

CHARACTER_JSON = {
    'character': {
        'id': '123456',
        'name': 'John Wick'
    }
}

class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.campaign_id = 666
        self.chat_id = 123456
        self.username = 'foo'
        self.character_id = 987654321
        self.db = Mock()
        self.db.set_character_link = Mock(return_value=True)
        self.db.get_campaign = Mock(return_value=(self.campaign_id, None))
        self.db.get_character_id = Mock(return_value=(self.character_id))
        self.db.get_character = Mock(return_value=self.__get_character())

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
        get = Mock()

        # execution
        cmd = 'hello_world'
        rtn = import_character(cmd, self.db, get)

        # expected
        self.assertEqual(rtn, 'hello_world is not a valid URL')

    def test_import_with_request_error(self):
        # conditions
        response = Mock()
        response.status_code = 500
        get = Mock(return_value=response)

        # execution
        cmd = 'http://example.com/my/character'
        rtn = import_character(cmd, self.db, get)

        # expected
        self.assertEqual(rtn, 'Error fetching http://example.com/my/character (status_code: 500)')

    def test_valid_import(self):
        # conditions
        response = Mock()
        response.status_code = 200
        response.json = Mock(return_value=CHARACTER_JSON)
        get = Mock(return_value=response)

        # execution
        cmd = 'http://example.com/my/character'
        rtn = import_character(cmd, self.db, get)

        # expected
        self.db.save_character_info.assert_called_with('123456', CHARACTER_JSON)
        self.assertEqual(rtn, 'Character "John Wick" imported successfully!')

    def test_link_character_without_params(self):
        # execution
        args = '987654321'
        rtn = link_character(args, self.db, self.chat_id, self.username)

        # expected
        self.db.set_character_link.assert_called_with(self.campaign_id, self.username, args)
        self.assertEqual('Character with id 987654321 linked to foo successfully!', rtn)

    def test_link_character_with_params(self):
        # execution
        args = '987654321 @foobar'
        rtn = link_character(args, self.db, self.chat_id, self.username)

        # expected
        self.db.set_character_link.assert_called_with(self.campaign_id, 'foobar', '987654321')
        self.assertEqual('Character with id 987654321 linked to foobar successfully!', rtn)

    def test_initiative_roll(self):
        # execution
        rtn = initiative_roll('', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual(True, rtn.find("@foo initiative roll for Amarok Skullsorrow:\r\nFormula: 1d20 + DEX(1)\r\n*1d20+1*") == 0)

    def test_short_rest_roll(self):
        # execution
        rtn = short_rest_roll('', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual(True, rtn.find("@foo short rest roll for Amarok Skullsorrow:\r\nFormula: 1d6 + CON(0)\r\n*1d6+0*") == 0)


    def test_status_without_params(self):
        # execution
        rtn = get_status('', self.db, self.chat_id, self.username)

        # expected
        self.db.get_character_id.assert_called_with(self.campaign_id, 'foo')
        self.assertEqual((f'```\r\nAmarok Skullsorrow | Human Sorcerer Level 1\r\nHP: 6/6 | XP: 25/300 \r\n'
                        f'0 CP | 0 SP | 0 EP | 0 GP | 0 PP ```'), rtn)

    def test_status_with_params(self):
        # execution
        rtn = get_status('@foobar', self.db, self.chat_id, self.username)

        # expected
        self.db.get_character_id.assert_called_with(self.campaign_id, 'foobar')
        self.assertEqual((f'```\r\nAmarok Skullsorrow | Human Sorcerer Level 1\r\nHP: 6/6 | XP: 25/300 \r\n'
                        f'0 CP | 0 SP | 0 EP | 0 GP | 0 PP ```'), rtn)

    def test_ability_check_with_empty_params(self):
        # execution
        rtn = ability_check('', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual('Invalid ability. Supported options: str, dex, int, wis, cha', rtn)

    def test_ability_check_with_ability(self):
        # execution
        rtn = ability_check('str', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual(True, rtn.find("@foo ability check for Amarok Skullsorrow with STR:\r\nFormula: 1d20 + STR(4)\r\n*1d20+4*") == 0)

    def test_ability_check_with_ability_and_skill(self):
        # execution
        rtn = ability_check('wis perception', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual(True, rtn.find("@foo ability check for Amarok Skullsorrow with WIS (Perception):\r\nFormula: 1d20 + WIS(1) + Perception(3)\r\n*1d20+4*") == 0)

    def test_ability_check_with_ability_and_invalid_skill(self):
        # execution
        rtn = ability_check('str perception', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual('Invalid skill. Supported options: athletics', rtn)

    def test_get_spells(self):
        # execution
        rtn = get_spells('', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual("Attack spells for Amarok Skullsorrow: thunderclap, create-bonfire, fire-bolt, magic-missile", rtn)

    def test_get_weapons_without_username(self):
        # execution
        rtn = get_weapons('', self.db, self.chat_id, self.username)

        # expected
        self.db.get_character_id.assert_called_with(self.campaign_id, self.username)
        self.assertEqual(f"Weapons in Amarok Skullsorrow's inventory: dagger, dagger, quarterstaff, crossbow, dart, sling", rtn)

    def test_get_weapons_with_username(self):
        # execution
        rtn = get_weapons('foobar', self.db, self.chat_id, self.username)

        # expected
        self.db.get_character_id.assert_called_with(self.campaign_id, 'foobar')
        self.assertEqual(f"Weapons in Amarok Skullsorrow's inventory: dagger, dagger, quarterstaff, crossbow, dart, sling", rtn)

    def test_get_weapons_with_no_weapons(self):
        # conditions
        character = self.__get_character()
        character.weapons = []
        self.db.get_character = Mock(return_value=character)

        # execution
        rtn = get_weapons('foobar', self.db, self.chat_id, self.username)

        # expected
        self.db.get_character_id.assert_called_with(self.campaign_id, 'foobar')
        self.assertEqual(f"Amarok Skullsorrow does not have any weapon", rtn)



    def __get_character(self):
        with open('tests/fixtures/character.json', 'r') as jd:
            json_data = json.loads(jd.read())

        with open('tests/fixtures/race_data.json', 'r') as rd:
            race_data = json.loads(rd.read())

        return Character(json_data, race_data, False)
