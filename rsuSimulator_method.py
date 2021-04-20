import math


def distanceToCar(rsu, car, currentTime):
    carPosition = car.getPosition(currentTime)
    return math.sqrt(
        pow(carPosition[0] - rsu.xcord, 2) + pow(carPosition[1] - rsu.ycord, 2) + pow(rsu.zcord, 2)
    )
