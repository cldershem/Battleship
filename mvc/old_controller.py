#!/usr/bin/env python
"""
    battleship.py

    A simple battleship game CLI.

    For lisense, copywrite, and author see TOPMATTER.rst
"""
import random
import logging
import config
import utils
# import models


def startGame():
    """
    Starts game by asking user if they want to play SinglePlayer or
    MultiPlayer modes then sends them appropriately.

    Yes, Y, y, yes, YES, y*, No, N, n, no, NO, n* are all valid inputs.
    """
    utils.clear_terminal()
    utils.print_box("Let's play battleship!")
    if config.DEBUG:
        logging.basicConfig(level=logging.debug,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    while True:
        try:
            response = raw_input(
                "Would you like to play single player? (y/n)>").lower()
            if response:
                response = response[0]
                if response == "y":
                    singlePlayer()
                    break
                elif response == "n":
                    multiPlayer()
                    break
                else:
                    utils.print_box("That is not a valid answer!")
            else:
                utils.print_box("That is not a valid answer!")
        except (KeyboardInterrupt, ValueError):
            print ""
            utils.print_box("You're leaving!")
            exit()


def singlePlayer():
    """
    Logic for SinglePlayer game.
    """
    while True:
        try:
            level = raw_input("1. Easy, 2. Medium, or 3. Hard? >").lower()
            if level:
                level = level[0]
                if level in ("1", "e"):
                    level = "Easy"
                    break
                elif level in ("2", "m"):
                    level = "Medium"
                    break
                elif level in ("3", "h"):
                    level = "Hard"
                    break
                else:
                    utils.print_box("That is not a valid level!")
            else:
                utils.print_box("That is not a valid level!")
        except ValueError:
            utils.print_box("That is not a valid level!")
    player = Player("Player", level)
    player.createBoard()
    turns = player.turns
    while turns > 0:
        print player.board
        utils.print_box(str(turns) + " turns left")
        utils.print_box(
            str((len(player.ships))-len(player.shipsSunk)) + " ships left")
        if config.CHEAT:
            count = 1
            for ship in player.ships:
                # print("ship %i %s" % (count, ship))
                print("ship {} {}").format(count, ship)
                count += 1
        guessCoords = player.getGuess()
        turns -= 1
        checkedGuess = player.checkGuess(guessCoords)
        if checkedGuess == "hit":
            turns += 1
        elif checkedGuess == "sunk":
            turns += 3
        elif checkedGuess == "won":
            print player.board
            playAgain()
    else:
        utils.print_box("You missed everytime!")
        utils.print_box("You are out of turns!")
        utils.print_box("Here is the answer:")
        markShip = [shipCoord for ship in player.ships for shipCoord in ship]
        for ship in markShip:
            if ((player.board[ship[0]-1][ship[1]-1] != utils.bold("@")) and
                    (player.board[ship[0]-1][ship[1]-1] != utils.bold("+"))):
                        # marks bold s for ship on map
                        player.board[ship[0]-1][ship[1]-1] = utils.bold("S")
        print player.board
        utils.print_box("Game Over")
    playAgain()


def multiPlayer():
    """
    Creates multiPlayer game.  Loops players through turns until game is won.
    """
    level = "Multi"
    player1 = Player(raw_input("What is Player One's name? >"), level)
    player2 = Player(raw_input("What is Player Two's name? >"), level)
    player1.createBoard()
    player2.createBoard()
    while True:
        if multiPlayerTurn(player1) == "won":
            winner = player1
            loser = player2
            break
        elif multiPlayerTurn(player2) == "won":
            winner = player2
            loser = player1
            break
    print (winner, loser)
    playAgain()


def multiPlayerTurn(player):
    """
    Takes player and has logic for their turn.
    Returns "won" if player has won game.
    """
    utils.print_box(player.name)
    print player.board
    utils.print_box(str((
        len(player.ships))-len(player.shipsSunk)) + " ships left")
    if config.CHEAT:
        count = 1
        for ship in player.ships:
            # print("ship %i %s" % (count, ship))
            print("ship {} {}".format(count, ship))
            count += 1
    guessCoords = player.getGuess()
    checkedGuess = player.checkGuess(guessCoords)
    if checkedGuess == "won":
        return "won"


class Player(object):
    """
    Player class has the following methods:
        createMultiShips()
        createShipFleet()
        getGuess()
        checkGuess()
        createBoards()
    """
    levels = {
        "Easy": {"boardSize": 5,
                 "maxShips": 4,
                 "turns": 4,
                 "minShipSize": 2,
                 "maxShipSize": 4
                 },
        "Medium": {"boardSize": 9,
                   "maxShips": 7,
                   "turns": 5,
                   "minShipSize": 2,
                   "maxShipSize": 5
                   },
        "Hard": {"boardSize": 9,
                 "maxShips": 5,
                 "turns": 4,
                 "minShipSize": 2,
                 "maxShipSize": 5
                 },
        "Multi": {"boardSize": 9,
                  "maxShips": 5,
                  "turns": 4,
                  "minShipSize": 2,
                  "maxShipSize": 5
                  }
        }

    def __init__(self, name, level):
        """
        Takes name and level of player and initializes all variables.
        """
        self.name = name
        self.board = []
        self.ships = []
        self.shipsSunk = []
        self.level = level
        self.boardSize = self.levels[self.level]["boardSize"]
        self.maxShips = self.levels[self.level]["maxShips"]
        self.turns = self.levels[self.level]["turns"]
        self.minShipSize = self.levels[self.level]["minShipSize"]
        self.maxShipSize = self.levels[self.level]["maxShipSize"]
        self.shipNum = self.levels[self.level]["maxShips"]

    def createMultiShips(self, shipSize):
        """
        Takes shipSize from createShipFleet and creates a ship that size.

        Returns 0 for isError if all goes well.
        """
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
        """
        Takes shipNum and creates that many ships.
        """
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
        """
        Gets guess from user trying again if invalid input.

        Returns guessCoords.
        """
        while True:
            try:
                guess_row = int(raw_input("Guess Row:"))
                guess_col = int(raw_input("Guess Col:"))
                break
            except (TypeError, ValueError):
                utils.print_box("That is not a valid number!")
        if ((guess_row < 1 or guess_row > self.boardSize) or
                (guess_col < 1 or guess_col > self.boardSize)):
            utils.print_box("Oops, that's not even in the ocean.")
            return self.getGuess()
        elif (self.board[(guess_row-1)][(guess_col-1)] != "~"):
            utils.print_box("You guessed that one already.")
            return self.getGuess()
        else:
            guessCoords = (guess_row, guess_col)
            return guessCoords

    def checkGuess(self, guessCoords):
        """
        Takes guessCoords and checks if it is a hit.  If it is a hit, checks
        to see if that sunk the ship.  If that sunk the ship, checks to see if
        that was the last ship.

        Returns "miss", "hit", "sunk", "won".
        """
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
            # shipType = shipNames["%s" % len(hitShip)]
            shipType = shipNames["{}".format(len(hitShip))]
            # utils.print_box("You hit my %s!" % shipType)
            utils.print_box("You hit my {}!".format(shipType))
            self.board[(guess_row)][(guess_col)] = utils.bold("@")
            isShipSunk = []
            for shipCoord in hitShip:
                if self.board[(shipCoord[0]-1)][(shipCoord[1]-1)] == (
                        utils.bold("@")):
                    isShipSunk.append(shipCoord)
            if len(isShipSunk) == len(hitShip):
                isSunk = True
            else:
                isSunk = False
            if isSunk:
                self.shipsSunk.append(ship)
                # utils.print_box("Good Job! You sunk my %s!" % shipType)
                utils.print_box("Good Job! You sunk my {}!".format(shipType))
                markShip = [ship for ship in self.ships
                            for shipCoord in ship if shipCoord == guessCoords]
                for shipCoord in markShip[0]:
                    # marks bold s for ship on map
                    self.board[shipCoord[0]-1][shipCoord[1]-1] = (
                        utils.bold("+"))
                if len(self.shipsSunk) == len(self.ships):
                    utils.print_box(
                        "Congratulations! You sunk my whole fleet!")
                    return "won"
                return "sunk"
            else:
                return "hit"
        else:
            utils.print_box("You missed!")
            self.board[(guess_row)][(guess_col)] = utils.bold("X")

    def createBoard(self):
        """
        Creates board for player using the self.boardSize instance variable.
        """
        for i in range(0, self.boardSize):
            self.board.append(["~"] * self.boardSize)
        self.createShipFleet(self.shipNum)


def playAgain():
    """
    Asks if player would like to play again.  Restarts or exits.
    """
    newGame = raw_input("Would you like to play again? (y/n)>").lower()
    if newGame[0] == "y":
        startGame()
    else:
        exit()

if __name__ == "__main__":
    startGame()
