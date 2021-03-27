from optimizers.optimizer import Optimizer
from config import Config
from optimizers.q_learning_method import getBehaviorPolicy, getState, mappingStateToInt, calculateReward, updateQTable
import numpy as np


class CarQLearning(Optimizer):
    def __init__(self, car, policy_func=getBehaviorPolicy, policy_parameters=Config.policyParamatersCar):
        self.car = car
        self.nStates = Config.nStatesCar
        self.nActions = Config.nActionsCar
        self.QTable = np.zeros((self.nStates, self.nActions))

        self.dictState = dict()
        self.numState = -1

        self.currentState = None
        self.currentIntState = None
        self.policyAction = None
        self.doAction = None

        self.policy = policy_func(nActions=self.nActions, parameters=policy_parameters).getPolicy()

    # def initializationQTable(self):
    #     self.QTable = np.zeros((self.nStates, self.nActions))

    def getState(self, message, func=getState):
        return func(self.car, message)

    def getValue(self, stateInforInt):
        return self.QTable[stateInforInt]

    def mappingStateToInt(self, state, func=mappingStateToInt):
        """
        Mapping from tuple State to Int number
        """
        return func(self, state)

    def calculateReward(self, message, func=calculateReward):
        func(self, message)

    # def updateQTable(self, message, func=updateQTable):
    #     func(self, message)
