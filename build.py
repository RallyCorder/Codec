import sys
import threading
import re
import random
from PySide6 import QtCore,QtWidgets,QtGui
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap, QAction, QWindow, QScreen
from PySide6.QtCore import Qt, QSize, QObject

app=QtWidgets.QApplication([])

class Config():

    with open('buddy.config','r') as config:

        animated=config.readline()
        animated=re.split("=",animated)
        animated.remove("animated")

        neutral=config.readline()
        neutral=re.split("=",neutral)
        neutral.remove("neutral")

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
        stopspeak=threading.Timer(2,speechtech.speechend)
        stopspeak.start()

widgetdva=Subs()
widgetdva.setMaximumHeight(35)
widgetdva.setMinimumHeight(35)

class マナ(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.pixmap=QPixmap(Config.neutral[0].strip(' \n'))
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

        self.pseudorandomblink=[1000,5101,6767,5849,4224,4015,3141,2722,6945,1334,5213,6014,3687]

        if Config.animated[0].strip(' \n') == 'False':
            pass
        else:
            timer=QtCore.QTimer(self)
            timer.timeout.connect(blinktech.blinker)
            for i in range(442108):
                timer.start(self.pseudorandomblink[0+1])

    def pingsubs(self):
        if widgetdva.isVisible() == True:
            widgetdva.hide()
        else:
            widgetdva.show()
            widgetdva.subtext.setText("Hello User!")
            widgetdva.subsdecay()
        if Config.animated[0].strip(' \n') == 'False':
            pass
        else:
            speechtech.speech()

class Blink(QtWidgets.QWidget):

        def blinker(self):
            swap=threading.Timer(0.05,blinktech.blinker2)
            swap.start()

        def blinker2(self):
            widget.label.move(-200,0)
            swap=threading.Timer(0.05,blinktech.blinker3)
            swap.start()

        def blinker3(self):
            widget.label.move(-400,0)
            swap=threading.Timer(0.05,blinktech.blinker4)
            swap.start()

        def blinker4(self):
            widget.label.move(-200,0)
            swap=threading.Timer(0.05,blinktech.blinker5)
            swap.start()

        def blinker5(self):
            widget.label.move(0,0)
        
blinktech=Blink()

class Dialog(QtWidgets.QWidget):

    if Config.animated[0].strip(' \n') == 'False':
        pass
    else:
        def speech(self):
            widget.label.move(-600,0)
            global swap
            swap=threading.Timer(random.uniform(0.2,0.5),speechtech.speech2)
            swap.start()
                
        def speech2(self):
            widget.label.move(-800,0)
            global swapling
            swapling=threading.Timer(random.uniform(0.2,0.5),speechtech.speech)
            swapling.start()

        def speechend(self):
            swap.cancel()
            swapling.cancel()
            widget.label.move(0,0)

speechtech=Dialog()

widget=マナ()
width=widget.pixmap.width()//5
height=widget.pixmap.height()
widget.setFixedSize(width,height)
widget.show()
widget.setWindowTitle('Codec')
sys.exit(app.exec())