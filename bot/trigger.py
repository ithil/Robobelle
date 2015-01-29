from module_loader import ModuleLoader
from twisted.python import log

class Trigger(object):
    contents = ""       # Contains the contents
    author = ""         # Contains a string representation of the sender
    channel = ""
    modules = None
    reply_handle = None # Contains the object to user for replying to the message

    def __init__(self, contents, author, channel, reply_handle):
        self.contents = contents
        self.author = author
        self.channel = channel
        self.reply_handle = reply_handle



    def reply(self, message):
        """
        Sends a reply to the message; either back to the channel from which
        it originated, or back to the user/PM.

        message --  String to reply with
        """
        if self.channel == self.author:
            self.reply_handle.msg(self.author, message)
            log.msg("Sending reply to {}".format(self.author))
        else:
            self.reply_handle.msg(self.channel, message)
            log.msg("Sending reply to {}".format(self.channel))
