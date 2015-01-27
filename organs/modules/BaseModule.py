import re

class BaseModule(object):
    matchers = dict({})
    def __init__(self, new_matchers):
        for regex, function in new_matchers.items():
            self.matchers[regex] = function


    def run_if_matches(idk,obj,msg):
        print("Running run_if_matches with msg {}".format(msg))
        for regex, function in obj.matchers.items():
            if re.compile(regex).match(msg):
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
