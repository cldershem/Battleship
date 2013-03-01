import random

board = []
ships = []

def print_board(board):	
    headerRow = []
    count = 1
    for x in board:
	    headerRow.append("%s" % count)
	    count += 1
    print "  " + " ".join(headerRow)
    count = 1
    for row in board:
	    print str(count) + " " + " ".join(row)
	    count += 1

def createShips(shipNum):
    for i in range(0,shipNum):
        ship_row = random.randint(1,len(board))
        ship_col = random.randint(1,len(board[0]))
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
    try:
	numShips = int(raw_input("How many ships (1-5)? >"))
    except ValueError:
	print "That is not a valid number!"
	startGame()
    if numShips <= 0 or numShips > 5:
	print "That is not a valid number!"
	startGame()
    for i in range(0,5):
	board.append(["O"] * 5)
    createShips(numShips)
    checkTurn(4)
    	
def getGuess(turn):
    guess_row = int(raw_input("Guess Row:"))
    guess_col = int(raw_input("Guess Col:"))
    if (guess_row < 1 or guess_row > 5) or (guess_col < 1 or guess_col > 5):
	print "Oops, that's not even in the ocean."
	return getGuess(turn)
    elif board[(guess_row-1)][(guess_col-1)] == "\033[1mX\033[0m":
	print "You guessed that one already."
	return getGuess(turn)
    else:
	guessCoords = [guess_row, guess_col]
	return guessCoords

def checkGuess(guessCoords, turn):
    guess_row = guessCoords[0]-1
    guess_col = guessCoords[1]-1
    for i in range(0,len(ships)):
        if guessCoords == ships[i]:
	    del ships[i]
	    i -= 1
	    if len(ships) > 0:
                print "Congratulations! You sunk my battleship!"
		board[(guess_row)][(guess_col)] = "\033[1m-\033[0m"
		turn += 3
                checkTurn(turn)
	    else:
		print "Congratulations! You sunk all my battleships!"
                exit()
        else:
	    if len(ships)-i == 1:
		print "You missed my battleship!"
		board[(guess_row)][(guess_col)] = "\033[1mX\033[0m"
		if turn == 0:
		    print "You missed everytime!"
		    print "You are out of turns!"
		    board[(guess_row)][(guess_col)] = "\033[1mX\033[0m"	#marks bold x on map
		    print "Here is the answer."
		    for i in range(0,len(ships)):
			board[ships[i][0]][ships[i][1]] = "\033[1mS\033[0m"		#marks bold s for ship on map
		    print_board(board)
		    print "Game Over"
		    exit()
		else:
                    checkTurn(turn)
	    else:
		i += 1

def checkTurn(turn):
    if turn > 0:
        print str(turn) + " turns left"
	print str(len(ships)) + " ships left"
        print_board(board)
	print ships
	guessCoords = getGuess(turn)
        turn -= 1
	checkGuess(guessCoords, turn)
    else:
        print "Yeah, that happened."

startGame()
