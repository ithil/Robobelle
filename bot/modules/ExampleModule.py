from BaseModule import BaseModule

class ExampleModule(BaseModule):

    matchers = {"!match_this": "run_function"}
    events = { "joined": "do_this_on_user_join" }

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def run_function(discard,msg):
        """
        Function that will be run when command !match_this is provided.
        This docstring becomes the help message when !help is run.
        """
        return msg

    def do_this_on_user_join(self):
      """This function will be run when the 'joined' event hook is triggered"""
      return None

    def raw(discard, msg):
        """ Function that will always be run, on any message. No reply can be sent"""
        print("Received message {}".format(msg))
