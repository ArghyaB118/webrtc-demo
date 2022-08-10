# https://stackoverflow.com/questions/1423251/talking-between-python-tcp-server-and-a-c-client
# server.py
import socket
from time import sleep

def f(s):
	r,a = s.accept()
	print(int.from_bytes(r.recv(100), "big"))
	#print(r.recv(100))


s = socket.socket()
s.bind(('localhost',8081))

#for i in range(10):
#	s.listen(1)
#	f(s)
	# wait around a bit for the client to send it's second packet
#	sleep(1)

#s.listen(1)
#f(s)
#sleep(10)
s.listen(1)
buf = ''
while len(buf) < 4:
    buf += s.recv(8)
num = struct.unpack('!i', buf[:4])[0]
sleep(10)


