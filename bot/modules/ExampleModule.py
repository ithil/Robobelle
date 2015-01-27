from BaseModule import BaseModule

class ExampleModule(BaseModule):

    matchers = {"!match_this" : "run_function"}

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self.matchers)

    def run_function(discard,msg):
        """ Function that will be run when command !match_this is provided"""
        return msg

    def raw(discard, msg):
        """ Function that will always be run, on any message. No reply can be sent"""
        print("Received message {}".format(msg))
