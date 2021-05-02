import numpy as np

from behaviorPolicy.epsilonGreedy import EpsilonGreedy
from config import Config


def getBehaviorPolicy(nActions, parameters):
    policy = EpsilonGreedy(
        nActions=nActions,
        epsilon=parameters["epsilon"]
    )
    return policy


def getNeighborCar(car, message):
    """
    Select near car has minimum capacity
    :param car:
    :return:
    """

    def sortFunc(e):
        return e[0]

    tmp = []
    for car_ in car.neighborCars:
        if car_.id in message.indexCar:
            continue
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
    res.append(int(car.currentNumMessage / 2))

    # Infor of it's neighbor car
    neighborCarInfo = getNeighborCar(car, message)

    if car.currentNumMessage > neighborCarInfo[0]:
        res.append(1)
    else:
        res.append(0)

    # res.append(int(neighborCarInfo[0] / 2))

    # Infor of it's neghbor Rsu
    neighborRsuInfo = getNeighborRsu(car)

    # print(res)
    # only one rsu
    return (tuple(res), neighborCarInfo[-1], neighborRsuInfo)


def mappingStateToInt(carQLearning, state):
    if state in carQLearning.dictState:
        return carQLearning.dictState[state]
    else:
        carQLearning.numState += 1
        carQLearning.dictState[state] = carQLearning.numState

    return carQLearning.dictState[state]


def calculateReward(carQLearning, message, carReceived):
    # TODO: cần thêm các thông tin về carDelayPackage + carCantGenerate
    # 0: sendToCar, 1:sendToRsu, 2: sendToGnb, 3:noChange
    deltaTime = message.currentTime - message.sendTime[0]
    theta = carQLearning.car.fuzzyInference.inference(carQLearning.car.currentNumMessage, deltaTime)
    theta = theta['Theta']
    # sendToCar
    if carQLearning.policyAction == 0:
        reward = carQLearning.car.currentNumMessage - carReceived.currentNumMessage
    # sendToRsu
    elif carQLearning.policyAction == 1:
        # (C* - C_r) / (1 + t)
        reward = (carQLearning.car.carMaxCapacity - int(theta * carQLearning.car.currentNumMessage))
    # sendToGnb
    elif carQLearning.policyAction == 2:
        reward = - (int(theta * carQLearning.car.carMaxCapacity) - carQLearning.car.currentNumMessage)
    # noChange
    else:
        reward = 0

    if deltaTime >= Config.deltaTime:
        reward = reward - 1000
    carQLearning.reward = reward


def calculateReward2(carQLearning, message, carReceived):
    reward = 0
    # 0: sendToCar, 1:sendToRsu, 2: sendToGnb, 3:noChange

    if (message.currentTime - message.sendTime[
        0] >= Config.deltaTime) or carQLearning.doAction != carQLearning.policyAction:
        reward = - 1000

    # sendToCar
    elif carQLearning.policyAction == 0 and carReceived is not None:
        reward = int((carQLearning.car.currentNumMessage - carReceived.currentNumMessage) / 1) / (
                1 + message.currentTime - message.sendTime[0])

    # sendToRsu
    elif carQLearning.policyAction == 1:
        reward = (carQLearning.car.carMaxCapacity - int(8 / 10 * carQLearning.car.currentNumMessage)) / (
                1 + message.currentTime - message.sendTime[0])
    # sendToGnb
    elif carQLearning.policyAction == 2:
        reward = - (int(8 / 10 * carQLearning.car.carMaxCapacity) - carQLearning.car.currentNumMessage) / (
                1 + message.currentTime - message.sendTime[0])

    # noChange
    else:
        reward = - 1 / (1 + message.currentTime - message.sendTime[0])
    carQLearning.reward = reward


def updateQTable(carQLearning, learning_rate=Config.learningRateCar, gamma=Config.disCountingFactorCar):
    """
    Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
    """

    currentStateInt = carQLearning.mappingStateToInt(carQLearning.currentState)
    newStateInt = carQLearning.mappingStateToInt(carQLearning.newState)
    actionInt = carQLearning.policyAction

    carQLearning.QTable[currentStateInt][actionInt] = carQLearning.QTable[currentStateInt][
                                                          actionInt] + learning_rate * (
                                                              carQLearning.reward + gamma * np.max(
                                                          carQLearning.QTable[newStateInt]) -
                                                              carQLearning.QTable[currentStateInt][actionInt])
