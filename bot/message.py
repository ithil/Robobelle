
class Message(object):
    contents = ""       # Contains the contents
    author = ""         # Contains a string representation of the sender
    channel = ""
    modules = RoboFactory.modules()["regex"]
    reply_handle = None # Contains the object to user for replying to the message

    def __init__(self, contents, author, channel, reply_handle):
        self.contents = contents
        self.author = author
        self.channel = channel
        self.reply_handle = reply_handle

    def dispatch(self):

    def reply(self, message):
        """
        Sends a reply to the message; either back to the channel from which
        it originated, or back to the user/PM.

        message --  String to reply with
        """
        reply_handle.msg(author, message) if channel == author else reply_handle.msg(channel, message)
