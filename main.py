from network import Network
from carSimulator import CarSimulator
from rsuSimulator import RsuSimulator
from gnbSimulator import GnbSimulator
from config import Config
from optimizers.q_learning import CarQLearning
import pandas as pd
import numpy as np
import ast


def main():
    gnb = GnbSimulator()

    print("-" * 50)
    rsuList = getRsuList()
    print("RSU length: ", len(rsuList))

    carList = carAppear()
    print("Car length: ", len(carList))

    listTimeMessages = prepareTimeMessages()
    print("Message length: ", len(listTimeMessages))
    print("-" * 50)

    network = Network(
        gnb=gnb,
        rsuList=rsuList,
        carList=carList,
        listTimeMessages=listTimeMessages
    )

    network.run()


# Generate RSU
def getRsuList():
    global rsuData
    try:
        rsuData = pd.read_csv(Config.rsuPath)
    except:
        print("RSU file not found")
        exit()
    res = []
    rsu_x, rsu_y = rsuData['x'].values, rsuData['y'].values
    index = 0
    for x, y in zip(rsu_x, rsu_y):
        rsu = RsuSimulator(
            id=index,
            xcord=x,
            ycord=y,
            zcord=1
        )
        res.append(rsu)
        index += 1
    Config.rsuNumbers = len(res)
    return res


def carCapacity():
    try:
        f = open(Config.carMaxCapacity, "r")
    except:
        print("File carCapacity not found")
        exit()
    res = []
    for x in f:
        tmp = int(x)
        res.append(tmp)
    return res


# Generate Sensor on Car
def carAppear():
    global data, carQTable
    carMaxCapacity = carCapacity()
    try:
        data = pd.read_csv(Config.carData)
        carQTable = pd.read_csv(Config.carQTablePath)
    except:
        print('Read data failed!')
        exit()
    carQTableDict = carQTable.set_index('CarID')['QTable'].to_dict()

    carTime = data.sort_values(['Time']).groupby('CarID').head(1)[['CarID', 'Time']]
    carID = carTime['CarID'].values
    Config.simStartTime = int(carTime[carTime['CarID'] == carID[0]]['Time'].values)

    startTime = carTime.groupby('CarID')['Time'].apply(int).to_dict()
    endTime = data.sort_values(['Time']).groupby('CarID').tail(1)[['CarID', 'Time']].groupby('CarID')['Time'].apply(
        int).to_dict()

    res = []

    carIDNetwork = 0
    for id in carID:
        if startTime[id] - Config.simStartTime > 60 * Config.simTime:
            break
        timeLocation = data[data['CarID'] == id].groupby('Time')[['Xcord', 'Ycord']].apply(
            lambda g: list(map(tuple, g.values.tolist()))).to_dict()

        car = CarSimulator(carIDNetwork=carIDNetwork, carID=id, startTime=startTime[id], endTime=endTime[id],
                           carMaxCapacity=10, timeLocation=timeLocation)
        optimizer = CarQLearning(car=car)
        car.optimizer = optimizer

        """
        Read infor from QTable Dict
        """
        if id in carQTableDict:
            qTable = np.array(ast.literal_eval(carQTableDict[id]))
            car.optimizer.QTable = qTable

        res.append(car)
        carIDNetwork += 1
        print(car.optimizer.QTable)

    return res


# Time Messages
def prepareTimeMessages():
    try:
        f = open(Config.carPacketStrategy, "r")
    except:
        print("File packet not found !!!")
        exit()
    currentTime = 0
    res = []
    for x in f:
        tmp = float(x)
        timeStartFromCar = currentTime + tmp
        if timeStartFromCar > Config.simTime:
            break
        currentTime = timeStartFromCar
        res.append(timeStartFromCar)
    return res


if __name__ == "__main__":
    main()
