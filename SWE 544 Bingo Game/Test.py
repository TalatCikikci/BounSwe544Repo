# import BingoCardGenerator
# bingoTuple = BingoCardGenerator.generateBingoCard()
# print bingoTuple[0]
# print bingoTuple[1]

# import Game
# import threading

# players = []
# players.append("ali")
# players.append("veli")

# game = Game.GameSession(1, players)
# game.start()

# game.join()



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
host = '169.254.226.95'
port = 12345

# host = raw_input('Enter server IP: ')
# port = raw_input('Enter server port: ')
print('Connecting to ' + host + ':' + str(port) + '...')

# Bind to the port
clientSocket.connect((host, int(port)))
print('Connected!')

while True:
	data = 'LOGIN:ahmet'
	data = pickle.dumps(data)
	clientSocket.send(data)
	data = clientSocket.recv(1024)
	data = pickle.loads(data)
	print(data)