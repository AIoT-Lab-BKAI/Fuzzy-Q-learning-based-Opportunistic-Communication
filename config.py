import datetime


class Config:
    # Current date time
    current_date_and_time = datetime.datetime.now()
    current_date_and_time_string = str(current_date_and_time)

    # gnb config
    gnbCarMeanTranfer = 0.0009765625

    # rsu config
    rsuNumbers = None
    # xList = [375, 750, 1125]
    # yList = [1, 1, 1]
    # zList = [10, 10, 10]
    rsuPath = "resources/cityData/rsu.csv"

    rsuCoverRadius = 1000
    rsuRsuMeanTranfer = 0.00001
    rsuCarMeanTranfer = 0.0004768371582
    rsuGnbMeanTranfer = 0.00004768371582

    # car and sensor config
    # carSpeed = 12
    # Dung lượng tối đa của sensor trên car
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
    # Chiến lược xuất hiện xe và gói tin
    carData = "resources/cityData/dataDay11.csv"
    # carAppearStrategy = "resources/car_random_5_05.inp"
    # carPacketStrategy = "resources/packet_random_02_005.inp"
    carPacketStrategy = "resources/packet_deu1.inp"
    # carPacketStrategy = "resources/poisson_70.inp"

    # kích thước của 1 gói tin
    packetSize = 1
    # simulator Time
    simStartTime = None
    simTime = 50
    # Khe thời gian
    cycleTime = 1
    # deltaTime: thời gian ngưỡng
    deltaTime = 5
    # Thời gian trễ gói tin (nếu không truyền) => Sang lần xử lý tiếp theo
    delayPacketTime = cycleTime / 5

    dumpDelayDetail = "results/detail/" + current_date_and_time_string + ".txt"
    dumDelayGeneral = "results/general.txt"
