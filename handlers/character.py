import sys
import requests
from urllib.parse import urlparse

from handlers.roll import roll
from database import Database
from models.character import Character
from exceptions import CharacterNotFound

CLOSE_COMBAT_DISTANCE = 5 # feet

SIZE_MODIFIER = {
    'Colossal': -8,
    'Small': 1,
    'Gargantuan': -4,
    'Tiny': 2,
    'Huge': -2,
    'Diminutive': 4,
    'Large': -1,
    'Fine': 8,
    'Medium': 0
}

def handler(bot, update, command, txt_args):
    db = Database()
    chat_id = update.message.chat.id
    username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name

    if command == '/import_char':
        response = import_character(txt_args, db, requests.get)
    if command == '/link_char':
        response = link_character(txt_args, db, chat_id, username)
    elif command == '/attack_roll':
        response = attack_roll(txt_args, db, chat_id, username)
    elif command == '/initiative_roll':
        response = initiative_roll(txt_args, db, chat_id, username)
    elif command == '/short_rest_roll':
        response = short_rest_roll(txt_args, db, chat_id, username)
    elif command == '/weapons':
        response = get_weapons(txt_args, db, chat_id, username)
    elif command == '/status':
        response = get_status(txt_args, db, chat_id, username)
    elif command == '/say' or command == '/yell' or command == '/whisper':
        response = talk(command, txt_args, db, chat_id, username)
        #bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

    bot.send_message(chat_id=update.message.chat_id, text=response, parse_mode="Markdown")

def import_character(url, db, get):
    parsed_url = urlparse(url)
    if parsed_url[0] == '':
        return f'{url} is not a valid URL'

    response = get(url)
    if response.status_code != 200:
        return f'Error fetching {url} (status_code: {response.status_code})'

    character_data = response.json()
    character_id = character_data['character']['id']
    character_name = character_data['character']['name']

    if db.save_character_info(character_id, character_data) != None:
        return f'Character "{character_name}" imported successfully!'
    else:
        return f'Something went wrong importing {character_name}'

def link_character(args, db, chat_id, username):
    params = [x.strip() for x in args.split(' ')]

    character_id = params[0]
    if len(params) > 1:
        player = params[1].replace('@', '').strip()
    else:
        player = username

    campaign_id, campaign = db.get_campaign(chat_id)
    db.set_character_link(campaign_id, player, character_id)

    return f'Character with id {character_id} linked to {player} successfully!'

def attack_roll(txt_args, db, chat_id, username):
    args = [a.strip() for a in txt_args.split(' ')]
    if len(args) < 2:
        return ('Invalid syntax. Usage:'
                '\r\n/attack\\_roll <weapon> <attack>(melee|range) \\[distance] \\[adv|disadv]')

    weapon_name = args[0]
    attack_type = args[1]
    distance = 5 if len(args) <= 2 else args[2]
    adv = False
    disadv = False
    if len(args) > 3 and args[3] == 'adv':
        adv = True
    elif len(args) > 3 and args[3] == 'disadv':
        disadv = True

    mods = 0
    txt_mod = ''
    adv_mod = ''
    prof = ''
    base_notation = '1d20'
    distance = int(distance)

    character = get_linked_character(db, chat_id, username)
    weapon = character.get_weapon(weapon_name)

    if attack_type in ["ranged", "r"] and distance > weapon.long_range:
        return f"You can attack a target beyond the range of your weapon ({weapon_name}, {weapon.long_range}ft)"

    prof = " + PRO(0)"
    if character.has_weapon_proficiency(weapon_name):
        mods += character.proficiency
        prof = f" + PRO({character.proficiency})"

    if attack_type in ["melee", "m"]:
        if weapon.has_finesse() and character.dex_mod > character.str_mod:
            txt_mod += f" + DEX({character.dex_mod})<finesse>"
            mods += character.dex_mod
        else:
            txt_mod += f" + STR({character.str_mod})"
            mods += character.str_mod
    elif attack_type in ["ranged", "r"]:
        if weapon.has_thrown() and character.str_mod > character.dex_mod:
            txt_mod += f" + STR({character.str_mod})<thrown>"
            mods += character.str_mod
        else:
            txt_mod += f" + DEX({character.dex_mod})"
            mods += character.dex_mod

    size_mod = SIZE_MODIFIER[character.size]
    txt_mod += f" + SIZE({size_mod})"
    mods += size_mod

    if attack_type in ["ranged", "r"] and \
            (distance <= CLOSE_COMBAT_DISTANCE or (distance >= weapon.range and distance <= weapon.long_range)):
        if not adv:
            adv_mod = " + DISADV"
    elif disadv == True:
        adv_mod = " + DISADV"
    elif adv == True:
        adv_mod = " + ADV"

    txt_formula = f"{base_notation}{prof}{txt_mod}{adv_mod}"
    if mods > 0:
        dice_notation = f"{base_notation}+{mods}"
    else:
        dice_notation = base_notation

    if adv_mod != "":
        dice_notation = f"{dice_notation},{dice_notation}"

    results = roll(dice_notation)
    dice_rolls = results[list(results.keys())[0]]

    return (f"@{username} attack roll for {character.name} with {weapon_name} ({attack_type}):"
            f"\r\nFormula: {txt_formula}"
            f"\r\n*{dice_notation}*: {dice_rolls}")

def initiative_roll(txt_args, db, chat_id, username):
    character = get_linked_character(db, chat_id, username)
    dice_notation = f'1d20+{character.dex_mod}'
    results = roll(dice_notation)
    dice_rolls = results[list(results.keys())[0]][0]
    return f'@{username} initiave roll for {character.name} ({dice_notation}): {dice_rolls}'

def short_rest_roll(txt_args, db, chat_id, username):
    character = get_linked_character(db, chat_id, username)

    if character.hit_dice_used == character.level:
        return f'{character.name} spent all the hit dice already. You need to take a long rest to replenish them.'

    dice_notation = f'1d{character.hit_dice}+{character.con_mod}'
    results = roll(dice_notation)
    dice_rolls = results[list(results.keys())[0]][0]
    return f'@{username} short rest roll for {character.name} ({dice_notation}): {dice_rolls}'

def get_weapons(other_username, db, chat_id, username):
    search_param = other_username if other_username != '' else username
    character = get_linked_character(db, chat_id, search_param)

    if len(character.weapons) > 0:
        weapons = [w.name for w in character.weapons]
        return f'Weapons in {character_name}\'s inventory: {weapons}'
    else:
        return f'{character_name} does not have any weapon'

def get_status(other_username, db, chat_id, username):
    search_param = other_username if other_username != '' else username
    character = get_linked_character(db, chat_id, search_param)

    return (f'{character.name} | {character.race} {character._class} Level {character.level}\r\n'
            f'HP: {character.current_hit_points}/{character.max_hit_points} | XP: {character.current_experience}')

#response = talk(command, txt_args, db, chat_id, username)
def talk(command, txt_args, db, chat_id, username):
    args = txt_args.split(' ')
    if len(args) < 2:
        return ('Invalid syntax. Usage:'
                '\r\n' + command +' <character> <message>')

    character_name = args[0]
    message = args[1]
    if command == 'yell':
        message = message.upper()
    elif command == 'whisper':
        message = f"__{message}__"

    return f"```\r\n{character_name} says:\r\n–{message}\r\n```"

def ability_check(chat_id, username, ability):
    pass

def get_linked_character(db, chat_id, username):
    campaign_id, campaign = db.get_campaign(chat_id)
    character_id = db.get_character_id(campaign_id, username)
    char = db.get_character(character_id, find_by_id=True)

    if character == None:
        raise CharacterNotFound

    return char

#if __name__ == "__main__":
#    db = Database()
#    url = "https://dl.dropbox.com/s/awlpwcwi0eetdoq/ghamorz.json?dl=0"
#    #import_character(url)
#    #load_character('123456')
#    #print(attack_roll('satanas82', '/attack_roll Ghamorz Javelin ranged 10', db))
#    #print(get_weapons('/weapons Ghamorz', db))
#    print(initiative_roll('/initiative_roll Ghamorz', db))
