from config import Config
from utils import getNext


class Object:

    def __init__(self):
        self.waitList = []
        self.preReceiveFromCar = 0.0
        self.preReceiveFromRsu = 0.0
        self.preReceiveFromGnb = 0.0
        self.meanDelay = 0.0

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

    def simulateTranferTime(self, preReceive, meanTranfer, message, numOfPacket=1):
        """Simulate the tranfer time from here to another object

        Args:
            preReceive ([float]): [description]
            meanTranfer ([float]): [description]
            message ([Message]): [description]
            numOfPacket ([int]): số lượng Packet truyền
        """
        # Add currentTime to list sendTime of message
        message.sendTime.append(message.currentTime)

        #  calculate tranfer time and receive time
        tranferTime = getNext(1.0 / meanTranfer) * message.packetSize * numOfPacket
        selectedTime = max(preReceive, message.currentTime)
        receiveTime = tranferTime + selectedTime

        # Set receive time to list receiveTime of message and change current time
        message.receiveTime.append(receiveTime)
        message.currentTime = receiveTime

    def simulateSuccessTransmission(self, message):
        """
        Successful transmission confirmation simulation

        :param message:
        :return:
        """
        message.isDone = True
