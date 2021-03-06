import math
import random
import numpy as np
from config import Config


def getNearCar(car, currentTime, network):
    minDis = float('inf')
    listRes = []
    for car_ in network.carList:
        # remove itself
        if car_.id == car.id:
            continue
        if (car_.startTime - Config.simStartTime) / 60 > currentTime:
            continue
        if car_.currentNumMessage >= car_.carMaxCapacity:
            continue
        distance = car.distanceToCar(car_, currentTime)
        if distance > Config.carCoverRadius:
            continue
        if distance < minDis:
            minDis = distance
            listRes = [car_]
        elif distance == minDis:
            listRes.append(car_)
    # print(listRes)
    if listRes:
        return listRes[random.randint(0, len(listRes) - 1)]
    else:
        return None


def getNearRsu(car, currentTime, network):
    minDis = float('inf')
    listRes = []
    for rsu in network.rsuList:
        distance = car.distanceToRsu(rsu, currentTime)
        if distance > Config.rsuCoverRadius:
            continue
        if distance < minDis:
            minDis = distance
            listRes = [rsu]
        elif distance == minDis:
            listRes.append(rsu)
    if listRes:
        return listRes[random.randint(0, len(listRes) - 1)]
    else:
        return None


def getPosition(car, currentTime):
    """
    car: Car object
    curentTime: number [0; simTime]

    return: posistion of this car
    """

    currentTimeCar = car.startTime + 60 * currentTime
    if currentTimeCar in car.timeLocation:
        car.currentLocation = car.timeLocation[currentTimeCar][0]
        return car.currentLocation
    return car.currentLocation


def distanceToCar(car1, car2, currentTime):
    car1Position = car1.getPosition(currentTime)
    car2Position = car2.getPosition(currentTime)
    dist = np.linalg.norm(np.array(car1Position) - np.array(car2Position))
    # print(dist)
    return dist


def distanceToRsu(car, rsu, currentTime):
    carPosition = car.getPosition(currentTime)
    return math.sqrt(
        pow(carPosition[0] - rsu.xcord, 2) + pow(carPosition[1] - rsu.ycord, 2) + pow(rsu.zcord, 2)
    )


def getAction2(car, message, currentTime, network, optimizer=None):
    """Get action of this car for the message
    Args:
        car ([CarSimulator]): [description]
        message ([Message]): [description]
        currentTime ([float]): [description]
        network ([Network]): [description]
        optimizer ([type], optional): [description]. Defaults to None.
    Returns:
        action: [0:sendToCar, 1:sendToRsu, 2:sendToGnb or 3:noChange]
        nextLocation: [The location where the message will be sent to]
    """
    pCarToCar = 0.4
    pCarToRsu = 0.4
    pCarToGnb = 0.1
    rand = random.random()
    if rand < pCarToCar:
        nearCar = car.getNearCar(currentTime, network)
        if nearCar:
            return (0, nearCar)
        else:
            if car.currentNumMessage == car.carMaxCapacity:
                return (2, network.gnb)
            return (3, None)
    elif rand < pCarToCar + pCarToRsu:
        nearRsu = car.getNearRsu(currentTime, network)
        if nearRsu:
            return (1, nearRsu)
        else:
            if car.currentNumMessage == car.carMaxCapacity:
                return (2, network.gnb)
            return (3, None)
    elif rand < pCarToCar + pCarToRsu + pCarToGnb:
        return (2, network.gnb)
    else:
        return (3, None)


def getAction(car, message, currentTime, network, optimizer=None):
    """
    Get action of this car for the message
    :param car:
    :param message:
    :param currentTime:
    :param network:
    :param optimizer:
    :return:
    """
    # 0: car, 1:rsu, 2:gnb, 3:no change

    # action = epsilon_greedy_policy(Q, State) #
    stateInfo = car.optimizer.getState(message)
    neighborCar = stateInfo[1]
    neighborRsu = stateInfo[2]

    car.optimizer.currentState = stateInfo
    allActionValues = car.optimizer.mappingStateToValue(stateInfo)

    exclude_actions = []
    if neighborCar is None:
        exclude_actions.append(0)
    if neighborRsu is None:
        exclude_actions.append(1)

    actionByPolicy = car.optimizer.policy(allActionValues, exclude_actions)
    car.optimizer.policyAction = actionByPolicy

    if actionByPolicy == 0:
        res = (0, stateInfo[1])
    elif actionByPolicy == 1:
        res = (1, stateInfo[2])
    elif actionByPolicy == 2:
        res = (2, network.gnb)
    else:
        res = (3, None)

    return res
