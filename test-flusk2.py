#!/usr/bin/env python3
import socket
import sys
 
# Create a connection to the server application on port 81
tcp_socket = socket.create_connection(('localhost', 81))
 
try:
    data = str(3000)
    tcp_socket.sendall(data)
 
finally:
    print("Closing socket")
    tcp_socket.close()


