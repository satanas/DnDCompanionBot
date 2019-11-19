from database import Database
from exceptions import CampaignNotFound, NotADM

def handler(bot, update, command, txt_args):
    db = Database()
    chat_id = update.message.chat.id
    text = update.message.text
    username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name

    if command == '/start_campaign':
        response = start_campaign(chat_id, txt_args, db)
    elif command == '/close_campaign':
        response = close_campaign(chat_id, db)
    elif command == '/start_battle':
        response = start_battle(chat_id, txt_args, db, username)
    elif command == '/set_positions':
        response = set_battle_positions(chat_id, txt_args, db, username)

    bot.send_message(chat_id=update.message.chat_id, text=response, parse_mode="Markdown")

def start_campaign(chat_id, text, db):
    campaign_id, campaign = db.get_campaign(chat_id)
    if campaign_id != None or campaign != None:
        return 'There is an active campaign for this group. Close the active campaign before creating a new one'

    db.create_campaign(chat_id, text)
    return "Campaign created successfully!"

def close_campaign(chat_id, db):
    campaign_id, campaign = db.get_campaign(chat_id)
    if campaign_id == None or campaign == None:
        return 'There are no active campaigns for this group'

    db.close_campaign(campaign_id)
    return "Campaign closed successfully!"

def start_battle(chat_id, txt_args, db, username):
    campaign_id, campaign = db.get_campaign(chat_id)
    if campaign_id == None or campaign == None:
        raise CampaignNotFound

    dm_username = campaign.get('dm_username', None)
    if dm_username != username:
        raise NotADM

    args = txt_args.split(' ')
    if len(args) < 2:
        return f"You must set the battle field width and height"

    if not args[0].isdigit() or not args[1].isdigit():
        return f"Width and height must be integer values"
    elif int(args[0]) < 3 or int(args[1]) < 3:
        return f"Width and height must be greater than 3"

    battle_field = {
        'width': int(args[0]),
        'heigth': int(args[1]),
    }

    db.start_battle(campaign_id, battle_field)

    return "Battle field ready!"

def set_battle_positions(chat_id, txt_args, db, username):
    campaign_id, campaign = db.get_campaign(chat_id)
    if campaign_id == None or campaign == None:
        raise CampaignNotFound

    dm_username = campaign.get('dm_username', None)
    if dm_username != username:
        raise NotADM

    args = txt_args.split(',')
    positions = {}
    for position in args:
        position = position.split(' ')
        position = list(filter(None, position))
        positions[position[0]] = position[1]

    db.set_battle_positions(campaign_id, positions)

    return "Positions setted successfully!"

if __name__ == "__main__":
    db = Database()
    print(start_campaign('3383241', 'TEst', db))

