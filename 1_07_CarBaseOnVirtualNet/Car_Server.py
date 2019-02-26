#coding:utf-8

import os
from multiprocessing import Process
import sys
import tty,termios
import time
import RPi.GPIO as GPIO
import socket
replyData = 0
recivedata = 0
Time = 0
t1 = 0
qt2 = 0
velocity = 0.02
revelocity = 0.03


#############信号引脚定义##############
GPIO.setmode(GPIO.BCM)

#########红外线管脚#############
IR_R = 18
IR_L = 27
IR_M = 22

########电机驱动接口定义#################
ENA = 13	#//L298使能A
ENB = 20	#//L298使能B
IN1 = 19	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 21	#//电机接口3
IN4 = 26	#//电机接口4

########超声波接口定义#################
ECHO_1 = 4	#超声波1接收脚位
TRIG_1 = 17	#超声波1发射脚位

ECHO_2 = 14	#超声波2接收脚位
TRIG_2 = 15	#超声波2发射脚位
#########管脚类型设置及初始化##########
GPIO.setwarnings(False)
#########电机初始化为LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)

GPIO.setup(IR_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_M,GPIO.IN,pull_up_down=GPIO.PUD_UP)

##########超声波模块管脚类型设置#########
GPIO.setup(TRIG_1,GPIO.OUT,initial=GPIO.LOW)#超声波模块发射端管脚设置trig
GPIO.setup(ECHO_1,GPIO.IN,pull_up_down=GPIO.PUD_UP)#超声波模块接收端管脚设置echo
GPIO.setup(TRIG_2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO_2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#########电机电机前进函数##########

run =True
def Motor_TurnRight():
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
#########电机电机后退函数##########
def Motor_TurnLeft():
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
#########电机电机左转函数##########
def Motor_Backward():
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
#########电机电机右转函数##########
def Motor_Forward():
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
#########电机电机停止函数##########
def Motor_Stop():
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)

####################################################
##函数名称 ：Get_Distence()
##函数功能 超声波测距，返回距离（单位是厘米）
##入口参数 ：无
##出口参数 ：无
####################################################
def	Get_Distance(DisSensor):
	if DisSensor == 1:
		GPIO_TR = TRIG_1
		GPIO_EC = ECHO_1
	if DisSensor == 2:
		GPIO_TR = TRIG_2
		GPIO_EC = ECHO_2
	time.sleep(0.01)
	GPIO.output(GPIO_TR,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(GPIO_TR,GPIO.LOW)
	while not GPIO.input(GPIO_EC):
				pass
	t1 = time.time()
	while GPIO.input(GPIO_EC):
				pass
	t2 = time.time()
	Distence = (t2-t1)*340/2*100
	time.sleep(0.01)
	if Distence>300:
		return 0
	else:
		return Distence

def move(ch):
	if ch == 'w':
			Motor_Stop()
			time.sleep(revelocity)
			Motor_Forward()
			time.sleep(velocity)
			Motor_Stop()
			time.sleep(revelocity)
			Motor_Forward()
			time.sleep(velocity)
			Motor_Stop()
			time.sleep(revelocity)
			Motor_Forward()
			time.sleep(velocity)
			Motor_Stop()
			time.sleep(revelocity)
			Motor_Forward()
			time.sleep(velocity)

	elif ch == 'a':
			Motor_Stop()
			time.sleep(revelocity)
			Motor_TurnLeft()
			time.sleep(velocity)
			Motor_Stop()
			time.sleep(revelocity)
			Motor_TurnLeft()
			time.sleep(velocity)
			Motor_Stop()
			time.sleep(revelocity)
			Motor_TurnLeft()
			time.sleep(velocity)
			Motor_Stop()
			time.sleep(revelocity)
			Motor_TurnLeft()
			time.sleep(velocity)

	elif ch == 'd':
			Motor_Stop()
			time.sleep(revelocity)
			Motor_TurnRight()
			time.sleep(velocity)
			Motor_Stop()
			time.sleep(revelocity)
			Motor_TurnRight()
			time.sleep(velocity)
			Motor_Stop()
			time.sleep(revelocity)
			Motor_TurnRight()
			time.sleep(velocity)
			Motor_Stop()
			time.sleep(revelocity)
			Motor_TurnRight()
			time.sleep(velocity)
def getSensorSignal():
	if GPIO.input(IR_L) == False:
		leftSensor = 0
	else :
		leftSensor = 1
	if GPIO.input(IR_R) == False:
		rightSensor = 0
	else:
		rightSensor = 1
	if GPIO.input(IR_M) == False:
		midSensor = 0
	else:
		midSensor = 1
	return [leftSensor, rightSensor, midSensor]
def sendCarState():
	global SensorSiginal
	global distance
	while True:
		distance_1 = int(Get_Distance(1))
		distance_2 = int(Get_Distance(2))
		SensorSiginal = getSensorSignal()
		replyData = distance_1 * 10000 + distance_2 * 1000 + 100 * SensorSiginal[0] + 10 * SensorSiginal[1] + SensorSiginal[2]
		s.sendto(str(replyData).encode("utf-8"), readdr)
		print('TIME:', Time, 'distance_1 : %s \n distance_2 : %s'%(distance_1, distance_2))
		time.sleep(0.2)


def reciveCommand():
	global recivedata
	global Time
	while True:
		recivedata, addr = s.recvfrom(2048)
		data = recivedata.decode()
		Time = data[1:]
		data = data[0]
		move(data)
		# if SensorSiginal[0] == 1:
		# 	Motor_TurnRight()
		# elif SensorSiginal[1] == 1:
		# 	Motor_TurnLeft()
		# elif SensorSiginal[2] == 1:
		# 	Motor_Backward()
		# recordfile = open('serverRecord.txt', 'a')
		# recordfile.write('%s action:' % Time + str(data) + '\n')
		# print('%s action:' % Time, data, '\n')
		# recordfile.close()
		# time.sleep(0.1)

if __name__ == '__main__':
	try :
		address = ('192.168.43.166', 6666)  # server_IP
		readdr = ('192.168.43.76', 6666)  # PC_IP
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(address)
		recordfile = open('serverRecord.txt','w')
		recordfile.close()
		print('car ready!!')
		threads = []
		reciveCommandThread = Process(target = reciveCommand)
		sendCarStateThread = Process(target = sendCarState)
		reciveCommandThread.start()
		sendCarStateThread.start()
		threads.append(reciveCommandThread)
		threads.append(sendCarStateThread)
		for t in threads:
			t.join()
	except:
		print('Child process end')
		s.close()
