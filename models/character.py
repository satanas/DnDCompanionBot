import math

from models.armor import Armor
from models.weapon import Weapon

class Character:
    def __init__(self, json_data, race_data, by_id):
        character = json_data if by_id else json_data['character']
        self.id = character['id']
        self.beyond_url = character['readonlyUrl']
        self.name = character['name']
        self.level = int(character['classes'][0]['level'])
        self.race = character['race']['fullName']
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
        self.current_hit_points = self.max_hit_points - int(character['removedHitPoints'])
        self.hit_dice = int(character['classes'][0]['definition']['hitDice'])
        self.hit_dice_used = int(character['classes'][0]['hitDiceUsed'])
        self.current_experience = int(character['currentXp'])
        self.initiative = self.dex_mod
        self.weapons = [Weapon(x) for x in character['inventory'] if x['definition']['filterType'] == "Weapon"]
        self.armor = [Armor(x) for x in character['inventory'] if x['definition']['filterType'] == "Armor"]
        self.proficiencies = [x['friendlySubtypeName'] for x in character['modifiers']['class'] if x['type'] == 'proficiency']
        self.size = character['race']['size']
        self.proficiency = math.floor((self.level + 7) / 4)


    def has_weapon_proficiency(self, weapon):
        return True if weapon in self.proficiencies else False

    def get_weapon(self, weapon_name):
        result = [w for w in self.weapons if w.name == weapon_name]
        if len(result) > 0:
            return result[0]
        else:
            return None

    def __str__(self):
        return (f"Character name={self.name}, race={self.race}, str={self.str}({self.str_mod}), dex={self.dex}({self.dex_mod}), "
                f"con={self.con}({self.con_mod}), int={self.int}({self.int_mod}), wis={self.wis}({self.wis_mod}), "
                f"cha={self.cha}({self.cha_mod}), walking_speed={self.walking_speed}, max_hit_points={self.max_hit_points}, "
                f"current_hit_points={self.current_hit_points}, initiative={self.initiative}")

