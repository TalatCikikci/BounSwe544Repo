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
clientQueue = Queue.Queue()

# start paraser threads
rt = InputOutput.ReadThread(1, bingoAppSocket, recvQueue, sendQueue, screenQueue)
rt.start()

wt = InputOutput.WriteThread(2, bingoAppSocket, sendQueue, clientQueue)
wt.start()

# Now wait for client connection.
bingoAppSocket.listen(5)
while True:
	print('Waiting for new connection...')
	# Listen socket for read event every 5 ms
	try:
		connections, wlist, xlist = select.select([bingoAppSocket], [], [], 0.05)
	except KeyboardInterrupt:
		raise SystemExit
		
	
	print('test1')
	# Establish connection with client.
	for connection in connections:
		print('test4')
		bingoPlayerSocket, playerAddress = connection.accept()
		print('test2')
		bingoPlayerSocket.setblocking(0)
		print('test3')
		connectedClients.append(bingoPlayerSocket)
		print 'Got connection from ' , playerAddress
	
	clientList = []
	try:
		clientList, wlist, xlist = select.select(connectedClients, [], [], 0.05)
		print('test5')
	except select.error:
		pass
	else:
		for client in clientList:
			if clientList:
				#try:
				print('test6')
				data = client.recv(1024)
					#data = pickle.loads(data)
				#except socket.error:
					#pass
				print('test7')
				clientQueue.put(client)
				rt.readQueue.put(data)
				print('test8')
				# if sendQueue.qsize() > 0:
					# data = sendQueue.get()
					# # wt.writeQueue.put(data)
					# # data = pickle.dumps(data)
					# # wt.writeQueue.put(data)
					# # try:
					# print('test9')
					# client.send(data)
					# # except socket.error:
						# # pass
	print('test10')
	print clientList
	print connectedClients
	
# Close the connections
rt.join()
wt.join()
client.close()
bingoPlayerSocket.close()