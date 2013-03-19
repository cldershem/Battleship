import random
import os
import logging

cheat = True
debug = False
single = False

boardSize = 5
maxShips = 5
minShipSize = 2
maxShipSize = 4
shipNum = 2

def main():
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] ) #clears terminal window
    printBox("Let's play battleship!")
    if debug == True:
        logging.basicConfig(level=logging.DEBUG, format=
                            '%(asctime)s - %(levelname)s - %(message)s')
    single = raw_input("Would you like to play single player? (y/n)")
    single = single.lower()
    if single == "y":
        singlePlayer()
    else:
        multiPlayer()

def singlePlayer():
    turns = 4
    player = Player("Player")
    player.startGame()
    while turns > 0:
        print_board(player.board)
        printBox(str(turns) + " turns left")
        printBox(str((len(player.ships))-len(player.shipsSunk)) + " ships left")
        if cheat == True:
            count = 1
            for ship in player.ships:
                print("ship %i %s" % (count, ship))
                count += 1
        guessCoords = player.getGuess()
        turns -= 1
        checkedGuess = player.checkGuess(guessCoords)
        if checkedGuess == "hit":
            turns += 1
        elif checkedGuess == "sunk":
            turns += 3
        elif checkedGuess == "won":
            print_board(self.board)
            playAgain()
    else:
        printBox("You missed everytime!")
        printBox("You are out of turns!")
        printBox("Here is the answer:")
        markShip = [shipCoord for ship in player.ships for shipCoord in ship]
        for ship in markShip:
            player.board[ship[0]-1][ship[1]-1] = "\033[1mS\033[0m" #marks bold s for ship on map
        print_board(player.board)
        printBox("Game Over")
    playAgain()

def multiPlayer():
    player1 = Player(raw_input("What is Player One's name?")) #change to raw_input
    player2 = Player(raw_input("What is Player Two's name?")) #change to raw_input
    player1.startGame()
    player2.startGame()
    while True:
        if multiPlayerTurn(player1) == "won":
            winner = player1
            loser = player2
            break
        elif multiPlayerTurn(player2) == "won":
            winner = player2
            loswer = player2
            break
        else:
            pass
    print_board(winner.board)
    playAgain()
    
def multiPlayerTurn(player):
    printBox(player.name)
    print_board(player.board)
    printBox(str((len(player.ships))-len(player.shipsSunk)) + " ships left")
    if cheat == True:
        count = 1
        for ship in player.ships:
            print("ship %i %s" % (count, ship))
            count += 1
    guessCoords = player.getGuess()
    checkedGuess = player.checkGuess(guessCoords)
    if checkedGuess == "won":
        return "won"
    else:
        pass

class Player(object):
    boardSize = 5
    
    def __init__(self, name):
        self.name = name
        self.board = []
        self.ships = []
        self.shipsSunk = []
        self.boardSize = boardSize
        self.maxShips = maxShips
        self.minShipSize = minShipSize
        self.maxShipSize = maxShipSize
        self.shipNum = shipNum

    def createMultiShips(self, shipSize):
        currentShip = []
        shipOrientation = random.choice(["N", "E", "S", "W"])
        ship_row = random.randint(1,self.boardSize)
        ship_col = random.randint(1,self.boardSize)
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
        else: #check for duplicates/out of ocean, then append to self.ships
            for currentShipCoord in currentShip:
                if ((currentShipCoord[0] > self.boardSize) or 
                    (currentShipCoord[0] < 1) or 
                    (currentShipCoord[1] > self.boardSize) or 
                    (currentShipCoord[1] < 1)):
                    shipSize = len(currentShip)
                    currentShip = []
                    return shipSize
                    break
            for ship in self.ships:
                for shipCoord in ship:
                    if currentShip and shipCoord in currentShip:
                        shipSize = len(currentShip)
                        currentShip = []
                        return shipSize
                        break
                    elif not currentShip:
                        break
            if currentShip:
                self.ships.append(currentShip)
                isError = 0
                return isError

    def createShipFleet(self, shipNum):
        shipSize = self.minShipSize
        while len(self.ships) < self.shipNum:
            if shipSize < self.maxShipSize:
                isError = self.createMultiShips(shipSize)
                if isError != 0:
                    shipSize = isError
                else:
                    shipSize += 1
            elif shipSize >= self.maxShipSize:
                self.createMultiShips(shipSize)

    def getGuess(self):
        while True:
            try:
                guess_row = int(raw_input("Guess Row:"))
                guess_col = int(raw_input("Guess Col:"))
                break
            except (TypeError, ValueError):
                printBox("That is not a valid number!")
        if (guess_row < 1 or guess_row > self.boardSize) or (guess_col < 1 or guess_col > self.boardSize):
            printBox("Oops, that's not even in the ocean.")
            return self.getGuess()
        elif (self.board[(guess_row-1)][(guess_col-1)] != "~"):
            printBox("You guessed that one already.")
            return self.getGuess()
        else:
            guessCoords = (guess_row, guess_col)
            return guessCoords

    def checkGuess(self, guessCoords):
        shipNames = {   "2": "Patrol Boat",
                        "3": "Submarine",
                        "4": "Battleship",
                        "5": "Aircraft Carrier",
                }
        guess_row = (guessCoords[0]-1)
        guess_col = (guessCoords[1]-1)
        isHit = [shipCoord for ship in self.ships for shipCoord in ship if shipCoord == guessCoords]
        if isHit:
            hitShip = ([shipCoords for ship in 
                        [ship for ship in self.ships for shipCoord in ship
                        if shipCoord == guessCoords] 
                        for shipCoords in ship])
            shipType = shipNames["%s" % len(hitShip)]
            printBox("You hit my %s!" % shipType)
            self.board[(guess_row)][(guess_col)] = "\033[1m@\033[0m"
            isShipSunk = []
            for shipCoord in hitShip:
                if self.board[(shipCoord[0]-1)][(shipCoord[1]-1)] == "\033[1m@\033[0m":
                    isShipSunk.append(shipCoord)
            if len(isShipSunk) == len(hitShip):
                isSunk = True
            else:
                isSunk = False
            if isSunk:
                self.shipsSunk.append(ship)
                printBox("Good Job! You sunk my %s!" %shipType)
                markShip = [ship for ship in self.ships for shipCoord in ship if shipCoord == guessCoords]
                for shipCoord in markShip[0]:
                    self.board[shipCoord[0]-1][shipCoord[1]-1] = "\033[1m+\033[0m" #marks bold s for ship on map
                if len(self.shipsSunk) == len(self.ships):
                    printBox("Congratulations! You sunk my whole fleet!")
                    return "won"
                return "sunk"
            else:
                return "hit"
        else:
            printBox("You missed!")
            self.board[(guess_row)][(guess_col)] = "\033[1mX\033[0m"            
    
    def startGame(self):
        for i in range(0,boardSize):
            self.board.append(["~"] * boardSize)
        self.createShipFleet(shipNum)

def printBox(printOut):
    """
    This prints things out with a box around them.
    """
    print "#" * 80
    print "%s".center(40, " ") % printOut
    print "#" * 80

def print_board(board):
    #~ if self.boardSize == 5:
        #~ boarderLength = 15
    #~ elif self.boardSize == 9:
        #~ boarderLength = 23
    boarderLength = 15
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

def playAgain():
    newGame = raw_input("Would you like to play again? (y/n)>")
    newGame = newGame.lower()
    if newGame[0] == "y":
        main()
    else:
        exit()

main()

