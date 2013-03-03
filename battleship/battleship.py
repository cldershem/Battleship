import random

board = []
ships = []

def main():
    printBox("Let's play battleship!")
    startGame()

def printBox(printOut):
    print "#" * 50
    #print "#" * (len(printOut)+30)
    #print "%s" % printOut
    print "%s".center(30, " ") % printOut
    print "#" * 50

def print_board(board):
    print "***************"
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
    print "***************"

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
    del board[0:len(board)]
    del ships[0:len(ships)]
    try:
	numShips = int(raw_input("How many ships (1-5)? >"))
    except ValueError:
	printBox("That is not a valid number!")
	startGame()
    if numShips <= 0 or numShips > 5:
	printBox("That is not a valid number!")
	startGame()
    for i in range(0,5):
	board.append(["~"] * 5)
    createShips(numShips)
    checkTurn(4)
    	
def getGuess(turn):
    guess_row = int(raw_input("Guess Row:"))
    guess_col = int(raw_input("Guess Col:"))
    if (guess_row < 1 or guess_row > 5) or (guess_col < 1 or guess_col > 5):
	printBox("Oops, that's not even in the ocean.")
	return getGuess(turn)
    elif board[(guess_row-1)][(guess_col-1)] == "\033[1mX\033[0m":
	printBox("You guessed that one already.")
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
                printBox("Congratulations! You sunk my battleship!")
		board[(guess_row)][(guess_col)] = "\033[1m-\033[0m"
		turn += 3
                checkTurn(turn)
	    else:
		printBox("Congratulations! You sunk all my battleships!")
                #exit()
		playAgain()
        else:
	    if len(ships)-i == 1:
		printBox("You missed my battleship!")
		board[(guess_row)][(guess_col)] = "\033[1mX\033[0m"
		if turn == 0:
		    printBox("You missed everytime!")
		    printBox("You are out of turns!")
		    board[(guess_row)][(guess_col)] = "\033[1mX\033[0m"	#marks bold x on map
		    printBox("Here is the answer.")
		    for i in range(0,len(ships)):
			board[ships[i][0]-1][ships[i][1]-1] = "\033[1mS\033[0m"		#marks bold s for ship on map
		    print_board(board)
		    printBox("Game Over")
		    #exit()
		    playAgain()
		else:
                    checkTurn(turn)
	    else:
		i += 1

def checkTurn(turn):
    if turn > 0:
        print_board(board)
        printBox(str(turn) + " turns left")
	printBox(str(len(ships)) + " ships left")
	print ships
	guessCoords = getGuess(turn)
        turn -= 1
	checkGuess(guessCoords, turn)
    else:
        print "Yeah, that happened."

def playAgain():
    newGame = raw_input("Would you like to play again? (y/n)>")
    newGame = newGame.lower()
    if newGame[0] == "y":
	#clear old game
	main()
    else:
	exit()

main()
