import math
from object import Object
from message import Message
from config import Config
from rsuSimulator_method import getAction, getNearCar, getNearRsu


class RsuSimulator(Object):

    def __init__(self, id, xcord, ycord, zcord):
        Object.__init__(self)
        self.id = id
        self.xcord = xcord
        self.ycord = ycord
        self.zcord = zcord
        self.nearRsuList = []


    # Gửi thông điệp thành công xuống xe
    def sendToCar(self, car, message, currentTime, network):
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
        )

        # Add current location to list locations of message
        # and change preReceiveFromRsu of this car
        message.locations.append(0)
        car.preReceiveFromRsu = message.currentTime

        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            car.waitList.append(message)
        else:
            network.addToHeap(message)

    def sendToRsu(self, rsu, message, currentTime, network):
        """Simualte send message from rsu to rsu

        Args:
            rsu ([RsuSimulator]): [description]
            message ([Message]): [description]
            currentTime ([float]): [description]
            network ([Network]): [description]
        """
        # Add index rsu to list indexRsu of message
        message.indexRsu.append(rsu.id)

        # Simulate tranfer time to rsu
        self.simulateTranferTime(
            preReceive=rsu.preReceiveFromRsu,
            meanTranfer=Config.rsuRsuMeanTranfer,
            message=message,
        )

        # Add current location to list locations of message
        # and change preReceiveFromRsu of this rsu
        message.locations.append(1)
        rsu.preReceiveFromRsu = message.currentTime

        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            rsu.waitList.append(message)
        else:
            network.addToHeap(message)

    def sendToGnb(self, gnb, message, currentTime, network):
        """Simualte send message from rsu to gnb

        Args:
            gnb ([GnbSimulator]): [description]
            message ([Message]): [description]
            currentTime ([float]): [description]
            network ([Network]): [description]
        """

        # Simulate tranfer time to rsu
        self.simulateTranferTime(
            preReceive=gnb.preReceiveFromRsu,
            meanTranfer=Config.rsuGnbMeanTranfer,
            message=message,
        )

        # Add current location to list locations of message
        # and change preReceiveFromRsu of gnb
        message.locations.append(2)
        gnb.preReceiveFromRsu = message.currentTime

        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            gnb.waitList.append(message)
        else:
            network.addToHeap(message)

    def process(self, message, currentTime, network):
        # Simulate process time
        self.simulateProcessTime(
            processPerSecond=Config.rsuProcessPerSecond,
            message=message,
        )
        if message.currentTime > currentTime + Config.cycleTime:
            self.waitList.append(message)
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

    def working(self, message, currentTime, network, getAction=getAction):
        if message.isDone:
            startCar = network.carList[message.indexCar[0]]
            if startCar.getPosition(currentTime) > Config.roadLength or \
                    self.distanceToCar(startCar, currentTime) > Config.rsuCoverRadius:
                message.isDropt = True
                network.output.append(message)
            else:
                self.sendToCar(startCar, message, currentTime, network)
            return
        else:
            action, nextLocation = getAction(self, message, currentTime, network)
            # 0: sendToCar, 1:sendToRsu, 2: sendToGnb, 3:process
            if action == 0:
                self.sendToCar(nextLocation, message, currentTime, network)
            elif action == 1:
                self.sendToRsu(nextLocation, message, currentTime, network)
            elif action == 2:
                self.sendToGnb(nextLocation, message, currentTime, network)
            else:
                self.process(message, currentTime, network)



