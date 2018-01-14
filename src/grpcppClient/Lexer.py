from Core.File import File
from Core.Singelton import Singelton

class Lexer():
    __metaclass__ = Singelton

    def __init__(self):
        self.__parsedSchemas = {}
        self.__symbolHandlers = {'service': self.HandleServiceToken,
                                 '{': self.HandleServiceToken}

    def ParseLine(self, line):
        tokenizedLine = line.split(' ')
        for idx, symbol in enumerate(tokenizedLine):
            if self.__symbolHandlers.has_key(symbol):
                self.__symbolHandlers[symbol](tokenizedLine[idx + 1:])

    def ParseSchema(self, idlLocation):
        with File(idlLocation) as file:
            for line in file:
                self.ParseLine(line.split('\n')[0])

    def HandleServiceToken(self, subTokenizedLine):
        print subTokenizedLine


