# Import necessary modules
import socket
import threading
import Queue

class ReadThread (threading.Thread):

	def __init__(self, id, csoc, readQueue, writeQueue, screenQueue):
		threading.Thread.__init__(self)
		self.id = id
		self.csoc = csoc
		self.readQueue = readQueue
		self.screenQueue = screenQueue
		self.writeQueue = writeQueue

	def incoming_parser(self, data):
		
		# Handle empty message from server
		if len(data) == 0:
			return
		
		else:
			splitted = data.split(':')
			print(splitted)
			command = splitted[0]
			parameter = splitted[1]
			
			if command == 'LOGIN':
				username = parameter.strip()
				######### USERNAME CHECK HERE
				msg = 'LOGINOK:' + username
				self.writeQueue.put(msg)
			
			elif command == 'LOGOUT':
				msg = 'LOGOUTOK:' + username
				self.writeQueue.put(msg)
			
			elif command == 'LISTSES':
				######### FOR EVERY SESSION IN SERVER
				msg = 'SESSION:' + sessionName + ':' + sessionPlayers
				self.writeQueue.put(msg)
			
			elif command == 'JOINSES':
				sessionToJoin = parameter.strip()
				######### CHECK SESSION AVAILABILITY
				msg = 'JOINOK'
				self.writeQueue.put(msg)
			
			elif command == 'LEAVESES':
				msg = 'LEAVEOK'
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
			data = self.readQueue.get()
			self.incoming_parser(data)
			
class WriteThread (threading.Thread):

	def __init__(self, id, csoc, writeQueue):
		threading.Thread.__init__(self)
		self.id = id
		self.csoc = csoc
		self.writeQueue = writeQueue

	def run(self):
		while True:
			if self.writeQueue.qsize() > 0:
				queue_message = self.writeQueue.get()
				self.csoc.send(queue_message)
				#try:
				#	self.csoc.send(queue_message)
				#except socket.error:
				#	self.csoc.close()
				#	break