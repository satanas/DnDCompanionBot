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
    pass
