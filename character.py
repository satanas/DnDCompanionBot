import sys
import requests
from firebase import firebase

from models.character import Character

RACE_URLS = {
    "Dwarf": "http://www.dnd5eapi.co/api/races/1",
    "Elf": "http://www.dnd5eapi.co/api/races/2",
    "Halfling": "http://www.dnd5eapi.co/api/races/3",
    "Human": "http://www.dnd5eapi.co/api/races/4",
    "Dragonborn": "http://www.dnd5eapi.co/api/races/5",
    "Gnome": "http://www.dnd5eapi.co/api/races/6",
    "Half-Elf": "http://www.dnd5eapi.co/api/races/7",
    "Half-Orc": "http://www.dnd5eapi.co/api/races/8",
    "Tiefling": "http://www.dnd5eapi.co/api/races/9"
}
FIREBASE_API_SECRET = os.environ.get('FIREBASE_API_SECRET')

def import_handler(bot, update, firebase_db):
    pass

def import_character(url, character_id, firebase_db):
    character_data = requests.get(url).json()

    results = firebase_db.put('/characters', character_id, character_data, params={'auth': FIREBASE_API_SECRET})

def load_character(character_id, firebase_db):
    json_data = firebase_db.get('/characters', character_id, params={'auth': FIREBASE_API_SECRET})
    race = json_data['character']['race']['fullName']
    race_data = requests.get(RACE_URLS[race]).json()

    c = Character(json_data, race_data)
    print(c)



if __name__ == "__main__":
    url = "https://dl.dropbox.com/s/awlpwcwi0eetdoq/ghamorz.json?dl=0"
    #import_character(url)
    load_character('123456')

