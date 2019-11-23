import json

from models.character import Character

def get_test_character():
    with open('tests/fixtures/character.json', 'r') as jd:
        json_data = json.loads(jd.read())

    with open('tests/fixtures/race_data.json', 'r') as rd:
        race_data = json.loads(rd.read())

    return Character(json_data, race_data, False)

def get_test_weapon_data():
    with open('tests/fixtures/weapon.json', 'r') as jd:
        json_data = json.loads(jd.read())
    return json_data
