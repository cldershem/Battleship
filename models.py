#!/usr/bin/env python
"""
    models.py

    Objects for battleship.py

    For license, copyright, and author...see TOPMATTER.rst.
"""
import random
import config


class Player(object):
    """
    """

    def __init__(self, name):
        # self.name = raw_input('Name?')
        self.name = name
        self.turns = 5
        self.hits = []
        self.misses = []
        self.sunk = []
        self.board = Board(self.hits, self.misses, self.sunk)
        self.fleet = {
            'patrolBoat': Ship('PatrolBoat'),
            'patrolBoat2': Ship('PatrolBoat'),
            'submarine': Ship('Submarine'),
            'battleship': Ship('Battleship'),
            'aircraftCarrier': Ship('AircraftCarrier'),
            }

    def take_turn(self):
        # print board
        # guess = raw_input("What yo guess?")
        # checked_guess = check_guess(guess)
        # if check_guess(guess) == 'Hit':
        #   hit the board
        #   turn += 3
        # if check_guess(guess) == 'Miss':
        #   miss the board
        #   turn -= 1
        # print results and new board
        pass

    def check_guess(self, guess):
        # for ship in self.fleet:
        #   if ship.is_hit(guess) == 'Hit':
        #       return "Hit"
        #   elif ship.is_hit(guess) == 'Sunk':
        #       return "Sunk"
        #   else:
        #       add coord to miss
        #       return "Miss"
        pass

    def print_board(self):
        print self.board(self.hits, self.misses, self.sunk)

    def __str__(self):
        return str(self.__dict__)


class Board(object):
    """
    """
    chars = {
        'water': "~",
        'miss': "X",
        'hit': "@",
        'sunk': "+",
        'border': "#",
        }

    def __init__(self, hits, misses, sunk):
        self.width = config.BOARD['width']
        self.height = config.BOARD['height']
        self.coords = self.initCoords()

    def initCoords(self):
        coords_dict = {}
        coords = ((i, j) for i in xrange(0, self.width)
                  for j in xrange(0, self.height))
        for coord in coords:
            coordname = coord
            coord = {
                'location': coord,
                'status': 'water',
                }
            coords_dict[coordname] = coord
        return coords_dict

    def show_miss(self):
        pass

    def show_hit(self):
        pass

    def show_sunk(self):
        pass

    def player_status(self):
        pass

    def clear_board(self):
        pass

    def winner_board(self):
        pass

    def loser_board(self):
        pass

    def __str__(self):
        width = self.width
        height = self.height
        border = "{} ".format(Board.chars['border'] * width)
        header = "{}".format(''.join(str(i) for i in xrange(0, width)))

        order = ((i, j) for i in xrange(0, width)
                 for j in xrange(0, height))
        status = (self.coords[coord]['status'] for coord in order)
        char = (Board.chars[char_type] for char_type in status)

        row = []
        for i, c in enumerate(char):
            if i > 0 and (i+1) % width == 0 and (i+1) < width * height:
                c += "\n"
            row.append("{}".format(c))
        row = "{}".format(''.join(str(i) for i in row))

        board = ("{}\n{}\n{}\n{}\n".format(border, header, row, border))
        return board

    def print_board(self):
        width = self.width
        height = self.height
        print '{}'.format(' '.join(Board.chars['border'] * width))
        print '{}'.format(' '.join(str(i) for i in xrange(0, width)))
        for row in xrange(0, height):
            print '{}'.format(' '.join(str(
                Board.chars[self.coords[(row, col)]['status']])
                for col in xrange(0, width)))
        print '{}'.format(' '.join(Board.chars['border'] * width))

    def print_another(self):
        width = self.width
        height = self.height
        border = '{}'.format(''.join(Board.chars['border'] * width))
        header = '{}'.format(''.join(str(i) for i in xrange(0, width)))

        taco = ''
        for row in xrange(0, height):
            for col in xrange(0, width):
                taco += Board.chars[self.coords[(row, col)]['status']]
            if (row, col) != (height-1, width-1):
                taco += '\n'

        return "{}\n{}\n{}\n{}\n".format(border, header, taco, border)


    # def __repr__(self):
        # pass


class Ship(object):
    """
    """

    ships = {
        'PatrolBoat': {
            'name': 'Patrol Boat',
            'length': 2,
            },
        'Submarine': {
            'name': 'Submarine',
            'length': 3,
            },
        'Battleship': {
            'name': 'Battleship',
            'length': 4,
            },
        'AircraftCarrier': {
            'name': 'Aircraft Carrier',
            'length': 5,
            },
        }

    board_width = config.BOARD['width']
    board_height = config.BOARD['height']

    def __init__(self, ship_type):
        self.name = self.ships[ship_type]['name']
        self.length = self.ships[ship_type]['length']
        self.ship_type = ship_type
        self.is_hit = False
        self.is_sunk = False
        self.location = self.place_ship(ship_type)
        self.orientation = random.choice(['N', 'E', 'S', 'W'])

    def place_ship(self, ship_type):
        location = []
        x = random.randint(0, config.BOARD['width'])
        y = random.randint(0, config.BOARD['height'])
        return location.append((x, y))

    def is_sunk(self):
        self.is_sunk = True

    def is_hit(self, guess):
        if guess in self.location:
            #do some hit shit
            # move coord to hit
            # del loc from ship
            if self.is_hit is True:
                #check if sunk
                # move coord to sunk
                # del loc from ship or delete ship?
                return 'Sunk'
            else:
                self.is_hit = True
                return 'Hit'

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return "<Ship({})>".format(self.ship_type)


if __name__ == '__main__':
    # from pprint import pprint

    bob = Player('Bob')
    bob.board.coords[(0, 0)]['status'] = 'hit'
    bob.board.coords[(1, 1)]['status'] = 'miss'
    bob.board.coords[(1, 0)]['status'] = 'sunk'
    bob.board.coords[(3, 4)]['status'] = 'miss'
    # pprint(bob)
    # pprint(bob.fleet)
    print('__str__')
    print(bob.board)
    print('printboard')
    bob.board.print_board()
    print('\nanother')
    print bob.board.print_another()
    # pprint(bob.board.coords)
