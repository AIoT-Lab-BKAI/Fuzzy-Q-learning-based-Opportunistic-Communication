import datetime


class Config:
    # Current date time
    current_date_and_time = datetime.datetime.now()
    current_date_and_time_string = str(current_date_and_time)

    # gnb config
    gnbCarMeanTranfer = 0.0009765625

    # rsu config
    rsuNumbers = None
    rsuPath = "resources/cityData/newRSU.csv"

    rsuCoverRadius = 350
    # TODO:
    rsuRsuMeanTranfer = 0.00001
    rsuCarMeanTranfer = 0.0004768371582
    rsuGnbMeanTranfer = 0.00004768371582

    # car and sensor config
    carMaxCapacity = "resources/capacity10_30.inp"

    carCoverRadius = 120
    carCarMeanTranfer = 0.00001
    carRsuMeanTranfer = 0.0009765625
    carGnbMeanTranfer = 0.0004768371582

    nActionsCar = 4
    nStatesCar = 1000  # TODO
    policyParamatersCar = {"epsilon": 0.1}
    disCountingFactorCar = 0.9
    learningRateCar = 0.01

    # other
    carData = "resources/cityData/dataDay11_240.csv"
    carPacketStrategy = "resources/packet_deu1.inp"
    carQTablePath = "results/carQTableDay1.pkl"

    packetSize = 1
    # simulator Time
    simStartTime = None
    simTime = 1000
    cycleTime = 1
    # deltaTime
    #
    deltaTime = 10
    # Thời gian trễ gói tin (nếu không truyền) => Sang lần xử lý tiếp theo
    delayPacketTime = 1

    dumpDelayDetail = "results/detail/" + current_date_and_time_string + ".txt"
    dumDelayGeneral = "results/general.txt"
