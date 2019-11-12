import sys

from commands import GENERAL_COMMANDS, CAMPAIGN_COMMANDS, CHARACTER_COMMANDS, ALL_COMMANDS

# To update commands in README.md:
# python3 help.py --mdtables
#
# To update commands in @botfather:
# python3 help.py --botfather


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



# Markdown with tables. Used to regenerate the list of commands in README.md
def help_in_markdown_tables():
    return "{}\n{}\n\n{}\n{}\n\n{}\n{}".format(
                GENERAL_COMMANDS_TABLE_HEADER,
                '\n'.join([formatting_command(cmd, info, True, '|', True) for cmd, info in GENERAL_COMMANDS.items()]),
                CAMPAIGN_COMMANDS_TABLE_HEADER,
                '\n'.join([formatting_command(cmd, info, True, '|', True) for cmd, info in CAMPAIGN_COMMANDS.items()]),
                CHARACTER_COMMANDS_TABLE_HEADER,
                '\n'.join([formatting_command(cmd, info, True, '|', True) for cmd, info in CHARACTER_COMMANDS.items()])
            )

# Markdown with no tables. Used for the response of /help
def help_in_markdown(include_summary=False, escape=False):
    pass

# Just a list of plain text, no markup, no arguments.
# Used to update the list of commands in @botfather
def help_for_botfather():
    def escape(cmd):
        return cmd[1:]

    return '\n'.join([escape(formatting_command(cmd, info)) for cmd, info in ALL_COMMANDS.items()]).strip()

def help_handler(bot, update):
    help_message = "{}\n\n*General commands:*\n{}\n\n*Campaign commands:*\n{}\n\n*Character commands:*\n{}".format(
                HELP_SUMMARY,
                '\n'.join([formatting_command(cmd, info, True, '-', escape) for cmd, info in GENERAL_COMMANDS.items()]),
                '\n'.join([formatting_command(cmd, info, True, '-', escape) for cmd, info in CAMPAIGN_COMMANDS.items()]),
                '\n'.join([formatting_command(cmd, info, True, '-', escape) for cmd, info in CHARACTER_COMMANDS.items()])
            )
    bot.send_message(chat_id=update.message.chat_id, text=help_message, parse_mode="Markdown", disable_web_page_preview=True)

def formatting_command(cmd, info, add_params=False, separator='-', escape=False):
    params = ', '.join(info[1]) + ' ' if add_params is True and info[1] is not None else ''
    params = escape_md(params) if escape is True else params
    desc = info[2]
    formatted_cmd = f"{cmd} {params}{separator} {desc}"
    return formatted_cmd

def escape_md(text):
    text = text.replace('_', '\_')
    text = text.replace('<', '\<')
    text = text.replace('>', '\>')
    text = text.replace('|', '\|')
    return text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fmt = sys.argv[1]
        if fmt == "--botfather" or fmt == "-b":
            print(help_for_botfather())
        elif fmt == "--markdown" or fmt == "-m":
            print(help_in_markdown())
        elif fmt == "--mdtables" or fmt == "-t":
            print(help_in_markdown_tables())
