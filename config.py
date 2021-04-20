import datetime


class Config:
    # Current date time
    current_date_and_time = datetime.datetime.now()
    current_date_and_time_string = str(current_date_and_time)

    # gnb config
    gnbCarMeanTranfer = 0.0009765625

    # rsu config
    rsuNumbers = None
    rsuPath = "resources/cityData/rsu.csv"

    rsuCoverRadius = 1000
    rsuRsuMeanTranfer = 0.00001
    rsuCarMeanTranfer = 0.0004768371582
    rsuGnbMeanTranfer = 0.00004768371582

    # car and sensor config
    carMaxCapacity = "resources/capacity10_30.inp"

    carCoverRadius = 150
    carCarMeanTranfer = 0.00001
    carRsuMeanTranfer = 0.0009765625
    carGnbMeanTranfer = 0.0004768371582

    nActionsCar = 4
    nStatesCar = 1000  # TODO
    policyParamatersCar = {"epsilon": 0.01}
    disCountingFactorCar = 0.9
    learningRateCar = 0.001

    # other
    carData = "resources/cityData/dataDay11.csv"
    carPacketStrategy = "resources/packet_deu5.inp"

    packetSize = 1
    # simulator Time
    simStartTime = None
    simTime = 800
    cycleTime = 1
    # deltaTime
    deltaTime = 5
    # Thời gian trễ gói tin (nếu không truyền) => Sang lần xử lý tiếp theo
    delayPacketTime = 1

    dumpDelayDetail = "results/detail/" + current_date_and_time_string + ".txt"
    dumDelayGeneral = "results/general.txt"
