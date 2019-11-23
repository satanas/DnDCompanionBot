import utils

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

def get_character(_func=None, *, from_params=False):
    def get_character_decorator(func):
        def wrapper(command, txt_args, db, chat_id, username, **kargs):
            if 'campaign' not in kargs:
                raise CampaignNotFound

            args = txt_args.split(' ')

            search_param = args[0] if from_params is True and len(args) > 0 and args[0] != '' else username
            search_param = utils.normalized_username(search_param)

            kargs['character_id'] = db.get_character_id(kargs.get('campaign_id'), search_param)
            kargs['character'] = db.get_character(kargs.get('character_id'), find_by_id=True)

            if kargs.get('character') is None:
                raise CharacterNotFound

            return func(command, txt_args, db, chat_id, username, **kargs)
        return wrapper

    if _func is None:
        return get_character_decorator
    else:
        return get_character_decorator(_func)

