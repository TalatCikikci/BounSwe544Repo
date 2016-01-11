# This script generates a bingo card with three rows.
import random

def generateBingoCard():

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
	
generateBingoCard()