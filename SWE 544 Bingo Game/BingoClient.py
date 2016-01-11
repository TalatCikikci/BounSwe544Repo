# Import socket module
import socket
import threading
import Queue
import time

# Create a TCP socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sendQueue = Queue.Queue()
screenQueue = Queue.Queue()

# Set host IP and Port variables to bind the socket
host = '192.168.0.14'
port = 12345

# host = raw_input('Enter server IP: ')
# port = raw_input('Enter server port: ')
print('Connecting to ' + host + ':' + port + '...')

# Bind to the port
clientSocket.connect((host, int(port)))
print('Connected!')

nickname = raw_input('Enter your nickname: ')

# data = clientSocket.recv(4096)
# print(data)

# start threads
rt = ReadThread("ReadThread", clientSocket, sendQueue, screenQueue, nickname)
rt.start()

wt = WriteThread("WriteThread", clientSocket, sendQueue, nickname)
wt.start()

rt.join()
wt.join()
clientSocket.close()

class ReadThread (threading.Thread):

	def __init__(self, name, csoc, threadQueue, screenQueue, userName):
		threading.Thread.__init__(self)
		self.name = name
		self.csoc = csoc
		self.userName = userName
		self.threadQueue = threadQueue
		self.screenQueue = screenQueue

	def incoming_parser(self, data):
		theTime = time.strftime("%H:%M:%S")
		
		# Handle empty message from server
		if len(data) == 0:
			return
		
		# Handle message with first word longer than 3 letters
		elif len(data) > 3 and not data[3] == " " and loginStatus:
			response = "ERR"
			self.csoc.send(response)
			return
		
		# This condition responds to server "TIC" with a "TOC" but due to server bug server responds again with an "ERR". So it is commented out for now.
		#elif data[0:3] == "TIC":
			#response = "TOC"
			#self.csoc.send(response)
		
		else:
			rest = data[4:]
			
			if data[0:3] == "BYE":
				username = rest.strip()
				msg = "Goodbye " + username + ", we hope to see you again!"
			
			elif data[0:3] == "ERL":
				msg = "You need to login to do that. Login command: /nick <username>"
			
			elif data[0:3] == "HEL":
				username = rest.strip()
				msg = "Login successful. Welcome " + username + "!"
			
			elif data[0:3] == "REJ":
				username = rest.strip()
				msg = "Username " + username + " already exists in the system. Please login with a different username."
			
			elif data[0:3] == "MNO":
				username = rest.strip()
				msg = "User " + username + " could not be found. Message was not delivered."
			
			elif data[0:3] == "MSG":
				splitted = rest.split(":")
				username = splitted[0]
				message = ' '.join(splitted[1:])
				msg = username + " <private> : " + message
				# This condition responds to server "MSG" with a "MOK" but due to server bug server responds again with an "ERR". So it is commented out for now.
				#response = "MOK"
				#self.csoc.send(response)
			
			elif data[0:3] == "SAY":
				splitted = rest.split(":")
				username = splitted[0]
				message = splitted[1]
				msg = username + " : " + message
				# This condition responds to server "SAY" with a "SOK" but due to server bug server responds again with an "ERR". So it is commented out for now.
				# response = "SOK"
				# self.csoc.send(response)
			
			elif data[0:3] == "SYS":
				msg = "<SYSTEM> : " + rest
				# This condition responds to server "SYS" with a "YOK" but due to server bug server responds again with an "ERR". So it is commented out for now.
				# response = "YOK"
				# self.csoc.send(response)
			
			elif data[0:3] == "LSA":
				splitted = rest.split(":")
				listOfUsers = splitted
				msg = "<SYSTEM> Registered nicks: "
				for i in splitted:
					msg += i + ", "
				msg = msg[:-2]
				self.app.model.clear()
				for user in listOfUsers:
					nickLister = QStandardItem(user)
					self.app.model.appendRow(nickLister)
			
			elif data[0:3] == "TOC":
				msg = "TOC!"
			
			elif data[0:3] == "SOK":
				msg = "Message sent to everyone."
			
			elif data[0:3] == "MOK":
				msg = "Private message delivered to user."
			
			elif data[0:3] == "ERR":
				msg = "Invalid command."
			
			else:
				if loginStatus:
					response = "ERR"
					self.csoc.send(response)
				return

	def run(self):
		while True:
			data = self.csoc.recv(4096)
			self.incoming_parser(data)
			
class WriteThread (threading.Thread):

	def __init__(self, name, csoc, threadQueue, userName):
		threading.Thread.__init__(self)
		self.name = name
		self.csoc = csoc
		self.userName = userName
		self.threadQueue = threadQueue

	def run(self):
		self.csoc.send('USERNAME:'+self.userName)
		while True:
			if self.threadQueue.qsize() > 0:
				queue_message = self.threadQueue.get()
				self.csoc.send(queue_message)
				#try:
				#	self.csoc.send(queue_message)
				#except socket.error:
				#	self.csoc.close()
				#	break