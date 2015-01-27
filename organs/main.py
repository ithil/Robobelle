import copy

from twisted.internet import protocol
from twisted.python import log
from twisted.words.protocols import irc

from module_loader import ModuleLoader

class RoboBelle(irc.IRCClient):
    mods = []

    def connectionMade(self):
        """Called when a connection is made."""
        self.nickname = self.factory.nick
        self.realname = self.factory.realname
        irc.IRCClient.connectionMade(self)
        log.msg("Connection established")

    def connectionLost(self, reason):
        """Called when a connection is lost."""
        irc.IRCClient.connectionLost(self, reason)
        log.msg("connectionLost {!r}".format(reason))

    # Event callbacks
    def signedOn(self):
        """Called when bot has successfully signed on to server."""
        log.msg("Logged in")
        if self.nickname != self.factory.nick:
            log.msg('Nickname was taken, actual nickname is now '
                    '"{}"'.format(self.nickname))

        for channel in self.factory.channels:
            self.join(channel)

    def joined(self, channel):
        """Called when the bot joins the channel."""
        log.msg("[{nick} has joined {channel}]".format(nick=self.nickname,
                                                       channel=channel))

    def privmsg(self, user, channel, msg):
        """Called when the bot receives a message."""

        if msg.startswith(self.factory.command_prefix):
            sender = user.split('!', 1)[0]
            reply_to = ''

            # If it's a PM
            if channel == self.nickname:
                reply_to = sender
            else:
                reply_to = channel

            for module in self.factory.loader.modules:
                reply = getattr(module,'run_if_matches')(module,msg)
                if reply:
                    log.msg("Sending reply to {sender} ({mess})".format(sender=reply_to, mess=reply))
                    self.msg(reply_to, reply)
                else:
                    log.msg("Reply came out as {}".format(reply))


class RobotFactory(protocol.ClientFactory):
    """ This class inherits IRC protocol stuff
    from Twisted and sets up the basics """

    # Instantiate IRC protocol
    protocol = RoboBelle

    def __init__(self, settings):
        self.modules = []                   # Array containing modules

        for channel in settings["channels"]:
            print("I HAVE CHANNEL: "+channel)

        """ Initialize the bot factory with provided settings """
        self.network = settings["network"]
        self.channels = settings["channels"]
        self.realname = settings["realname"]
        self.user = settings["user"]
        self.nick = settings["nick"]
        self.command_prefix = settings["command_prefix"]
        self.loader = copy.copy(ModuleLoader())
