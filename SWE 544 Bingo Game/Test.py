# import BingoCardGenerator
# bingoTuple = BingoCardGenerator.generateBingoCard()
# print bingoTuple[0]
# print bingoTuple[1]

import Game
import threading

players = []
players.append("ali")
players.append("veli")

game = Game.GameSession(1, players)
game.start()

game.join()