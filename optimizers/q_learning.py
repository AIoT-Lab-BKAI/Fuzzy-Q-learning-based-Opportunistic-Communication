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
        self.calculateReward(message=message, carReceived=carReceived)
        self.newState = self.getState(message)
        self.updateQTable()
