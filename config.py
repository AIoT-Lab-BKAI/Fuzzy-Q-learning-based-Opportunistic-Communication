import datetime


class Config:
    # Current date time
    current_date_and_time = datetime.datetime.now()
    current_date_and_time_string = str(current_date_and_time)

    # gnb config
    gnbCarMeanTranfer = 0.0009765625

    # rsu config
    rsuNumbers = 6
    xList = [125, 375, 625, 875, 1125, 1375]
    yList = [1, 1, 1, 1, 1, 1]
    zList = [10, 10, 10, 10, 10, 10]

    rsuCoverRadius = 151

    rsuRsuMeanTranfer = 0.00001
    rsuCarMeanTranfer = 0.0004768371582
    rsuGnbMeanTranfer = 0.00004768371582

    # car and sensor config
    carSpeed = 12
    carCoverRadius = 70

    # Dung lượng tối đa của sensor trên car
    carMaxCapacity = 20

    # Tỷ lệ số gói tin truyền lên Gnb
    carGnbTranssmissionRate = 1 / 5

    carCarMeanTranfer = 0.00001
    carRsuMeanTranfer = 0.0009765625
    carGnbMeanTranfer = 0.0004768371582

    # other
    # Chiến lược xuất hiện xe và gói tin
    carAppearStrategy = "resources/car_deu5.inp"
    carPacketStrategy = "resources/packet_deu1.inp"

    # kích thước của 1 gói tin
    packetSize = 1

    # simulator Time
    simTime = 20

    # Khe thời gian
    cycleTime = 1.0

    # deltaTime: thời gian ngưỡng
    deltaTime = 10

    # Độ dài của đường (hiện tại đang mô phỏng là đường thẳng)
    roadLength = 1500

    dumpDelayDetail = "results/delayDetail/" + current_date_and_time_string + ".txt"
    dumDelayGeneral = "results/delayGeneral.txt"
