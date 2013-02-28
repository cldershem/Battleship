####this is here for making notes####

def startGame():
    #build board
    #greeting
    #get number of ships
    #print_board(board)
    #createShips(numShips)
    	
def getGuess(turn):
    #get guesses
    #check that guess isn't crazy
	#return getGuess(turn)
    #else check if already guess
	#print "You guessed that one already."
	#return getGuess(turn)
    #else:
	#set guessCoords
	#ppreturn guessCoords

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
		turn -= 3
		print "TURNS MOTHA!!!!!" + str(turn)
		break
	    else:
		print "Congratulations! You sunk all my battleships!"
		return "won"
        else:
	    if len(ships)-i == 1:
		print "You missed my battleship!"
		board[(guess_row)][(guess_col)] = "\033[1mX\033[0m"
		while turn == 3:
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
		    print str(4-turn-1) + " turns left"
		    print str(len(ships)) + " ships left"
		    print_board(board)
	    else:
		i += 1
		print str(4-turn-1) + " turns left"
		print str(len(ships)) + " ships left"
		print_board(board)

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



def gameEngine():
    turn = 0
    if turn < 4:
	startGame()
	print ships
	guessCoords = getGuess(turn)
        if checkGuess(guessCoords, turn) == "won":
	    exit()
	else:
            pass
