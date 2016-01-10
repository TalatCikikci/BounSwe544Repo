# Import socket module
import socket
import thread

# Create a TCP socket object
bingoAppSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set host IP and Port variables to bind the socket
host = socket.gethostbyname(socket.gethostname())
port = 12345

print('Server socket binding at ' + host + ':' + str(port) + ' ...')

# Bind to the port
bingoAppSocket.bind((host, port))
print('Server socket bound.')

# Now wait for client connection.
bingoAppSocket.listen(5)
while True:
	print('Waiting for new connection...')
	# Establish connection with client.
	bingoPlayerSocket, playerAddress = bingoAppSocket.accept()
	print 'Got connection from ' , playerAddress
	bingoPlayerSocket.sendall('Thank you for connecting!')
bingoPlayerSocket.close() # Close the connection