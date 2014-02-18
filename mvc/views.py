#!/usr/bin/env python
# encoding: utf-8

import sys
import signal
# import config
from models import Player  # , Board, Ship
from PyQt4 import QtGui  # , QtCore


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initWin()

    def initWin(self):
        # self.setGeometry(200, 200, 500, 500)
        # self.setMinimumWidth(400)
        self.setWindowTitle('Battleship')
        self.setWindowIcon(QtGui.QIcon(
            '/home/cldershem/hg-Python/app/static/img/favicon.png'))
        self.statusBar()
        self.menu_bar()
        self.place_board()

    def place_board(self):
        self.board = QBoard()
        self.harbor = QHarbor()

        self.mainLayout = QtGui.QGridLayout()
        self.mainLayout.setSpacing(10)
        self.mainLayout.addWidget(self.board, 0, 0, 5, 5)
        self.mainLayout.addWidget(self.harbor, 0, 6, 5, 5)

        # self.mainLayout = QtGui.QHBoxLayout()
        # self.mainLayout.addWidget(self.board)
        # self.mainLayout.addWidget(self.harbor)

        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)

    def menu_bar(self):
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.closeEvent)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def closeEvent(self, event):
        # reply = QtGui.QMessageBox.question(
        #     self, 'Message', "Are you sure to quit?",
        #     QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
        #     QtGui.QMessageBox.No)

        # if reply == QtGui.QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()
        pass

    def set_status(self, message):
        self.statusBar().showMessage(message)


class QBoard(QtGui.QWidget):

    # width = config.BOARD['width']
    # height = config.BOARD['height']

    def __init__(self):
        super(QBoard, self).__init__()
        self.player = Player('bob')
        self.draw_board()

    def draw_board(self):
        grid = QtGui.QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        for coord in self.player.board.coords:
            location = self.player.board.coords[coord]['location']
            button = QtGui.QPushButton()
            button.setFlat(True)
            button.setStyleSheet("border: 1px solid grey")
            button.name = str(coord)
            button.setFixedSize(25, 25)
            grid.addWidget(button, location[0], location[1])

        self.setLayout(grid)
        self.move(300, 150)

    def buttonClicked(self):
        sender = self.sender()
        mainWindow.set_status(sender.name + ' clicked')


class QHarbor(QtGui.QWidget):

    ship_types = [
        'patrolBoat',
        'patrolBoat',
        'submarine',
        'battleship',
        'aircraftCarrier']

    def __init__(self):
        super(QHarbor, self).__init__()
        self.draw_harbor()

    def draw_harbor(self):
        grid = QtGui.QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        for ship in QHarbor.ship_types:
            ship = QShip(ship)
            grid.addWidget(ship)

        self.setLayout(grid)


class QShip(QtGui.QWidget):

    ships = {
        'patrolBoat': 2,
        'submarine': 3,
        'battleship': 4,
        'aircraftCarrier': 5,
        }

    def __init__(self, ship_type):
        super(QShip, self).__init__()
        self.ship_type = ship_type
        self.draw_ship(self.ship_type)

    def draw_ship(self, ship_type):
        ship = QtGui.QGridLayout()
        ship.setHorizontalSpacing(0)
        ship.setVerticalSpacing(0)
        ship.length = QShip.ships[ship_type]

        for j in range(0, ship.length):
            button = QtGui.QPushButton()
            button.setFlat(True)
            button.setStyleSheet("border: 1px solid grey")
            button.setFixedSize(25, 25)
            ship.addWidget(button, j, 0)

        self.setLayout(ship)
        self.move(300, 150)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()

    # qdock = QtGui.QDockWidget()
    # harbor = QHarbor()
    # qdock.setWidget(harbor)
    # mainWindow.addDockWidget(QtCore.Qt.TopDockWidgetArea, qdock)
    # bob = Player('bob')

    mainWindow.show()
    sys.exit(app.exec_())
