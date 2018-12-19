import socket
from multiprocessing import Process
import matplotlib.pyplot as plt
import os
import numpy as np
import sys
import tty,termios
import time
from ai import Dqn

ACTION = ['a', 'w', 'd']
train = Dqn(5, 3, 0.9)
scores = []
ITE = []
lines = []
fig = plt.figure(1, figsize=(10, 8), dpi=120)
ax = fig.add_subplot(1, 1, 1)
plt.ion()  # 使图标实时显示
plt.show()
plt.xlabel('iteration')
plt.ylabel('scores')
plt.title('ScoreResult')
def save():
    train.save()
    global scores
    global ITE
    global iteration
    global lines
    global ax
    try :
        ax.lines.remove(lines[0])
    except Exception:
        pass
    lines = ax.plot(ITE, scores, 'r-', lw = 3)
    plt.savefig('scores.png')
    print("saving brain...")



def load():
    print("loading last saved brain...")
    train.load()

def getCarState(recivedata):
    DATA = int(recivedata)
    distance = int(DATA / 1000)
    leftSignal = int((DATA % 1000) / 100)
    rightSignal = int((DATA % 100) / 10)
    middleSignal = int((DATA % 10))
    return [ leftSignal, middleSignal, rightSignal, distance, -distance]

def getReward(sensorResult):
    global last_dis
    if sensorResult[0] == 0 and sensorResult[1] == 0 and sensorResult[2] == 0:
        reward = 0.1
    else:
        reward = -1
    # if sensorResult[3] < last_dis :
    #     reward = 0.1
    if sensorResult[3] <= 15 or sensorResult[3] >= 100 :
        reward = -1
    last_dis = sensorResult[3]
    return reward

def learnCarState():
    global action
    global Time
    global iteration
    global ITE
    global scores
    while True:
        s.sendto((ACTION[action] + Time).encode("utf-8"), address)
        print('%s send:' % Time, ACTION[action])
        recivedata, addrg = s.recvfrom(2048)
        sensorResult = getCarState(recivedata.decode())
        reward = getReward(sensorResult)
        action = train.update(reward, sensorResult).numpy()
        Time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        recordfile = open('PCRecord.txt', 'a')
        recordfile.write('%s:' % Time + '\t' + str(sensorResult[0]) + '\t\t' + str(sensorResult[1]) + '\t\t' + str(sensorResult[2])\
                         + '\t\t''' + str(sensorResult[3]) + '\t' + str(reward) + '\t' + str(action) + '\n')
        recordfile.close()
        iteration += 1
        if iteration%200 == 0 :
            scores.append(train.score())
            ITE.append(iteration)
            save()
        time.sleep(0.5)

if __name__ == '__main__':
    try :
        address = ('192.168.43.166', 6666)  # server_IP
        readdr = ('192.168.43.76', 6666)  # PC_IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(readdr)
        sensorResult = [0,0,0,0,0]
        reward = 0
        last_dis = 100
        action = train.update(reward, sensorResult)
        Time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        recordfile = open('PCRecord.txt', 'w')
        recordfile.write( '_________\t' + 'L_Sen' + '\t' + 'M_Sen' + '\t' + 'R_Sen' \
            + '\t' + 'Dis' + '\t' + 'Rew' + '\t' + 'Act' + '\n')
        recordfile.close()
        recivedata = '0'.encode()
        iteration = 0
        try:
            load()
        except:
            pass
        threads = []
        learnThread = Process(target = learnCarState)
        learnThread.start()
        threads.append(learnThread)
        for t in threads:
            t.join()
    except :
        save()
        s.close()
        plt.ioff()
        print('exit....')

