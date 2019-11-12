import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from commands import ALL_COMMANDS, command_handler, default_handler, parse_command
from exceptions import CommandNotFound, CampaignNotFound, CharacterNotFound

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def handler(bot, update):
    command = parse_command(update.message.text)
    txt_args = ' '.join(update.message.text.split(' ')[1:])
    command_handler(command)(bot, update, command, txt_args)

    try:
        command_handler(command)(bot, update, command, txt_args)
    except CommandNotFound:
        default_handler(bot, update, f'Command {command} not found')
    except CharacterNotFound:
        default_handler(bot, update, f'Character not found. Cannot execute {update.message.text}')
    except CampaignNotFound:
        default_handler(bot, update, f'Campaign not found. Theres must be an active campaign')

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

    #dp.add_handler(CommandHandler('start', start_handler))
    #dp.add_handler(CommandHandler('help', help_handler))

    for command in ALL_COMMANDS:
        command_key = command
        dp.add_handler(CommandHandler(command_key.replace('/', '').strip(), handler))

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
