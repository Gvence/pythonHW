import socket
from multiprocessing import Process
import os
import numpy as np
import sys
import tty,termios
import time
from ai import Dqn
ACTION = ['a', 'w', 'd']
train = Dqn(5, 3, 0.9)

def getCarState(recivedata):
        DATA = int(recivedata)
        distance = int(DATA / 1000)
        leftSignal = int((DATA % 1000) / 100)
        rightSignal = int((DATA % 100) / 10)
        middleSignal = int((DATA % 10))
        return [ leftSignal, middleSignal, rightSignal, distance, -distance]

def getReward(sensorResult):
    if sensorResult[0] == 1:
        reward = 0.1
    elif sensorResult[1] == 1:
        reward = 0.1
    elif sensorResult[2] == 1:
        reward = 0.1
    else:
        reward = -1
    return reward

def sendCommand():
    while True:
        # Time = str(time.strftime('%H:%M:%S', time.localtime(time.time())))
        # s.sendto((ACTION[action] + Time).encode("utf-8"), address)
        # print('send:', ACTION[action])
        time.sleep(0.5)
def learnCarState():
    global action
    global Time
    while True:
        s.sendto((ACTION[action] + Time).encode("utf-8"), address)
        print('send:', ACTION[action])
        recivedata, addrg = s.recvfrom(2048)
        sensorResult = getCarState(recivedata.decode())
        reward = getReward(sensorResult)
        action = train.update(reward, sensorResult)
        Time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        recordfile = open('PCRecord.txt', 'a')
        recordfile.write('%s:' % Time + '\t' + str(sensorResult[0]) + '\t' + str(sensorResult[1]) + '\t' + str(sensorResult[2])\
                         + '\t' + str(sensorResult[3]) + '\t' + str(reward) + '\t' + str(action) + '\n')
        #print('%s :' % Time, sensorResult[0], sensorResult[1], sensorResult[2], reward, action, '\n')
        #Time = str(time.strftime('%H:%M:%S', time.localtime(time.time())))

        recordfile.close()
        time.sleep(0.5)

if __name__ == '__main__':
    address = ('192.168.1.101', 6666)  # server_IP
    readdr = ('192.168.1.100', 6666)  # PC_IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(readdr)
    sensorResult = [0,0,0,0,0]
    reward = 0
    action = train.update(reward, sensorResult)
    Time = time.strftime('%H:%M:%S', time.localtime(time.time()))
    recordfile = open('PCRecord.txt', 'w')
    recordfile.write( '_________\t' + 'L_Sen' + '\t' + 'M_Sen' + '\t' + 'R_Sen' \
        + '\t' + 'Dis' + '\t' + 'Rew' + '\t' + 'Act' + '\n')
    recordfile.close()
    recivedata = '0'.encode()
    threads = []
    #sendCommand = Process(target = sendCommand)
    learnThread = Process(target = learnCarState)
    #sendCommand.start()
    learnThread.start()
    #threads.append(sendCommand)
    threads.append(learnThread)
    for t in threads:
        t.join()
    print('Exiting Thread')
    s.close()
