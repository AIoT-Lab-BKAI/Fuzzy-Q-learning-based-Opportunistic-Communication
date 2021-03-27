import numpy as np

from behaviorPolicy.epsilonGreedy import EpsilonGreedy
from config import Config


def getBehaviorPolicy(nActions, parameters):
    policy = EpsilonGreedy(
        nActions=nActions,
        epsilon=parameters["epsilon"]
    )
    return policy


def getNeighborCar(car):
    """
    Lựa chọn xe có dung lượng hiện tại nhỏ nhất.
    :param car:
    :return:
    """

    def sortFunc(e):
        return e[0]

    tmp = []
    for car_ in car.neighborCars:
        # TODO: update if currentNumMessage is Max -> continue
        # TODO: update current ID car is not Message send car
        tmp.append((car_.currentNumMessage, car_))
    tmp.sort(key=sortFunc)
    if not tmp:
        return (0.0, None)
    return tmp[0]


def getNeighborRsu(car):
    return car.neighborRsu


def getState(car, message):
    # Infor of this message
    res = [message.packetSize]
    # Time of message
    messageDelayTime = message.currentTime - message.sendTime[0]
    res.append(int(messageDelayTime))

    # Infor of this car
    res.append(car.currentNumMessage)

    # Infor of it's neighbor car
    neighborCarInfo = car.getNearCar
    res.append(neighborCarInfo[0])

    # Infor of it's neghbor Rsu
    neighborRsuInfo = getNeighborRsu(car)
    return (tuple(res), neighborCarInfo[-1], neighborRsuInfo[-1])


def mappingStateToInt(carQLearning, state):
    if state in carQLearning.dictState:
        return carQLearning.dictState[state]
    else:
        carQLearning.numState += 1
        carQLearning.dictState[state] = carQLearning.numState

    return carQLearning.dictState[state]


def calculateReward(carQLearning, message):




    pass


# def updateQTable(qTable, state, newState, action, reward, learning_rate=Config.learningRateCar,
#                  gamma=Config.disCountingFactorCar):
#     """
#     Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
#     :param carQLearning:
#     :return:
#     """
#     qTable[state][action] = qTable[state][action] + learning_rate * (
#             reward + gamma * np.max(qTable[newState] - qTable[state][action]))
#     return qTable

def updateQTable(carQLearning, message):
    """
    Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
    """

    pass
