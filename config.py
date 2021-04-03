import datetime


class Config:
    # Current date time
    current_date_and_time = datetime.datetime.now()
    current_date_and_time_string = str(current_date_and_time)

    # gnb config
    gnbCarMeanTranfer = 0.0009765625

    # rsu config
    # rsuNumbers = 6
    # xList = [125, 375, 625, 875, 1125, 1375]
    # yList = [1, 1, 1, 1, 1, 1]
    # zList = [10, 10, 10, 10, 10, 10]

    # rsuNumbers = 5
    # xList = [250, 500, 750, 1000, 1250]
    # yList = [1, 1, 1, 1, 1]
    # zList = [10, 10, 10, 10, 10]

    # rsuNumbers = 4
    # xList = [300, 600, 900, 1200]
    # yList = [1, 1, 1, 1]
    # zList = [10, 10, 10, 10]

    rsuNumbers = 3
    xList = [375, 750, 1125]
    yList = [1, 1, 1]
    zList = [10, 10, 10]

    # rsuNumbers = 2
    # xList = [375, 1125]
    # yList = [1, 1]
    # zList = [10, 10]

    # rsuNumbers = 1
    # xList = [750]
    # yList = [1]
    # zList = [10]

    rsuCoverRadius = 151
    rsuRsuMeanTranfer = 0.00001
    rsuCarMeanTranfer = 0.0004768371582
    rsuGnbMeanTranfer = 0.00004768371582

    # car and sensor config
    carSpeed = 12
    # Dung lượng tối đa của sensor trên car
    carMaxCapacity = 20

    carCoverRadius = 70
    carCarMeanTranfer = 0.00001
    carRsuMeanTranfer = 0.0009765625
    carGnbMeanTranfer = 0.0004768371582

    nActionsCar = 4
    nStatesCar = 1000  # TODO
    policyParamatersCar = {"epsilon": 0.001}
    disCountingFactorCar = 0.9
    learningRateCar = 0.001

    # other
    # Chiến lược xuất hiện xe và gói tin
    # carAppearStrategy = "resources/car_deu5.inp"
    # carAppearStrategy = "resources/car_deu20.inp"
    carAppearStrategy = "resources/car_random_5_05.inp"
    carPacketStrategy = "resources/packet_random_02_005.inp"
    # carPacketStrategy = "resources/packet_deu02.inp"
    # carPacketStrategy = "resources/poisson_70.inp"

    # kích thước của 1 gói tin
    packetSize = 1
    # simulator Time
    simTime = 500
    # Khe thời gian
    cycleTime = 0.5
    # deltaTime: thời gian ngưỡng
    deltaTime = 3
    # Thời gian trễ gói tin (nếu không truyền) => Sang lần xử lý tiếp theo
    delayPacketTime = cycleTime
    # Độ dài của đường (hiện tại đang mô phỏng là đường thẳng)
    roadLength = 1500

    dumpDelayDetail = "results/detail/" + current_date_and_time_string + ".txt"
    dumDelayGeneral = "results/general.txt"
