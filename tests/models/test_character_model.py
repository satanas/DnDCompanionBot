import json
import unittest

from unittest.mock import patch, Mock, PropertyMock

from models.character import Character

class TestCharacterModel(unittest.TestCase):
    def setUp(self):
        self.character = self.__get_character()

    def test_heal(self):
        # conditions
        self.character.current_hit_points = 1

        # execution
        self.character.heal(3)

        # expected
        self.assertEqual(4, self.character.current_hit_points)

    def test_overflow_heal(self):
        # conditions
        self.character.current_hit_points = 1

        # execution
        self.character.heal(999)

        # expected
        self.assertEqual(6, self.character.current_hit_points)

    def test_damage(self):
        # conditions
        self.character.current_hit_points = 6

        # execution
        self.character.damage(3)

        # expected
        self.assertEqual(3, self.character.current_hit_points)

    def test_overflow_damage(self):
        # conditions
        self.character.current_hit_points = 1

        # execution
        self.character.damage(999)

        # expected
        self.assertEqual(0, self.character.current_hit_points)

    def test_add_currency_with_not_enough_money(self):
        # conditions
        self.character.currencies['gp'] = 10

        # execution
        rtn = self.character.add_currency(-15, 'gp')

        # expected
        self.assertFalse(rtn)

    def test_add_currency_with_not_enough_money(self):
        # conditions
        self.character.currencies['cp'] = 10

        # execution
        rtn = self.character.add_currency(25, 'cp')

        # expected
        self.assertTrue(rtn)
        self.assertEqual(self.character.currencies['cp'], 35)

    def __get_character(self):
        with open('tests/fixtures/character.json', 'r') as jd:
            json_data = json.loads(jd.read())

        with open('tests/fixtures/race_data.json', 'r') as rd:
            race_data = json.loads(rd.read())

        return Character(json_data, race_data, False)
