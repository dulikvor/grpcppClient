import grpcppClient.Lexer

class Singelton(type):
    __instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instance:
            cls.__instance[cls] = super(Singelton, cls).__call__(*args, **kwargs)
        return cls.__instance[cls]