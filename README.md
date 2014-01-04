###KNOWN BUGS

###FEATURE REQUESTS
- functions could be a lot smaller
- redo player class
    - player has a
        - board
    - create methods for classes
        - ship.setLocation()
        - ship.getLocation()
        - ship.isAlive()?
- multiplayer
    - sanitize user names?
        - is this even needed?
    - make Turn clearer
        - print Player1 left, Player2 right
            - (80 - len(headerRow))
    - allow players to set their own ships
        - each board belongs to the opposite?
- documentation

###CHANGELOG
- added docstrings, albeit crappy ones.
- cleaned up a few things
    - renamed some methods
    - added if __name__ == "__main__"
- pep8'd this mutha
- added bold()wrapper to clean up "\033[1X\033[0" or what have you
- Reorganized Repo
- added SinglePlayerMode difficulty choice
- added validation for "singlePlayer?"
- cleaned up KeyboardInterrupt
- MultiPlayer - prints both boards at end of game
- MultiPlayer Working
- SinglePlayerMode working
- added classes for multiplayer
- removed singleShip remnants (it will be missed)
- added "You hit my Cruiser"/"Sank my aircraft carrier" style
- added Aircraft Carrier
- adjusted configs
- changed turns when hit
    - hit ship get 1 turn
    - sink ship get 3 turns
- added multi length ship options
- add configuration options
- added debugging logs
- bug fixes
- Sinking a ship gives you extra turns
- changed level to how many ships
- cleaned up output
    - added box around board
    - added box around responses
    - made board have ~ for waves instead of O for ocean
    - added clear screen
- added play again function

###FIXED BUGS
- can hang sometimes in Easy mode
- multiplayer is using levels
- when answer board is printed S covers hits and sunk
- number of ships left never changes
- board border isn't long enough for bigger boards    
- sinking does not print new map
- sinking a ship does not give you extra turns
- printing the S for ship is causing an error - commented
- enter letters exits poorly
- out of ocean on last turn bug
- sinking non-first ship bug    
- always out of ocean bug
- Error on game over with a ship in row or column 5 bug
- error when entering a non number
- randomly ships[] will have extra numbers at end
- can hit ship which is already sunk
- if guess is already hit "you missed"

###MISC NOTES
- list slice
- list comprehension
- save to DB by P1-P2-time
