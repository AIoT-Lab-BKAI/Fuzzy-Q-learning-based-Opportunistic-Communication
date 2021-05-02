import math
import numpy as np

from object import Object
from message import Message
from config import Config
from carSimulator_method import *
from fuzzy_inference.fuzzy_inference import FuzzyInference


class CarSimulator(Object):

    def __init__(self, carIDNetwork, carID, startTime, endTime, carMaxCapacity, timeLocation, optimizer=None):
        Object.__init__(self)
        self.id = carIDNetwork
        self.carID = carID
        self.startTime = startTime
        self.endTime = endTime
        self.timeLocation = timeLocation
        self.currentLocation = timeLocation[startTime][0]

        self.carMaxCapacity = carMaxCapacity
        self.numMessage = 0  # Total num Message
        self.transferredNumMessage = 0
        self.currentNumMessage = 0
        self.receivedNumMessage = 0

        self.cntSendToCar = 0
        self.cntSendToRsu = 0
        self.cntSendToGnb = 0

        self.optimizer = optimizer
        self.neighborCars = []
        self.neighborRsu = None

        self.fuzzyInference = FuzzyInference(self.carMaxCapacity, Config.deltaTime)

    def collectMessages(self, currentTime, listTimeMessages, network):
        """Collect the messages in waitList which have the current time
        in [currentTime, currentTime + cycleTime] and generate time from
        list time prepared

        Args:
            currentTime ([float]): [description]
            listTimeMessages ([list(float)]): [description]

        Returns:
            [list(Messages)]: [description]
        """
        # If car ins't in network
        if (self.endTime - Config.simStartTime) / 60 < currentTime:
            return []

        # Collect from waitList
        res = Object.collectMessages(self, currentTime)

        # Generate message
        if self.numMessage >= len(listTimeMessages) or self.currentNumMessage >= self.carMaxCapacity:
            # Count packet generate fail
            if self.currentNumMessage >= self.carMaxCapacity:
                network.countPacketFail += 1
            return res
        curTime = listTimeMessages[self.numMessage]

        while True:
            sendTime = (self.startTime - Config.simStartTime) / 60 + curTime
            if sendTime > currentTime + Config.cycleTime:
                return res
            mes = Message(indexCar=self.id, time=sendTime, carID=self.carID)
            res.append(mes)
            self.numMessage += 1
            self.currentNumMessage += 1

            if self.numMessage >= len(listTimeMessages) or self.currentNumMessage >= self.carMaxCapacity:
                # Count packet generate fail
                if self.currentNumMessage >= self.carMaxCapacity:
                    network.countPacketFail += 1
                return res
            curTime = listTimeMessages[self.numMessage]

        return res

    def sendToCar(self, car, message, currentTime, network, numOfPacket, delayPacketTime=Config.delayPacketTime):
        """Simualte send message from car to car

        Args:
            car ([CarSimulator]): [description]
            message ([Message]): [description]
            currentTime ([float]): [description]
            network ([Network]): [description]
        """
        # Update received num message
        car.receivedNumMessage += 1
        car.currentNumMessage += 1

        # Update time Delay in car
        message.currentTime += delayPacketTime

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
        message.locations.append([0, car.carID])
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

    def noChange(self, message, currentTime, network, delayPacketTime=Config.delayPacketTime):
        message.locations.append([0, self.carID])

        message.currentTime += delayPacketTime

        if message.currentTime - message.sendTime[0] >= Config.deltaTime:
            message.isDropt = True
            network.addToHeap(message)
        elif message.currentTime > currentTime + Config.cycleTime:
            self.waitList.append(message)
        else:
            network.addToHeap(message)

    def getPosition(self, currentTime, func=getPosition):
        return func(self, currentTime)

    def distanceToCar(self, car, currentTime, func=distanceToCar):
        return func(self, car, currentTime)

    def distanceToRsu(self, rsu, currentTime, func=distanceToRsu):
        return func(self, rsu, currentTime)

    def getNearCar(self, currentTime, network, func=getNearCar):
        return func(self, currentTime, network)

    def getNearRsu(self, currentTime, network, func=getNearRsu):
        return func(self, currentTime, network)

    def working(self, message, currentTime, network, getAction=getAction):
        if message.isDone or message.isDropt:
            if message.currentTime - message.sendTime[0] >= Config.deltaTime:
                message.isDropt = True
                network.output.append(message)
                # self.optimizer.update(message)
            else:
                network.output.append(message)
        else:
            action, nextLocation = getAction(self, message, currentTime, network)
            # 0: sendToCar, 1:sendToRsu, 2: sendToGnb, 3:noChange
            if action != 3:
                self.transferredNumMessage += 1
                self.currentNumMessage = self.numMessage - self.transferredNumMessage + self.receivedNumMessage

            if action == 0:
                # numOfPacket: send and receive (2)
                self.cntSendToCar += 1
                self.sendToCar(nextLocation, message, currentTime, network, numOfPacket=2)
                self.optimizer.update(message, nextLocation)
            elif action == 1:
                # numOfPacket: only send (receive simulate in RSU)
                self.cntSendToRsu += 1
                self.sendToRsu(nextLocation, message, currentTime, network, numOfPacket=1)
                self.optimizer.update(message)
            elif action == 2:
                self.cntSendToGnb += 1
                self.sendToGnb(nextLocation, message, currentTime, network, numOfPacket=1)
                self.optimizer.update(message)
            else:
                self.noChange(message, currentTime, network)
                self.optimizer.update(message)
