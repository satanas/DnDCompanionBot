import os
import json
import logging
import telegram

from commands import GENERAL_COMMANDS, CAMPAIGN_COMMANDS, CHARACTER_COMMANDS

from telegram.ext import Updater
from telegram.ext import CommandHandler

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
        if command == '/start':
            start_handler()
        if command == '/help':
            help_handler()
        elif command in GENERAL_COMMANDS:
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

def start_handler(bot, update):
    chat_id = update.message.chat.id
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")

def help_handler(bot, update):
    help_message = "{}\n\n*General commands:*\n{}\n\n*Campaign commands:*\n{}\n\n*Character commands:*\n{}".format(
                HELP_SUMMARY,
                '\n'.join([concat_command(c, True, '-', escape) for c in GENERAL_COMMANDS]),
                '\n'.join([concat_command(c, True, '-', escape) for c in CAMPAIGN_COMMANDS]),
                '\n'.join([concat_command(c, True, '-', escape) for c in CHARACTER_COMMANDS])
            )
    bot.send_message(chat_id=update.message.chat_id, text=help_message, parse_mode="Markdown", disable_web_page_preview=True)

def concat_command(command, add_params=False, separator='-', escape=False):
    cmd = command[0]
    params = f"{command[1]} " if add_params is True and command[1] is not None else ''
    desc = command[2]
    formatted_cmd = f"{cmd} {params}{separator} {desc}"
    return formatted_cmd if escape is False else escape_md(formatted_cmd)

def escape_md(text):
    return text.replace('_', '\_')
