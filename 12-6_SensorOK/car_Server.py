#coding:utf-8

import os
import sys
import tty,termios
import time
import RPi.GPIO as GPIO
import socket
address = ('192.168.1.100',5999)#本主机IP
readdr = ("192.168.1.105",3888)#客户端主机IP
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(address)

#############信号引脚定义##############
GPIO.setmode(GPIO.BCM)

#########管脚类型设置及初始化##########
GPIO.setwarnings(False)

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
ECHO = 4	#超声波接收脚位  
TRIG = 17	#超声波发射脚位

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
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)#超声波模块发射端管脚设置trig
GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_UP)#超声波模块接收端管脚设置echo

#########电机电机前进函数##########

run =True
def Motor_TurnRight():
	print ('turnright')
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
#########电机电机后退函数##########
def Motor_TurnLeft():
	print ('turnleft')
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
#########电机电机左转函数##########
def Motor_Backward():
	print ('backward')
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
#########电机电机右转函数##########
def Motor_Forward():
	print('forward')
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
#########电机电机停止函数##########
def Motor_Stop():
	print ('stop')
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
def	Get_Distance():
	time.sleep(0.01)
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG,GPIO.LOW)
	while not GPIO.input(ECHO):
				pass
	t1 = time.time()
	while GPIO.input(ECHO):
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
		print('forwarding')
		Motor_Forward()
	elif ch == 's':
		print('stoping')
		Motor_Stop()
	elif ch == 'a':
		print('lefting')
		Motor_TurnLeft()
	elif ch == 'd':
		print('righting')
		Motor_TurnRight()
	elif ch == 'c':
		print('server cutdown!!!')
		Motor_Stop()
	else:
		print('I don\'t what U mean')

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

if __name__ == '__main__':
	t1 = 0
	t2 = 0
	ch = 'w'
	print('car ready!!')	
	while run:
		data,addr=s.recvfrom(2048)
		if data != 0:
			print("got data from",addr)
			ch = data.decode()
			move(ch)
			data = 0
		distance = int(Get_Distance())
		SensorSiginal = getSensorSignal()
		replydata = distance * 1000 + 100 * SensorSiginal[0] + 10 * SensorSiginal[1] + SensorSiginal[2]
		s.sendto(str(replydata).encode("utf-8"), readdr)
		if ch == 'c':
			break
	s.close()

