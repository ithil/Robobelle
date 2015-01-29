import re

from trigger import Trigger
from twisted.python import log

from bot.module_loader import ModuleLoader

class Event(Trigger):

    target = ""
    event = ""

    """
    Wraps all important information in an event and triggers
    appropriate functions in modules depending on the content.
    This is managed by the Trigger class.
    """
    def __init__(self, event, contents, source, target, channel, reply_handle):
        self.target = target
        self.event = event
        super(self.__class__,self).__init__(contents, source, channel, reply_handle)


    def dispatch(self):
        log.msg("Event {} triggered".format(self.event))
        for event, modules in ModuleLoader.modules["event"].items():
            if self.event is event:
                for module in modules:
                    log.msg("Event matched ")
                    log.msg(module)
                    reply = getattr(module["module"], module["function"])(self)
