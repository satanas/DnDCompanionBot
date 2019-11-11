import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from roll import handler as roll_handler
from charsheet import handler as charsheet_handler
#from help import handler as help_handler
from character import handler as character_handler
from turns import handler as turn_handler
from dm import handler as dm_handler
from campaign import handler as campaign_handler

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    chat_id = context.message.chat.id
    update.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")

def roll(bot, update):
    roll_handler(bot, update)

def charsheet(bot, update):
    charsheet_handler(bot, update)

def help(bot, update):
    help_handler(bot, update)

def turn(bot, update):
    turn_handler(bot, update)

def campaign(bot, update):
    campaign_handler(bot, update)  

def character(bot, update):
    character_handler(bot, update)  

def unknown(update, context):
    chat_id = context.message.chat.id
    update.send_message(chat_id=chat_id, text="Sorry, I didn't understand that command.")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    #"""Start the bot."""
    updater = Updater(token=TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(CommandHandler('roll', roll))
    dp.add_handler(CommandHandler('charsheet', charsheet))
    dp.add_handler(CommandHandler('help', help))

    dp.add_handler(CommandHandler('set_turns', turn))
    dp.add_handler(CommandHandler('turn', turn))
    dp.add_handler(CommandHandler('next_turn', turn))
    dp.add_handler(CommandHandler('prev_turn', turn))

    dp.add_handler(CommandHandler('start_campaign', campaign))
    dp.add_handler(CommandHandler('close_campaign', campaign))

    dp.add_handler(CommandHandler('talk', character))
    dp.add_handler(CommandHandler('say', character))
    dp.add_handler(CommandHandler('whisper', character))
    dp.add_handler(CommandHandler('yell', character))

    dp.add_handler(CommandHandler('import_char', character))
    dp.add_handler(CommandHandler('link_char', character))

    dp.add_handler(CommandHandler('status', character))
    dp.add_handler(CommandHandler('weapons', character))

    dp.add_handler(MessageHandler(Filters.command, unknown))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
