import os
import string
import utils

from database import Database
from exceptions import CampaignNotFound, NotADM

def handler(bot, update, command, txt_args, username, chat_id, db):
    if command == '/start_campaign':
        response = start_campaign(chat_id, txt_args, db)
    elif command == '/close_campaign':
        response = close_campaign(chat_id, db)
    elif command == '/start_battle':
        response = start_battle(chat_id, txt_args, db, username)
    elif command == '/set_positions':
        response = set_battle_positions(chat_id, txt_args, db, username)
    elif command == '/map':
        response = render_map(chat_id, db)

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
        positions[utils.normalized_username(position[0])] = position[1]
        positions[position[0]] = position[1]

    db.set_battle_positions(campaign_id, positions)

    return "Positions setted successfully!"

def render_map(chat_id, db):
    campaign_id, campaign = db.get_campaign(chat_id)
    battle_field = campaign.get('battle_field', None)

    positions = battle_field.get('positions', None)

    coords = {}
    for character in positions:
        pos = positions[character]
        x = pos[0]
        y = pos[1:len(pos)]
        if y not in coords:
            coords[int(y)] = {}
            coords[int(y)][string.ascii_uppercase.index(x)] = character
        else:
            coords[int(y)][string.ascii_uppercase.index(x)] = character

    bf_map = '```'
    letters = string.ascii_uppercase
    for y in range(battle_field['heigth'] + 4):
        for x in range(battle_field['width'] + 1):
            if y == 0 or y == 2 or y == (battle_field['heigth'] + 3):
                if x == 0:
                    bf_map += '+----+'
                else:
                    bf_map += '----+\n' if x == battle_field['width'] else '----+'
            elif y == 1:
                if x > 9:
                    bf_map += f' {x} |\n' if x == battle_field['width'] else f' {x} |'
                elif x == 0:
                    bf_map += '|    |'
                else:
                    bf_map += f'  {letters[x-1]} |\n' if x == battle_field['width'] else f'  {letters[x-1]} |'
            elif x == 0 and y > 2 and y < (battle_field['heigth'] + 3):
                if (y-3) > 9:
                    bf_map += f'| {y-3} |'
                else:
                    bf_map += f'|  {y-3} |'
            else:
                char = '--'
                if y in coords:
                    if x in coords[y]:
                        char = coords[y][x]
                        char = char[0:2]

                bf_map += f' {char} |'

                if x == battle_field['width']:
                    bf_map += '\n'
    return bf_map + '```'

if __name__ == "__main__":
    db = Database()
    print(start_campaign('3383241', 'TEst', db))

