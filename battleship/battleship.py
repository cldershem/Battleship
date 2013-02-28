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
    for x in range(0,5):
	board.append(["O"] * 5)
    print "Let's play Battleship!"
    numShips = int(raw_input("What level (1-5, 1 is hardest)? >"))
    if numShips == 0 or numShips > 5:
	print "Invalid: entry"
	exit(0)
    else:
	pass
    print_board(board)
    createShips(numShips)
    	
def getGuess(turn):
    guess_row = input("Guess Row:")
    guess_col = input("Guess Col:")
    if (guess_row < 1 or guess_row > 5) or (guess_col < 1 or guess_col > 5):
	print "Oops, that's not even in the ocean."
	print "turn" + str(turn)
	print "row" + str(guess_row)
	print "col" + str(guess_col)
	return getGuess(turn)
    else:
	guessCoords = [guess_row, guess_col]
	print "end of getGuess" + str(guessCoords)
	return guessCoords

def checkGuess(guessCoords, turn):
    guess_row = guessCoords[0]-1
    guess_col = guessCoords[1]-1
    for i in range(0,len(ships)):
        if guessCoords == ships[i]:
            print "Congratulations! You sunk my battleship!"
	    won = "won"
            return won
        elif turn == 3:
            print "You missed everytime!"
	    print "You are out of turns!"
            board[(guess_row)][(guess_col)] = "\033[1mX\033[0m" #marks bold x on map
            print "Here is the answer."
            for i in range(0,len(ships)):
		board[ships[i][0]][ships[i][1]] = "\033[1mS\033[0m"           #makrs bold s for ship on map
            print_board(board)
            print "Game Over"
        else:
            if board[(guess_row)][(guess_col)] == "\033[1mX\033[0m":
                print "You guessed that one already."
            else:
                print "You missed my battleship!"
                board[(guess_row)][(guess_col)] = "\033[1mX\033[0m"
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
