import sys
import threading
import re
from PySide6 import QtCore,QtWidgets,QtGui
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt,QSize


app=QtWidgets.QApplication([])

class Config():

    with open('buddy.config','r') as config:

        animated=config.readline()
        animated=re.split("=",neutral)
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

    def pingsubs(self):
        if widgetdva.isVisible() == True:
            widgetdva.hide()
        else:
            widgetdva.show()
            widgetdva.subtext.setText("Hello User!")
            widgetdva.subsdecay()

widget=マナ()
widget.setMaximumSize(200,281)
widget.setMinimumSize(200,281)
widget.show()
sys.exit(app.exec())