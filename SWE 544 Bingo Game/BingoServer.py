# Import socket module
import socket
import thread
import select

# Create a TCP socket object
bingoAppSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set host IP and Port variables to bind the socket
host = socket.gethostbyname(socket.gethostname())
port = 12345

print('Server socket binding at ' + host + ':' + str(port) + ' ...')

# Bind to the port
bingoAppSocket.bind((host, port))
print('Server socket bound.')

connectedClients = []

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
			data = client.recv(1024)
			readData(data)
			data = writeData()
			client.send(data)

	print clientList
	print connectedClients
	
# Close the connections
client.close()
bingoPlayerSocket.close() 