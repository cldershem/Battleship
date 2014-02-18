#!/usr/bin/env python
# encoding: utf-8
"""
    battleship.py

    A simple battlship game.

    For lisense, copywrite, and author see TOPMATTER.rst
"""
# import config
from utils import clear_terminal  # , bold, print_box
from models import Player  # , Ship, Board


def start_game():
    clear_terminal()
    player1 = Player(raw_input("What is your name?>  "))
    player2 = Player(raw_input("What is your name?>  "))
    # print bold(player1.name)
    # print player1.board
    # print print_box(player2.name)
    # print player2.board

    while True:
        try:
            print player1.take_turn()
            print player2.take_turn()
        except (KeyboardInterrupt, SystemExit):
            raise


if __name__ == '__main__':
    start_game()
