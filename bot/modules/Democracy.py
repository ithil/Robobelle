from BaseModule import BaseModule

class Democracy(BaseModule):

    matchers = [dict({"regex": "^!poll",
                     "function": "create_poll",
                     "description": "Creates a new poll (!poll title;answer1;answer2)"
                     }),
                    dict({"regex": "^!vote <number>",
                     "function": "vote",
                     "description": "Vote for option with provided number in current poll"
                     }),
                    dict({"regex": "^!polls",
                     "function": "last_polls",
                     "description": "Returns a list of the most recent polls and their IDs"
                     }),
                    dict({"regex": "^!answer",
                      "function": "add_answer",
                      "description": "Adds an option to the current poll"
                     })]

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
