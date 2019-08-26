import sys
import requests

from roll import roll
from database import Database
from models.character import Character

CLOSE_COMBAT_DISTANCE = 5 # feet

def import_handler(bot, update):
    db = Database()
    chat_id = update.message.chat.id
    url = update.message.text.replace('/import_char ', '').strip()
    return import_character(url, chat_id, db)

def import_character(chat_id, user_id, url, db):
    # 1. Get campaign for chat_id
    # 2. Get usernames for campaign
    # 3. Get character id from username
    # Goal: Get character_id from chat_id and username
    character_data = requests.get(url).json()

    return db.save_character_info(character_id, character_data)

def get_weapons(chat_id, username, db):
    character = db.get_character(chat_id, username)


def ability_check(chat_id, username, ability):
    pass

def attack_roll(chat_id, username, weapon_name, attack_type, distance, db):
    mods = 0
    txt_mod = ''
    disadv = ''
    prof = ''
    base_notation = '1d20'
    distance = int(distance)

    campaign_id, campaign = db.get_campaign(chat_id)

    # Finding character in campaign
    characters = campaign['characters']
    ids = [key for key in characters if characters[key]['username'] == username]
    if len(ids) > 0:
        character_id = ids[0]
    else:
        return f'Character not found for @{username}'

    character = db.get_character(character_id)
    weapon = character.get_weapon(weapon_name)

    if attack_type in ["ranged", "r"] and distance > weapon.long_range:
        return f"You can attack a target beyond the range of {weapon_name} ({weapon.long_range}ft)"

    if character.has_weapon_proficiency(weapon_name):
        mods += character.proficiency
        prof = "+pro"

    if attack_type in ["melee", "m"]:
        if weapon.has_finesse() and character.dex_mod > character.str_mod:
            txt_mod += "+dex(finesse)"
            mods += character.dex_mod
        else:
            txt_mod += "+str"
            mods += character.str_mod
    elif attack_type in ["ranged", "r"]:
        if weapon.has_thrown() and character.str_mod > character.dex_mod:
            txt_mod += "+str(thrown)"
            mods += character.str_mod
        else:
            txt_mod += "+dex"
            mods += character.dex_mod

    if attack_type in ["ranged", "r"] and distance >= weapon.range and distance <= weapon.long_range:
        disadv = " (with disadv)"

    txt_formula = f"{base_notation}{prof}{txt_mod}{disadv}"
    if mods > 0:
        dice_notation = f"{base_notation}+{mods}"
    else:
        dice_notation = base_notation

    if disadv != "":
        dice_notation = f"{dice_notation},{dice_notation}"

    results = roll(dice_notation)

    return (f"Attack roll for @{username} - {weapon_name} ({attack_type}):"
                f"\r\n`Formula: {txt_formula}`"
                f"\r\n*{dice_notation}*: {results}")

if __name__ == "__main__":
    db = Database()
    url = "https://dl.dropbox.com/s/awlpwcwi0eetdoq/ghamorz.json?dl=0"
    #import_character(url)
    #load_character('123456')
    print(attack_roll('3383241', 'satanas82', 'Javelin', 'ranged', 55, db))
