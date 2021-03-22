import random
from config import Config


def getNearCar(car, currentTime, network):
    minDis = Config.roadLength
    listRes = []
    for car_ in network.carList:
        if car_.id == car.id:
            continue
        if car_.startTime > currentTime:
            continue
        distance = car.distanceToCar(car_, currentTime)
        if distance > Config.carCoverRadius:
            continue
        if distance < minDis:
            minDis = distance
            listRes = [car_]
        elif distance == minDis:
            listRes.append(car_)
    if listRes:
        return listRes[random.randint(0, len(listRes) - 1)]
    else:
        return None


def getNearRsu(car, currentTime, network):
    minDis = 10000000
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


def getAction(car, message, currentTime, network, optimizer=None):
    """Get action of this car for the message

    Args:
        car ([CarSimulator]): [description]
        message ([Message]): [description]
        currentTime ([float]): [description]
        network ([Network]): [description]
        optimizer ([type], optional): [description]. Defaults to None.

    Returns:
        action: [0:sendToCar, 1:sendToRsu, 2:sendToGnb or 3:process]
        nextLocation: [The location where the message will be sent to]
    """
    pCarToCar = 0.05
    pCarToRsu = 0.45
    pCarToGnb = 0.45
    rand = random.random()
    if rand < pCarToCar:
        nearCar = car.getNearCar(currentTime, network)
        if nearCar:
            return (0, nearCar)
        else:
            return (2, network.gnb)
    elif rand < pCarToCar + pCarToRsu:
        nearRsu = car.getNearRsu(currentTime, network)
        if nearRsu:
            return (1, nearRsu)
        else:
            return (2, network.gnb)
    elif rand < pCarToCar + pCarToRsu + pCarToGnb:
        return (2, network.gnb)
    else:
        return (3, None)
