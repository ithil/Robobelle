from twisted.internet import protocol
from twisted.python import log
from twisted.words.protocols import irc


class RobotFactory(protocol.ClientFactory):
    """ This class inherits IRC protocol stuff from Twisted and sets up the basics """
    # Instantiate IRC protocol
    protocol = RoboBelle
    def __init__(self, settings):
        """ Initialize the bot factory with provided settings """
        self.network = settings["network"]
        self.channels = settings["channel"]
        self.realname = settings["realname"]
        self.user = settings["user"]
        self.nick = settings["nick"]
        self.


class RoboBelle(irc.IRCClient):
    def connectionMade(self):
        """Called when a connection is made."""

    def connectionLost(self, reason):
        """Called when a connection is lost."""

    # Event callbacks

    def signedOn(self):
        """Called when bot has successfully signed on to server."""


    def joined(self, channel):
        """Called when the bot joins the channel."""


    def privmsg(self, user, channel, msg):
        """Called when the bot receives a message."""
