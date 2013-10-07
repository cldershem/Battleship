import random
import os
import logging

board = []
ships = []
shipsSunk = []
shipNames = {   "2": "Patrol Boat",
                "3": "Submarine",
                "4": "Battleship",
                "5": "Aircraft Carrier",
            }
levels = {  
            "Easy": {   "boardSize": 5,
                        "maxShips": 5,
                        "turns": 4,
                        "minShipSize": 2,
                        "maxShipSize": 5},
            "Medium": { "boardSize": 9,
                        "maxShips": 7,
                        "turns": 4,
                        "minShipSize": 2,
                        "maxShipSize": 5},
            "Hard": {   "boardSize": 9,
                        "maxShips": 5,
                        "turns": 4,
                        "minShipSize": 2,
                        "maxShipSize": 5},
            "Test": {   "boardSize": 5,
                        "maxShips": 5,
                        "turns": 4,
                        "minShipSize": 2,
                        "maxShipSize": 5},
            }

cheat = False
debug = False
level = "Medium"
boardSize = levels[level]["boardSize"]
maxShips = levels[level]["maxShips"]
turns = levels[level]["turns"]
minShipSize = levels[level]["minShipSize"]
maxShipSize = levels[level]["maxShipSize"]
shipNum = levels[level]["maxShips"]

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
    if boardSize == 5:
        boarderLength = 15
    elif boardSize == 9:
        boarderLength = 23
    print "*" * boarderLength
    headerRow = []
    count = 1
    for col in board:
        headerRow.append("%s" % count)
        count += 1
    print "*   " + " ".join(headerRow) + " *"
    count = 1
    for row in board:
        print "* " + str(count) + " " + " ".join(row) + " *"
        count += 1
    print "*" * boarderLength

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

def createShipFleet(shipNum):
    shipSize = minShipSize
    while len(ships) < shipNum:
        if shipSize < maxShipSize:
            isError = createMultiShips(shipSize)
            if isError != 0:
                shipSize = isError
            else:
                shipSize += 1
        elif shipSize >= maxShipSize:
            createMultiShips(shipSize)

def startGame():
    del board[0:len(board)]
    del ships[0:len(ships)]
    #~ while True:
        #~ try:
            #~ shipNum = int(raw_input("How many ships (1-%i)? >" % maxShips))
            #~ break
        #~ except (ValueError, TypeError):
            #~ printBox("That is not a valid number!")
    #~ if shipNum <= 0 or shipNum > maxShips:
        #~ printBox("That is not a valid number!")
        #~ startGame()
    #~ else:
    for i in range(0,boardSize):
        board.append(["~"] * boardSize)
    createShipFleet(shipNum)
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
    elif (board[(guess_row-1)][(guess_col-1)] != "~"):
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
        hitShip = ([shipCoords for ship in 
                    [ship for ship in ships for shipCoord in ship
                    if shipCoord == guessCoords] 
                    for shipCoords in ship])
        shipType = shipNames["%s" % len(hitShip)]
        printBox("You hit my %s!" %shipType)
        board[(guess_row)][(guess_col)] = "\033[1m@\033[0m"
        turn += 1
        isShipSunk = []
        for shipCoord in hitShip:
            if board[(shipCoord[0]-1)][(shipCoord[1]-1)] == "\033[1m@\033[0m":
                isShipSunk.append(shipCoord)
        if len(isShipSunk) == len(hitShip):
            isSunk = True
        else:
            isSunk = False
        if isSunk:
            turn +=2
            shipsSunk.append(ship)
            printBox("Good Job! You sunk my %s!" %shipType)
            markShip = [ship for ship in ships for shipCoord in ship if shipCoord == guessCoords]
            for shipCoord in markShip[0]:
                board[shipCoord[0]-1][shipCoord[1]-1] = "\033[1m+\033[0m" #marks bold s for ship on map
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
            printBox("Here is the answer:")
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
        printBox(str((len(ships))-len(shipsSunk)) + " ships left")
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
