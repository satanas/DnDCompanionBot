class Campaign:
    def __init__(self, chat_id, name):
        self.active = True
        self.chat_id = chat_id
        self.name = name
        self.turn_index = 0
        self.characters = []
        self.turns = []
        self.dm_user_id = 0
        self.dm_username = None

    def to_json(self):
        return {
            'active': self.active,
            'name': self.name,
            'characters': self.characters,
            'chat_id': int(self.chat_id),
            'dm_user_id': int(self.dm_user_id),
            'dm_username': self.dm_username,
            'turn_index': int(self.turn_index),
            'turns': self.turns
        }
