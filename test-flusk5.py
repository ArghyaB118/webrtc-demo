# client.py
import socket
from time import sleep

s = socket.socket()
s.connect(('localhost',8081))

for i in range(10):
	val = pack('!i', i)
	s.send(val)
	#s.send(i.to_bytes(2, 'big'))
	# wait around for a while so that the socket in server.py goes out of scope
# 	sleep(1)

#s.send(b'hello 2')
