# Import necessary modules
import socket
import threading
import Queue

class ReadThread (threading.Thread):

	def __init__(self, id, csoc, threadQueue, screenQueue):
		threading.Thread.__init__(self)
		self.id = id
		self.csoc = csoc
		self.threadQueue = threadQueue
		self.screenQueue = screenQueue

	def incoming_parser(self, data):
		
		# Handle empty message from server
		if len(data) == 0:
			return
		
		else:
			splitted = data.split(':')
			command = splitted[0]
			parameter = splitted[1]
			
			if command == 'LOGIN':
				username = parameter.strip()
				######### USERNAME CHECK HERE
				msg = 'LOGINOK:' + username
				self.threadQueue.put(msg)
			
			elif command == 'LOGOUT':
				msg = 'LOGOUTOK:' + username
				self.threadQueue.put(msg)
			
			elif command == 'LISTSES':
				######### FOR EVERY SESSION IN SERVER
				msg = 'SESSION:' + sessionName + ':' + sessionPlayers
				self.threadQueue.put(msg)
			
			elif command == 'JOINSES':
				sessionToJoin = parameter.strip()
				######### CHECK SESSION AVAILABILITY
				msg = 'JOINOK'
				self.threadQueue.put(msg)
			
			elif command == 'LEAVESES':
				msg = 'LEAVEOK'
				self.threadQueue.put(msg)
				
			elif command == 'ENDTURN':
				msg = 'ENDTURNOK'
				self.threadQueue.put(msg)
			
			elif command == 'COVER':
				numberToCover = parameter.strip()
				msg = 'COVEROK'
				self.threadQueue.put(msg)
			
			elif command == 'CINKO':
				whoDid = parameter
				######## CHECK CINKO
				msg = 'CINKOOK'
				self.threadQueue.put(msg)
			
			elif command == 'BINGO':
				whoDid = parameter
				######## CHECK BINGO
				msg = 'BINGOOK'
				self.threadQueue.put(msg)
			
			elif command == 'TIC':
				msg = 'TOC'
				self.threadQueue.put(msg)
				
			else:
				msg = 'ERR'
				self.threadQueue.put(msg)
				return

	def run(self):
		while True:
			data = self.csoc.recv(1024)
			self.incoming_parser(data)
			
class WriteThread (threading.Thread):

	def __init__(self, id, csoc, threadQueue):
		threading.Thread.__init__(self)
		self.id = id
		self.csoc = csoc
		self.threadQueue = threadQueue

	def run(self):
		while True:
			if self.threadQueue.qsize() > 0:
				queue_message = self.threadQueue.get()
				self.csoc.send(queue_message)
				#try:
				#	self.csoc.send(queue_message)
				#except socket.error:
				#	self.csoc.close()
				#	break