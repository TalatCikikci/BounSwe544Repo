# Import socket module
import socket
import threading
import Queue
# import time

# Create a TCP socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

writeQueue = Queue.Queue()
screenQueue = Queue.Queue()

# Set host IP and Port variables to bind the socket
#host = '192.168.0.14'
host = socket.gethostbyname(socket.gethostname())
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
rt = ReadThread("ReadThread", clientSocket, writeQueue, screenQueue, nickname)
rt.start()

wt = WriteThread("WriteThread", clientSocket, writeQueue, nickname)
wt.start()

rt.join()
wt.join()
clientSocket.close()

class ReadThread (threading.Thread):

	def __init__(self, name, csoc, writeQueue, screenQueue, userName):
		threading.Thread.__init__(self)
		self.name = name
		self.csoc = csoc
		self.userName = userName
		self.writeQueue = writeQueue
		self.screenQueue = screenQueue
		self.readSessions = 0

	def incoming_parser(self, data):
		# theTime = time.strftime("%H:%M:%S")
		
		# Handle empty message from server
		if len(data) == 0:
			return
		
		else:
			if ':' in data:
				splitted = data.split(':')
				print(splitted)
				command = splitted[0]
				parameter = splitted[1:]
			else:
				command = data
			
			if command == 'LOGINOK':
				msg = 'LISTSES'
				self.writeQueue.put(msg)
			
			elif command == 'LOGINREJ':
				nickname = raw_input('Enter your nickname: ')
				msg = 'LOGIN:' + nickname
				self.writeQueue.put(msg)
			
			elif command == 'LOGOUTOK':
				self.csoc.close()
			
			elif command == 'SESSION':
			################################################### param[0] --> nr of sessions
															#	param[1] --> session name
															#	param[2:]--> user list of session
															#	MOVE THIS TO SCREEN THREAD AND KEEP SESSION INFO UNTIL SELECTION
				totalSessions = int(parameter[0])
				sessionName = parameter[1].strip()
				playersInSession = []
				for iter in range(len(parameter)-2):
					playersInSession = playersInSession.append(parameter[iter+2])
				print('Session ' + iter+1 + ':' + sessionName + '\nPlayers in session:' + playersInSession + '\n' )
				self.readSessions += 1
				if self.readSessions == totalSessions:
					scr = 'SESDONE'
					self.screenQueue.put(scr)
					self.readSessions = 0
			
			elif command == 'JOINOK':
				scr = 'JOINOK'
				self.writeQueue.put(msg)
				
			elif command == 'ENDTURN':
				msg = 'ENDTURNOK'
				self.writeQueue.put(msg)
			
			elif command == 'COVER':
				numberToCover = parameter.strip()
				msg = 'COVEROK'
				self.writeQueue.put(msg)
			
			elif command == 'CINKO':
				whoDid = parameter
				######## CHECK CINKO
				msg = 'CINKOOK'
				self.writeQueue.put(msg)
			
			elif command == 'BINGO':
				whoDid = parameter
				######## CHECK BINGO
				msg = 'BINGOOK'
				self.writeQueue.put(msg)
			
			elif command == 'TIC':
				msg = 'TOC'
				self.writeQueue.put(msg)
				
			else:
				msg = 'ERR'
				self.writeQueue.put(msg)
				return

	def run(self):
		while True:
			data = self.csoc.recv(4096)
			self.incoming_parser(data)
			
class WriteThread (threading.Thread):

	def __init__(self, name, csoc, writeQueue, userName):
		threading.Thread.__init__(self)
		self.name = name
		self.csoc = csoc
		self.userName = userName
		self.writeQueue = writeQueue

	def run(self):
		self.csoc.send('LOGIN:'+self.userName)
		while True:
			if self.writeQueue.qsize() > 0:
				queue_message = self.writeQueue.get()
				self.csoc.send(queue_message)
				#try:
				#	self.csoc.send(queue_message)
				#except socket.error:
				#	self.csoc.close()
				#	break
				
class SessionDisplayThread (threading.Thread):

	def __init__(self, name, writeQueue, screenQueue, userName):
		threading.Thread.__init__(self)
		self.name = name
		self.userName = userName
		self.writeQueue = writeQueue
		self.screenQueue = screenQueue
		
	def run(self):
		while True:
			if self.screenQueue.qsize() > 0:
				screen_message = self.screenQueue.get()
				
				if screen_message == 'SESDONE':
					sessionSelection = raw_input('Please type the session name you wish to join: ')
					wrt = 'JOINSES:'sessionSelection
					self.writeQueue.put(wrt)
				
				
				
				
				
				
				
		