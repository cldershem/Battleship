import random


class Player(object):
    name = ["Player1", "Player2", "Single Player", realName]
    board = []
    ships = []
    turns = 

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

#numbers can never go negative
#find if ships collide
#player has board, ships
#strikethrough to show linked?
#for guess in ships:
# if hit:
# ships[guess] = "hit"

#~ def fuckme():
            #~ if currentShipCoord in currentShip[range(0,len(currentShip)]
            #~ ships.append(currentShip)
            #~ checkErrors = Ship(shipSize)
            #~ isShipError = Ship.checkShipErrors(checkErrors)
            #~ if isShipError == True:
                #~ renewShip = Ship(shipSize)
                #~ Ship.createMultiShips(renewShip, shipSize)
            #~ else:
                #~ pass
        
    #~ def checkShipErrors(shipSize):
        #~ shipCoordList = []
        #~ duplicate = []
        #~ if len(ships) > 1:
            #~ for ship in ships:
                #~ for shipCoords in ship:
                    #~ shipCoordList.append(shipCoords)
                    #~ coordOccurance = shipCoordList.count(shipCoords)
                    #~ print coordOccurance
                    #~ if coordOccurance != 1:
                        #~ del ships[:-1]
                        #~ duplicate.append(shipCoords)
                        #~ print "Fucking Duplicate" *2
                        #~ print duplicate
                        #~ return True
                    #~ else:
                        #~ print "All clear"
                        #~ return False
