# Import socket module
import socket

# Create a TCP socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set host IP and Port variables to bind the socket

clientSocket.connect(('192.168.0.14',12345))

# host = raw_input('Enter server IP: ')
# port = raw_input('Enter server port: ')
# print('Connecting to ' + host + ':' + port + '...')

# # Bind to the port
# clientSocket.connect((host, int(port)))
print('Connected!')

data = clientSocket.recv(4096)
print(data)
