from database import Database

def handler(bot, update):
    db = Database()
    chat_id = update.message.chat.id
    text = update.message.text
    if text == '/set_dm':
        return set_dm(chat_id, update, db)
    elif text == '/dm':
        return get_dm(chat_id, db)

def set_dm(chat_id, update, db):
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    db.set_dm(chat_id, user_id, username)
    return f"@{username} has been set as DM"

def get_dm(chat_id, db):
    campaign = db.get_campaign(chat_id)
    dm_username = campaign.get('dm_username', None)
    campaign_name = campaign.get('name', None)
    return f"DM for campaign \"{campaign_name}\" is @{username}"
