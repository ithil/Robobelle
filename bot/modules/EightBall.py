from BaseModule import BaseModule
import random

class EightBall(BaseModule):

    matchers = [dict({"regex": "^!8ball",
                     "function": "eightball",
                     "description": "Picks a random 8ball reply"
                     })]
    events = {}

    answers = ["It is certain",
               "It is decidedly so",
               "Without a doubt",
               "Yes definitely",
               "You may rely on it",
               "As I see it, yes",
               "Most likely",
               "Outlook good",
               "Yes",
               "Signs point to yes",
               "Reply hazy try again",
               "Ask again later",
               "Better not tell you now",
               "Cannot predict now",
               "Concentrate and ask again",
               "Don't count on it",
               "My reply is no",
               "My sources say no",
               "Outlook not so good",
               "Very doubtful"]

    def __init__(self, args):
        """
          Initialize the class as a subclass of BaseModule
          and call parent constructor with the defined matchers.
          These will be turned into regex-matchers that redirect to
          the provided function name
        """
        super(self.__class__,self).__init__(self)

    def eightball(discard,msg):
        """ Pick a random element from the EightBall.answers array """
        return random.choice(discard.answers)
