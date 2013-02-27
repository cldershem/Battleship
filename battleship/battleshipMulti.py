import random

boardOne = []
boardTwo = []
ships = []

def print_board(board):	
    headerRow = []
    count = 1
    for x in board:
	    headerRow.append("%s" % count)
	    count += 1
    print "  " + " ".join(headerRow)
    if board == boardOne and board != boardTwo:
	print "Player One"
    if board == boardTwo:
	print "Player Two"
    count = 1
    for row in board:
	    print str(count) + " " + " ".join(row)
	    count += 1

def createShips(shipNum):
    for i in range(0,shipNum):
        ship_row = random.randint(0,len(board)-1)
        ship_col = random.randint(0,len(board[0])-1)
        shipCoords = [ship_row, ship_col]
	if len(ships) >= 1:
	    for new_i in range(0,len(ships)):
		if shipCoords == ships[new_i]:
		    print "stupid ships match"
		    createShips(shipNum)
		else:
		    ships.append(i)
		    ships[i] = shipCoords
		    break
	else:
	    ships.append(i)
	    ships[i] = shipCoords

def startGame():
    print "Let's play Battleship!"
    numPlayers = int(raw_input("How many players (1 or 2)? >"))
    if numPlayers == 1:
	for x in range(0,5):
	    boardOne.append(["O"] * 5)
	numShips = int(raw_input("What level (1-5, 1 is hardest)? >"))
	if numShips == 0 or numShips > 5:
	    print "Invalid: entry"
	    exit(0)
	else:
	    pass
	print_board(boardOne)
	createShips(numShips)
    elif numPlayers == 2:
	for x in range(0,5):
	    boardOne.append(["O"] * 5)
	    boardTwo.append(["O"] * 5)
	print "two players"
	print_board(boardOne)
	print_board(boardTwo)
    else:
	print "You did not enter a valid number of players."
def getGuess(turn):
    guess_row = input("Guess Row:")
    guess_col = input("Guess Col:")
    try:
	val = int(guess_row)
	val = int(guess_col)
	guessCoords = [guess_row, guess_col]
	return guessCoords
    except ValueError:
	print("You did not enter a number.")
	getGuess(turn)

def checkGuess(guessCoords, turn):
    guess_row = guessCoords[0]
    guess_col = guessCoords[1]
    for i in range(0,len(ships)):
        if guessCoords == ships[i]:
            print "Congratulations! You sunk my battleship!"
	    won = "won"
            return won
        elif turn == 3:
            print "You missed my battleship!"
	    print "You are out of turns!"
            board[(guess_row-1)][(guess_col-1)] = "\033[1mX\033[0m" #marks bold x on map
            print "Here is the answer."
            for i in range(0,len(ships)):
		board[ships[i][0]][ships[i][1]] = "\033[1mS\033[0m"           #makrs bold s for ship on map
            print_board(board)
            print "Game Over"
        else:
            if (guess_row < 0 or guess_row > 5) or (guess_col < 0 or guess_col > 5):
                print "Oops, that's not even in the ocean."
            elif board[(guess_row-1)][(guess_col-1)] == "\033[1mX\033[0m":
                print "You guessed that one already."
            else:
                print "You missed my battleship!"
                board[(guess_row-1)][(guess_col-1)] = "\033[1mX\033[0m"
	    print str(4-turn-1) + " turns left"
	    print_board(board)
	    break

def checkTurns():
    for turn in range(0,4):
	print ships
	guessCoords = getGuess(turn)
	if checkGuess(guessCoords, turn) == "won":
	    break
	else:
	    pass

startGame()
checkTurns()