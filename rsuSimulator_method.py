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
