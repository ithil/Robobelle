from BaseModule import BaseModule

class Democracy(BaseModule):

    matchers = {"^!poll": "create_poll", "^!vote\s+\d": "vote", "^!polls": "last_polls", "^!answer": "add_answer"}

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def create_poll(self, msg):
      """Creates a new poll (either !poll title;answer1;answer2, or !poll title followed by !answer First option)"""
      return None

    def last_polls(self, msg):
      """Returns a list of the most recent polls and their IDs"""
      return None

    def vote(self, msg):
      """Vote for option with provided number in current poll"""
      return None

    def add_answer(self, msg):
      """Adds an option to the current poll"""
      return None
