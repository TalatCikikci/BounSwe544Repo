import threading
import random
import time

class GameSession (threading.Thread):
	
	def __init__(self, name, maxPlayers):
		threading.Thread.__init__(self)
		self.userList = []
		self.maxPlayers = maxPlayers
		self.name = name
		self.timeout = 120
		self.userGameArray = []
		self.userUpdatedArray = []
		self.drawnNumbers = []
		
	def countdown(initTime):
		time = initTime
		while time > 0:
			sleep(1)
			time = time-1
		return True
		
	def prepareSession(self):
		existingCards = range(len(self.userList))
		sessionUserSlot = 0
		
		for user in self.userList:
			singleUser = range(2)
			while True:
				singleUser[0], singleUser[1] = self.generateBingoCard()
				if singleUser[1] in existingCards:
					continue
				else:
					existingCards[sessionUserSlot] = singleUser[1]
					singleUser.append(user)
					self.userGameArray.append([sessionUserSlot,singleUser])
					sessionUserSlot += 1
					break

	def drawRandomNumber(self):
		while True:
			drawnNumber = random.randint(1,90)
			if drawnNumber in self.drawnNumbers:
				continue
			else:
				self.drawnNumbers.append(drawnNumber)
				break
		return drawnNumber
		
	def checkCardsForDrawn(self, checkNumber):
		for i in range(len(self.userList)):
			if self.userGameArray[0] == i:
				tempCard = self.userGameArray[1]
				tempList = tempCard[1]
				for row in range(len(tempList)):
					if checkNumber in tempList[row]:
						tempRow = tempList[row]
						theIndex = tempRow.index(checkNumber)
						tempRow[theIndex] = 'X'
					tempList[row] = tempRow
				tempCard[1] = tempList
				self.userUpdatedArray[1] = tempCard
				
	def generateBingoCard(self):

		# Will hold the generated bingo card tuples.
		bingoCard = []
		# Holds the already selected numbers.
		cardChecklist = []

		# Loop for 3 rows.
		for cinquina in range(3):

			# Column iterator.
			i = 0
			# Holds numbers for the current row.
			cinquinaAccepted = []

			while i < 5:
				# Generate random number.
				cardCandidate = random.randint(1,90)
				
				# Check if number already exists in the card.
				if cardCandidate in cardChecklist:
					continue
					
				# Insert initial number to the card.
				elif len(cinquinaAccepted) == 0:
					cardChecklist.append(cardCandidate)
					cinquinaAccepted.append(cardCandidate)
					i += 1
				
				else:
					for alreadyIncluded in cinquinaAccepted:
						
						# Check if the number exists in the current row.
						if cardCandidate in cinquinaAccepted:
							continue
						
						alreadyIncludedStr = str(alreadyIncluded)
						cardCandidateStr = str(cardCandidate)
						
						# A row must have at most one of each tenths digit. Check for "0" tenths.
						if len(alreadyIncludedStr) == 1:
							if alreadyIncludedStr == cardCandidateStr:
								continue
							else:
								cardChecklist.append(cardCandidate)
								cinquinaAccepted.append(cardCandidate)
								i += 1
							
						# A row must have at most one of each tenths digit. Check for tenths digit > "0"
						else:
							if alreadyIncludedStr[0] == cardCandidateStr[0]: 
								continue
							else:
								cardChecklist.append(cardCandidate)
								cinquinaAccepted.append(cardCandidate)
								i += 1
						
						continue
			
			# Sort row in ascending order
			cinquinaAccepted = sorted(cinquinaAccepted)
			bingoCard.append(cinquinaAccepted)

		# This commented section is for debugging.
		# for i in range(3):
			# print(bingoCard[i])
		
		cardChecklist = sorted(cardChecklist)
		
		return bingoCard, cardChecklist
				
	def run(self):
		self.prepareSession()
		# Commented out print for testing purposes.
		# print(self.userGameArray)
		
		self.userUpdatedArray = self.userGameArray
		
		while True:
			okCount = 0
			theNumber = self.drawRandomNumber()
			checkCardsForDrawn(theNumber)
			
			###### SEND NR TO ALL PAYERS
			###### CHECK FOR BINGO
			###### CHECK FOR CINKO
			
			while okCount < len(self.userList):
				if countdown(20):
					break

		
