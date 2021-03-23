import math
from object import Object
from message import Message
from config import Config
from rsuSimulator_method import getNearCar, getNearRsu


class RsuSimulator(Object):

    def __init__(self, id, xcord, ycord, zcord):
        Object.__init__(self)
        self.id = id
        self.xcord = xcord
        self.ycord = ycord
        self.zcord = zcord
        self.nearRsuList = []

    def sendToCar(self, car, message, currentTime, network, numOfPacket=1):
        """Simualte send message from rsu to car

        Args:
            car ([CarSimulator]): [description]
            message ([Message]): [description]
            currentTime ([float]): [description]
            network ([Network]): [description]
        """
        # Add index car to list indexCar of message
        message.indexCar.append(car.id)

        # Simulate tranfer time to car
        self.simulateTranferTime(
            preReceive=car.preReceiveFromRsu,
            meanTranfer=Config.rsuCarMeanTranfer,
            message=message,
            numOfPacket=numOfPacket
        )

        # Add current location to list locations of message
        # and change preReceiveFromRsu of this car
        message.locations.append([0, car.id])
        car.preReceiveFromRsu = message.currentTime

        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            car.waitList.append(message)
        else:
            network.addToHeap(message)

    def distanceToCar(self, car, currentTime):
        positionCar = car.getPosition(currentTime)
        return math.sqrt(
            pow(positionCar - self.xcord, 2) + pow(self.ycord, 2) + pow(self.zcord, 2)
        )

    def distanceToRsu(self, rsu):
        return math.sqrt(
            pow(self.xcord - rsu.xcord, 2) + \
            pow(self.ycord - rsu.ycord, 2) + \
            pow(self.zcord - rsu.zcord, 2))

    def getNearCar(self, currentTime, network, func=getNearCar):
        func(self, currentTime, network)

    def getNearRsu(self, func=getNearRsu):
        func(self)

    def working(self, message, currentTime, network):
        self.simulateSuccessTransmission(
            message=message,
        )

        startCar = network.carList[message.indexCar[0]]
        if startCar.getPosition(currentTime) > Config.roadLength or \
                self.distanceToCar(startCar, currentTime) > Config.rsuCoverRadius:
            message.isDropt = True
            network.output.append(message)
        else:
            self.sendToCar(startCar, message, currentTime, network, numOfPacket=1)
