from exceptions import CharacterNotFound, CampaignNotFound, NotADM

def only_dm(func):
    def wrapper(command, txt_args, db, chat_id, username, **kargs):
        if kargs.get('campaign') is None:
            raise CampaignNotFound

        dm_username = kargs.get('campaign').get('dm_username', None)
        if dm_username != username:
            raise NotADM
        return func(command, txt_args, db, chat_id, username, **kargs)
    return wrapper

def get_campaign(func):
    def wrapper(command, txt_args, db, chat_id, username, **kargs):
        campaign_id, campaign = db.get_campaign(chat_id)
        if campaign_id is None:
            raise CampaignNotFound

        kargs['campaign'] = campaign
        kargs['campaign_id'] = campaign_id
        return func(command, txt_args, db, chat_id, username, **kargs)
    return wrapper

def get_character(func):
    def wrapper(command, txt_args, db, chat_id, username, **kargs):
        if 'campaign' not in kargs:
            raise CampaignNotFound

        kargs['character_id'] = db.get_character_id(kargs.get('campaign_id'), username)
        kargs['character'] = db.get_character(kargs.get('character_id'), find_by_id=True)

        if kargs.get('character') is None:
            raise CharacterNotFound

        return func(command, txt_args, db, chat_id, username, **kargs)
    return wrapper

