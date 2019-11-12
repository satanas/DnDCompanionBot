class CommandNotFound(Exception):
    """Raised when the command tried by the user doesn't exist or is not supported"""
    pass

class NotACommand(Exception):
    """Raised when the message from the chat is not a command"""
    pass
