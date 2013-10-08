import random
import os
import logging

cheat = False
debug = False
consoleWidth = 80


def main():
    os.system(['clear', 'cls'][os.name == 'nt'])  # clears terminal
    printBox("Let's play battleship!")
    if debug is True:
        logging.basicConfig(level=logging.DEBUG, format=
                            '%(asctime)s - %(levelname)s - %(message)s')
    while True:
        try:
            single = raw_input("Would you like to play single player? (y/n)>")
            single = single.lower()
            if single[0] == "y":
                singlePlayer()
                break
            elif single[0] == "n":
                multiPlayer()
                break
            else:
                printBox("That is not a valid answer!")
        except KeyboardInterrupt:
            print ""
            printBox("You're leaving!")
            exit()


def singlePlayer():
    while True:
        try:
            level = raw_input("1. Easy, 2. Medium, or 3. Hard? >")
            if level == "1" or level[0].lower() == "e":
                level = "Easy"
                break
            elif level == "2" or level[0].lower() == "m":
                level = "Medium"
                break
            elif level == "3" or level[0].lower() == "h":
                level = "Hard"
                break
            else:
                printBox("That is not a valid level!")
        except ValueError:
            printBox("That is not a valid level!")
    player = Player("Player", level)
    player.startGame()
    turns = player.turns
    while turns > 0:
        print_board(player.board)
        printBox(str(turns) + " turns left")
        printBox(str((len(player.ships))-len(player.shipsSunk))+" ships left")
        if cheat is True:
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
            print_board(player.board)
            playAgain()
    else:
        printBox("You missed everytime!")
        printBox("You are out of turns!")
        printBox("Here is the answer:")
        markShip = [shipCoord for ship in player.ships for shipCoord in ship]
        for ship in markShip:
            if ((player.board[ship[0]-1][ship[1]-1] != bold("@")) and
                    (player.board[ship[0]-1][ship[1]-1] != bold("+"))):
                        # marks bold s for ship on map
                        player.board[ship[0]-1][ship[1]-1] = bold("S")
        print_board(player.board)
        printBox("Game Over")
    playAgain()


def multiPlayer():
    level = "Multi"
    player1 = Player(raw_input("What is Player One's name? >"), level)
    player2 = Player(raw_input("What is Player Two's name? >"), level)
    player1.startGame()
    player2.startGame()
    while True:
        if multiPlayerTurn(player1) == "won":
            winner = player1
            loser = player2
            break
        elif multiPlayerTurn(player2) == "won":
            winner = player2
            loser = player1
            break
        else:
            pass
    printWinner(winner, loser)
    playAgain()
    pass


def multiPlayerTurn(player):
    printBox(player.name)
    print_board(player.board)
    printBox(str((len(player.ships))-len(player.shipsSunk)) + " ships left")
    if cheat is True:
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
    levels = {
        "Easy": {"boardSize": 5,
                 "maxShips": 4,
                 "turns": 4,
                 "minShipSize": 2,
                 "maxShipSize": 4},
        "Medium": {"boardSize": 9,
                   "maxShips": 7,
                   "turns": 5,
                   "minShipSize": 2,
                   "maxShipSize": 5},
        "Hard": {"boardSize": 9,
                 "maxShips": 5,
                 "turns": 4,
                 "minShipSize": 2,
                 "maxShipSize": 5},
        "Multi": {"boardSize": 9,
                  "maxShips": 5,
                  "turns": 4,
                  "minShipSize": 2,
                  "maxShipSize": 5}
        }

    def __init__(self, name, level):
        self.name = name
        self.board = []
        self.ships = []
        self.shipsSunk = []
        #~ self.boardSize = boardSize
        #~ self.maxShips = maxShips
        #~ self.minShipSize = minShipSize
        #~ self.maxShipSize = maxShipSize
        #~ self.shipNum = shipNum
        self.level = level
        self.boardSize = self.levels[self.level]["boardSize"]
        self.maxShips = self.levels[self.level]["maxShips"]
        self.turns = self.levels[self.level]["turns"]
        self.minShipSize = self.levels[self.level]["minShipSize"]
        self.maxShipSize = self.levels[self.level]["maxShipSize"]
        self.shipNum = self.levels[self.level]["maxShips"]

    def createMultiShips(self, shipSize):
        currentShip = []
        shipOrientation = random.choice(["N", "E", "S", "W"])
        ship_row = random.randint(1, self.boardSize)
        ship_col = random.randint(1, self.boardSize)
        shipBow = (ship_row, ship_col)
        currentShip.append(shipBow)
        while len(currentShip) < shipSize:
            if shipOrientation == "N":
                currentShip.append((currentShip[-1][0], currentShip[-1][1]-1))
            elif shipOrientation == "E":
                currentShip.append((currentShip[-1][0]+1, currentShip[-1][1]))
            elif shipOrientation == "S":
                currentShip.append((currentShip[-1][0], currentShip[-1][1]+1))
            elif shipOrientation == "W":
                currentShip.append((currentShip[-1][0]-1, currentShip[-1][1]))
            else:
                logging.debug("Fuck")
        else:  # check for duplicates/out of ocean, then append to self.ships
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
        if ((guess_row < 1 or guess_row > self.boardSize) or
                (guess_col < 1 or guess_col > self.boardSize)):
            printBox("Oops, that's not even in the ocean.")
            return self.getGuess()
        elif (self.board[(guess_row-1)][(guess_col-1)] != "~"):
            printBox("You guessed that one already.")
            return self.getGuess()
        else:
            guessCoords = (guess_row, guess_col)
            return guessCoords

    def checkGuess(self, guessCoords):
        shipNames = {"2": "Patrol Boat",
                     "3": "Submarine",
                     "4": "Battleship",
                     "5": "Aircraft Carrier",
                     }
        guess_row = (guessCoords[0]-1)
        guess_col = (guessCoords[1]-1)
        isHit = [shipCoord for ship in self.ships
                 for shipCoord in ship if shipCoord == guessCoords]
        if isHit:
            hitShip = ([shipCoords for ship in
                       [ship for ship in self.ships for shipCoord in ship
                        if shipCoord == guessCoords]
                        for shipCoords in ship])
            shipType = shipNames["%s" % len(hitShip)]
            printBox("You hit my %s!" % shipType)
            self.board[(guess_row)][(guess_col)] = bold("@")
            isShipSunk = []
            for shipCoord in hitShip:
                if self.board[(shipCoord[0]-1)][(shipCoord[1]-1)] == bold("@"):
                    isShipSunk.append(shipCoord)
            if len(isShipSunk) == len(hitShip):
                isSunk = True
            else:
                isSunk = False
            if isSunk:
                self.shipsSunk.append(ship)
                printBox("Good Job! You sunk my %s!" % shipType)
                markShip = [ship for ship in self.ships
                            for shipCoord in ship if shipCoord == guessCoords]
                for shipCoord in markShip[0]:
                    # marks bold s for ship on map
                    self.board[shipCoord[0]-1][shipCoord[1]-1] = bold("+")
                if len(self.shipsSunk) == len(self.ships):
                    printBox("Congratulations! You sunk my whole fleet!")
                    return "won"
                return "sunk"
            else:
                return "hit"
        else:
            printBox("You missed!")
            self.board[(guess_row)][(guess_col)] = bold("X")

    def startGame(self):
        for i in range(0, self.boardSize):
            self.board.append(["~"] * self.boardSize)
        self.createShipFleet(self.shipNum)


def printBox(printOut):
    leftMargin = (consoleWidth/2)
    """
    This prints things out with a box around them.
    """
    print "#" * consoleWidth
    print "%s".center(leftMargin, " ") % printOut
    print "#" * consoleWidth


def bold(s):
    return "\033[1m" + s + "\033[0m"


def print_board(board):
    headerRow = []
    count = 1
    for col in board:
        headerRow.append("%s" % count)
        count += 1
    if len(headerRow) == 5:
        borderLength = 15
    elif len(headerRow) == 9:
        borderLength = 23
    print "*" * borderLength
    print "*   " + " ".join(headerRow) + " *"
    count = 1
    for row in board:
        print "* " + str(count) + " " + " ".join(row) + " *"
        count += 1
    print "*" * borderLength


def printWinner(winner, loser):
    borderLength = 23
    widthApart = (consoleWidth - (borderLength*2))

    #mark up loser board
    markShip = [shipCoord for ship in loser.ships for shipCoord in ship]
    for ship in markShip:
        if ((loser.board[ship[0]-1][ship[1]-1] != bold("@")) and
                (loser.board[ship[0]-1][ship[1]-1] != bold("+"))):
            loser.board[ship[0]-1][ship[1]-1] = bold("S")
    #prints boards
    nameRow = (winner.name + " " * (consoleWidth - len(winner.name) -
                                    len(loser.name)) + loser.name)
    print "#" * consoleWidth
    print "%s" % nameRow
    print "#" * consoleWidth
    winnerHeader = []
    for col in range(0, len(winner.board[0])):
        winnerHeader.append("%s" % str(col+1))
    loserHeader = []
    for col in range(0, len(loser.board[0])):
        loserHeader.append("%s" % str(col+1))
    print("*" * borderLength + " " * widthApart + "*" * borderLength)
    print("*   " + " ".join(winnerHeader) + " *" + " " * widthApart + "*   " +
          " ".join(loserHeader) + " *")
    for row in range(0, len(winner.board)):
        print("* " + str(row+1) + " " + " ".join(winner.board[row]) + " *" +
              " " * widthApart + "* " + str(row+1) + " " +
              " ".join(loser.board[row]) + " *")
    print("*" * borderLength + " " * widthApart + "*" * borderLength)


def playAgain():
    newGame = raw_input("Would you like to play again? (y/n)>")
    newGame = newGame.lower()
    if newGame[0] == "y":
        main()
    else:
        exit()

main()
