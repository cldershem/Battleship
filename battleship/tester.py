import random
#~ class Ship(object):
    #~ size = ["1","2","3","4"] # range?
    #~ orientation = ["vertical", "horizontal"]
    #~ state = ["unharmed", "damaged", "sunk"]
    #~ bowCoords = [,]
    #~ 
    #~ def __init__(self):
        #~ pass
    #~ 
    #~ def creatShips(self):
        #~ shipSize = range(0,shipNum)
        #~ shipOrientation = random.randint(0,5)
        #~ #emptyOcean = available spots on board taking size, oritientation, other ships in account
        #~ ship_row = random.randint(1,boardSize)
        #~ ship_col = random.randint(1,boardSize)
        #~ state = "unharmed"
        #~ ships.append(shipSize, shipOrientation, state, shipCoords)
        
        #~ def createShips(shipNum):
        #~ shipSizeMin = 0
        #~ shipSizeMax = shipNum
        #~ for ship in range (0,shipNum):
            #~ shipSize = ship+1
            #~ shipOrientation = random.choice(["N", "E", "S", "W"])
            #~ #emptyOcean = available spots on board taking size, oritientation, other ships in account
            #~ ship_row = random.randint(1,boardSize)
            #~ ship_col = random.randint(1,boardSize)
            #~ if shipOrientation == "N" and shipSize >= 1:
                #~ shipCoords = [(ship_row, ship_col), (ship_row, ship_col-1)]
            #~ elif shipOrientation == "E" and shipSize >= 1:
                #~ shipCoords = [(ship_row, ship_col), (ship_row+1, ship_col)]
            #~ elif shipOrientation == "S" and shipSize >= 1:
                #~ shipCoords = [(ship_row, ship_col), (ship_row, ship_col+1)]
            #~ elif shipOrientation == "W" and shipSize >= 1:
                #~ shipCoords = [(ship_row, ship_col), (ship_row-1, ship_col)]
            #~ else:
                #~ shipCoords = [ship_row, ship_col]
            #~ shipState = "unharmed"
            #~ ships.append([shipState, shipCoords, shipOrientation, shipSize])
        
#~ 
#~ class Player(object):
    #~ name = ["Player1", "Player2", "Single Player", realName]
    #~ board = []
    #~ ships = []
    #~ turns = 
boardSize = 5
ships = []

def createShips(shipNum):
        shipSizeMin = 0
        shipSizeMax = shipNum
        for ship in range (0,shipNum):
            shipSize = ship+1
            shipOrientation = random.choice(["N", "E", "S", "W"])
            #emptyOcean = available spots on board taking size, oritientation, other ships in account
            ship_row = random.randint(1,boardSize)
            ship_col = random.randint(1,boardSize)
            if shipOrientation == "N" and shipSize >= 1:
                shipCoords = [(ship_row, ship_col), (ship_row, ship_col-1)]
            elif shipOrientation == "E" and shipSize >= 1:
                shipCoords = [(ship_row, ship_col), (ship_row+1, ship_col)]
            elif shipOrientation == "S" and shipSize >= 1:
                shipCoords = [(ship_row, ship_col), (ship_row, ship_col+1)]
            elif shipOrientation == "W" and shipSize >= 1:
                shipCoords = [(ship_row, ship_col), (ship_row-1, ship_col)]
            else:
                shipCoords = [ship_row, ship_col]
            shipState = "unharmed"
            ships.append(shipCoords)

createShips(2)
print ships
