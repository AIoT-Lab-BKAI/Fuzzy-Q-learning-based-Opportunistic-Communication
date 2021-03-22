class Message:
    cnt = 0

    def __init__(self, indexCar, time):
        self.stt = Message.cnt
        Message.cnt += 1
        self.indexCar = [indexCar]
        self.indexRsu = []
        self.sendTime = [time]
        self.receiveTime = []
        self.locations = [0]  # locations 0: car, 1:rsu, 2:gnb
        self.currentTime = time
        self.isDone = False
        self.isDropt = False
        self.type = ""

    def setType(self):
        for location in self.locations:
            if location == 0:
                self.type += "sensor_"
            elif location == 1:
                self.type += "rsu_"
            else:
                self.type += "gnb_"

        # Loại bỏ dấu "_" ở cuối
        self.type = self.type[:-1]
