import sys

# To update commands in README.md:
# python3 help.py --tables
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
                '\n'.join([concat_command(c, True, '|') for c in GENERAL_COMMANDS]),
                CAMPAIGN_COMMANDS_TABLE_HEADER,
                '\n'.join([concat_command(c, True, '|') for c in CAMPAIGN_COMMANDS]),
                CHARACTER_COMMANDS_TABLE_HEADER,
                '\n'.join([concat_command(c, True, '|') for c in CHARACTER_COMMANDS])
            )

# Markdown with no tables. Used for the response of /help
def help_in_markdown(include_summary=False, escape=False):
    pass

# Just a list of plain text, no markup, no arguments.
# Used to update the list of commands in @botfather
def help_for_botfather():
    def escape(cmd):
        return cmd[1:]

    command_list = GENERAL_COMMANDS + CAMPAIGN_COMMANDS + CHARACTER_COMMANDS
    return '\n'.join([escape(concat_command(c)) for c in command_list]).strip()



if __name__ == "__main__":
    if len(sys.argv) > 1:
        fmt = sys.argv[1]
        if fmt == "--botfather" or fmt == "-b":
            print(help_for_botfather())
        elif fmt == "--markdown" or fmt == "-m":
            print(help_in_markdown())
        elif fmt == "--tables" or fmt == "-t":
            print(help_in_markdown_tables())
