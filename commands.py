from roll import handler as roll_handler
from charsheet import handler as charsheet_handler
#from help import handler as help_handler
from character import handler as character_handler
from turns import handler as turn_handler
from dm import handler as dm_handler
from campaign import handler as campaign_handler
    
# cmd, handler, args, description
GENERAL_COMMANDS = {
    #"/start": (start, None, "starts the DnDCompanionBot"),
    "/roll": (roll_handler, "<expression>", "rolls the dice using the [dice notation](https://en.wikipedia.org/wiki/Dice_notation)"),
    "/charsheet": (charsheet_handler, "<username>", "returns the character sheet associated with username"),
    #"/combatsheet": (None, None, "returns the link of the combat cheatsheet"),
    #"/help": (help_handler, None, "shows this help message"),
}

CAMPAIGN_COMMANDS = {
    "/start_campaign": (campaign_handler, None, "starts a new campaign in the invoked group"),
    "/close_campaign": (campaign_handler, None, "closes an active campaign"),
    "/set_turns": (turn_handler, "<username1>,...<usernameN>", "creates a list with the order of players for a given round"),
    "/turn": (turn_handler, None, "shows the current player in the turns list"),
    "/next_turn": (turn_handler,  None, "moves to the next player in the turns list"),
    "/set_dm": (dm_handler, "<username>", "sets the username of the DM for the current campaign"),
    "/dm": (dm_handler, None, "shows the DM for the current campaign"),
}

CHARACTER_COMMANDS = {
    "/import_char": (character_handler, "<url>", "imports the JSON data of a character from a URL"),
    "/link_char": (character_handler, "<char_id> <username> OR <char_id>", "links character to target username or self username"),
    "/status": (character_handler, "<username OR character>", "shows the list of weapons of a character"),
    "/weapons": (character_handler, "<username OR character>", "shows the list of weapons of a character"),
    "/attack_roll": (character_handler, "<character> <weapon> melee|range <distance> adv|disadv", "performs an attack roll on a character"),
    "/initiative_roll": (character_handler, "<character>", "performs an initiative roll for a character"),
    "/short_rest_roll": (character_handler, "<username OR character>", "performs an short rest roll for a character"),
    "/talk": (character_handler, "<character> <message>", "prints a message using in-game conversation format"),
    "/say": (character_handler, "<character> <message>", "prints a normal message using in-game conversation format"),
    "/whisper": (character_handler, "<character> <message>", "prints a whisper message using in-game conversation format"),
    "/yell": (character_handler, "<character> <message>", "prints a yell message using in-game conversation format"),
}
