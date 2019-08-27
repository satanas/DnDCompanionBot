def handler(bot, update):
    help_text = (
        "Hi! I am the Dungeons & Dragons Companion Bot and I can help you manage a few things in your D&D "
        "campaigns. This is the list of commands you can use:\n\n"
        "*General commands:*\n"
        "/start - starts the DnDCompanionBot\n"
        "/roll <expression> - rolls the dice using the [dice notation](https://en.wikipedia.org/wiki/Dice_notation)\n"
        "/charsheeet <username> - returns the character sheet associated with username\n"
        "/help - shows this help message\n\n"
        "*Campaign commands:*\n"
        "/start\\_campaign - starts a new campaign in the invoked group\n"
        "/close\\_campaign - closes an active campaign\n"
        "/import\\_char <json_url> - imports the JSON data of a character\n"
        "/set\\_turns <p1>,<p2>... - creates a list with the order of players in a combat\n"
        "/turn - shows the current player in the combat order list\n"
        "/next\\_turn - moves the turn to the next player in the combat order list\n"
        "/set\\_dm <username> - sets the DM of the current campaign\n"
        "/dm - shows the DM for the current campaign\n\n"
        "*Character commands:*\n"
        "/weapons <character> - shows the list of weapons of a character\n"
        "/attack\\_roll <character> <weapon> <attack>(melee|range) \\[distance] \\[adv|disadv] - performs an attack roll\n"
        "/initiative\\_roll <character> - performs an initiative roll for the character\n"
        )
    bot.send_message(chat_id=update.message.chat_id, text=''.join(help_text), parse_mode="Markdown", disable_web_page_preview=True)
