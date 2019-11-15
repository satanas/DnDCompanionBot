import math

import utils

from models.armor import Armor
from models.weapon import Weapon
from models.spell import Spell

ABILITIES = [
    'str',
    'dex',
    'int',
    'wis',
    'cha'
]

SKILLS = {
    'str': [
        'athletics'
    ],
    'dex': [
        'acrobatics',
        'sleight-of-hand',
        'stealth'
    ],
    'int': [
        'arcana',
        'history',
        'investigation',
        'nature',
        'religion'
    ],
    'wis': [
        'animal-handling',
        'insight',
        'medicine',
        'perception',
        'survival'
    ],
    'cha': [
        'deception',
        'intimidation',
        'performance',
        'persuasion'
    ]
}

ABILITIES_INDEX = {
    0: 'str',
    1: 'dex',
    2: 'con',
    3: 'int',
    4: 'wis',
    5: 'cha'
}

class Character:
    def __init__(self, json_data, race_data, by_id):
        character = json_data if by_id else json_data['character']

        self.id = character['id']
        self.beyond_url = character['readonlyUrl']
        self.name = character['name']
        self.level = int(character['classes'][0]['level'])
        self.race = character['race']['baseName']
        self._class = character['classes'][0]['definition']['name']
        self.str = int(character['stats'][0]['value']) + int(race_data['ability_bonuses'][0])
        self.dex = int(character['stats'][1]['value']) + int(race_data['ability_bonuses'][1])
        self.con = int(character['stats'][2]['value']) + int(race_data['ability_bonuses'][2])
        self.int = int(character['stats'][3]['value']) + int(race_data['ability_bonuses'][3])
        self.wis = int(character['stats'][4]['value']) + int(race_data['ability_bonuses'][4])
        self.cha = int(character['stats'][5]['value']) + int(race_data['ability_bonuses'][5])
        self.str_mod = math.floor((self.str - 10) / 2)
        self.dex_mod = math.floor((self.dex - 10) / 2)
        self.con_mod = math.floor((self.con - 10) / 2)
        self.int_mod = math.floor((self.int - 10) / 2)
        self.wis_mod = math.floor((self.wis - 10) / 2)
        self.cha_mod = math.floor((self.cha - 10) / 2)
        self.walking_speed = int(character['race']['weightSpeeds']['normal']['walk'])
        self.max_hit_points = int(character['baseHitPoints']) + self.con_mod
        self.removed_hit_points = int(character['removedHitPoints'])
        self.current_hit_points = self.max_hit_points - self.removed_hit_points
        self.hit_dice = int(character['classes'][0]['definition']['hitDice'])
        self.hit_dice_used = int(character['classes'][0]['hitDiceUsed'])
        self.current_experience = int(character['currentXp'])
        self.initiative = self.dex_mod
        self.weapons = [Weapon(x) for x in character['inventory'] if x['definition']['filterType'] == "Weapon"]
        self.armor = [Armor(x) for x in character['inventory'] if x['definition']['filterType'] == "Armor"]
        self.proficiencies = [x['subType'] for x in character['modifiers']['class'] if x['type'] == 'proficiency']
        self.size = character['race']['size']
        self.proficiency = math.floor((self.level + 7) / 4)
        self.spells = []

        self.mods = self.__calculate_modifiers()

        # Define spellcasting stuff
        if character['classes'][0]['definition']['canCastSpells'] is True:
            spellcasting_ability_id = int(character['classes'][0]['definition']['spellCastingAbilityId']) - 1
            self.spellcasting_ability_mod = self.mods[ABILITIES_INDEX[spellcasting_ability_id]] + self.proficiency
            # Load spells from feat
            if 'spells' in character:
                if 'feat' in character['spells']:
                    for x in character['spells']['feat']:
                        if "Damage" in x['definition']['tags']:
                            self.spells.append(Spell(x))

            # Load spells from class spells
            for x in character['classSpells']:
                for y in x['spells']:
                    if "Damage" in y['definition']['tags']:
                        self.spells.append(Spell(y))

    def has_proficiency(self, arg):
        return True if utils.to_snake_case(arg) in self.proficiencies else False

    def get_weapon(self, weapon_name):
        result = [w for w in self.weapons if w.name == weapon_name]
        if len(result) > 0:
            return result[0]
        else:
            return None

    def get_spell(self, spell_name):
        result = [s for s in self.spells if s.name == spell_name]
        if len(result) > 0:
            return result[0]
        else:
            return None

    def __calculate_modifiers(self):
        mods = {
            'str': self.str_mod,
            'dex': self.dex_mod,
            'con': self.con_mod,
            'int': self.int_mod,
            'wis': self.wis_mod,
            'cha': self.cha_mod
        }

        for ability in ABILITIES:
            for skill in SKILLS[ability]:
                mods[skill] = mods[ability]
                if self.has_proficiency(skill):
                    mods[skill] += self.proficiency

        return mods


    def __str__(self):
        return (f"Character name={self.name}, race={self.race}, str={self.str}({self.str_mod}), dex={self.dex}({self.dex_mod}), "
                f"con={self.con}({self.con_mod}), int={self.int}({self.int_mod}), wis={self.wis}({self.wis_mod}), "
                f"cha={self.cha}({self.cha_mod}), walking_speed={self.walking_speed}, max_hit_points={self.max_hit_points}, "
                f"current_hit_points={self.current_hit_points}, initiative={self.initiative}")

