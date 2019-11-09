import sys
import requests
from urllib.parse import urlparse

from roll import roll
from database import Database
from models.character import Character

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

def handler(bot, update):
    db = Database()
    chat_id = update.message.chat.id
    text = update.message.text
    username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name

    if text.startswith('/import_char'):
        response = import_character(text, db, requests.get)
    if text.startswith('/link_char'):
        response = link_character(text, db, chat_id, username)
    elif text.startswith('/attack_roll'):
        response = attack_roll(username, text, db)
    elif text.startswith('/initiative_roll'):
        response = initiative_roll(username, text, db)
    elif text.startswith('/weapons'):
        response = get_weapons(text,db)
    elif text.startswith('/talk'):
        response = talk(text)
        bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    elif text.startswith('/say'):
        response = chat(text, 'say')
        bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)        
    elif text.startswith('/yell'):
        response = chat(text, 'yell')
        bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    elif text.startswith('/whisper'):
        response = chat(text, 'whisper')
        bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    else:
        response = "Invalid command"

    bot.send_message(chat_id=update.message.chat_id, text=response, parse_mode="Markdown")

def talk(text):
    command = text.replace('/talk', '').strip()
    sep = command.find(" ")
    character_name = command[:sep]
    message = command[sep + 1:]
    response = f"```\r\n{character_name} says:\r\n–{message}\r\n```"  

    return response

def chat(text, tone):
    command = text.replace('/'+tone, '').strip()
    sep = command.find(" ")
    character_name = command[:sep]
    message = command[sep + 1:]    
    if tone == 'yell':
        message = message.upper()
    elif tone == 'whisper':
        message = f"__{message}__"
    response = f"```\r\n{character_name} says:```\r\n–{message}\r\n"  

    return response    

def import_character(text, db, get):
    url = text.replace('/import_char', '').strip()
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

def link_character(text, db, chat_id, username):
    command = text.replace('/link_char', '').strip()
    params = [u.strip() for u in command.split(' ')]

    if (len(params) > 1):
        character_id = params[0]
        player = params[1].replace('@', '').strip()
    else:
        character_id = params[0]
        player = username

    campaign_id, campaign = db.get_campaign(chat_id)
    db.set_character_link(campaign_id, player, character_id)

    return f'Character with id {character_id} linked to {player} successfully!'

def get_weapons(text, db):
    character_name = text.replace('/weapons', '').strip()

    character = db.get_character(character_name)
    if character == None:
        return f'Character "{character_name}" not found'

    if len(character.weapons) > 0:
        weapons = [w.name for w in character.weapons]
        return f'Weapons in {character_name}\'s inventory: {weapons}'
    else:
        return f'{character_name} does not have any weapon'

def initiative_roll(username, text, db):
    character_name = text.replace('/initiative_roll', '').strip()

    character = db.get_character(character_name)
    if character == None:
        return f'Character "{character_name}" not found'

    dice_notation = f'1d20+{character.dex_mod}'
    results = roll(dice_notation)
    dice_rolls = results[list(results.keys())[0]][0]
    return f'@{username} initiave roll for {character_name} ({dice_notation}): {dice_rolls}'


def ability_check(chat_id, username, ability):
    pass

def attack_roll(username, text, db):
    args = [a.strip() for a in text.replace('/attack_roll ', '').split(' ')]
    if len(args) < 3:
        return ('Invalid syntax. Usage:'
                '\r\n/attack\\_roll <character> <weapon> <attack>(melee|range) \\[distance] \\[adv|disadv]')

    character_name = args[0]
    weapon_name = args[1]
    attack_type = args[2]
    distance = 5 if len(args) <= 3 else args[3]
    adv = False
    disadv = False
    if len(args) > 4 and args[4] == 'adv':
        adv = True
    elif len(args) > 4 and args[4] == 'disadv':
        disadv = True

    mods = 0
    txt_mod = ''
    adv_mod = ''
    prof = ''
    base_notation = '1d20'
    distance = int(distance)

    character = db.get_character(character_name)
    if character == None:
        return f'Character "{character_name}" not found'

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

    return (f"@{username} attack roll for {character_name} with {weapon_name} ({attack_type}):"
            f"\r\nFormula: {txt_formula}"
            f"\r\n*{dice_notation}*: {dice_rolls}")

#if __name__ == "__main__":
#    db = Database()
#    url = "https://dl.dropbox.com/s/awlpwcwi0eetdoq/ghamorz.json?dl=0"
#    #import_character(url)
#    #load_character('123456')
#    #print(attack_roll('satanas82', '/attack_roll Ghamorz Javelin ranged 10', db))
#    #print(get_weapons('/weapons Ghamorz', db))
#    print(initiative_roll('/initiative_roll Ghamorz', db))

