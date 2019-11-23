import unittest

from unittest.mock import Mock
from models.weapon import Weapon
from tests.helper import get_test_weapon_data

class TestWeaponModel(unittest.TestCase):
    def setUp(self):
        self.json_data = get_test_weapon_data()

    def test_weapon_without_properties(self):
        # conditions
        del self.json_data['definition']['properties']

        # execution
        weapon = Weapon(self.json_data)

        # expected
        self.assertEqual(0, len(weapon.properties))

    def test_weapon_has_finesse(self):
        # execution
        weapon = Weapon(self.json_data)

        # conditions
        weapon.properties = ["Finesse"]

        # expected
        self.assertTrue(weapon.has_finesse())

    def test_weapon_has_thrown(self):
        # execution
        weapon = Weapon(self.json_data)

        # conditions
        weapon.properties = ["Thrown"]

        # expected
        self.assertTrue(weapon.has_thrown())

    def test_weapon_has_no_special_attributes(self):
        # execution
        weapon = Weapon(self.json_data)

        # conditions
        weapon.properties = []

        # expected
        self.assertFalse(weapon.has_finesse())
        self.assertFalse(weapon.has_thrown())


