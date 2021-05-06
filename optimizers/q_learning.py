from optimizers.optimizer import Optimizer
from config import Config
from optimizers.q_learning_method import getBehaviorPolicy, getState, mappingStateToValue, calculateReward, updateQTable
import numpy as np


class CarQLearning(Optimizer):
    def __init__(self, car, policy_func=getBehaviorPolicy, policy_parameters=Config.policyParamatersCar):
        self.car = car
        self.nStates = Config.nStatesCar
        self.nActions = Config.nActionsCar
        self.QTable = dict()
        self.currentState = None
        self.newState = None
        self.policyAction = None
        self.doAction = None
        self.reward = None
        self.parameters = policy_parameters
        self.policy = policy_func(nActions=self.nActions, parameters=self.parameters).getPolicy()

    def getState(self, message, func=getState):
        return func(self.car, message)

    def mappingStateToValue(self, state, func=mappingStateToValue):
        """
        Mapping from tuple State to Int number
        """
        return func(self, state)

    def calculateReward(self, message, carReceived=None, func=calculateReward):
        func(self, message, carReceived)

    def updateQTable(self, func=updateQTable):
        func(self)

    def update(self, message, carReceived=None):
        self.newState = self.getState(message)
        self.calculateReward(message=message, carReceived=carReceived)
        self.updateQTable()

        # def mappingState(state):
        #     state = list(state)
        #     state[1] = 0 if state[1] is None else 1
        #     state[2] = 0 if state[2] is None else 1
        #     state = tuple(state)
        #     return state
        #
        # if message.currentTime - message.sendTime[0] >= Config.deltaTime:
        #     print(mappingState(self.currentState))
        #     print(self.reward)
        #     print(self.QTable)
