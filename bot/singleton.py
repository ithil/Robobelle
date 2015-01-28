class Singleton(type):
    """
    This is a metaclass that allows the module loader to be a singleton,
    because there should never be a need for multiple module loaders,
    and a module loader should be accessed without reinstantiation.
    """
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance
