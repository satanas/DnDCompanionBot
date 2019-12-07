import json
import unittest

from unittest.mock import patch, Mock, PropertyMock

from models.character import Character
from handlers.character import talk, import_character, link_character, get_status, ability_check, get_spells, \
                               initiative_roll, short_rest_roll, get_weapons, set_hp, handler, set_currency

CHARACTER_JSON = {
    'character': {
        'id': '123456',
        'name': 'John Wick'
    }
}

class TestCharacterHandler(unittest.TestCase):
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
        self.db.get_character = Mock(return_value=self.__get_character())
        self.db.set_character_link = Mock()

    def test_handler_import(self):
        # conditions
        self.db.set_dm = Mock()

        # execution
        rtn = handler(self.bot, self.update, '/link_char', 'http://my.url', self.username, self.chat_id, self.db)

        # expected
        self.bot.send_message.assert_called_with(chat_id=self.chat_id, parse_mode="Markdown",
                text="Character with id http://my.url linked to foo successfully!")

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
        rtn = link_character('/link_char', args, self.db, self.chat_id, self.username)

        # expected
        self.db.set_character_link.assert_called_with(self.campaign_id, self.username, args)
        self.assertEqual('Character with id 987654321 linked to foo successfully!', rtn)

    def test_link_character_with_params(self):
        # execution
        args = '987654321 @foobar'
        rtn = link_character('/link_char', args, self.db, self.chat_id, self.username)

        # expected
        self.db.set_character_link.assert_called_with(self.campaign_id, 'foobar', '987654321')
        self.assertEqual('Character with id 987654321 linked to foobar successfully!', rtn)

    def test_initiative_roll(self):
        # execution
        rtn = initiative_roll('/initiative_roll', '', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual(True, rtn.find("@foo initiative roll for Amarok Skullsorrow:\r\nFormula: 1d20 + DEX(1)\r\n*1d20+1*") == 0)

    def test_short_rest_roll(self):
        # execution
        rtn = short_rest_roll('/short_rest_roll', '', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual(True, rtn.find("@foo short rest roll for Amarok Skullsorrow:\r\nFormula: 1d6 + CON(0)\r\n*1d6+0*") == 0)

    def test_get_spells_without_username(self):
        # execution
        rtn = get_spells('/spells', '', self.db, self.chat_id, self.username)

        # expected
        self.db.get_character_id.assert_called_with(self.campaign_id, self.username)
        self.assertEqual("Attack spells for Amarok Skullsorrow: thunderclap, create-bonfire, fire-bolt, magic-missile", rtn)

    def test_get_spells_with_username(self):
        # execution
        rtn = get_spells('/spells', 'foobar', self.db, self.chat_id, self.username)

        # expected
        self.db.get_character_id.assert_called_with(self.campaign_id, 'foobar')
        self.assertEqual("Attack spells for Amarok Skullsorrow: thunderclap, create-bonfire, fire-bolt, magic-missile", rtn)

    def test_get_spells_with_no_spells(self):
         # conditions
        character = self.__get_character()
        character.spells = []
        self.db.get_character = Mock(return_value=character)

        # execution
        rtn = get_spells('/spells', '', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual("Amarok Skullsorrow does not have any attack spells", rtn)

    def test_get_weapons_without_username(self):
        # execution
        rtn = get_weapons('/weapons', '', self.db, self.chat_id, self.username)

        # expected
        self.db.get_character_id.assert_called_with(self.campaign_id, self.username)
        self.assertEqual(f"Weapons in Amarok Skullsorrow's inventory: dagger, dagger, quarterstaff, crossbow, dart, sling", rtn)

    def test_get_weapons_with_username(self):
        # execution
        rtn = get_weapons('/weapons', 'foobar', self.db, self.chat_id, self.username)

        # expected
        self.db.get_character_id.assert_called_with(self.campaign_id, 'foobar')
        self.assertEqual(f"Weapons in Amarok Skullsorrow's inventory: dagger, dagger, quarterstaff, crossbow, dart, sling", rtn)

    def test_get_weapons_with_no_weapons(self):
        # conditions
        character = self.__get_character()
        character.weapons = []
        self.db.get_character = Mock(return_value=character)

        # execution
        rtn = get_weapons('/weapons', 'foobar', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual(f"Amarok Skullsorrow does not have any weapon", rtn)

    def test_status_without_params(self):
        # execution
        rtn = get_status('/status', '', self.db, self.chat_id, self.username)

        # expected
        self.db.get_character_id.assert_called_with(self.campaign_id, 'foo')
        self.assertEqual((f'```\r\nAmarok Skullsorrow | Human Sorcerer | Level 1\r\nHP: 6/6 | XP: 25/300 \r\n'
                        f'0 CP | 0 SP | 0 EP | 0 GP | 0 PP ```'), rtn)

    def test_status_with_params(self):
        # execution
        rtn = get_status('/status', '@foobar', self.db, self.chat_id, self.username)

        # expected
        self.db.get_character_id.assert_called_with(self.campaign_id, 'foobar')
        self.assertEqual((f'```\r\nAmarok Skullsorrow | Human Sorcerer | Level 1\r\nHP: 6/6 | XP: 25/300 \r\n'
                        f'0 CP | 0 SP | 0 EP | 0 GP | 0 PP ```'), rtn)

    def test_set_currency_without_params(self):
        # execution
        rtn = set_currency('/set_currency', '@foobar', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual('Invalid command. Usage: /set_currency <username|character> <currencies>', rtn)

    def test_set_currency_with_invalid_equation(self):
        # execution
        rtn = set_currency('/set_currency', '10gp @foobar', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual('Your request did not have a valid equation. Please use the currency notation (for example: 10gp, -20cp)', rtn)

    def test_set_currency_with_not_enough_money(self):
        # execution
        rtn = set_currency('/set_currency', '@foobar -99999gp', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual('You cannot afford -99999gp. Operation cancelled.', rtn)

    def test_set_currency_with_valid_params(self):
        # conditions
        expected_character = self.__get_character()
        expected_character.currencies['gp'] = 25

        # execution
        rtn = set_currency('/set_currency', '@foobar 25gp', self.db, self.chat_id, self.username)

        # expected
        self.db.set_char_currency.assert_called_with(expected_character.id, expected_character.currencies)
        self.assertEqual((f'```\r\nAmarok Skullsorrow | Human Sorcerer | Level 1\r\nHP: 6/6 | XP: 25/300 \r\n'
                        f'0 CP | 0 SP | 0 EP | 25 GP | 0 PP ```'), rtn)

    def test_set_hp_with_empty_params(self):
        # execution
        rtn = set_hp('/damage', '', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual('Invalid command. Usage: /damage <username|character> <hp>', rtn)

    def test_set_hp_with_invalid_params(self):
        # execution
        rtn = set_hp('/damage', '9 @foobar', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual('Invalid command. Usage: /damage <username|character> <hp>', rtn)

    def test_set_hp_with_valid_params(self):
        # execution
        rtn = set_hp('/damage', '@foobar 9', self.db, self.chat_id, self.username)

        # expected
        self.assertEqual('Amarok Skullsorrow received 9 pts of damage. HP: 0/6', rtn)

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



    def __get_character(self):
        with open('tests/fixtures/character.json', 'r') as jd:
            json_data = json.loads(jd.read())

        with open('tests/fixtures/race_data.json', 'r') as rd:
            race_data = json.loads(rd.read())

        return Character(json_data, race_data, False)
