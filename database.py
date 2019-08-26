import os
import json

from firebase import firebase
from firebase.jsonutil import JSONEncoder

FIREBASE_API_SECRET = os.environ.get('FIREBASE_API_SECRET')

class Database:
    def __init__(self):
        self.firebase_db = firebase.FirebaseApplication('https://dndbot-c2cad.firebaseio.com', authentication=None)

    # TODO: Only active campaigns
    def get_campaign(self, chat_id):
        results = self.firebase_db.get('/', 'campaigns', params={'orderBy': '\"chat_id\"',
                                                                 'equalTo': chat_id,
                                                                 'auth': FIREBASE_API_SECRET})
        index = list(results.keys())[0]
        return index, results[index]

    def set_turn_index(self, campaign_id, turn_index):
        return self.firebase_db.patch(f'/campaigns/{campaign_id}',
                                      data={'turn_index': turn_index},
                                      params={'auth': FIREBASE_API_SECRET})

    def set_turns(self, campaign_id, turns):
        return self.firebase_db.patch(f'/campaigns/{campaign_id}',
                                      data={'turns': turns, 'turn_index': '0'},
                                      params={'auth': FIREBASE_API_SECRET})

    def get_character(self, chat_id, username):
        results = self.firebase_db.get('/', 'characters',
                                       params={'orderBy': '\"chat_id\", \"username\"',
                                               'equalTo': [chat_id, username],
                                               'auth': FIREBASE_API_SECRET})
        index = list(results.keys())[0]
        json_data = results[index]

        if not json_data:
            return None

        race = json_data['character']['race']['fullName']
        race_data = requests.get(RACE_URLS[race]).json()
        return Character(json_data, race_data)

    def save_character_info(self, character_id, character_data):
        return self.firebase_db.put('/characters', character_id, character_data, params={'auth': FIREBASE_API_SECRET})

    def set_dm(self, campaign_id, user_id, username):
        return self.firebase_db.patch(f'/campaigns/{campaign_id}',
                                      data={'dm_user_id': user_id, 'dm_username': username},
                                      params={'auth': FIREBASE_API_SECRET})

