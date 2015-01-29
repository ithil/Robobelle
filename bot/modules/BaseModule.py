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
        if hasattr(module,'matchers') and len(module.matchers):
            for regex,function in module.matchers.items():
                ModuleLoader.register_regex(loader, regex, module, function, getattr(module, function).__doc__)
        if hasattr(module,'events') and len(module.events):
            for event, action in module.events.items():
                ModuleLoader.register_event(loader, event, module, action, getattr(module, function).__doc__)
