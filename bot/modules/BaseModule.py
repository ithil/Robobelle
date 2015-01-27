import re
from twisted.python import log

class BaseModule(object):
    matchers = dict({})
    def __init__(self, new_matchers):
        for regex, function in new_matchers.items():
            self.matchers[regex] = function


    def run_if_matches(self,obj,msg):
        """
            This function will be run on each object, and continues
            to run the function on the object associated with its regex.
            The regex matcher will be stripped from the message before
            the message is passed to the objects function.

            self  --  Explicit self
            obj  --  Instantiated module object to execute function on
            msg  --  Message that may trigger the function
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
                    log.msg("Calling {function} on {object}".format(function=function, object=obj.__class__.__name__))
                    reply = getattr(obj, function)(msg)
                    log.msg("{object}.{function} returned {reply}".format(object=obj.__class__.__name__, function=function, reply=reply))
                    return reply
        return False
