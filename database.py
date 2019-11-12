import os
import json
import requests

from models.campaign import Campaign
from models.character import Character

from firebase import firebase
from firebase.jsonutil import JSONEncoder

FIREBASE_DB_URL = os.environ.get('FIREBASE_DB_URL')
FIREBASE_API_SECRET = os.environ.get('FIREBASE_API_SECRET')

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

# https://firebase.google.com/docs/database/rest/retrieve-data#section-rest-filtering
class Database:
    def __init__(self):
        self.firebase_db = firebase.FirebaseApplication(FIREBASE_DB_URL, authentication=None)

    def create_campaign(self, chat_id, name):
        campaign = Campaign(chat_id, name)

        self.firebase_db.post('/campaigns',
                              data=campaign.to_json(),
                              params={'auth': FIREBASE_API_SECRET})

    # TODO: Only active campaigns
    def get_campaign(self, chat_id):
        results = self.firebase_db.get('/', 'campaigns', params={'orderBy': '\"chat_id\"',
                                                                 'equalTo': chat_id,
                                                                 'auth': FIREBASE_API_SECRET})

        active_campaigns = [(c, results[c]) for c in list(results.keys()) if results[c]['active'] == True]
        if len(active_campaigns) == 0:
            return None, None
        campaign_id, campaign = active_campaigns[0]
        return campaign_id, campaign

    def close_campaign(self, campaign_id):
        return self.firebase_db.patch(f'/campaigns/{campaign_id}',
                                      data={'active': False},
                                      params={'auth': FIREBASE_API_SECRET})

    def set_turn_index(self, campaign_id, turn_index):
        return self.firebase_db.patch(f'/campaigns/{campaign_id}',
                                      data={'turn_index': turn_index},
                                      params={'auth': FIREBASE_API_SECRET})

    def set_turns(self, campaign_id, turns):
        return self.firebase_db.patch(f'/campaigns/{campaign_id}',
                                      data={'turns': turns, 'turn_index': '0'},
                                      params={'auth': FIREBASE_API_SECRET})

    def get_character_id(self, campaign_id, username):
        result = self.firebase_db.get('/', f'campaigns/{campaign_id}/characters', params={'orderBy': '\"$key\"',
                                                                 'equalTo': '\"'+username+'\"',
                                                                 'auth': FIREBASE_API_SECRET})

        if not result:
            return None

        return result[username]

    def get_character(self, character, find_by_id):
        if find_by_id:
            result = self.firebase_db.get('/', f'/characters/{character}', params={'auth': FIREBASE_API_SECRET})
        else:
            result = self.firebase_db.get('/', 'characters', params={'orderBy': '\"character/name\"',
                                                                    'equalTo': f'\"{character}\"',
                                                                    'auth': FIREBASE_API_SECRET})
        if not result:
            return None

        json_data = result[list(result.keys())[0]]

        race = json_data['race']['baseName'] if find_by_id else json_data['character']['race']['baseName']
        race_data = requests.get(RACE_URLS[race]).json()
        return Character(json_data, race_data, find_by_id)

    def save_character_info(self, character_id, character_data):
        return self.firebase_db.put('/characters', character_id, character_data, params={'auth': FIREBASE_API_SECRET})

    def set_character_link(self, campaign_id, username, character_id):
        return self.firebase_db.patch(f'/campaigns/{campaign_id}/characters',
                                      data={username: character_id},
                                      params={'auth': FIREBASE_API_SECRET})

    def set_dm(self, campaign_id, user_id, username):
        return self.firebase_db.patch(f'/campaigns/{campaign_id}',
                                      data={'dm_user_id': user_id, 'dm_username': username},
                                      params={'auth': FIREBASE_API_SECRET})

    def set_user_char(self, campaign_id, user_id, char_name):
        return self.firebase_db.patch(f'/campaigns/{campaign_id}',
                                      data={'dm_user_id': user_id, 'dm_username': username},
                                      params={'auth': FIREBASE_API_SECRET})        


class CampaignActiveException(Exception):
    def __init__(self, message):
        super().__init__(message)

class CampaignNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
