from ConfigParser import ConfigParser
from twisted.application.service import IServiceMaker, Service
from twisted.internet.endpoints import clientFromString
from twisted.plugin import IPlugin
from twisted.python import usage, log
from zope.interface import implementer
from organs.main import RobotFactory

class Options(usage.Options):
    # Using Twisted's usage Options
    optParameters = [
        ['config', 'c', 'settings.ini', 'Configuration file.'],
    ]

class RoboBelleService(Service):
    def __init__(self, endpoint, channels, nick, realname, user, modules):
        self._endpoint = endpoint
        self._channels = channels
        self._nick = nick
        self._realname = realname
        self._user = user
        self._modules = modules

    def startService(self):
        """Construct a client and connect to server"""
        from twisted.internet import reactor

        def connected(bot):
            self._bot = bot
        def failure(err):
            log.err(err, _why='Could not connect to specified server')
            reactor.stop()

        client = clientFromString(reactor, self._endpoint)
        factory = RobotFactory({"network" : self._endpoint, "channels": self._channels, "user": self._user, "nick": self._nick , "modules": self._modules, "realname": self._realname })

        return client.connect(factory).addCallbacks(connected,failure)

    def stopService(self):
        """Disconnect"""
        if self._bot and self._bot.transport.connected:
            self._bot.transport.loseConnection()

@implementer(IServiceMaker, IPlugin)
class RoboBelleServiceMaker(object):
    tapname = "belle"
    description = "A modular IRC bot"
    options = Options

    def makeService(self, options):
        """Creates the service"""
        config = ConfigParser()
        config.read([options['config']])
        modules = filter(None, list(module.strip() for module in config.get('belle', 'modules').split('\n')))
        channels = filter(None, list(channel.strip() for channel in config.get('irc','channels').split('\n')))

        return RoboBelleService(
            endpoint = config.get('irc','endpoint'),
            channels = channels,
            nick = config.get('irc', 'nick'),
            realname = config.get('irc', 'realname'),
            user = config.get('irc', 'user'),
            modules = modules,
        )


serviceMaker = RoboBelleServiceMaker()
