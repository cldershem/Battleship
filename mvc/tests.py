#!/usr/bin/env python
"""
    tests.py

    Tests for battleship.py.

    For license, copyright, and author...see TOPMATTER.rst
"""
import unittest
from models import Player, Board, Ship
import config


class ConfigTests(unittest.TestCase):

    def test_config(self):
        self.assertEqual(config.BOARD['width'], 5)
        self.assertEqual(config.BOARD['height'], 5)


class PlayerTests(unittest.TestCase):

    def setUp(self):
        self.bob = Player('Bob')
        self.bob.fleet['patrolBoat'].coords = [(0, 1), (0, 2)]
        self.bob.fleet['patrolBoat2'].coords = [(4, 5), (0, 4)]
        self.bob.fleet['submarine'].coords = [(4, 5), (0, 4)]
        self.bob.fleet['battleship'].coords = [(4, 5), (0, 4)]
        self.bob.fleet['aircraftCarrier'].coords = [(4, 5), (0, 4)]

    def test_player_init(self):
        self.assertEqual(self.bob.name, 'Bob')
        self.assertEqual(self.bob.turns, 5)
        self.assertEqual(self.bob.hits, [])
        self.assertEqual(self.bob.misses, [])
        self.assertEqual(self.bob.sunk, [])
        self.assertTrue(isinstance(self.bob.board, Board))
        self.assertEqual(self.bob.__repr__(), "<Player('Bob')>")
        self.assertEqual(self.bob.__str__(), ("<Player: name=Bob, turns=5, "
                                              "hits=[], misses=[], sunk=[]>"))

    def test_player_fail(self):
        self.assertNotEqual(self.bob.name, 'Sally')

    def test_player_board(self):
        self.assertEqual(self.bob.board.width, config.BOARD['width'])
        self.assertEqual(self.bob.board.height, config.BOARD['height'])

    def test_player_ships(self):
        self.assertTrue(isinstance(self.bob.fleet['patrolBoat'], Ship))
        self.assertTrue(isinstance(self.bob.fleet['patrolBoat2'], Ship))
        self.assertTrue(isinstance(self.bob.fleet['submarine'], Ship))
        self.assertTrue(isinstance(self.bob.fleet['battleship'], Ship))
        self.assertTrue(isinstance(self.bob.fleet['aircraftCarrier'], Ship))
        # check that ships are valid

    def test_check_guess(self):
        self.assertEqual(self.bob.check_guess((1, 1)), ('miss', None))
        self.assertEqual(self.bob.misses, [(1, 1)])

        self.assertEqual(self.bob.check_guess((0, 1)), ('hit', 'patrolBoat'))
        self.assertEqual(self.bob.hits, [(0, 1)])

        self.assertEqual(self.bob.check_guess((4, 4)), ('miss', None))
        self.assertEqual(self.bob.misses, [(1, 1), (4, 4)])

        self.assertEqual(self.bob.check_guess((0, 2)), ('sunk', 'patrolBoat'))
        self.assertEqual(self.bob.sunk, ['patrolBoat'])
        self.assertIn((0, 2), self.bob.hits)

    def test_update_player(self):
        self.assertEqual(self.bob.turns, 5)
        self.bob.update_player('miss')
        self.assertEqual(self.bob.turns, 4)
        self.bob.update_player('hit')
        self.assertEqual(self.bob.turns, 4)
        self.bob.update_player('sunk')
        self.assertEqual(self.bob.turns, 6)
        self.bob.update_player('miss')
        self.assertEqual(self.bob.turns, 5)
        self.bob.update_player('miss')
        self.assertEqual(self.bob.turns, 4)
        self.bob.update_player('miss')
        self.assertEqual(self.bob.turns, 3)
        self.bob.update_player('miss')
        self.assertEqual(self.bob.turns, 2)
        self.bob.update_player('miss')
        self.assertEqual(self.bob.turns, 1)
        self.bob.update_player('miss')
        self.assertEqual(self.bob.turns, 0)

    def test_get_guess(self):
        # self.bob.get_guess = lambda: ''
        # self.assertEqual(self.bob.get_guess(), '')
        self.assertTrue(self.bob.is_unique((0, 1)))
        self.bob.misses.append((0, 1))
        self.assertFalse(self.bob.is_unique((0, 1)))
        self.assertTrue(self.bob.in_ocean((0, 1)))
        self.assertFalse(self.bob.in_ocean((0, 11)))

    def test_take_turn(self):
        self.bob.get_guess = lambda: (0, 0)
        self.assertEqual(self.bob.take_turn(), 'You missed.')
        self.bob.get_guess = lambda: (0, 1)
        self.assertEqual(self.bob.take_turn(), 'You hit my patrolBoat.')
        self.bob.get_guess = lambda: (0, 2)
        self.assertEqual(self.bob.take_turn(), 'You sunk my patrolBoat.')

    def test_lose(self):
        self.bob.get_guess = lambda: (0, 2)
        self.bob.turns = 0
        self.assertEqual(self.bob.take_turn(), 'You lose.')

    def test_won(self):
        self.bob.turns = 1
        self.bob.sunk = [(), (), (), ()]
        self.bob.get_guess = lambda: (0, 1)
        self.assertEqual(self.bob.take_turn(), 'You hit my patrolBoat.')
        self.bob.get_guess = lambda: (0, 2)
        self.assertEqual(self.bob.take_turn(), 'You won.')


class ShipTests(unittest.TestCase):

    def setUp(self):
        self.ship = Ship('PatrolBoat')

    def test_ship_init(self):
        self.assertEqual(self.ship.name, 'Patrol Boat')
        self.assertEqual(self.ship.length, 2)
        self.assertEqual(self.ship.ship_type, 'PatrolBoat')
        self.assertTrue(len(self.ship.coords) == self.ship.length)
        self.ship.coords = [(0, 1), (0, 2)]
        self.assertEqual(self.ship.__str__(), "<Ship(ship_type=PatrolBoat, "
                         "coords=[(0, 1), (0, 2)])>")
        self.assertEqual(self.ship.__repr__(), "<Ship(name=Patrol Boat, "
                         "length=2, ship_type=PatrolBoat, coords=[(0, 1), "
                         "(0, 2)]>")

    def test_location(self):
        self.assertTrue(self.ship.coords[0][0] in range(0,
                        config.BOARD['width']+1))
        self.assertTrue(self.ship.coords[0][1] in range(0,
                        config.BOARD['height']+1))

    def test_loc_overlap(self):
        pass

    def test_check_damage(self):
        self.ship.coords = [(0, 1), (0, 2)]
        self.assertEqual(self.ship.check_damage((1, 1)), 'miss')
        self.assertEqual(self.ship.check_damage((0, 1)), 'hit')
        self.assertEqual(self.ship.check_damage((4, 4)), 'miss')
        self.assertEqual(self.ship.check_damage((0, 2)), 'sunk')

    def test_sink_ship(self):
        self.assertIsNone(self.ship.sink_ship())


class BoardTests(unittest.TestCase):

    def setUp(self):
        self.bob = Player('Bob')
        self.bob.fleet['patrolBoat'].coords = [(0, 1), (0, 2)]
        self.bob.fleet['patrolBoat2'].coords = [(4, 5), (0, 4)]
        self.bob.fleet['submarine'].coords = [(4, 5), (0, 4)]
        self.bob.fleet['battleship'].coords = [(4, 5), (0, 4)]
        self.bob.fleet['aircraftCarrier'].coords = [(4, 5), (0, 4)]

    def test_board_init(self):
        board = Board([], [], [])
        self.assertEqual(board.width, 5)
        self.assertEqual(board.height, 5)
        self.assertEqual(board.__str__(), (
            "# # # # #\n0 1 2 3 4\n"
            "~ ~ ~ ~ ~ \n~ ~ ~ ~ ~ \n"
            "~ ~ ~ ~ ~ \n~ ~ ~ ~ ~ \n~ ~ ~ ~ ~ \n# # # # #\n"))
        self.assertEqual(board.__repr__(), (
            "<models.Board(hits=[], misses=[], sunk=[])>"))

    def test_update_board(self):
        self.bob.fleet['patrolBoat'].coords = [(0, 1), (0, 2)]
        self.assertEqual(self.bob.board.coords[(0, 1)]['status'], 'water')
        self.bob.board.update_board((0, 1), 'miss')
        self.assertEqual(self.bob.board.coords[(0, 1)]['status'], 'miss')
        self.bob.get_guess = lambda: (0, 3)
        self.assertEqual(self.bob.take_turn(), 'You missed.')
        self.assertEqual(self.bob.board.coords[(0, 3)]['status'], 'miss')

    def test_print_winner(self):
        self.assertIsNone(self.bob.board.print_winner_board())

    def test_print_loser(self):
        self.assertIsNone(self.bob.board.print_loser_board())

if __name__ == '__main__':
    unittest.main()
