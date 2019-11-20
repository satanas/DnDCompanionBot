import sys
import requests

from urllib.parse import urlparse

import re
import utils
from handlers.roll import roll
from database import Database
from utils import normalized_username
from currency import optimal_exchange
from models.character import Character, ABILITIES, SKILLS
from exceptions import CharacterNotFound, CampaignNotFound, InvalidCommand, NotADM

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

CURRENCY_PATTERN = re.compile('([-]?\d+)(cp|sp|ep|gp|pp)*(\d+)*')

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
    elif command == '/spells':
        response = get_spells(txt_args, db, chat_id, username)
    elif command == '/status':
        response = get_status(txt_args, db, chat_id, username)
    elif command == '/set_currency':
        response = set_currency(txt_args, db, chat_id, username)
    elif command == '/say' or command == '/yell' or command == '/whisper':
        response = talk(command, txt_args)
    elif command == '/move':
        response = move(txt_args, db, chat_id, username)
    elif command == '/damage' or command == '/heal':
        response = set_hp(command, txt_args, db, chat_id, username)
    elif command == '/ability_check':
        response = ability_check(txt_args, db, chat_id, username)

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
    if (len(params) > 1):
        player = utils.normalized_username(params[1])
    else:
        player = username

    campaign_id, campaign = db.get_campaign(chat_id)
    if campaign_id is None:
        return f'You must be in an active campaign to link characters!'

    db.set_character_link(campaign_id, player, character_id)

    return f'Character with id {character_id} linked to {player} successfully!'

def attack_roll(txt_args, db, chat_id, username):
    args = [a.strip() for a in txt_args.split(' ')]
    if len(args) < 2:
        return ('Invalid syntax. Usage:'
                '\r\n/attack\\_roll <weapon|spell> <attack>(melee|range) \\[distance] \\[adv|disadv]')

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
    try:
        distance = int(distance)
    except ValueError:
        raise InvalidCommand

    character = get_linked_character(db, chat_id, username)
    weapon = character.get_weapon(weapon_name)
    if weapon is None:
        #weapon = character.get_spell(weapon_name)
        #if weapon is None:
        return f"{character.name} doesn't have a weapon/spell called {weapon_name}"

    # TODO: Attack with spell
    # Attack with weapon
    if attack_type in ["ranged", "r"] and distance > weapon.long_range:
        return f"You can't attack a target beyond the range of your weapon ({weapon_name}, {weapon.long_range}ft)"

    prof = " + PRO(0)"
    if character.has_proficiency(weapon_name):
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
    return (f'@{username} initiative roll for {character.name}:'
            f'\r\nFormula: 1d20 + DEX({character.dex_mod})'
            f'\r\n*{dice_notation}*: {dice_rolls}')

def short_rest_roll(txt_args, db, chat_id, username):
    character = get_linked_character(db, chat_id, username)

    if character.hit_dice_used == character.level:
        return f'{character.name} spent all the hit dice already. You need to take a long rest to replenish them.'

    dice_notation = f'1d{character.hit_dice}+{character.con_mod}'
    results = roll(dice_notation)
    dice_rolls = results[list(results.keys())[0]][0]
    return (f'@{username} short rest roll for {character.name}:'
            f'\r\nFormula: 1d{character.hit_dice} + CON({character.con_mod})'
            f'\r\n*{dice_notation}*: {dice_rolls}')

def get_weapons(other_username, db, chat_id, username):
    search_param = other_username if other_username != '' else username
    search_param = utils.normalized_username(search_param)
    character = get_linked_character(db, chat_id, search_param)

    if len(character.weapons) > 0:
        weapons = ', '.join([w.name for w in character.weapons])
        return f'Weapons in {character.name}\'s inventory: {weapons}'
    else:
        return f'{character.name} does not have any weapon'

def get_spells(other_username, db, chat_id, username):
    search_param = other_username if other_username != '' else username
    search_param = utils.normalized_username(search_param)
    character = get_linked_character(db, chat_id, search_param)

    if len(character.spells) > 0:
        spells = ', '.join([s.name for s in character.spells])
        return f'Attack spells for {character.name}: {spells}'
    else:
        return f'{character.name} does not have any attack spells'

def get_status(other_username, db, chat_id, username):
    search_param = other_username if other_username != '' else username
    search_param = utils.normalized_username(search_param)
    character = get_linked_character(db, chat_id, search_param)

    return (f'```\r\n{character.name} | {character.race} {character._class} Level {character.level}\r\n'
            f'HP: {character.current_hit_points}/{character.max_hit_points} | XP: {character.current_experience}/{character.experience_needed} \r\n'
            f'{character.currency["cp"]} CP | '
            f'{character.currency["sp"]} SP | '
            f'{character.currency["ep"]} EP | '
            f'{character.currency["gp"]} GP | '
            f'{character.currency["pp"]} PP ```')

def set_currency(txt_args, db, chat_id, username):
    campaign_id, campaign = db.get_campaign(chat_id)
    dm_username = campaign.get('dm_username', None)
    if dm_username != username:
        return f'Only the Dungeon Master can execute this command'

    args = txt_args.split(' ')

    user_param = args[0]
    user_param = utils.normalized_username(user_param)
    character = get_linked_character(db, chat_id, user_param)

    equation = CURRENCY_PATTERN.findall(txt_args)

    if len(equation) <= 0:
        raise Exception('your request was not a valid equation! Please use the currency notation (for example: 10gp, -20cp)')

    currencies = character.currency

    for i in range(0, len(equation)):
        parts = equation[i]
        currencies[parts[1]] += int(parts[0])
        if currencies[parts[1]] < 0:
            return f"You can't afford that ammount"

    db.set_char_currency(character.id, currencies)

    return (f'{character.name} currencies pouch has been updated: ```\r\n'
            f'{currencies["cp"]} CP | {currencies["sp"]} SP | '
            f'{currencies["ep"]} EP | {currencies["gp"]} GP | {currencies["pp"]} PP ```')

def set_hp(command, txt_args, db, chat_id, username):
    args = txt_args.split(' ')
    if args[0].isdigit():
        return f'Invalid commands parameters, the correct structure is: \r\n {command}  <integer>  <username|character>'

    user_param = args[0]
    points = int(args[1])

    campaign_id, campaign = db.get_campaign(chat_id)
    dm_username = campaign.get('dm_username', None)
    if dm_username != username:
        raise NotADM

    user_param = utils.normalized_username(user_param)
    character = get_linked_character(db, chat_id, user_param)

    if command == '/damage':
        result = character.removed_hit_points + int(points)
        if result > character.max_hit_points:
            result = character.max_hit_points
    else:
        result = character.removed_hit_points - int(points)
        if result < 0:
            result = 0

    character.current_hit_points = character.max_hit_points - result

    db.set_char_hp(character.id, hit_points=result)
    return f'{character.name} received {points} pts of { command.replace("/", "").strip()}. HP: {character.current_hit_points}/{character.max_hit_points}'

def talk(command, txt_args):
    args = txt_args.split(' ')
    if len(args) < 2:
        return ('Invalid syntax. Usage:'
                '\r\n' + command +' <character> <message>')

    character_name = args[0]
    message = ' '.join(args[1:])
    if command == '/yell':
        message = message.upper()
    elif command == '/whisper':
        message = f"__{message}__"

    return f"```\r\n{character_name} says:\r\n–{message}\r\n```"

def move(txt_args, db, chat_id, username):
    args = txt_args.split(' ')
    campaign_id, campaign = db.get_campaign(chat_id)
    dm_username = campaign.get('dm_username', None)
    
    turns = campaign.get('turns', None)
    turn_index = int(campaign.get('turn_index', '0'))
    current_turn = turns[turn_index % len(turns)]

    if len(args) > 1:
        user_param = utils.normalized_username(args[0])
        position = args[1]
        if dm_username != username:
            return f"Only the Dungeon Master can move other characters"
    else:
        user_param = username
        position = args[0]
        if utils.normalized_username(current_turn) != username:
            return f"Is the turn of {current_turn}. You can move only on your turn"

    result = db.set_char_position(campaign_id, user_param, position)
    
    if result is None:
        return f"{user_param} does not exist on this battle field"

    return f"{user_param} moved to {position} successfully!"

def ability_check(txt_args, db, chat_id, username):
    args = txt_args.split(' ')
    if len(args) == 0:
        return ('Invalid syntax. Usage:'
                '\r\n/ability_check <ability> (skill)')

    skill = None
    ability = args[0].lower()
    base_notation = '1d20'
    if len(args) == 2:
        skill = args[1].lower()

    if ability not in ABILITIES:
        return ('Invalid ability. Supported options: ' + ', '.join(ABILITIES))
    if skill is not None and skill not in SKILLS[ability]:
        return ('Invalid skill. Supported options: ' + ', '.join(SKILLS[ability]))

    character = get_linked_character(db, chat_id, username)

    txt_skill_mod = ''
    txt_ability_mod = f' + {ability.upper()}({character.mods[ability]})'
    ability_desc = ability.upper()
    mods = character.mods[ability]
    if skill is not None:
        ability_desc = f'{ability_desc} ({skill.capitalize()})'
        mods += character.mods[skill]
        txt_skill_mod = f' + {skill.capitalize()}({character.mods[skill]})'

    txt_formula = f"{base_notation}{txt_ability_mod}{txt_skill_mod}"
    if mods > 0:
        dice_notation = f"{base_notation}+{mods}"
    else:
        dice_notation = base_notation

    results = roll(dice_notation)
    dice_rolls = results[list(results.keys())[0]]

    return (f"@{username} ability check for {character.name} with {ability_desc}:"
            f"\r\nFormula: {txt_formula}"
            f"\r\n*{dice_notation}*: {dice_rolls}")

def get_linked_character(db, chat_id, username):
    campaign_id, campaign = db.get_campaign(chat_id)

    if campaign_id is None:
        raise CampaignNotFound

    character_id = db.get_character_id(campaign_id, username)
    character = db.get_character(character_id, find_by_id=True)

    if character == None:
        raise CharacterNotFound

    return character

#if __name__ == "__main__":
#    db = Database()
#    url = "https://dl.dropbox.com/s/awlpwcwi0eetdoq/ghamorz.json?dl=0"
#    #import_character(url)
#    #load_character('123456')
#    #print(attack_roll('satanas82', '/attack_roll Ghamorz Javelin ranged 10', db))
#    #print(get_weapons('/weapons Ghamorz', db))
#    print(initiative_roll('/initiative_roll Ghamorz', db))

