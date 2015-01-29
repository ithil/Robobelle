from BaseModule import BaseModule

class UrbanDictionary(BaseModule):

    matchers = [{"regex": "!ud", "function": "lookup",
                 "description": "Looks up a term on UrbanDictionary"}
                ]

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def lookup(self,msg):
        """ Function that will be run when command !match_this is provided"""
        return msg
