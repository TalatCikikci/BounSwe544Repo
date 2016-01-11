import BingoCardGenerator
import threading

class GameSession (threading.Thread):
	
	def __init__(self, id, userList):
		threading.Thread.__init__(self)
		self.userList = userList
		self.id = id
		self.userGameArray = []
		
	def prepareSession(self):
		existingCards = range(len(self.userList))
		sessionUserSlot = 0
		
		for user in self.userList:
			singleUser = range(2)
			while True:
				singleUser[0], singleUser[1] = BingoCardGenerator.generateBingoCard()
				if singleUser[1] in existingCards:
					continue
				else:
					existingCards[sessionUserSlot] = singleUser[1]
					singleUser.append(user)
					self.userGameArray.append([sessionUserSlot,singleUser])
					sessionUserSlot += 1
					break

	def run(self):
		self.prepareSession()
		print(self.userGameArray)