from config import Config
from utils import getNext


class Object:

    def __init__(self):
        self.waitList = []
        self.preProcess = 0.0
        self.preReceiveFromCar = 0.0
        self.preReceiveFromRsu = 0.0

    def collectMessages(self, currentTime):
        """Collect the messages in waitList which have the current time
        in [currentTime, currentTime + cycleTime]

        Args:
            currentTime ([float]): [description]

        Returns:
            [list(Message)]: [description]
        """
        tmp = self.waitList
        self.waitList = []
        res = []
        for mes in tmp:
            if mes.currentTime > currentTime + Config.cycleTime:
                self.waitList.append(mes)
            else:
                res.append(mes)
        return res

    def simulateTranferTime(self, preReceive, meanTranfer, message):
        """Simulate the transfer time from here to another object

        Args:
            preReceive ([float]): [description]
            meanTranfer ([float]): [description]
            message ([Message]): [description]
        """
        # Add currentTime to list sendTime of message
        message.sendTime.append(message.currentTime)

        # Calculate transfer time and receive time
        tranferTime = getNext(1.0 / meanTranfer)

        selectedTime = max(preReceive, message.currentTime)

        receiveTime = tranferTime + selectedTime

        # Set receive time to list receiveTime of message and change current time
        message.receiveTime.append(receiveTime)
        message.currentTime = receiveTime

    def simulateProcessTime(self, processPerSecond, message):
        """Simulate the process time

        Args:
            processPerSecond ([float]): [description]
            message ([Message]): [description]
        """
        # calculate process time
        selectedTime = max(message.currentTime, self.preProcess)
        processTime = getNext(processPerSecond)
        processedTime = selectedTime + processTime

        # Change currentTime of message and set is done
        message.currentTime = processedTime
        message.isDone = True

        # Change preprocess time of this object
        self.preProcess = processedTime
