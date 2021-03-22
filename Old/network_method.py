import datetime

from config import Config


def dumpOutputPerCycle(network, currentTime):
    if not network.output:
        return

    network.totalOutsize += len(network.output)
    f = open(Config.dumpDelayDetail, "w")
    for mes in network.output:
        delay = mes.currentTime - mes.sendTime[0]
        network.maxDelay = max(delay, network.maxDelay)
        if mes.isDropt:
            network.countDropt += 1
        else:
            network.meanDelay += delay
        mes.setType()

        f.write(f"{mes.sendTime[0]} \t {mes.currentTime} \t {delay} \t {mes.type} \t {network.maxDelay} \n")

    network.output = []


def dumpOutputFinal(network):
    network.meanDelay = (network.meanDelay + \
                         network.countDropt * network.maxDelay) / network.totalOutsize
    f = open(Config.dumDelayGeneral, "a")
    f.write(f"{Config.current_date_and_time_string} \t {Config.carPacketStrategy} \t {Config.carAppearStrategy} \t \
        {Config.rsuNumbers} \t {network.meanDelay} \t {network.countDropt} \t \
        {network.totalOutsize} \n")
    f.close()
    print("Done dumping final output!!!")
