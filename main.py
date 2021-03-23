from network import Network
from carSimulator import CarSimulator
from rsuSimulator import RsuSimulator
from gnbSimulator import GnbSimulator
from config import Config


def main():
    gnb = GnbSimulator()

    rsuList = getRsuList()
    print("RSU length: ", len(rsuList))

    carList = carAppear()
    print("Car length: ", len(carList))

    listTimeMessages = prepareTimeMessages()
    print("Message length: ", len(listTimeMessages))

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


# Generate Sensor on Car
def carAppear():
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
        car = CarSimulator(index, timeStartCar)
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
