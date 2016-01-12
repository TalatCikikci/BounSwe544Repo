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
print('Connecting to ' + host + ':' + str(port) + '...')

# Bind to the port
clientSocket.connect((host, int(port)))
print('Connected!')

nickname = raw_input('\nEnter your nickname: ')

# data = clientSocket.recv(4096)
# print(data)

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
				#print(splitted)
				command = splitted[0]
				parameter = splitted[1:]
			else:
				command = data
			
			if command == 'LOGINOK':
				username = ' '.join(parameter).strip()
				scr = 'LOGINOK:' + username
				self.screenQueue.put(scr)
			
			elif command == 'LOGINREJ':
				nickname = raw_input('Enter your nickname: ')
				msg = 'LOGIN:' + nickname
				self.writeQueue.put(msg)
			
			elif command == 'LOGOUTOK':
				self.csoc.close()
			
			elif command == 'SESSION':
				if self.readSessions == 0:
					scr = 'SESNEW'
					self.screenQueue.put(scr)
					
				totalSessions = int(parameter[0])
				sessionName = parameter[1].strip()
				playersInSession = parameter[2:]
				playersInSession = ':'.join(playersInSession)
				scr = 'SESADD:' + sessionName + ':' + playersInSession
				self.screenQueue.put(scr)
				self.readSessions += 1
				
				if self.readSessions == totalSessions:
					scr = 'SESDONE'
					self.screenQueue.put(scr)
					self.readSessions = 0
			
			elif command == 'JOINOK':
				scr = 'JOINOK'
				self.screenQueue.put(scr)
				
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
				
			elif command == 'CREATEOK':
				gname = ' '.join(parameter).strip()
				scr = 'CREATEOK:' + gname
				self.screenQueue.put(scr)
				
			else:
				msg = 'ERR'
				self.writeQueue.put(msg)
				return

	def run(self):
		while True:
			data = self.csoc.recv(1024)
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
		self.gatheredSessions = []
		self.gatheredSessionsNr = 1
		self.sessionName = ''
	
	def parseScreen(self, screen_message):
		
		if len(screen_message) == 0:
			return
			
		else:
			if ':' in screen_message:
				temp = screen_message.split(':')
				#print(temp)
				command = temp[0]
				parameter = temp[1:]
			else:
				command = screen_message
		
			if command == 'LOGINOK':
				acceptedNick = ' '.join(parameter).strip()
				self.userName = acceptedNick
				print('Hello "' + self.userName + '"! You can choose a pending game session, or create a new one!')
				while True:
					menuSelection = raw_input('-To list sessions type "list".\n-To start a new game session type "new".\n\nWhat would you like to do?: ')
					if menuSelection == 'list':
						wrt = 'LISTSES'
						self.writeQueue.put(wrt)
						break
					elif menuSelection == 'new':
						gameName = raw_input('\nType the game name: ')
						while True:
							maxPlayers = raw_input('\nMax players(2-8): ')
							if maxPlayers in ['2','3','4','5','6','7','8']:
								break
							else:
								print('Invalid entry. Please enter a value between 2 and 8.')
						break
					else:
						print('Invalid entry. Please type "list" or "new"')	
				wrt = 'CREATESES:' + gameName + ':' + maxPlayers
				self.writeQueue.put(wrt)
		
			elif command == 'SESNEW':
				self.gatheredSessions = []
				self.gatheredSessionsNr = 1
		
			elif command == 'SESADD':
				splitted = screen_message.split(':')
				sessionName = splitted[0]
				playersInSession = splitted[1:]
				playersInSession = ', '.join(playersInSession)
				sessionTuple = [self.gatheredSessionsNr, sessionName, playersInSession]
				self.gatheredSessions.append(sessionTuple)
				self.gatheredSessionsNr += 1
			
			elif command == 'SESDONE':
				for iter in range(len(self.gatheredSessions)):
					printTuple = self.gatheredSessions[iter]
					print('Session ' + printTuple[1] + ': ' + printTuple[2] + '\n')
					print('Players :' + printTuple[3])
				sessionSelection = raw_input('Please type the session number you wish to join: ')
				########### IMPLEMENT HOW THE SESSOPN WILL BE RECOGNIZED IN SERVER SIDE
				wrt = 'JOINSES:' + sessionSelection
				self.writeQueue.put(wrt)
				
			elif command == 'JOINOK':
				wrt = 'Joined selected session.'
				self.writeQueue.put(wrt)
				
			elif command == 'CREATEOK':
				self.sessionName = ' '.join(parameter).strip()
				print('Created a new session with the name "' + self.sessionName + '"')
				
	def run(self):
		while True:
			if self.screenQueue.qsize() > 0:
				screenMessage = self.screenQueue.get()
				self.parseScreen(screenMessage)
				

###############################  MAIN
				
# start threads
rt = ReadThread("ReadThread", clientSocket, writeQueue, screenQueue, nickname)
rt.start()

wt = WriteThread("WriteThread", clientSocket, writeQueue, nickname)
wt.start()

st = SessionDisplayThread("SessionDisplayThread", writeQueue, screenQueue, nickname)
st.start()

st.join()
rt.join()
wt.join()
clientSocket.close()
