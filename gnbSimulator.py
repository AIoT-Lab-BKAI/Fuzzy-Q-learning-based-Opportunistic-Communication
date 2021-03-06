from object import Object
from config import Config


class GnbSimulator(Object):
    def sendToCar(self, car, message, currentTime, network, numOfPacket=1):
        """Simulate send message from gnb to car

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
            preReceive=car.preReceiveFromGnb,
            meanTranfer=Config.gnbCarMeanTranfer,
            message=message,
            numOfPacket=numOfPacket
        )

        # Add current location to list locations of message
        # and change preReceiveFromGnb of this car
        message.locations.append([0, car.carID])
        car.preReceiveFromGnb = message.currentTime

        if message.currentTime > currentTime + Config.cycleTime:
            car.waitList.append(message)
        # Add to output
        else:
            network.output.append(message)

    def working(self, message, currentTime, network):
        # Simulate working time
        self.simulateSuccessTransmission(
            message=message,
        )

        finalCar = network.carList[message.indexCar[-1]]
        self.sendToCar(finalCar, message, currentTime, network, numOfPacket=1)
