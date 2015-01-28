from BaseModule import BaseModule

class ExampleModule(BaseModule):

    matchers = [{"regex": "!match_this", "function": "run_function",
                 "description": "When !match_this matches the message, run_function()"}
                ]
    events = dict("joined": dict{"function": "do_this_on_user_join",
                                 "description": "Perform action on event"})

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def run_function(discard,msg):
        """ Function that will be run when command !match_this is provided"""
        return msg

    def raw(discard, msg):
        """ Function that will always be run, on any message. No reply can be sent"""
        print("Received message {}".format(msg))
