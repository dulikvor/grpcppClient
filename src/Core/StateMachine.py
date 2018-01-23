class State:
    def HandleTransition(self, transitionInput):
        raise NotImplementedError('HandleTransition is not supported')

class StateMachine:
    __slots__ = '__currentState'

    def __init__(self, initialState):
        self.__currentState = initialState

    def HandleTransition(self, transitionInput):
        self.__currentState = self.__currentState.HandleTransition(transitionInput)
