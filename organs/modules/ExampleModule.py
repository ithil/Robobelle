from BaseModule import BaseModule

class ExampleModule(BaseModule):

    matchers = {"!match_this" : "run_function"}

    def __init__(self, args):
        super(ExampleModule,self).__init__(self.matchers)

    def run_function(discard,msg):
        return msg
