# Import socket module
import socket
import thread
import select
import InputOutput
import Queue
import pickle

# Create a TCP socket object
bingoAppSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set host IP and Port variables to bind the socket
host = socket.gethostbyname(socket.gethostname())
port = 12345

print('Server socket binding at ' + host + ':' + str(port) + ' ...')

# Bind to the port
bingoAppSocket.bind((host, port))
print('Server socket bound.')

recvQueue = Queue.Queue()
sendQueue = Queue.Queue()
screenQueue = Queue.Queue()
connectedClients = []

# start paraser threads
rt = InputOutput.ReadThread(1, bingoAppSocket, recvQueue, sendQueue, screenQueue)
rt.start()

# wt = InputOutput.WriteThread(2, bingoAppSocket, sendQueue)
# wt.start()

# Now wait for client connection.
bingoAppSocket.listen(5)
while True:
	print('Waiting for new connection...')
	# Listen socket for read event every 5 ms
	connections, wlist, xlist = select.select([bingoAppSocket], [], [], 0.05)
	
	# Establish connection with client.
	for connection in connections:
		bingoPlayerSocket, playerAddress = connection.accept()
		connectedClients.append(bingoPlayerSocket)
		print 'Got connection from ' , playerAddress
	
	clientList = []
	try:
		clientList, wlist, xlist = select.select(connectedClients, [], [], 0.05)
	except select.error:
		pass
	else:
		for client in clientList:
			try:
				data = client.recv(1024)
				data = pickle.loads(data)
			except socket.error:
				pass

			rt.readQueue.put(data)
			data = rt.writeQueue.get()
			data = pickle.dumps(data)
			# wt.writeQueue.put(data)
			try:
				client.send(data)
			except socket.error:
				pass

	print clientList
	print connectedClients
	
# Close the connections
rt.join()
# wt.join()
client.close()
bingoPlayerSocket.close() 