from object import Object
from config import Config


class GnbSimulator(Object):
    def sendToCar(self, car, message, currentTime, network):
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
        )

        # Add current location to list locations of message
        # and change preReceiveFromGnb of this car
        message.locations.append(0)
        car.preReceiveFromGnb = message.currentTime

        if message.currentTime > currentTime + Config.cycleTime:
            car.waitList.append(message)
        # Add to output
        else:
            network.output.append(message)

    def process(self, message, currentTime, network):
        # Simulate process time
        self.simulateProcessTime(
            processPerSecond=Config.gnbProcessPerSecond,
            message=message,
        )

        if message.currentTime > currentTime + Config.cycleTime:
            self.waitList.append(message)
        else:
            startCar = network.carList[message.indexCar[0]]
            if startCar.getPosition(currentTime) > Config.roadLength:
                message.isDropt = True
                network.output.append(message)
            else:
                self.sendToCar(startCar, message, currentTime, network)
