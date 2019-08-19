import os
import json
import logging

import telegram
from roll import handler as roll_handler
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

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    logger.error('The TELEGRAM_TOKEN must be set')
    raise NotImplementedError

updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher

def start(bot, update, **args):
    bot.send_message(chat_id=update.message.chat_id, text="Welcome to Dungeons and Dragons on Telegram.")

start_cmd = CommandHandler('start', start)
roll_cmd = CommandHandler('roll', roll_handler)

dispatcher.add_handler(start_cmd)
dispatcher.add_handler(roll_cmd)



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


def webhook(event, context):
    """
    Runs the Telegram webhook.
    """

    bot = configure_telegram()
    logger.info('Event: {}'.format(event))

    if event.get('httpMethod') == 'POST' and event.get('body'):
        update = telegram.Update.de_json(json.loads(event.get('body')), bot)
        chat_id = update.message.chat.id
        text = update.message.text

        if text.startswith('/start'):
            start(bot, update)
        elif text.startswith('/roll'):
            roll_handler(bot, update)

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

if __name__ == "__main__":
    updater.start_polling()
