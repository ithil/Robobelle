from BaseModule import BaseModule

class SayHello(BaseModule):

    matchers = [{"regex": "!hi", "function" : "say_hello", "description": "Responds to !hi with HELLO"}]

    def __init__(self, args):
        super(SayHello,self).__init__(self)

    def say_hello(discard,msg):
        return "HELLO"
