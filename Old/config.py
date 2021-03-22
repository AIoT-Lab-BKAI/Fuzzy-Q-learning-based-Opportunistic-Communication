import datetime


class Config:
    # Current date time
    current_date_and_time = datetime.datetime.now()
    current_date_and_time_string = str(current_date_and_time)

    # gnb config
    gnbProcessPerSecond = 1280
    gnbCarMeanTranfer = 0.0009765625

    # rsu config
    rsuNumbers = 6
    xList = [125, 375, 625, 875, 1125, 1375]
    yList = [1, 1, 1, 1, 1, 1]
    zList = [10, 10, 10, 10, 10, 10]
    rsuCoverRadius = 151

    rsuProcessPerSecond = 320

    rsuRsuMeanTranfer = 0.00001
    rsuCarMeanTranfer = 0.0004768371582
    rsuGnbMeanTranfer = 0.00004768371582

    # car config
    carSpeed = 12
    carCoverRadius = 70
    carProcessPerSecond = 100
    carCarMeanTranfer = 0.00001
    carRsuMeanTranfer = 0.0009765625
    carGnbMeanTranfer = 0.0004768371582

    # other
    # Chiến lược xuất hiện xe
    carAppearStrategy = "resources/car_deu5.inp"
    carPacketStrategy = "resources/poisson_70.inp"

    # simulator Time
    simTime = 50

    # Khe thời gian
    cycleTime = 1.0

    # deltaTime: thời gian ngưỡng
    deltaTime = 10

    # Độ dài của đường (hiện tại đang mô phỏng là đường thẳng)
    roadLength = 1500

    dumpDelayDetail = "results/delayDetail/" + current_date_and_time_string + ".txt"
    dumDelayGeneral = "results/delayGeneral.txt"
