from network import Network
from carSimulator import CarSimulator
from rsuSimulator import RsuSimulator
from gnbSimulator import GnbSimulator
from config import Config
from optimizers.q_learning import CarQLearning


def main():
    gnb = GnbSimulator()

    print("-" * 50)
    rsuList = getRsuList()
    print("RSU length: ", len(rsuList))

    carList = carAppear()
    print("Car length: ", len(carList))

    listTimeMessages = prepareTimeMessages()
    print("Message length: ", len(listTimeMessages))
    print("-" * 50)

    network = Network(
        gnb=gnb,
        rsuList=rsuList,
        carList=carList,
        listTimeMessages=listTimeMessages
    )

    network.run()


# Generate RSU
def getRsuList():
    res = []
    for i in range(Config.rsuNumbers):
        rsu = RsuSimulator(
            id=i,
            xcord=Config.xList[i],
            ycord=Config.yList[i],
            zcord=Config.zList[i],
        )
        res.append(rsu)
    return res


def carCapacity():
    try:
        f = open(Config.carMaxCapacity, "r")
    except:
        print("File carCapacity not found")
        exit()
    res = []
    for x in f:
        tmp = int(x)
        res.append(tmp)
    return res


# Generate Sensor on Car
def carAppear():
    carMaxCapacity = carCapacity()

    try:
        f = open(Config.carAppearStrategy, "r")
    except:
        print("File car not found")
        exit()
    res = []
    currentTime = 0
    index = 0
    for x in f:
        tmp = float(x)
        timeStartCar = currentTime + tmp
        if timeStartCar > Config.simTime:
            return res
        car = CarSimulator(id=index, startTime=timeStartCar, carMaxCapacity=carMaxCapacity[index])
        optimizer = CarQLearning(car=car)
        car.optimizer = optimizer
        res.append(car)
        index += 1
        currentTime = timeStartCar
    return res


# Time Messages
def prepareTimeMessages():
    try:
        f = open(Config.carPacketStrategy, "r")
    except:
        print("File packet not found !!!")
        exit()
    currentTime = 0
    res = []
    for x in f:
        tmp = float(x)
        timeStartFromCar = currentTime + tmp
        if timeStartFromCar > Config.simTime:
            break
        currentTime = timeStartFromCar
        res.append(timeStartFromCar)
    return res


if __name__ == "__main__":
    main()
