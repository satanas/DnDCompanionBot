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
    'statusCode': 400,
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
        text = update.message.text

        if text == '/start':
            start(bot, update)
        elif text.startswith('/roll'):
            roll_handler(bot, update)
        elif text.startswith('/charsheet'):
            charsheet_handler(bot, update)
        elif text.startswith('/help'):
            help_handler(bot, update)
        elif text.startswith('/importchar'):
            character_handler(bot, update)
        elif text.startswith('/attack_roll') > 0:
            character_handler(bot, update)
        elif text.find('turn') > 0:
            turn_handler(bot, update)
        elif text.find('dm') > 0:
            dm_handler(bot, update)
        elif text.find('campaign') > 0:
            campaign_handler(bot, update)

        return OK_RESPONSE

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
