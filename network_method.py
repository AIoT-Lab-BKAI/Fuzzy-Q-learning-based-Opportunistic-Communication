from config import Config


def dumpOutputPerCycle(network, currentTime):
    if not network.output:
        return

    network.totalOutsize += len(network.output)
    f = open(Config.dumpDelayDetail, "a")
    for mes in network.output:
        delay = mes.currentTime - mes.sendTime[0]

        if mes.isDropt:
            network.countDropt += 1
        else:
            network.meanDelay += delay
        mes.setType()

        f.write(
            f"{mes.stt}\t {network.countDropt} \t{mes.sendTime[0]} \t {mes.currentTime} \t {delay} \t  {mes.type}\n")
        # print(mes.indexCar, mes.receiveTime, mes.stt)
        # print(mes.sendTime)

    network.output = []


def dumpOutputFinal(network):
    # network.meanDelay = (network.meanDelay + \
    #                      network.countDropt * network.maxDelay) / network.totalOutsize
    # f = open(Config.dumDelayGeneral, "a")
    # f.write(f"{Config.current_date_and_time_string} \t {Config.carPacketStrategy} \t {Config.carAppearStrategy} \t \
    #     {Config.rsuNumbers} \t {network.meanDelay} \t {network.countDropt} \t \
    #     {network.totalOutsize} \n")
    # f.close()
    print("Done dumping final output!!!")
