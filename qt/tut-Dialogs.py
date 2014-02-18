#!/usr/bin/env python
# encoding: utf-8

import sys
from PyQt4 import QtGui  # , QtCore

test_img = '/home/cldershem/hg-Python/app/static/img/favicon.png'


# class Example(QtGui.QWidget):
class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()
        # self.initDialog()
        # self.initColor()
        # self.intFont()
        # self.initFile()

    def initDialog(self):
        self.btn = QtGui.QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog1)

        self.le = QtGui.QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')

    def showDialog1(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Diallog',
                                              'Enter your name:')
        if ok:
            self.le.setText(str(text))

    def initColor(self):
        col = QtGui.QColor(0, 0, 0)

        self.btn = QtGui.QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog2)

        self.frm = QtGui.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s}" % col.name())
        self.frm.setGeometry(130, 22, 100, 100)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Color dialog')
        self.show()

    def showDialog2(self):
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                                   % col.name())

    def initFont(self):
        vbox = QtGui.QVBoxLayout()
        btn = QtGui.QPushButton('Dialog', self)
        btn.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        btn.move(20, 20)
        vbox.addWidget(btn)
        btn.clicked.connect(self.showDialog3)

        self.lbl = QtGui.QLabel('Knowledge only matters', self)
        self.lbl.move(130, 20)

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Font dialog')

    def showDialog3(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)

    def initFile(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QtGui.QAction(QtGui.QIcon(test_img), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog4)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')

    def showDialog4(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        f = open(fname, 'r')
        with f:
            data = f.read()
            self.textEdit.setText(data)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
