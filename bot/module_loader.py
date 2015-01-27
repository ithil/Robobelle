import pkgutil
import os
import sys
import re
import copy
from twisted.python import log

class ModuleLoader(object):
    modules = []    # Contains instances of each module

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "modules")
        modules = pkgutil.iter_modules(path=[path])
        sys.path.append(path)

        for loader, mod_name, ispkg in modules:
            # Ensure that module isn't already loaded
            if mod_name not in sys.modules:
                # Import module
                loaded_mod = __import__(mod_name, fromlist=[mod_name])

                # Load class from imported module
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', mod_name)
                file_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
                loaded_class = getattr(loaded_mod, mod_name)

                # Create an instance of the class
                # except if it's the BaseModule class
                if mod_name != "BaseModule":
                    instance = loaded_class(mod_name)
                    self.modules.append(copy.copy(instance))
                    log.msg("Loaded module {}".format(mod_name))
