#coding:utf-8

import os
import sys
import tty,termios
import time
import RPi.GPIO as GPIO
import socket
address = ('192.168.1.104',5999)#本主机IP
readdr = ("192.168.1.105",3888)#客户端主机IP
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 
s.bind(address)

#############信号引脚定义##############
GPIO.setmode(GPIO.BCM)

#########管脚类型设置及初始化##########
GPIO.setwarnings(False)

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
if __name__ == '__main__':
	t1 = 0
	t2 = 0
	print('car ready!!')	
	while run:
#		fd = sys.stdin.fileno()
#		old_settings = termios.tcgetattr(fd)
#		try:
#			tty.setraw(fd)
#			ch = sys.stdin.read(1)
#		finally:
#			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		data,addr=s.recvfrom(2048)
		print("got data from",addr)
		ch = data.decode()
		try :
			if ch == 'w':
				replydata = 'forwarding'
				Motor_Forward()
			elif ch == 's':
				replydata = 'stoping'
				Motor_Stop()
			elif ch == 'a':
				replydata = 'lefting'
				Motor_TurnLeft()
			elif ch == 'd':
				replydata = 'righting'
				Motor_TurnRight()
			elif ch == 'c':
				replydata = 'server cutdown!!!'
				Motor_Stop()
		except :
			print('I don\'t what U mean')
			pass
		print(replydata)
		s.sendto(replydata.encode("utf-8"),readdr)
		if ch == 'c':
			break
	s.close()

