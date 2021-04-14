from queue import PriorityQueue
from utils import PrioritizedItem
from config import Config
from network_method import dumpOutputPerCycle, dumpOutputFinal


class Network:
    def __init__(self, gnb, rsuList, carList, listTimeMessages):
        self.gnb = gnb
        self.rsuList = rsuList
        self.carList = carList
        self.listTimeMessages = listTimeMessages
        self.q = PriorityQueue()
        self.output = []
        self.meanDelay = 0.0

        self.countDone = 0
        self.countDropt = 0
        self.countSendGnb = 0
        self.countSendRsu = 0
        self.countPacketFail = 0

    def collectMessages(self, currentTime):
        res = []
        for car in self.carList:
            res.append(car.collectMessages(
                currentTime, self.listTimeMessages, self))

        # for car in self.carList:
        #     print(car.id, car.numMessage, car.currentNumMessage, car.transferredNumMessage, car.receivedNumMessage)

        for rsu in self.rsuList:
            res.append(rsu.collectMessages(currentTime))
        res.append(self.gnb.collectMessages(currentTime))

        res = [i for sublist in res for i in sublist]

        for mes in res:
            self.addToHeap(mes)

    def addToHeap(self, message):
        self.q.put(PrioritizedItem(
            priority=(message.currentTime, message.stt),
            item=message))

    def setNeighborCar(self, car, currentTime):
        # Set neighbor Car
        car.neighborCars = []
        for car_ in self.carList:
            if car_.getPosition(currentTime) > Config.roadLength \
                    or car_.startTime > currentTime or car_.id == car.id:
                continue
            distence = car.distanceToCar(car_, currentTime)
            if distence < Config.carCoverRadius:
                car.neighborCars.append(car_)

        # Set neighbor RSU
        # TODO: có thể chuyển về lấy RANDOM RSU - NOT
        minDistance = Config.rsuCoverRadius
        neighborRsu = None
        for rsu in self.rsuList:
            distance = car.distanceToRsu(rsu, currentTime)
            if distance < minDistance:
                minDistance = distance
                neighborRsu = rsu
        car.neighborRsu = neighborRsu

    def working(self, currentTime):
        #  Set neighbor list of this car
        for car in self.carList:
            self.setNeighborCar(car, currentTime)

        self.collectMessages(currentTime)
        while not self.q.empty():
            mes = self.q.get().item
            currentLocation = mes.locations[-1][0]
            if currentLocation == 0:
                car = self.carList[mes.indexCar[-1]]
                if car.getPosition(currentTime) > Config.roadLength / 2:
                    car.optimizer.parameters = {"epsilon": 0.001}
                car.working(
                    message=mes,
                    currentTime=currentTime,
                    network=self,
                )
            elif currentLocation == 1:
                rsu = self.rsuList[mes.indexRsu[-1]]
                rsu.working(mes, currentTime, self)
            else:
                self.gnb.working(mes, currentTime, self)

    # Hàm chạy của mạng
    def run(self):
        currentTime = 0
        while (currentTime < Config.simTime):
            self.working(currentTime)
            self.dumpOutputPerCycle(currentTime)
            currentTime += Config.cycleTime
            print("Current Time: ", currentTime)
        self.dumpOutputFinal()

    # Lưu thông tin kết quả
    def dumpOutputPerCycle(self, currentTime, func=dumpOutputPerCycle):
        func(self, currentTime)

    def dumpOutputFinal(self, func=dumpOutputFinal):
        func(self)
