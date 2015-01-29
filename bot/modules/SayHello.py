from BaseModule import BaseModule

class SayHello(BaseModule):

    matchers = [{"regex": "!hi", "function" : "say_hello", "description": "Responds to !hi with HELLO"}]
    events = {"nick": {"function": "say_hello",
                                 "description": "Perform action on event"}}

    def __init__(self, args):
        super(SayHello,self).__init__(self)

    def say_hello(self,msg):
        msg.reply("HELLO")
