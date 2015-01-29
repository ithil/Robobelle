from BaseModule import BaseModule

class SayHello(BaseModule):

    matchers = {"!hi": "say_hello"}
    events = { "nick": "say_hello" }

    def __init__(self, args):
        super(self.__class__,self).__init__(self)

    def say_hello(self,msg):
        """Responds to !hi with HELLO - just an example"""
        msg.reply("HELLO")
