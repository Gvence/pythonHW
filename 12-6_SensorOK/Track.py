#coding:utf-8
import os
import RPi.GPIO as GPIO
import time

#######################################
#############信号引脚定义##############
#######################################
GPIO.setmode(GPIO.BCM)

########红外传感器接口定义#################
IR_R = 18	#小车右侧巡线红外
IR_L = 27	#小车左侧巡线红外

########电机驱动接口定义#################
ENA = 13	#//L298使能A
ENB = 20	#//L298使能B
IN1 = 19	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 21	#//电机接口3
IN4 = 26	#//电机接口4

#########管脚类型设置及初始化##########
GPIO.setwarnings(False)

#########电机初始化为LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)

#########红外初始化为输入，并内部拉高#########
GPIO.setup(IR_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#########电机电机前进函数##########
def Motor_Forward():
	print 'motor forward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
#########电机电机后退函数##########
def Motor_Backward():
	print 'motor_backward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
#########电机电机左转函数##########
def Motor_TurnLeft():
	print 'motor_turnleft'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
#########电机电机右转函数##########
def Motor_TurnRight():
	print 'motor_turnright'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
#########电机电机停止函数##########
def Motor_Stop():
	print 'motor stop'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)

####################################################
##函数名称 TrackLine()
##函数功能 巡黑线模式
##入口参数 ：无
##出口参数 ：无
####################################################
def TrackLine():
	if (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == False): #黑线为高，地面为低
		Motor_Forward()
		return
	elif (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == True):
		Motor_TurnRight()
		return
	elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == False):
		Motor_TurnLeft()
		return
	elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == True): #两侧都碰到黑线
		Motor_Stop()
		return

while True:
	TrackLine()