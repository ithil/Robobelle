from trigger import Trigger
from bot.module_loader import ModuleLoader
from twisted.python import log
import re

class Message(Trigger):
    """
    Wraps all important information in a message and triggers
    appropriate functions in modules depending on the content.
    This is managed by the Trigger class.
    """
    clean_contents = ""

    def __init__(self, contents, author, channel, reply_handle):
        super(self.__class__,self).__init__(contents, author, channel, reply_handle)
        clean_contents = self.strip_command(contents)

    def dispatch(self):
        # Iterate through all loaded modules and call the BaseModule
        # method 'run_if_matches' - if a module has any function
        # associated to the provided command, then it will be executed
        for module in ModuleLoader.modules["regex"]:
            if re.compile(module["regex"]).match(self.contents):
                reply = getattr(module["module"],module["function"])(self)
                log.msg("{match} matched a trigger in {cls} which returned: {reply}".format(match=self.contents, cls=module["module"].__class__.__name__,reply=reply))

    def strip_command(self, raw):
      #command = self.reply_handle.factory.command_prefix+"\w+\s*"
      #self.clean_contents = re.sub(command, "", self.contents)
      split_message = raw.split()

      # Discard first word (command)
      split_message.pop(0)
      self.clean_contents = " ".join(split_message)
