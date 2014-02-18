#!/usr/bin/env python
"""
    models.py

    Objects for battleship.py.

    For license, copyright, and author...see TOPMATTER.rst.
"""
import random
import config
import itertools

width = config.BOARD['width']
height = config.BOARD['height']


class Player(object):
    """
    """

    def __init__(self, name):
        self.name = name
        self.turns = 5
        self.hits = []
        self.misses = []
        self.sunk = []
        self.board = Board(self.hits, self.misses, self.sunk)
        self.fleet = {}
        self.make_fleet()
        self.print_ships()
        print self.board

    def print_ships(self):
        for ship in self.fleet:
            print self.fleet[ship].coords

    def take_turn(self):
        if self.turns > 0:
            print(self.name)
            print(self.board)
            guess = self.get_guess()
            result, ship = self.check_guess(guess)
            self.update_player(result)
            self.board.update_board(guess, result)
            if result == 'miss':
                print(self.board)
                return "You missed."
            elif result == 'hit':
                print(self.board)
                return "You hit my {}.".format(ship)
            elif result == 'sunk':
                if len(self.sunk) == len(self.fleet):
                    print(self.board)
                    return "You won."
                else:
                    print(self.board)
                    return "You sunk my {}.".format(ship)
        else:
            return "You lose."

    def get_guess(self):
        while True:
            try:
                row = int(raw_input("row?"))
                col = int(raw_input("col?"))
            except (KeyboardInterrupt, SystemExit):
                raise
            except ValueError:
                print("Invalid entry, yo.")
                continue
            guess = (row, col)
            if not self.in_ocean(guess):
                print "Your guess is out of the ocean, silly."
                self.get_guess()
                break
            else:
                if not self.is_unique(guess):
                    print 'You already guessed that.'
                    self.get_guess()
                    break
                else:
                    return guess

    def in_ocean(self, coord):
        row, col = coord
        if row in xrange(0, width) and col in xrange(0, height):
            return True
        else:
            return False

    def is_unique(self, guess):
        if (guess in itertools.chain(self.misses, self.hits, self.sunk)):
            return False
        else:
            return True

    def make_fleet(self):
        ships = config.SHIPS
        for ship in ships:
            coords = self.place_ship_random(ship)
            # coords = self.place_ship(ship)
            for coord in coords:
                self.board.update_board(coord, 'ship')
            new_ship = Ship(ship, coords)
            self.fleet[new_ship.name] = new_ship

    def place_ship(self, ship):
        # new_ship = []
        # length = config.SHIPS[ship]['length']
        # board = self.board.coords
        # water = ([coord for coord in board
                  # if board[coord]['status'] == 'water'])
        pass

    def place_ship_random(self, ship):
        new_ship = []
        length = config.SHIPS[ship]['length']
        board = self.board.coords
        water = [coord for coord in board if board[coord]['status'] == 'water']
        new_ship.append(random.choice(water))
        # N = (-1, 0), E = (0, 1), S = (1, 0), W = (0, -1)
        orientation = random.choice([(-1, 0), (0, 1), (1, 0), (0, -1)])

        while len(new_ship) < length:
            new_coord = tuple([sum(i) for i in zip(new_ship[-1], orientation)])
            if self.in_ocean(new_coord) and self.ship_is_unique(new_coord):
                new_ship.append(new_coord)
            else:
                self.place_ship_random(ship)
        return new_ship

    def ship_is_unique(self, new_coord):
        """
        Takes a tuple, `new_coord` and returns `True` if no other ship contains
        that coordinate or `False` if it overlaps another ship.
        """
        ship_list = [self.fleet[ship].coords for ship in self.fleet]
        coord_list = list(itertools.chain.from_iterable(ship_list))
        if new_coord in coord_list:
            return False
        else:
            return True

    def update_player(self, checked_guess):
        if checked_guess == 'miss':
            self.turns -= 1
        elif checked_guess == 'hit':
            self.turns += 0
        elif checked_guess == 'sunk':
            self.turns += 2

    def check_guess(self, guess):
        """
        Takes a tuple, `guess`.

        Checks guess against each ship and updates `self.misses`, `self.hits`,
        and `self.sunk` accordingly.  Prints "You sunk my {}" and returns 'hit,
        'miss', or 'sunk'.
        """

        for ship in self.fleet:
            result = self.fleet[ship].check_damage(guess)
            if result != 'miss':
                break
        if result == 'hit':
            self.hits.append(guess)
        elif result == 'sunk':
            self.hits.append(guess)
            self.sunk.append(ship)
        elif result == 'miss':
            self.misses.append(guess)
            ship = None
        return result, ship

    def __str__(self):
        return ("<Player: name={}, turns={}, hits={}, misses={}, "
                "sunk={}>").format(self.name, self.turns, self.hits,
                                   self.misses, self.sunk)

    def __repr__(self):
        return "<Player('{}')>".format(self.name)


class Board(object):
    """
    """
    chars = {
        'water': "~",
        'miss': "X",
        'hit': "@",
        'sunk': "+",
        'border': "#",
        'ship': "S",
        }

    def __init__(self, hits, misses, sunk):
        self.coords = self.initCoords()
        self.hits = hits
        self.misses = misses
        self.sunk = sunk

    def initCoords(self):
        coords_dict = {}
        coords = ((i, j) for i in xrange(0, width)
                  for j in xrange(0, height))
        pass
        for coord in coords:
            coordname = coord
            coord = {
                'location': coord,
                'status': 'water',
                }
            coords_dict[coordname] = coord
        return coords_dict

    def update_board(self, coord, result):
        self.coords[coord]['status'] = result

    def __str__(self):
        border = '{}'.format(' '.join(Board.chars['border'] * width))
        header = '{}'.format(' '.join(str(i) for i in xrange(0, width)))

        board_rows = []
        for row in xrange(0, height):
            board_row = []
            for col in xrange(0, width):
                board_row.append(
                    Board.chars[self.coords[(row, col)]['status']])
            board_rows.append(' '.join(board_row))

        return "{0}\n{1}\n{2}\n{0}\n".format(
            border, header, ('\n'.join(board_rows)))

    def with_lists(self):
        board_rows = []
        board_rows.append([char for char in Board.chars['border'] * width])
        board_rows.append([str(i) for i in xrange(0, width)])

        for row in xrange(0, height):
            board_row = []
            for col in xrange(0, width):
                board_row.append(
                    Board.chars[self.coords[(row, col)]['status']])

        board_rows.append([char for char in Board.chars['border'] * width])
        return '{}'.format('\n'.join([' '.join(char) for char in board_rows]))

    def __repr__(self):
        return "<models.Board(hits={}, misses={}, sunk={})>".format(
               self.hits, self.misses, self.sunk)


class Ship(object):

    ships = config.SHIPS

    def __init__(self, ship_type, coords):
        """
            Takes a string, `ship_type` and creates an object, `Ship` with the
            the specificaiton in the `ships` dict with the following
            parameters:

            `self.name`: String name of the ship, derived from looking up the
                         `ships` dict.
            `self.length`: An integer representing the total length of the
                           ship.
            `self.ship_type`: String representing the type of ship, set to the
                              value that was passed in.
            `self.coords`: A list of tuples representing the locaiton of the
                           ship.
        """
        self.name = self.ships[ship_type]['name']
        self.length = self.ships[ship_type]['length']
        self.ship_type = ship_type
        self.coords = coords

    # def place_ship(self, coords, orientation):
        # """
        # Places ship according to the ships specification in the `ships` dict.
        # It returns a list of coordinates, `coords`.
        # """
        # coords = []
        # for i in xrange(self.length):
            # orientation = random.choice(['N', 'E', 'S', 'W'])
            # row = random.randint(0, width)
            # col = random.randint(0, height)
            # new_coord = (row, col)
            # do math according to orientation
            # if self.is_unique(new_coord):
                # coords.append(new_coord)
            # else:
                # self.place_ship()
        # return coords
        pass

    def check_damage(self, guess):
        """
        Takes a tuple, `guess`, and checks whether `guess` is a hit.  If it
        is a hit it calls the `hit_ship()` method.  It returns `hit`, `sunk`,
        or `miss`.
        """
        if guess in self.coords:
            status = self.hit_ship(guess)
            if status == 'hit':
                return 'hit'
            elif status == 'sunk':
                return 'sunk'
        else:
            return 'miss'

    def hit_ship(self, guess):
        """
        Takes a tuple, `guess` and checks if it was the last hit needed to
        sink the ship.  It returns 'hit' or 'sunk'.
        """
        self.coords.remove(guess)
        if len(self.coords) == 0:
            return 'sunk'
        else:
            return 'hit'

    def __str__(self):
        return "<Ship(ship_type={}, coords={})>".format(
               self.ship_type, self.coords)

    def __repr__(self):
        return "<Ship(name={}, length={}, ship_type={}, coords={}>".format(
            self.name, self.length, self.ship_type, self.coords)


if __name__ == '__main__':  # pragma: no cover
    pass
