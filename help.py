def handler(bot, update):
    help_text = (
        "Hi! I am the Dungeons and Dragons Companion Bot and I can help you manage a few things in your D&D ",
        "campaigns. This is the list of commands you can use:\n\n",
        "*General commands:*\n",
        "  /start - Starts the DnDCompanionBot\n",
        "  /roll _[expression]_ - Rolls the dice using the [dice notation](https://en.wikipedia.org/wiki/Dice_notation)\n",
        "  /help - Shows this help message")
    bot.send_message(chat_id=update.message.chat_id, text=''.join(help_text), parse_mode="Markdown")
