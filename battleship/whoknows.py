import random
import os
import logging

board = []
ships = []
shipsSunk = []
levels = {  
            "Easy": {   "boardSize": 5,
                        "maxShips": 5,
                        "turns": 4,
                        "minShipSize": 1,
                        "maxShipSize": 3},
            "Medium": { "boardSize": 5,
                        "maxShips": 7,
                        "turns": 4,
                        "minShipSize": 1,
                        "maxShipSize": 3},
            "Hard": {   "boardSize": 10,
                        "maxShips": 10,
                        "turns": 4,
                        "minShipSize": 2,
                        "maxShipSize": 5},
            }

cheat = True
debug = True
singleShip = False
level = "Easy"
boardSize = levels[level]["boardSize"]
maxShips = levels[level]["maxShips"]
turns = levels[level]["turns"]
minShipSize = levels[level]["minShipSize"]
maxShipSize = levels[level]["maxShipSize"]

def main():
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] ) #clears terminal window
    printBox("Let's play battleship!")
    if debug == True:
        logging.basicConfig(level=logging.DEBUG, format=
                            '%(asctime)s - %(levelname)s - %(message)s')
    startGame()

def printBox(printOut):
    """
    This prints things out with a box around them.
    """
    print "#" * 80
    print "%s".center(40, " ") % printOut
    print "#" * 80

def print_board(board):
    print "*" * 15
    headerRow = []
    count = 1
    for x in board:
            headerRow.append("%s" % count)
            count += 1
    print "*   " + " ".join(headerRow) + " *"
    count = 1
    for row in board:
            print "* " + str(count) + " " + " ".join(row) + " *"
            count += 1
    print "*" * 15

def createMultiShips(shipSize):
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
                (currentShipCoord[0] < 1) or 
                (currentShipCoord[1] > boardSize) or 
                (currentShipCoord[1] < 1)):
                shipSize = len(currentShip)
                currentShip = []
                return shipSize
                break
        for ship in ships:
            for shipCoord in ship:
                if currentShip and shipCoord in currentShip:
                    shipSize = len(currentShip)
                    currentShip = []
                    return shipSize
                    break
                elif not currentShip:
                    break
        if currentShip:
            ships.append(currentShip)
            isError = 0
            return isError
            
def createSingleShips(shipNum):
    while len(ships) < shipNum:
        ship_row = random.randint(1,boardSize)
        ship_col = random.randint(1,boardSize)
        shipCoords = (ship_row, ship_col)
        ships.append(shipCoords)
        if len(ships) > 0:
            for ship in ships[:-1]:
                if ships[-1] == ship:
                    ships.pop()
                else:
                    pass
    if shipNum != len(ships):
        logging.warning("extra numbers in ships")

def createShipFleet(shipNum):
    shipSize = 2
    while len(ships) < shipNum:
        if singleShip == True:
            #ship = Ship(shipNum)
            #Ship.createSingleShips(ship, shipNum)
            createSingleShips(shipNum)
            break
        elif shipSize < 5:
            #ship = Ship(shipSize)
            #isError = Ship.createMultiShips(ship, shipSize)
            isError = createMultiShips(shipSize)
            if isError != 0:
                shipSize = isError
            else:
                shipSize += 1
        elif shipSize >= 5:
            shipSize = 4
            #ship = Ship(shipSize)
            #Ship.createMultiShips(ship, shipSize)
            createMultiShips(shipSize)

def startGame():
    del board[0:len(board)]
    del ships[0:len(ships)]
    while True:
        try:
            numShips = int(raw_input("How many ships (1-%i)? >" % maxShips))
            break
        except (ValueError, TypeError):
            printBox("That is not a valid number!")
    if numShips <= 0 or numShips > maxShips:
        printBox("That is not a valid number!")
        startGame()
    else:
        for i in range(0,boardSize):
            board.append(["~"] * boardSize)
        createShipFleet(numShips)
        checkTurn(turns)
        
def getGuess(turn):
    while True:
        try:
            guess_row = int(raw_input("Guess Row:"))
            guess_col = int(raw_input("Guess Col:"))
            break
        except (TypeError, ValueError):
            printBox("That is not a valid number!")
    if (guess_row < 1 or guess_row > boardSize) or (guess_col < 1 or guess_col > boardSize):
        printBox("Oops, that's not even in the ocean.")
        return getGuess(turn)
    elif board[(guess_row-1)][(guess_col-1)] == "\033[1mX\033[0m":
        printBox("You guessed that one already.")
        return getGuess(turn)
    else:
        guessCoords = (guess_row, guess_col)
        return guessCoords

def checkGuess(guessCoords, turn):
    guess_row = (guessCoords[0]-1)
    guess_col = (guessCoords[1]-1)
    isHit = [shipCoord for ship in ships for shipCoord in ship if shipCoord == guessCoords]
    if isHit:
        printBox("Congratulations! You hit my battleship!")
        board[(guess_row)][(guess_col)] = "\033[1m@\033[0m"
        turn += 3       
        isShipSunk = []
        hitShip = [ship for ship in ships for shipCoord in ship if shipCoord == guessCoords]
        for shipCoord in hitShip[0]:
            if board[(shipCoord[0]-1)][(shipCoord[1]-1)] == "\033[1m@\033[0m":
                isShipSunk.append(shipCoord[0])
        if len(isShipSunk) == len(hitShip[0]):
            isSunk = True
        else:
            isSunk = False
        if isSunk:
            shipsSunk.append(ship)
            printBox("Congratulations! You sunk my battleship!")
            markShip = [ship for ship in ships for shipCoord in ship if shipCoord == guessCoords]
            for shipCoord in markShip[0]:
                board[shipCoord[0]-1][shipCoord[1]-1] = "\033[1m/\033[0m" #marks bold s for ship on map
            if len(shipsSunk) == len(ships):
                printBox("Congratulations! You sunk my whole fleet!")
                print_board(board)
                playAgain()
    else:
        printBox("You missed my battleship!")
        board[(guess_row)][(guess_col)] = "\033[1mX\033[0m"
        if turn == 0:
            printBox("You missed everytime!")
            printBox("You are out of turns!")
            board[(guess_row)][(guess_col)] = "\033[1mX\033[0m" #marks bold x on map
            printBox("Here is the answer.")
            markShip = [shipCoord for ship in ships for shipCoord in ship]
            for ship in markShip:
                board[ship[0]-1][ship[1]-1] = "\033[1mS\033[0m" #marks bold s for ship on map
            print_board(board)
            printBox("Game Over")
            playAgain()
    checkTurn(turn)

def checkTurn(turn):
    if turn > 0:
        print_board(board)
        printBox(str(turn) + " turns left")
        printBox(str(len(ships)) + " ships left")
        if cheat == True:
            count = 1
            for ship in ships:
                print("ship %i %s" % (count, ship))
                count += 1
        guessCoords = getGuess(turn)
        turn -= 1
        checkGuess(guessCoords, turn)
    else:
        print "Yeah, that happened."

def playAgain():
    newGame = raw_input("Would you like to play again? (y/n)>")
    newGame = newGame.lower()
    if newGame[0] == "y":
        main()
    else:
        exit()

main()
