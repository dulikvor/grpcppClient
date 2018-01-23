from Core.File import File
from Core.Singelton import Singelton
from Core.StateMachine import StateMachine, State

class SchemaContext:
    __metaclass__ = Singelton
    def __init__(self):
        self.services = []

class Service:
    def __init__(self, name):
        self.name = name
        self.operations = []

class Operation:
    def __init__(self, name):
        self.name = name
        self.argumentType = None
        self.returnArgumentType = None


class SchemaState(State):

    def HandleTransition(self, transitionInput):
        if transitionInput not in self.__handlers:
            raise AttributeError('Unknown token was provided - {0}'.format(transitionInput))
        return self.__handlers[transitionInput](self)

    def ServiceHandler(self):
        return ServiceState()

    __handlers = {'service': ServiceHandler}

class ServiceState(State):

    def HandleTransition(self, transitionInput):
        if transitionInput == '{':
            return self
        elif transitionInput == '}':
            return SchemaState()
        elif transitionInput == 'rpc':
            return OperationState()
        else:
            service = Service(transitionInput)
            SchemaContext().services.append(service)
            return self

class OperationState(State):
    def HandleTransition(self, transitionInput):
        if transitionInput == '(':
            return OperationArgumentState()
        elif transitionInput == 'returns':
            return OperationReturnState()
        elif transitionInput == '{':
            return self
        elif transitionInput == '}':
            return ServiceState()
        else:
            SchemaContext().services[-1].operations.append(Operation(transitionInput))
            return self

class OperationArgumentState(State):
   def HandleTransition(self, transitionInput):
       if transitionInput == ')':
           return OperationState()
       elif transitionInput == 'stream':
           raise KeyError('stream operation argument type is not supported is of now.')
       else:
           currentOperation = SchemaContext().services[-1].operations[-1]
           currentOperation.argumentType = transitionInput
           return self

class OperationReturnState(State):
    def HandleTransition(self, transitionInput):
        if transitionInput == '(':
            return self
        elif transitionInput == ')':
            return OperationState()
        else:
            currentOperation = SchemaContext().services[-1].operations[-1]
            currentOperation.returnArgumentType = transitionInput
            return self


class SchemaService:

    def __init__(self, name):
        self.__name = name
        self.__operations = []

    def AddOperation(self, operationName):
        self.__operations.append(operationName)

class Lexer():
    __metaclass__ = Singelton

    def __init__(self):
        self.__parsedSchemas = {}
        self.__stateMachine = StateMachine(SchemaState())

    def ParseLine(self, context, line):
        replaces = {'(': ' ( ', ')':' ) ', '{':' { ', '}': ' } '}
        line = reduce(lambda line, replacePair : line.replace(*replacePair), replaces.iteritems(), line)
        tokenizedLine = line.split(' ')
        for symbol in tokenizedLine:
            if '//' in symbol:
                return
            elif symbol == '':
                continue
            self.__stateMachine.HandleTransition(symbol)

    def ParseSchema(self, idlLocation):
        context = SchemaContext()
        with File(idlLocation) as file:
            for line in file:
                self.ParseLine(context, line.split('\n')[0])

