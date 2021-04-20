from object import Object
from config import Config
from rsuSimulator_method import distanceToCar


class RsuSimulator(Object):

    def __init__(self, id, xcord, ycord, zcord):
        Object.__init__(self)
        self.id = id
        self.xcord = xcord
        self.ycord = ycord
        self.zcord = zcord
        self.nearRsuList = []

    def sendToCar(self, car, message, currentTime, network, numOfPacket=1):
        """Simualte send message from rsu to car

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
            preReceive=car.preReceiveFromRsu,
            meanTranfer=Config.rsuCarMeanTranfer,
            message=message,
            numOfPacket=numOfPacket
        )

        # Add current location to list locations of message
        # and change preReceiveFromRsu of this car
        message.locations.append([0, car.id])
        car.preReceiveFromRsu = message.currentTime

        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            car.waitList.append(message)
        else:
            network.addToHeap(message)

    def distanceToCar(self, car, currentTime, func=distanceToCar):
        return func(self, car, currentTime)

    def working(self, message, currentTime, network):

        # Always message.isDone
        self.simulateSuccessTransmission(
            message=message,
        )

        finalCar = network.carList[message.indexCar[-1]]
        self.sendToCar(finalCar, message, currentTime, network, numOfPacket=1)
