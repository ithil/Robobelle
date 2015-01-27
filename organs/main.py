from twisted.internet import protocol
from twisted.python import log
from twisted.words.protocols import irc
from base_module import BaseModule


class RobotFactory(protocol.ClientFactory):
    """ This class inherits IRC protocol stuff from Twisted and sets up the basics """
    # Instantiate IRC protocol
    protocol = RoboBelle
    def __init__(self, settings):
        settings["modules"] = [BaseModule]

        for plugin in modules:
            self.modules.append(plugin())


        """ Initialize the bot factory with provided settings """
        self.network = settings["network"]
        self.channels = settings["channel"]
        self.realname = settings["realname"]
        self.user = settings["user"]
        self.nick = settings["nick"]
        self.modules = settings["modules"] # Contains all classes to load and initialize!
        self.command_prefix = "!"


class RoboBelle(irc.IRCClient):
    def connectionMade(self):
        """Called when a connection is made."""
        self.nickname = self.factory.nickname
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
        if self.nickname != self.factory.nickname:
            log.msg('Nickname was taken, actual nickname is now "{}"'.format(self.nickname))

        for channel in self.channels:
            self.join(channel)


    def joined(self, channel):
        """Called when the bot joins the channel."""
        log.msg("[{nick} has joined {channel}]".format(nick=self.nick, channel=channel))


    def privmsg(self, user, channel, msg):
        """Called when the bot receives a message."""

        if msg.startswith(self.command_prefix):
            sender = user.split('!', 1)[0]
            reply_to = ''

            # If it's a PM
            if channel == self.nick:
                reply_to = sender
            # If it's a channel message
            elif msg.startswith(self.nick):
                reply_to = channel

            for module in self.modules:
                reply = getattr(module, 'run_if_matches')()
                if reply:
                    self.msg(reply_to, reply)
