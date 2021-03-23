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

        # Loại bỏ dấu "_" ở cuối
        self.type = self.type[:-3]


### Test
# test = Message(indexCar=1, time=2)
# test.locations.append([1, 0])
# test.locations.append([2])
# test.locations.append([2])
# print(test.setType())
# print(test.type)
#
# test2 = Message(indexCar=3, time=4)
# print(test2.indexCar)
