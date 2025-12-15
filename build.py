from kivy.uix.sandbox import Context
import sys
import threading
import re
import random
import time
from PySide6 import QtCore,QtWidgets,QtGui
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt,QSize


app=QtWidgets.QApplication([])

class Config():

    with open('buddy.config','r') as config:

        animated=config.readline()
        animated=re.split("=",animated)
        animated.remove("animated")

        neutral=config.readline()
        neutral=re.split("=",neutral)
        neutral.remove("neutral")

        neutral2=config.readline()
        neutral2=re.split("=",neutral2)
        neutral2.remove("neutral2")

        neutral3=config.readline()
        neutral3=re.split("=",neutral3)
        neutral3.remove("neutral3")

Config()

class Subs(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout=QtWidgets.QGridLayout(self)
        self.subtext=QtWidgets.QLabel("")
        self.subtext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.subtext,0,0)

    def subsdecay(self):
        hider=threading.Timer(2,widgetdva.hide)
        hider.start()

widgetdva=Subs()
widgetdva.setMaximumHeight(35)
widgetdva.setMinimumHeight(35)

class マナ(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.pixmap=QPixmap(Config.neutral[0].strip(' \n'))
        self.pixmap1=QPixmap(Config.neutral2[0].strip(' \n'))
        self.label=QtWidgets.QLabel(self)
        self.label.setPixmap(self.pixmap)
        
        
        self.menubar=QtWidgets.QMenuBar(self)
        actiondd=self.menubar.addMenu('Actions')

        pingact=QtGui.QAction('Ping', self)        
        pingact.triggered.connect(self.pingsubs)
        actiondd.addAction(pingact)

        blinkact=QtGui.QAction('Blink',self)
        blinkact.triggered.connect(blinktech.blinker)
        actiondd.addAction(blinkact)

    def pingsubs(self):
        if widgetdva.isVisible() == True:
            widgetdva.hide()
        else:
            widgetdva.show()
            widgetdva.subtext.setText("Hello User!")
            widgetdva.subsdecay()

class Blink(QtWidgets.QWidget):

    def blinker(self):
        widget.pixmap.setPixmap=QPixmap(widget.pixmap)
        swap=threading.Timer(2,blinktech.blinker2)
        swap.start()
        print('1')

    def blinker2(self):
        widget.pixmap.setPixmap(Config.neutral2[0].strip(' \n'))
        swap=threading.Timer(2,blinktech.blinker3)
        swap.start()
        swap.sleep(1)
        swap.cancel()
        print('2')

    def blinker3(self):
        widget.pixmap=QPixmap(Config.neutral3[0].strip(' \n'))
        swap=threading.Timer(2,blinktech.blinker4)
        swap.start()
        print('3')

    def blinker4(self):
        widget.pixmap=QPixmap(Config.neutral2[0].strip(' \n'))
        swap=threading.Timer(2,blinktech.blinker5)
        swap.start()
        print('4')

    def blinker5(self):
        widget.pixmap=QPixmap(Config.neutral[0].strip(' \n'))
        print('5')
        
blinktech=Blink()

widget=マナ()
widget.setMaximumSize(200,281)
widget.setMinimumSize(200,281)
widget.show()
sys.exit(app.exec())