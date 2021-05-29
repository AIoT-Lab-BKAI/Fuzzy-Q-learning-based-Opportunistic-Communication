from queue import PriorityQueue
from utils import PrioritizedItem
from config import Config
from network_method import dumpOutputPerCycle, dumpOutputFinal, dumpOutputPerHour


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
            # Check car not in network
            if (car_.endTime - Config.simStartTime) / 60 < currentTime or \
                    (car_.startTime - Config.simStartTime) / 60 > currentTime or car_.id == car.id:
                continue
            distence = car.distanceToCar(car_, currentTime)
            if distence < Config.carCoverRadius:
                car.neighborCars.append(car_)

        # Set neighbor RSU
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

    # Network run
    def run(self):
        currentTime = 0
        while (currentTime < Config.simTime):
            self.working(currentTime)
            self.dumpOutputPerCycle(currentTime)
            currentTime += Config.cycleTime
            print("-" * 80)
            print("Current Time: ", currentTime)
            print("Total package: ", self.countDone + self.countDropt)
            print("Done package: ", self.countDone)
            print("Delay package: ", self.countDropt)
            print("Can't generate: ", self.countPacketFail)
            totalCountCar, totalCountRsu, totalCountGnb = 0, 0, 0
            for car in self.carList:
                totalCountRsu += car.cntSendToRsu
                totalCountGnb += car.cntSendToGnb

                if (car.endTime - Config.simStartTime) / 60 < currentTime or \
                        (car.startTime - Config.simStartTime) / 60 > currentTime:
                    continue
                else:
                    car.timeInSimulator += Config.cycleTime
                    if car.timeInSimulator < 480:
                        car.optimizer.policy_parameters = {"epsilon": 0.15}
                    elif car.timeInSimulator < 960:
                        car.optimizer.policy_parameters = {"epsilon": 0.12}
                    elif car.timeInSimulator < 1440:
                        car.optimizer.policy_parameters = {"epsilon": 0.09}
                    elif car.timeInSimulator < 1920:
                        car.optimizer.policy_parameters = {"epsilon": 0.06}
                    else:
                        car.optimizer.policy_parameters = {"epsilon": 0.03}

            print("-> RSU: ", totalCountRsu)
            print("-> Gnb: ", totalCountGnb)

            if currentTime % 60 == 0:
                self.dumpOutputPerHour(currentTime)

        self.dumpOutputFinal()

    # Save result
    def dumpOutputPerCycle(self, currentTime, func=dumpOutputPerCycle):
        func(self, currentTime)

    def dumpOutputFinal(self, func=dumpOutputFinal):
        func(self)

    def dumpOutputPerHour(self, currentTime, func=dumpOutputPerHour):
        func(self, currentTime)
