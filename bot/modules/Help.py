from BaseModule import BaseModule
from bot.module_loader import ModuleLoader
from bot.modules.ExampleModule import ExampleModule
import re
from time import sleep

class Help(BaseModule):

    matchers = {"!help": "help_message"}
    event = {"join": "say_hi"}

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def help_message(self,msg):
        """
        Prints a help message generated from docstrings from loaded modules
        """
        help = [(mod["regex"], mod["description"]) for mod in ModuleLoader.modules["regex"]]
        help = sorted(help, key=lambda command: command[0])

        count = 0
        msg.reply_handle.msg(msg.author, "I know the following commands: ")
        for h in help:
          if h[0] in ExampleModule.matchers.keys():
            continue
          # Remove regex notation (\s*+, \w*+, \b+*)
          cmd = re.sub(r'((\\w\**\+*)|(\\s\+*\**)|\^|\\b\**\+*)', '', h[0])
          cmd = re.sub(r'(\\d)',' <number>', cmd)
          print("\t" + cmd + "\t-\t" + h[1].strip())
          count += 1

          # Avoid flood limit by sending PM .. hopefully
          msg.reply_handle.msg(msg.author,"\t" + cmd + "\t-\t" + h[1].strip())
        msg.reply("I've sent my resume your way, {}. Check your PM!".format(msg.author))

        #msg.notice(help_message)
