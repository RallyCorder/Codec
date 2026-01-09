import sys
import threading
import re
import random
import os
import platform
import subprocess
from PySide6 import QtCore,QtWidgets,QtGui
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap, QAction, QWindow, QScreen
from PySide6.QtCore import Qt, QSize, QObject

app=QtWidgets.QApplication([])
codecwidth=int(QtWidgets.QApplication.primaryScreen().size().width()/5.33)

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

    def subsdecay(self,lifetime):
        hider=threading.Timer(lifetime,widgetdva.hide)
        hider.start()
        stopspeak=threading.Timer(lifetime,speechtech.speechend)
        stopspeak.start()

widgetdva=Subs()
widgetdva.setMaximumHeight(35)
widgetdva.setMinimumHeight(35)

class Codec(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.pixmap=QPixmap(Config.neutral[0].strip(' \n')).scaledToHeight(codecwidth)
        self.label=QtWidgets.QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.height=self.pixmap.height()
        self.width=self.pixmap.width()//5
        
        self.menubar=QtWidgets.QMenuBar(self)
        actiondd=self.menubar.addMenu('Actions')

        pingact=QtGui.QAction('Ping', self)        
        pingact.triggered.connect(self.pingsubs)
        actiondd.addAction(pingact)

        blinkact=QtGui.QAction('Blink',self)
        blinkact.triggered.connect(blinktech.blinker)
        actiondd.addAction(blinkact)

        netact=QtGui.QAction('Check Network',self)
        netact.triggered.connect(self.satcheck)
        actiondd.addAction(netact)

        helpdd=self.menubar.addMenu('Help')

        helphelp=QtGui.QAction('Help',self)
        helphelp.triggered.connect(self.helpdocs)
        helpdd.addAction(helphelp)

        abouthelp=QtGui.QAction('About',self)
        abouthelp.triggered.connect(abouttech.show)
        helpdd.addAction(abouthelp)

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
            widgetdva.subsdecay(2)
        if Config.animated[0].strip(' \n') == 'False':
            pass
        else:
            speechtech.speech()

    def satcheck(self):
        dishback=os.system("ping -c 1 google.com")
        if dishback == False:
            widgetdva.show()
            widgetdva.subtext.setText("Network Online!")
            widgetdva.subsdecay(2)
            speechtech.speech()
        else:
            widgetdva.show()
            widgetdva.subtext.setText("Huh, it seems you aren't connected...")
            widgetdva.subsdecay(4)
            speechtech.speech()

    def helpdocs(self):
        if platform.system()=='Darwin':
            subprocess.call(('open','docs.md'))
        elif platform.system()=='Windows':
            os.startfile('docs.md')
        else:
            subprocess.call(('xdg-open','docs.md'))

class AboutInfo(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout=QtWidgets.QGridLayout(self)
        self.logo=QPixmap('Andrei_tarkovsky_stamp_russia_2007.jpg')
        self.label=QtWidgets.QLabel(self)
        self.label.setPixmap(self.logo)
        self.label.setGeometry(50,40,200,200)
        self.abouttext=QtWidgets.QLabel("<b><a href='https://github.com/RallyCorder/Codec/'>Codec</a></b>, developped by <a href='https://github.com/RallyCorder/'>RallyCorder</a><br>Built with <a href='https://www.qt.io/development/qt-framework/python-bindings'>Qt6 PySide</a>")
        self.abouttext.setOpenExternalLinks(True)
        self.abouttext.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(self.abouttext)

abouttech=AboutInfo()
abouttech.setFixedSize(codecwidth,codecwidth)

class Blink(QtWidgets.QWidget):

        def blinker(self):
            swap=threading.Timer(0.05,blinktech.blinker2)
            swap.start()

        def blinker2(self):
            widget.label.move(int(-widget.width),0)
            swap=threading.Timer(0.05,blinktech.blinker3)
            swap.start()

        def blinker3(self):
            widget.label.move(int(-widget.width*2),0)
            swap=threading.Timer(0.05,blinktech.blinker4)
            swap.start()

        def blinker4(self):
            widget.label.move(int(-widget.width),0)
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
            widget.label.move(int(-widget.width*3),0)
            global swap
            swap=threading.Timer(random.uniform(0.2,0.5),speechtech.speech2)
            swap.start()
                
        def speech2(self):
            widget.label.move(int(-widget.width*4),0)
            global swapling
            swapling=threading.Timer(random.uniform(0.2,0.5),speechtech.speech)
            swapling.start()

        def speechend(self):
            swap.cancel()
            swapling.cancel()
            widget.label.move(0,0)

speechtech=Dialog()

widget=Codec()
if widget.width > codecwidth:
    widget.setFixedSize(codecwidth,widget.height)
else:
    widget.setFixedSize(widget.width,widget.height)
widget.setWindowTitle('Codec')
widget.show()
sys.exit(app.exec())