from Core.Singelton import Singelton

class Configuration:
    __metaclass__ = Singelton
    __slots__ = ('__keys', '__params')
    __keys = ['IDL_LOCATION']
    def __init__(self):
        self.__params = {}

    def AddParam(self, key, value):
        if self.__params.has_key(key):
            raise KeyError("An already existing key was provided, key - {0}".format(key))
        elif key not in Configuration.__keys:
            raise KeyError("Key - {0} is not supported".format(key))
        self.__params[key] = value

    def GetParam(self, key):
        if self.__params.has_key(key) == False:
            raise KeyError("A non existing key - {0} was requested".format(key))
        elif key not in Configuration.__keys:
            raise KeyError("Key - {0} is not supported".format(key))
        return self.__params[key]

    def LoadParams(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.AddParam(key, value)



