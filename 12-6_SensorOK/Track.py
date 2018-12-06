#coding:utf-8
import os
import RPi.GPIO as GPIO
import time

#######################################
#############�ź����Ŷ���##############
#######################################
GPIO.setmode(GPIO.BCM)

########���⴫�����ӿڶ���#################
IR_R = 18	#С���Ҳ�Ѳ�ߺ���
IR_L = 27	#С�����Ѳ�ߺ���

########��������ӿڶ���#################
ENA = 13	#//L298ʹ��A
ENB = 20	#//L298ʹ��B
IN1 = 19	#//����ӿ�1
IN2 = 16	#//����ӿ�2
IN3 = 21	#//����ӿ�3
IN4 = 26	#//����ӿ�4

#########�ܽ��������ü���ʼ��##########
GPIO.setwarnings(False)

#########�����ʼ��ΪLOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)

#########�����ʼ��Ϊ���룬���ڲ�����#########
GPIO.setup(IR_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#########������ǰ������##########
def Motor_Forward():
	print 'motor forward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
#########���������˺���##########
def Motor_Backward():
	print 'motor_backward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
#########��������ת����##########
def Motor_TurnLeft():
	print 'motor_turnleft'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
#########��������ת����##########
def Motor_TurnRight():
	print 'motor_turnright'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
#########������ֹͣ����##########
def Motor_Stop():
	print 'motor stop'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)

####################################################
##�������� TrackLine()
##�������� Ѳ����ģʽ
##��ڲ��� ����
##���ڲ��� ����
####################################################
def TrackLine():
	if (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == False): #����Ϊ�ߣ�����Ϊ��
		Motor_Forward()
		return
	elif (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == True):
		Motor_TurnRight()
		return
	elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == False):
		Motor_TurnLeft()
		return
	elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == True): #���඼��������
		Motor_Stop()
		return

while True:
	TrackLine()