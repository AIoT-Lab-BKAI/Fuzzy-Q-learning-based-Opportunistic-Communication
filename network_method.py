from config import Config


def dumpOutputPerCycle(network, currentTime, showCarInfor=False):
    if not network.output:
        return

    f = open(Config.dumpDelayDetail, "a")
    # f.write(f'*' * 100)
    f.write(f'\nCurrent time: {currentTime}\n')

    for mes in network.output:
        delay = mes.currentTime - mes.sendTime[0]

        if mes.isDropt:
            network.countDropt += 1
        else:
            network.countDone += 1
            network.meanDelay += delay
        mes.setType()

        f.write(
            f"{mes.stt}\t {network.countDropt} \t{mes.sendTime[0]} \t {mes.currentTime} \t {delay} \t  {mes.type}\n")

    if showCarInfor:
        for car in network.carList:
            f.write(
                f"{car.id} \t {car.numMessage} \t {car.currentNumMessage} \t {car.transferredNumMessage} \t "
                f"{car.receivedNumMessage} \t {car.cntSendToCar} \t {car.cntSendToRsu} \t{car.cntSendToGnb}\n")

    network.countSendGnb = 0
    network.countSendRsu = 0
    for car in network.carList:
        network.countSendGnb += car.cntSendToGnb
        network.countSendRsu += car.cntSendToRsu

    network.output = []


def dumpOutputFinal(network):
    f = open(Config.dumDelayGeneral, "a")

    totalCountCar, totalCountRsu, totalCountGnb = 0, 0, 0
    for car in network.carList:
        totalCountCar += car.cntSendToCar
        totalCountRsu += car.cntSendToRsu
        totalCountGnb += car.cntSendToGnb
    f.write(f"{Config.current_date_and_time_string} \t {Config.carPacketStrategy} \t {Config.carData} \t \
        {Config.rsuNumbers} \t {network.countDropt + network.countDone} \t{network.countPacketFail} \t {network.countDropt} \t {network.countDone} \t \
        {totalCountCar} \t {totalCountRsu} \t {totalCountGnb}\n")
    f.close()
    print("Done dumping final output!!!")
