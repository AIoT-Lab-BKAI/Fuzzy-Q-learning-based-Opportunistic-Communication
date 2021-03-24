from config import Config


class Message:
    cnt = 0

    def __init__(self, indexCar, time, packetSize=Config.packetSize):
        self.stt = Message.cnt  # Stt của gói tin
        Message.cnt += 1
        self.packetSize = packetSize
        self.indexCar = [indexCar]
        self.indexRsu = []
        self.sendTime = [time]
        self.receiveTime = []
        self.locations = [[0, indexCar]]  # locations 0: sensor, 1:rsu, 2:gnb
        self.currentTime = time
        self.isDone = False
        self.isDropt = False
        self.type = ""

    def setType(self):
        for location in self.locations:
            if location[0] == 0:
                self.type += "sensor_" + str(location[1]) + " -> "
            elif location[0] == 1:
                self.type += "rsu_" + str(location[1]) + " -> "
            else:
                self.type += "gnb" + " -> "

        # Loại bỏ dấu "-> " ở cuối
        # self.type = self.type[:-3]
        if self.isDropt == True:
            self.type += "Failure"
        else:
            self.type += "Success"
