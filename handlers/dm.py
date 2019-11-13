from database import Database

def handler(bot, update, command, txt_args):
    db = Database()
    chat_id = update.message.chat.id
    text = update.message.text
    if command == '/set_dm':
        user_id = update.message.from_user.id
        username = update.message.from_user.username
        response = set_dm(chat_id, user_id, username, db)
    elif command == '/dm':
        response = get_dm(chat_id, db)
    else:
        response = "Invalid command"

    bot.send_message(chat_id=update.message.chat_id, text=response, parse_mode="Markdown")

def set_dm(chat_id, user_id, username, db):
    campaign_id, campaign = db.get_campaign(chat_id)
    db.set_dm(campaign_id, user_id, username)
    return f"@{username} has been set as DM"

def get_dm(chat_id, db):
    campaign_id, campaign = db.get_campaign(chat_id)
    dm_username = campaign.get('dm_username', None)
    campaign_name = campaign.get('name', None)
    return f"DM for campaign \"{campaign_name}\" is @{dm_username}"
