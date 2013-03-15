import random


class Player(object):
    name = ["Player1", "Player2", "Single Player", realName]
    board = []
    ships = []
    turns = 
#~ 
class Ship(object):
    size = ["1","2","3","4"] # range?
    orientation = ["vertical", "horizontal"]
    state = ["unharmed", "damaged", "sunk"]
    bowCoords = [,]
    
    def __init__(self):
        pass
    
    def creatShips(self):
        shipSize = range(0,shipNum)
        shipOrientation = random.randint(0,5)
        #emptyOcean = available spots on board taking size, oritientation, other ships in account
        ship_row = random.randint(1,boardSize)
        ship_col = random.randint(1,boardSize)
        state = "unharmed"
        ships.append(shipSize, shipOrientation, state, shipCoords)

boardSize = 5
ships = []

