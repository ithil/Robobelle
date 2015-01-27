import re

class BaseModule(object):
    matchers = dict({})
    def __init__(self, new_matchers):
        for regex, function in new_matchers.items():
            self.matchers[regex] = function


    def run_if_matches(idk,obj,msg):
        """
            This function will be run on each object, and continues
            to run the function on the object associated with its regex.
            The regex matcher will be stripped from the message before
            the message is passed to the objects function.
        """

        # Iterate through the objects regex matchers
        for regex, function in obj.matchers.items():

            # If a match is found, and an function exists, run it and reply with
            # returned message (unless message is false). 
            if re.compile(regex).match(msg):
                msg = re.sub(regex, '', msg).strip()    # Strip Command from message
                if not hasattr(obj, function):
                    raise Exception("{classname} does not have a function named {functionname}".format(classname=self.__class__.__name__, functionname=function))
                else:
                    print("Calling {} on object".format(function))
                    reply = getattr(obj, function)(msg)
                    print("Function returned {}".format(reply))
                    return reply
            else:
                print("{} matched nothing".format(msg))
        return False
