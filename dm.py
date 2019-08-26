from database import Database

def handler(bot, update):
    db = Database()
    chat_id = update.message.chat.id
    text = update.message.text
    if text == '/set_dm':
        user_id = update.message.from_user.id
        username = update.message.from_user.username
        return set_dm(chat_id, user_id, username, db)
    elif text == '/dm':
        return get_dm(chat_id, db)

def set_dm(chat_id, user_id, username, db):
    campaign_id, campaign = db.get_campaign(chat_id)
    db.set_dm(campaign_id, user_id, username)
    return f"@{username} has been set as DM"

def get_dm(chat_id, db):
    campaign_id, campaign = db.get_campaign(chat_id)
    dm_username = campaign.get('dm_username', None)
    campaign_name = campaign.get('name', None)
    return f"DM for campaign \"{campaign_name}\" is @{dm_username}"
