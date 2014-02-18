#!/usr/bin/env python
# encoding: utf-8
import os
import config


def clear_terminal():
    """
    Clears terminal screen.
    """
    os.system(['clear', 'cls'][os.name == 'nt'])


def bold(s):
    """
    Takes a string and returns it in it's bold form for display in a console.
    """
    return "\033[1m" + s + "\033[0m"


def print_box(printOut):
    """
    Takes string and prints it to stdout with a box of "#" around it.
    """
    leftMargin = (config.CONSOLE_WIDTH/2)
    print("#" * config.CONSOLE_WIDTH)
    # print "%s".center(leftMargin, " ") % printOut
    print("{}".center(leftMargin, " ").format(printOut))
    print("#" * config.CONSOLE_WIDTH)
