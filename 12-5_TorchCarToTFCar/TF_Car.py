import socket
import sys
import tty,termios
import time
addr = ('192.168.1.104',5999)#目标主机IP
readdr = ('192.168.1.105',3888)#本主机IP
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind(readdr)
if __name__ == '__main__':
	while True:
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try :
		    tty.setraw(fd)
		    data = sys.stdin.read(1)
		except :
		    pass
		finally:
		    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
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
		print('send command:', action)
		s.sendto(data.encode("utf-8"),addr)
		recivedata,addrg = s.recvfrom(2048)
		if recivedata:
			print("from:",addrg)
			print("got recive :",recivedata.decode())
		if action == 'cutdown':
			print('hoster cutdown!!!')
			break
		time.sleep(0.3)
	s.close()
