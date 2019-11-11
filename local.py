import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from main import start_handler, help_handler
from commands import GENERAL_COMMANDS, CAMPAIGN_COMMANDS, CHARACTER_COMMANDS

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def roll(bot, update):
    roll_handler(bot, update)

def charsheet(bot, update):
    charsheet_handler(bot, update)

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

    dp.add_handler(CommandHandler('start', start_handler))
    dp.add_handler(CommandHandler('help', help_handler))

    for command in GENERAL_COMMANDS:
        command_key = command
        dp.add_handler(CommandHandler(command_key.replace('/', '').strip(), GENERAL_COMMANDS[command][0]))
    
    for command in CAMPAIGN_COMMANDS:
        command_key = command
        dp.add_handler(CommandHandler(command_key.replace('/', '').strip(), CAMPAIGN_COMMANDS[command][0]))
    
    for command in CHARACTER_COMMANDS:
        command_key = command
        dp.add_handler(CommandHandler(command_key.replace('/', '').strip(), CHARACTER_COMMANDS[command][0]))

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
