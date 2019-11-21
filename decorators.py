from exceptions import CharacterNotFound, CampaignNotFound, NotADM

def get_campaign(func):
    def fetch(command, txt_args, db, chat_id, username, **kargs):
        campaign_id, campaign = db.get_campaign(chat_id)
        if campaign_id is None:
            raise CampaignNotFound
        kargs['campaign'] = campaign
        kargs['campaign_id'] = campaign_id
        return func(command, txt_args, db, chat_id, username, **kargs)
    return fetch

#def get_linked_character(db, chat_id, username):
def get_linked_character_deco(func):
    def wrapper(command, txt_args, db, chat_id, username, **kargs):
        kargs['character_id'] = db.get_character_id(kargs.get('campaign_id'), username)
        kargs['character'] = db.get_character(kargs.get('character_id'), find_by_id=True)

        if kargs.get('character') == None:
            raise CharacterNotFound

        return func(command, txt_args, db, chat_id, username, **kargs)
    return wrapper

def only_dm(func):
    def validation(command, txt_args, db, chat_id, username, **kargs):
        if kargs.get('campaign') is None:
            raise CampaignNotFound

        dm_username = kargs.get('campaign').get('dm_username', None)
        if dm_username != username:
            raise NotADM
        return func(command, txt_args, db, chat_id, username, **kargs)
    return validation
