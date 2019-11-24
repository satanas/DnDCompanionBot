from database import Database
from decorators import get_campaign, only_dm, get_character

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
    elif command == '/add_xp':
        response = add_xp(command, txt_args, db, chat_id, username)
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
    if dm_username is None:
        return f"Campaign \"{campaign_name}\" doesn't have a DM set"
    else:
        return f"DM for campaign \"{campaign_name}\" is @{dm_username}"

@get_campaign
@only_dm
@get_character(from_params=True)
def add_xp(command, txt_args, db, chat_id, username, **kargs):
    args = txt_args.split(' ')
    if len(args) < 2 or args[1].isdigit() is False:
        return f'Invalid command. Usage: {command} <username|character> <xp>'

    points = int(args[1])
    character = kargs.get('character')
    command = command.replace('/', '').strip()

    character.add_xp(points)

    db.set_char_xp(character.id, xp_points=character.current_experience)
    db.set_char_level(character.id, level=character.level)
    return f'{character.name} received {points} pts of experience. XP: {character.current_experience} | Level: {character.level}'
