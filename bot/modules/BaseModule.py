import re
from bot.module_loader import ModuleLoader
from twisted.python import log


class BaseModule(object):
    matchers = dict({})
    events = dict({})

    def __init__(self, module):
        self.register_module(module)

    def register_module(self, module):
        loader = ModuleLoader()
        if hasattr(module,'matchers'):
            for matcher in module.matchers:
                ModuleLoader.register_regex(loader, matcher["regex"], module, matcher["function"], matcher["description"])
        if hasattr(module,'events'):
            for event, action in module.events.items():
                ModuleLoader.register_event(loader, event, module, action["function"], action["description"])
