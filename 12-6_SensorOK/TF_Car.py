import socket
import sys
import tty,termios
import time
addr = ('192.168.1.100',5999)#从机IP
readdr = ('192.168.1.105',3888)#本主机IP
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind(readdr)
if __name__ == '__main__':
	data = 'd'
	action = 'right'
	_action = 'forward'
	while True:
		# fd = sys.stdin.fileno()
		# old_settings = termios.tcgetattr(fd)
		# try :
		# 	tty.setraw(fd)
		# 	data = sys.stdin.read(1)
		# finally:
		# 	termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		if data == 'w':
			action = 'forward'
		elif data == 's':
			action = 'stop'
		elif data == 'a':
			action = 'left'
		elif data == 'd':
			action = 'right'
		elif data == 'c':
			action = 'cutdown'
		if action != _action :
			_action = action
			print('send command:', action)
			s.sendto(data.encode("utf-8"),addr)
		recivedata,addrg = s.recvfrom(2048)
		if recivedata != 0 :
			print("from:",addrg)
			recivedata = int(recivedata.decode())
			print("got recive :", recivedata)
			distance = int(recivedata / 1000)
			leftSignal = int((recivedata % 1000)/100)
			rightSignal = int((recivedata % 100) / 10)
			middleSignal = int((recivedata % 10))
			print('distance = ', distance,
				  '\nleftSignal = ', leftSignal,
				  '\nrightSignal = ', rightSignal,
				  '\nmiddleSignal = ', middleSignal,
				  )
			recivedata = 0
		if action == 'cutdown':
			print('hoster cutdown!!!')
			break
		time.sleep(0.3)
	s.close()
