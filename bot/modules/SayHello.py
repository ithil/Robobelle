from BaseModule import BaseModule

class SayHello(BaseModule):

    matchers = {"!hi" : "say_hello"}

    def __init__(self, args):
        super(SayHello,self).__init__(self.matchers)

    def say_hello(discard,msg):
        return "HELLO"
