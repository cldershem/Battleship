#!/usr/bin/env python
# encoding: utf-8

import sys
import signal
from PyQt4 import QtGui  # QtCore


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.board = Board().show()
        self.initWin()

    def initWin(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Battleship')
        self.setWindowIcon(QtGui.QIcon(
            '/home/cldershem/hg-Python/app/static/img/favicon.png'))
        self.statusBar()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(
            self, 'Message', "Are you sure to quit?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def add_menu(self):
        exitAction = QtGui.QAction(QtGui.QIcon(
            '/home/cldershem/hg-Python/app/static/img/favicon.png'
            ), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.closeEvent)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menubr')


class Board(QtGui.QWidget):

    def __init__(self):
        super(Board, self).__init__()

        # self.initUI()
        self.initBoard()

    def initUI(self):

        self.add_menu()

    def initBoard(self):

        grid = QtGui.QGridLayout()

        pos = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
               (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
               (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
               (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
               (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]

        for i, j in enumerate(range(0, 4)):
            button = QtGui.QPushButton(str(i))
            grid.addWidget(button, pos[j][0], pos[j][1])
            button.clicked.connect(self.buttonClicked)

        self.setLayout(grid)
        self.move(300, 150)

    def buttonClicked(self):
        # sender = self.sender()
        # self.statusBar().showMessage(sender.text() + ' clicked')
        pass


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
