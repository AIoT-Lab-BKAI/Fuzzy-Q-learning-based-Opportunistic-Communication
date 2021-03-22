import random
from config import Config


def getNearCar(rsu, currentTime, network):
    minDis = 10000000
    listRes = []
    for car in network.carList:
        if car.startTime > currentTime:
            continue
        distance = rsu.distanceToCar(car, currentTime)
        if distance > Config.rsuCoverRadius:
            continue
        if distance < minDis:
            minDis = distance
            listRes = [car]
        elif distance == minDis:
            listRes.append(car)
    if listRes:
        return listRes[random.randint(0, len(listRes) - 1)]
    else:
        return None


def getNearRsu(rsu):
    if rsu.nearRsuList:
        return rsu.nearRsuList[random.randint(0, len(rsu.nearRsuList) - 1)]
    else:
        return None


def getAction(rsu, message, currentTime, network, optimizer=None):
    """Gat action of this rsu for the message

    Args:
        rsu ([RsuSimulator]): [description]
        message ([Message]): [description]
        currentTime ([float]): [description]
        network ([Network]): [description]
        optimizer ([type], optional): [description]. Defaults to None.

    Returns:
        action: [0:sendToCar, 1:sendToRsu, 2:sendToGnb or 3:process]
        nextLocation: [The location where the message will be sent to]
    """
    pRsuToCar = 0.05
    pRsuToRsu = 0.05
    pRsuToGnb = 0.45
    rand = random.random()
    if rand < pRsuToCar:
        nearCar = rsu.getNearCar(currentTime, network)
        if nearCar:
            return (0, nearCar)
        else:
            return (2, network.gnb)
    elif rand < pRsuToCar + pRsuToRsu:
        nearRsu = rsu.getNearRsu()
        if nearRsu:
            return (1, nearRsu)
        else:
            return (2, network.gnb)
    elif rand < pRsuToCar + pRsuToRsu + pRsuToGnb:
        return (2, network.gnb)
    else:
        return (3, None)
