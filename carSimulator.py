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

        self.carMaxCapacity = Config.carMaxCapacity
        self.numMessage = 0  # Total num Message
        self.transferredNumMessage = 0
        self.currentNumMessage = 0
        self.receivedNumMessage = 0

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
            self.currentNumMessage += 1
            if self.numMessage >= len(listTimeMessages):
                return res
            curTime = listTimeMessages[self.numMessage]

        return res

    def sendToCar(self, car, message, currentTime, network, numOfPacket):
        """Simualte send message from car to car

        Args:
            car ([CarSimulator]): [description]
            message ([Message]): [description]
            currentTime ([float]): [description]
            network ([Network]): [description]
        """
        # Update received num message
        car.receivedNumMessage += 1

        # Add index car to list indexCar of message
        message.indexCar.append(car.id)

        # Simulate tranfer time to car
        self.simulateTranferTime(
            preReceive=car.preReceiveFromCar,
            meanTranfer=Config.carCarMeanTranfer,
            message=message,
            numOfPacket=numOfPacket,
        )

        # Add current location to list locations of message
        # and change preReceiveFromCar of this car
        message.locations.append([0, car.id])
        car.preReceiveFromCar = message.currentTime

        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            car.waitList.append(message)
        else:
            network.addToHeap(message)

    def sendToRsu(self, rsu, message, currentTime, network, numOfPacket):
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
            numOfPacket=numOfPacket,
        )

        # Add current location to list locations of message
        # and change preReceiveFromCar of this rsu
        message.locations.append([1, rsu.id])
        rsu.preReceiveFromCar = message.currentTime

        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            rsu.waitList.append(message)
        else:
            network.addToHeap(message)

    def sendToGnb(self, gnb, message, currentTime, network, numOfPacket):
        """Simualte send message from car to gnb

        Args:
            gnb ([GnbSimulator]): [description]
            message ([Message]): [description]
            currentTime ([float]): [description]
            network ([Network]): [description]
        """
        # Simulate tranfer time to gnb
        self.simulateTranferTime(
            preReceive=gnb.preReceiveFromCar,
            meanTranfer=Config.carGnbMeanTranfer,
            message=message,
            numOfPacket=numOfPacket,
        )

        # Add current location to list locations of message
        # and change preReceiveFromCar of gnb
        message.locations.append([2])
        gnb.preReceiveFromCar = message.currentTime

        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            gnb.waitList.append(message)
        else:
            network.addToHeap(message)

    def noChange(self, message, currentTime,network):
        message.locations.append([0, self.id])
        message.currentTime += 1
        if message.currentTime > currentTime + Config.cycleTime:
            self.waitList.append(message)
        else:
            network.addToHeap(message)

    def getPosition(self, currentTime):
        """Get the current position of the car
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
            # TODO: Viết hàm check so với deltaTime
            if message.currentTime - message.sendTime[0] >= Config.deltaTime:
                message.isDropt = True
                network.output.append(message)
            else:
                network.output.append(message)
            return
        else:
            action, nextLocation = getAction(self, message, currentTime, network)
            # 0: sendToCar, 1:sendToRsu, 2: sendToGnb, 3:noChange
            if action != 3:
                self.transferredNumMessage += 1
                self.currentNumMessage = self.numMessage - self.transferredNumMessage + self.receivedNumMessage

            if action == 0:
                # numOfPacket: send and receive (2)
                self.sendToCar(nextLocation, message, currentTime, network, numOfPacket=2)
            elif action == 1:
                # numOfPacket: only send (receive simulate in RSU)
                self.sendToRsu(nextLocation, message, currentTime, network, numOfPacket=1)
            elif action == 2:
                self.sendToGnb(nextLocation, message, currentTime, network, numOfPacket=1)
            else:
                self.noChange(message, currentTime, network)