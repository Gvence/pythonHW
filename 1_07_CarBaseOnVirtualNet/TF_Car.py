import socket
from multiprocessing import Process
import matplotlib.pyplot as plt
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import numpy as np
import sys
import tty,termios
import time
import tensorflow as tf
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
    #train.save()
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
    plt.pause(0.05)
    plt.savefig('scores.png')
    print("saving brain...")



def load():
    print("loading last saved brain...")
    #train.load()

def getCarState(recivedata):
    DATA = int(recivedata)
    distance = int(DATA / 1000)
    leftSignal = int((DATA % 1000) / 100)
    rightSignal = int((DATA % 100) / 10)
    middleSignal = int((DATA % 10))
    return [ leftSignal, middleSignal, rightSignal, distance, action]

def getReward(sensorResult):
    global last_dis
    global last_action
    if sensorResult[0] == 0 and sensorResult[1] == 0 and sensorResult[2] == 0:
        reward = 0.2
    else:
        reward = -1
    if sensorResult[3] < last_dis :
        reward += 1
    else:
        reward -= 1
    if sensorResult[3] <= 15 :#or sensorResult[3] >= 260 :
        reward -= 1
    if (last_action == action ) and (last_action == np.array([0])  or last_action == np.array([2])):
        reward  -= 0.2
    last_action = action
    last_dis = sensorResult[3]
    return reward
def getSensorResult(Status, Act):
    inputAct = (Act - 0.98)/2
    print('inputAct:', inputAct)
    #print('Status:', Status)
    xData = np.hstack([Status, inputAct])
    #print('xData:', xData.reshape((1,5)))
    predict = sess.run(prediction, feed_dict={x:xData.reshape((1,5))})
    #print('predict:',predict)
    SensorL_Val = round(predict[0][0] + SL[2])
    SensorM_Val = round(predict[0][1] + SM[2])
    SensorR_Val = round(predict[0][2] + SR[2])
    DisSensor_Val = round(predict[0][3]*(Dis[0] - Dis[1]) + Dis[2])
    return predict, [SensorL_Val, SensorM_Val, SensorR_Val, DisSensor_Val, int(Act)]
def learnCarState():
    global action
    global Time
    global iteration
    global ITE
    global scores
    global sensorResult
    global i
    global sess
    global x
    global prediction
    global Status
    meta_path = 'model/MODEL-1000.meta'
    model_path = 'model/'
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.7)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
    init = tf.initialize_all_variables()
    sess.run(init)
    saver = tf.train.import_meta_graph(meta_path)
    saver.restore(sess, tf.train.latest_checkpoint(model_path))
    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name('X_INPUT:0')
    prediction = graph.get_tensor_by_name('predict:0')
    while True:
        iteration += 1
        i += 1
        # if iteration == 8 :
        #     s.sendto((ACTION[action] + Time).encode("utf-8"), address)
        #     iteration = 0
        # print('%s send:' % Time, ACTION[action])
        # recivedata, addrg = s.recvfrom(2048)
        # sensorResult = getCarState(recivedata.decode())
        predict, sensorResult = getSensorResult(Status, action)
        Status = predict[0, 0:4]
        print('sensorResult:', sensorResult)
        reward = getReward(sensorResult)
        action = train.update(reward, sensorResult).numpy()
        print(action)
        Time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        recordfile = open('PCRecord.txt', 'a')
        recordfile.write('%s:' % Time + '\t' + str(sensorResult[0]) + '\t\t' + str(sensorResult[1]) + '\t\t' + str(sensorResult[2])\
                         + '\t\t''' + str(sensorResult[3]) + '\t\t' + '%.2f' % reward + '\t\t' + str(action) + '\n')
        recordfile.close()
        if i%50 == 0 :
            scores.append(train.score())
            ITE.append(i)
            save()
        time.sleep(1)

if __name__ == '__main__':
        DataFeature = np.loadtxt('Data.txt')
        SL = DataFeature[0, :]
        SM = DataFeature[1, :]
        SR = DataFeature[2, :]
        Dis = DataFeature[3, :]
        Act = DataFeature[4, :]
        print(Dis,   Act)

        # address = ('192.168.43.166', 6666)  # server_IP
        # readdr = ('192.168.43.76', 6666)  # PC_IP
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind(readdr)
        sensorResult = [0,0,0,100,0]
        reward = 0
        last_dis = 100
        Status = [-0.5, -0.5, -0.5, 0.2]
        action = train.update(reward, sensorResult).numpy()
        last_action = action
        Time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        recordfile = open('PCRecord.txt', 'w')
        recordfile.write( '_________\t' + 'L_Sen' + '\t' + 'M_Sen' + '\t' + 'R_Sen' \
            + '\t' + 'Dis' + '\t\t' + 'Rew' + '\t\t\t' + 'Act' + '\n')
        recordfile.close()
        recivedata = '0'.encode()
        iteration = 0
        i = 0
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

