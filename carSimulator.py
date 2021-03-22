import math
from object import Object
from message import Message
from config import Config
from carSimulator_method import getAction, getNearCar, getNearRsu


class CarSimulator(Object):

    def __init__(self, id, startTime):
        Object.__init__(self)
        self.id = id
        self.startTime = startTime
        self.numMessage = 0
        self.preReceiveFromGnb = 0.0

    def collectMessages(self, currentTime, listTimeMessages):
        """Collect the messages in waitList which have the current time
        in [currentTime, currentTime + cycleTime] and generate time from
        list time prepared

        Args:
            currentTime ([float]): [description]
            listTimeMessages ([list(float)]): [description]

        Returns:
            [list(Messages)]: [description]
        """
        # If car isn't in road, return
        if self.getPosition(currentTime) > Config.roadLength:
            return []

        # Collect from waitList
        res = Object.collectMessages(self, currentTime)

        # Generate message
        if self.numMessage >= len(listTimeMessages):
            return res
        curTime = listTimeMessages[self.numMessage]

        while True:
            sendTime = self.startTime + curTime
            if sendTime > currentTime + Config.cycleTime:
                return res
            mes = Message(indexCar=self.id, time=sendTime)
            res.append(mes)
            self.numMessage += 1
            if (self.numMessage >= len(listTimeMessages)):
                return res
            curTime = listTimeMessages[self.numMessage]

        return res

    def sendToCar(self, car, message, currentTime, network):
        """Simualte send message from car to car

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
            preReceive=car.preReceiveFromCar,
            meanTranfer=Config.carCarMeanTranfer,
            message=message,
        )

        # Add current location to list locations of message
        # and change preReceiveFromCar of this car
        message.locations.append(0)
        car.preReceiveFromCar = message.currentTime

        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            car.waitList.append(message)
        else:
            network.addToHeap(message)

    def sendToRsu(self, rsu, message, currentTime, network):
        """Simualte send message from car to rsu

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
            preReceive=rsu.preReceiveFromCar,
            meanTranfer=Config.carRsuMeanTranfer,
            message=message,
        )

        # Add current location to list locations of message
        # and change preReceiveFromCar of this rsu
        message.locations.append(1)
        rsu.preReceiveFromCar = message.currentTime

        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            rsu.waitList.append(message)
        else:
            network.addToHeap(message)

    def sendToGnb(self, gnb, message, currentTime, network):
        """Simualte send message from car to gnb

        Args:
            gnb ([GnbSimulator]): [description]
            message ([Message]): [description]
            currentTime ([float]): [description]
            network ([Network]): [description]
        """

        # Simulate tranfer time to rsu
        self.simulateTranferTime(
            preReceive=gnb.preReceiveFromCar,
            meanTranfer=Config.carGnbMeanTranfer,
            message=message,
        )

        # Add current location to list locations of message
        # and change preReceiveFromCar of gnb
        message.locations.append(2)
        gnb.preReceiveFromCar = message.currentTime

        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            gnb.waitList.append(message)
        else:
            network.addToHeap(message)

    def process(self, message, currentTime, network):
        # Simulate process time
        self.simulateProcessTime(
            processPerSecond=Config.carProcessPerSecond,
            message=message,
        )
        if message.currentTime > currentTime + Config.cycleTime:
            self.waitList.append(message)
        else:
            network.addToHeap(message)

    def getPosition(self, currentTime):
        """Get the current position of the car

        Args:
            currentTime ([float]): [description]

        Returns:
            [float]: [description]
        """
        return Config.carSpeed * (currentTime - self.startTime)

    def distanceToCar(self, car, currentTime):
        return abs(self.getPosition(currentTime) - car.getPosition(currentTime))

    def distanceToRsu(self, rsu, currentTime):
        position = self.getPosition(currentTime)
        return math.sqrt(
            pow(position - rsu.xcord, 2) + pow(rsu.ycord, 2) + pow(rsu.zcord, 2)
        )

    def getNearCar(self, currentTime, network, func=getNearCar):
        return func(self, currentTime, network)

    def getNearRsu(self, currentTime, network, func=getNearRsu):
        return func(self, currentTime, network)

    def working(self, message, currentTime, network, getAction=getAction):
        if message.isDone:
            startCar = network.carList[message.indexCar[0]]
            if startCar.getPosition(currentTime) > Config.roadLength or \
                    self.distanceToCar(startCar, currentTime) > Config.carCoverRadius:
                message.isDropt = True
                network.output.append(message)
            elif startCar.id == self.id:
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
