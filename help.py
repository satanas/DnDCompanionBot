import sys

# To update commands in README.md:
# python3 help.py --tables
#
# To update commands in @botfather:
# python3 help.py --botfather


GENERAL_COMMANDS = [
    ("/start", None, "starts the DnDCompanionBot"),
    ("/roll", "<expression>", "rolls the dice using the [dice notation](https://en.wikipedia.org/wiki/Dice_notation)"),
    ("/charsheet", "<username>", "returns the character sheet associated with username"),
    ("/combatsheet", None, "returns the link of the combat cheatsheet"),
    ("/help", None, "shows this help message"),
]

CAMPAIGN_COMMANDS = [
    ("/start_campaign", None, "starts a new campaign in the invoked group"),
    ("/close_campaign", None, "closes an active campaign"),
    ("/set_turns", "<username1>,...<usernameN>", "creates a list with the order of players for a given round"),
    ("/turn", None, "shows the current player in the turns list"),
    ("/next_turn", None, "moves to the next player in the turns list"),
    ("/set_dm", "<username>", "sets the username of the DM for the current campaign"),
    ("/import_char", "<url>", "imports the JSON data of a character from a URL"),
    ("/dm", None, "shows the DM for the current campaign"),
]

CHARACTER_COMMANDS = [
    ("/weapons", "<character>", "shows the list of weapons of a character"),
    ("/attack_roll", "<character> <weapon> melee|range <distance> adv|disadv", "performs an attack roll on a character"),
    ("/initiative_roll", "<character>", "performs an initiative roll for a character"),
    ("/talk", "<character> <message>", "prints a message using in-game conversation format"),
]
HELP_SUMMARY = (
    "Hi! I am the Dungeons & Dragons Companion Bot and I can help you manage a few things in your D&D "
    "campaigns. This is the list of commands you can use:"
)
GENERAL_COMMANDS_TABLE_HEADER = (
    "General commands | Action\n"
    "--------|-------"
)
CAMPAIGN_COMMANDS_TABLE_HEADER = (
    "Campaign commands | Action\n"
    "--------|-------"
)
CHARACTER_COMMANDS_TABLE_HEADER = (
    "Character commands | Action\n"
    "--------|-------"
)

def handler(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=help_in_markdown(True, True), parse_mode="Markdown", disable_web_page_preview=True)

# Markdown with tables. Used to regenerate the list of commands in README.md
def help_in_markdown_tables():
    return "{}\n{}\n\n{}\n{}\n\n{}\n{}".format(
                GENERAL_COMMANDS_TABLE_HEADER,
                '\n'.join([concat_command(c, True, '|') for c in GENERAL_COMMANDS]),
                CAMPAIGN_COMMANDS_TABLE_HEADER,
                '\n'.join([concat_command(c, True, '|') for c in CAMPAIGN_COMMANDS]),
                CHARACTER_COMMANDS_TABLE_HEADER,
                '\n'.join([concat_command(c, True, '|') for c in CHARACTER_COMMANDS])
            )

# Markdown with no tables. Used for the response of /help
def help_in_markdown(include_summary=False, escape=False):
    summary = HELP_SUMMARY if include_summary else ''
    return "{}\n\n*General commands:*\n{}\n\n*Campaign commands:*\n{}\n\n*Character commands:*\n{}".format(
                summary,
                '\n'.join([concat_command(c, True, '-', escape) for c in GENERAL_COMMANDS]),
                '\n'.join([concat_command(c, True, '-', escape) for c in CAMPAIGN_COMMANDS]),
                '\n'.join([concat_command(c, True, '-', escape) for c in CHARACTER_COMMANDS])
            )

# Just a list of plain text, no markup, no arguments.
# Used to update the list of commands in @botfather
def help_for_botfather():
    def escape(cmd):
        return cmd[1:]

    command_list = GENERAL_COMMANDS + CAMPAIGN_COMMANDS + CHARACTER_COMMANDS
    return '\n'.join([escape(concat_command(c)) for c in command_list]).strip()

def concat_command(command, add_params=False, separator='-', escape=False):
    cmd = command[0]
    params = f"{command[1]} " if add_params is True and command[1] is not None else ''
    desc = command[2]
    formatted_cmd = f"{cmd} {params}{separator} {desc}"
    return formatted_cmd if escape is False else escape_md(formatted_cmd)

def escape_md(text):
    return text.replace('_', '\_')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fmt = sys.argv[1]
        if fmt == "--botfather" or fmt == "-b":
            print(help_for_botfather())
        elif fmt == "--markdown" or fmt == "-m":
            print(help_in_markdown())
        elif fmt == "--tables" or fmt == "-t":
            print(help_in_markdown_tables())
