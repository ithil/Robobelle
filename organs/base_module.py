import re

class BaseModule(object):

    def __init__(new_matchers):
        for function, regex in new_matchers.items():
            register_matcher(regex, function)

    def register_matcher(matcher,function):
        self.matchers[function] = re.compile(matcher)

    def run_if_matches(msg):
        for function, regex in self.matchers.items():
            if regex.match(msg):
                if not hasattr(self, function):
                    raise Exception("{classname} does not have a function named {functionname}".format(classname=self.__class__.__name__, functionname=function))
                else:
                    return getattr(self, function)(msg)
        return False
