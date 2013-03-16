import random

boardSize = 5
ships = []
shipNum = 5

def main(shipNum):
    makeShips(shipNum)
    count = 1
    for ship in ships:
        print("ship %i %s" % (count, ship))
        count += 1

class Ship(object):
    def __init__(self, shipSize):
        self.shipSize = shipSize

    def createMultiShips(self, shipSize):
        currentShip = []
        shipOrientation = random.choice(["N", "E", "S", "W"])
        ship_row = random.randint(1,boardSize)
        ship_col = random.randint(1,boardSize)
        shipBow = (ship_row, ship_col)
        currentShip.append(shipBow)
        while len(currentShip) < shipSize:
            if shipOrientation == "N":
                currentShip.append((currentShip[-1][0],currentShip[-1][1]-1))
            elif shipOrientation == "E":
                currentShip.append((currentShip[-1][0]+1,currentShip[-1][1]))
            elif shipOrientation == "S":
                currentShip.append((currentShip[-1][0],currentShip[-1][1]+1))
            elif shipOrientation == "W":
                currentShip.append((currentShip[-1][0]-1,currentShip[-1][1]))
            else:
                logging.debug("Fuck")
        else: #check for duplicates/out of ocean, then append to ships
            for currentShipCoord in currentShip:
                if ((currentShipCoord[0] > boardSize) or 
                    (currentShipCoord[0] < 0) or 
                    (currentShipCoord[1] > boardSize) or 
                    (currentShipCoord[1] < 0)):
                    currentShip = []
                    break
            for ship in ships:
                for shipCoord in ship:
                    if currentShip and shipCoord in currentShip:
                        currentShip = []
                        break
                    elif not currentShip:
                        break
            if currentShip:
                ships.append(currentShip)

def makeShips(shipNum):
    shipSize = 2
    while len(ships) < shipNum:
        if shipSize < 5:
            ship = Ship(shipSize)
            Ship.createMultiShips(ship, shipSize)
            shipSize += 1
        elif shipSize >= 5:
            shipSize = 4
            ship = Ship(shipSize)
            Ship.createMultiShips(ship, shipSize)

main(shipNum)
print ships