class CommandNotFound(Exception):
    """Raised when the command tried by the user doesn't exist or is not supported"""
    pass

class NotACommand(Exception):
    """Raised when the message from the chat is not a command"""
    pass

class CampaignNotFound(Exception):
    """Raised when theres not an active campaign"""
    pass

class CharacterNotFound(Exception):
    """Raised when a character is not defined or doesn't exist in the database"""
    pass

class InvalidCommand(Exception):
    """Raised when a command doesn't have a valid structure"""
    pass

class NotADM(Exception):
    """Raised when a dm only command is triggered by a regular user"""
    pass
