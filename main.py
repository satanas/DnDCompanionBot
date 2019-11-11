import os
import json
import logging
import telegram

from roll import handler as roll_handler
from charsheet import handler as charsheet_handler
from help import handler as help_handler
from character import handler as character_handler
from turns import handler as turn_handler
from dm import handler as dm_handler
from campaign import handler as campaign_handler

from telegram.ext import Updater
from telegram.ext import CommandHandler

# cmd, handler, args, description
GENERAL_COMMANDS = {
    "/start": (start, None, "starts the DnDCompanionBot"),
    "/roll": (roll_handler, "<expression>", "rolls the dice using the [dice notation](https://en.wikipedia.org/wiki/Dice_notation)"),
    "/charsheet": (charsheet_handler, "<username>", "returns the character sheet associated with username"),
    #"/combatsheet": (None, None, "returns the link of the combat cheatsheet"),
    "/help": (help_handler, None, "shows this help message"),
}

CAMPAIGN_COMMANDS = {
    "/start_campaign": (campaign_handler, None, "starts a new campaign in the invoked group"),
    "/close_campaign": (campaign_handler, None, "closes an active campaign"),
    "/set_turns": (turn_handler, "<username1>,...<usernameN>", "creates a list with the order of players for a given round"),
    "/turn": (turn_handler, None, "shows the current player in the turns list"),
    "/next_turn": (turn_handler,  None, "moves to the next player in the turns list"),
    "/set_dm": (dm_handler, "<username>", "sets the username of the DM for the current campaign"),
    "/dm": (dm_handler, None, "shows the DM for the current campaign"),
}

CHARACTER_COMMANDS = {
    "/import_char": (character_handler, "<url>", "imports the JSON data of a character from a URL"),
    "/link_char": (character_handler, "<char_id> <username> OR <char_id>", "links character to target username or self username"),
    "/weapons": (character_handler, "<character>", "shows the list of weapons of a character"),
    "/attack_roll": (character_handler, "<character> <weapon> melee|range <distance> adv|disadv", "performs an attack roll on a character"),
    "/initiative_roll": (character_handler, "<character>", "performs an initiative roll for a character"),
    "/talk": (character_handler, "<character> <message>", "prints a message using in-game conversation format"),
    "/say": (character_handler, "<character> <message>", "prints a normal message using in-game conversation format"),
    "/whisper": (character_handler, "<character> <message>", "prints a whisper message using in-game conversation format"),
    "/yell": (character_handler, "<character> <message>", "prints a yell message using in-game conversation format"),
}

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 500,
    'body': json.dumps('Oops, something went wrong!')
}

def configure_telegram():
    """
    Configures the bot with a Telegram Token.
    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)

# TODO: Add command to generate commands list for BotFather
def webhook(event, context):
    """
    Runs the Telegram webhook.
    """

    bot = configure_telegram()
    logger.info('Event: {}'.format(event))

    if event.get('httpMethod') == 'POST' and event.get('body'):
        update = telegram.Update.de_json(json.loads(event.get('body')), bot)
        if update.message == None or update.message.text == None or update.message.text == '':
            return OK_RESPONSE

        command = update.message.text.split(' ')[0]
        instruction = update.message.text

        handler = None
        if command in GENERAL_COMMANDS:
            handler = GENERAL_COMMANDS[command][0]
        elif command in CAMPAIGN_COMMANDS:
            handler = CAMPAIGN_COMMANDS[command][0]
        elif command in CHARACTER_COMMANDS:
            handler = CHARACTER_COMMANDS[command][0]

        if handler != None:
            handler(instruction)
            return OK_RESPONSE
        else:
            return ERROR_RESPONSE

        #text = update.message.text

        #if text == '/start':
        #    start(bot, update)
        #elif text.startswith('/roll'):
        #    roll_handler(bot, update)
        #elif text.startswith('/charsheet'):
        #    charsheet_handler(bot, update)
        #elif text.startswith('/help'):
        #    help_handler(bot, update)
        #elif text.startswith('/import_char') or text.startswith('/attack_roll') or \
        #        text.startswith('/initiative_roll') or text.startswith('/weapons') or \
        #        text.startswith('/talk') or text.startswith('/say') or \
        #        text.startswith('/whisper') or text.startswith('/yell'):
        #    character_handler(bot, update)
        #elif text.find('turn') > 0:
        #    turn_handler(bot, update)
        #elif text.startswith('/set_dm') or text.startswith('/dm'):
        #    dm_handler(bot, update)
        #elif text.find('campaign') > 0:
        #    campaign_handler(bot, update)

        #return OK_RESPONSE

    return ERROR_RESPONSE


def set_webhook(event, context):
    """
    Sets the Telegram bot webhook.
    """

    logger.info('Event: {}'.format(event))
    bot = configure_telegram()
    url = 'https://{}/{}/'.format(
        event.get('headers').get('Host'),
        event.get('requestContext').get('stage'),
    )
    webhook = bot.set_webhook(url)

    if webhook:
        return OK_RESPONSE

    return ERROR_RESPONSE
