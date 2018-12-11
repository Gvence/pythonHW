
import socket
import threading
import numpy as np
import sys
import tty,termios
import time
from ai import Dqn
def initSSH():
    global s
    global addr
    global readdr
    addr = ('192.168.1.102', 6666)  # server_IP
    readdr = ('192.168.1.105', 8888)  # PC_IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(readdr)

def moveCar(action, Time):
    if action == 'w' or action == 'a' or action == 'd':
        s.sendto((action + Time).encode("utf-8"), addr)
        print('%s :'%Time, 'send command:', action)
        #time.sleep(0.5)
        return 'OK'

def getCarState():
    recivedata, addrg = s.recvfrom(2048)
    if recivedata != 0:
        print("from:", addrg)
        recivedata = int(recivedata.decode())
        print("got recive :", recivedata)
        distance = int(recivedata / 1000)
        leftSignal = int((recivedata % 1000) / 100)
        rightSignal = int((recivedata % 100) / 10)
        middleSignal = int((recivedata % 10))
        print('distance = ', distance,
              '\nleftSignal = ', leftSignal,
              '\nrightSignal = ', rightSignal,
              '\nmiddleSignal = ', middleSignal,
              )
        recivedata = 0
        return [ leftSignal, middleSignal, rightSignal, -distance, distance]

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

def updateCarState():
    global action
    sensorResult = getCarState()
    reward = getReward(sensorResult)
    action = train.update(reward, sensorResult)

class Thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("Starting " + self.name)
       # 获得锁，成功获得锁定后返回True
       # 可选的timeout参数不填时将一直阻塞直到获得锁定
       # 否则超时后将返回False
        if self.name == 'moveCarThread':
            threadLock.acquire()
            moveCar(ACTION[action], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            # 释放锁
            threadLock.release()
        elif self.name == 'updateCarStateThread':
            threadLock.acquire()
            updateCarState()
            threadLock.release()



if __name__ == '__main__':
    threadLock = threading.Lock()
    global reward
    global recivedata, addrg
    initSSH()
    ACTION = ['a', 'w', 'd']
    action = 1
    train = Dqn(5, 3, 0.9)
    threads = []
    moveCarThread = Thread(1, 'moveCarThread')
    updateCarStateThread = Thread(2, 'updateCarStateThread')
    moveCarThread.start()
    updateCarStateThread.start()

    threads.append(moveCarThread)
    threads.append(updateCarStateThread)

    for t in threads:
        t.join()
    print('Exiting Thread')
    # while True:
    #     try :
    #         moveCar(ACTION[action], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    #         sensorResult = getCarState()
    #         reward = getReward(sensorResult)
    #         action = train.update(reward, sensorResult)
    #     except :
    #         continue
    #     print('action :', ACTION[action])
    s.close()
