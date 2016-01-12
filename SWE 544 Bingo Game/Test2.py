# Import socket module
import socket
import threading
import Queue
import time
import pickle

# Create a TCP socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sendQueue = Queue.Queue()
screenQueue = Queue.Queue()

# Set host IP and Port variables to bind the socket
# host = '192.168.2.123'
host = socket.gethostbyname(socket.gethostname())
port = 12345

# host = raw_input('Enter server IP: ')
# port = raw_input('Enter server port: ')
print('Connecting to ' + host + ':' + str(port) + '...')

# Bind to the port
clientSocket.connect((host, int(port)))
print('Connected!')

while True:
	data = 'LEAVESES'
	#data = pickle.dumps(data)
	clientSocket.send(data)
	data = clientSocket.recv(1024)
	#data = pickle.loads(data)
	print(data)
	
clientSocket.close()