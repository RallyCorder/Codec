import sys
import threading
import random
import os
import platform
import subprocess
import re
import paramiko
from PySide6 import QtCore,QtWidgets,QtGui
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap, QAction, QWindow, QScreen
from PySide6.QtCore import Qt, QSize, QObject, QSettings, Slot

app=QtWidgets.QApplication([])
codecwidth=int(QtWidgets.QApplication.primaryScreen().size().width()/5.33)

conf=QSettings('Codec','codec')

conf.value('animated')
conf.value('spritesheet')
conf.sync

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
        if conf.value('animated') == 'True' or conf.value('animated') == 'true':
            stopspeak=threading.Timer(lifetime,speechtech.speechend)
            stopspeak.start()
widgetdva=Subs()
widgetdva.setMaximumHeight(35)
widgetdva.setMinimumHeight(35)

class Codec(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.pixmap=QPixmap(conf.value('spritesheet')).scaledToHeight(codecwidth)
        self.label=QtWidgets.QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.height=self.pixmap.height()
        self.width=self.pixmap.width()//5
        
        self.menubar=QtWidgets.QMenuBar(self)
        actiondd=self.menubar.addMenu('Actions')

        pingact=QtGui.QAction('Ping',self)        
        pingact.triggered.connect(self.pingsubs)
        actiondd.addAction(pingact)

        blinkact=QtGui.QAction('Blink',self)
        blinkact.triggered.connect(blinktech.blinker)
        actiondd.addAction(blinkact)

        netact=QtGui.QAction('Check Network',self)
        netact.triggered.connect(self.satcheck)
        actiondd.addAction(netact)

        useract=QtGui.QAction('Add a command',self)
        useract.triggered.connect(usertech.show)
        actiondd.addAction(useract)

        sshact=QtGui.QAction('Open the SSH picker',self)
        sshact.triggered.connect(sshtech.show)
        actiondd.addAction(sshact)

        conf.beginGroup('Custom')
        if conf.value('usercmd1')!=None:
            self.customdd=self.menubar.addMenu('Custom')
            self.stacker=1
            def miniloop():
                if conf.value('usercmd'+str(self.stacker))!=None:
                    code=compile(conf.value('usercmd'+str(self.stacker)),'<string>','exec')
                    exec(code)
                    self.stacker+=1
                    miniloop()
                else:
                    pass
            miniloop()
        else:
            pass
        conf.endGroup()

        helpdd=self.menubar.addMenu('Help')

        helphelp=QtGui.QAction('Help',self)
        helphelp.triggered.connect(self.helpdocs)
        helpdd.addAction(helphelp)

        abouthelp=QtGui.QAction('About',self)
        abouthelp.triggered.connect(abouttech.show)
        helpdd.addAction(abouthelp)

        self.pseudorandomblink=[1000,5101,6767,5849,4224,4015,3141,2722,6945,1334,5213,6014,3687]

        if conf.value('animated') == 'False' or conf.value('animated') == 'false':
            pass
        if conf.value('animated') == 'True' or conf.value('animated') == 'true':
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
        if conf.value('animated') == 'False' or conf.value('animated') == 'false':
            pass
        if conf.value('animated') == 'True' or conf.value('animated') == 'true':
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

nb=1
class UserCmd(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout=QtWidgets.QGridLayout(self)
        
        self.titlebox=QtWidgets.QTextEdit(self)
        self.titlebox.setPlaceholderText("Insert the command's name")
        self.titlebox.setTabChangesFocus(True)
        self.layout.addWidget(self.titlebox,0,0)
        self.cmdbox=QtWidgets.QTextEdit(self)
        self.cmdbox.setPlaceholderText('Insert a terminal command. If you want a chain of commands, separate them with ''f1'' && ''f2''')
        self.cmdbox.setTabChangesFocus(True)
        self.layout.addWidget(self.cmdbox,1,0)
        self.submit=QtWidgets.QPushButton('Submit')
        self.submit.clicked.connect(self.addusercmd)
        self.layout.addWidget(self.submit,2,0)
        self.nbcap=1

    def addusercmd(self):
        conf.beginGroup('Custom')
        title=usertech.titlebox.toPlainText()
        cmd=usertech.cmdbox.toPlainText()
        cmdin=cmd+'user'
        cmdcleaned=re.sub("\\W","_",cmdin)
        titlecleaned=re.sub("\\W","_",title)
        template= """{1}=QtGui.QAction('{0}',self)
def {3}():
    os.system("{2}")
{1}.triggered.connect({3})
self.customdd.addAction({1})""".format(title,titlecleaned,cmd,cmdcleaned)
        code=compile(template,'<string>','exec')
        def miniloop():
            if conf.value('usercmd'+str(usertech.nbcap))!=None:
                usertech.nbcap+=1
                miniloop()
            else:
                conf.setValue('usercmd'+str(usertech.nbcap),template)
        miniloop()
        conf.endGroup()
        conf.sync()
        os.execv(sys.executable, ['Codec'] + sys.argv)
usertech=UserCmd()
usertech.setFixedSize(codecwidth*2,codecwidth-codecwidth/3)

class SSHAgent(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout=QtWidgets.QGridLayout(self)

        self.ssh=paramiko.SSHClient()

        self.quickbox=QtWidgets.QTextEdit(self)
        self.quickbox.setPlaceholderText("Insert a ssh command 'ssh -p 2222 foo@bar.org'")
        self.layout.addWidget(self.quickbox)
        self.quickbox.setTabChangesFocus(True)
        self.advanced=QtWidgets.QPushButton(self)
        self.advanced.setText('Advanced')
        self.advanced.clicked.connect(self.advancedmenu)
        self.layout.addWidget(self.advanced)
        self.nick=QtWidgets.QPlainTextEdit(self)
        self.nick.setPlaceholderText('Enter a nickname')
        self.layout.addWidget(self.nick)
        self.nick.setTabChangesFocus(True)
        self.nick.hide()
        self.hostaddress=QtWidgets.QPlainTextEdit(self)
        self.hostaddress.setPlaceholderText('Enter the address or hostname')
        self.layout.addWidget(self.hostaddress)
        self.hostaddress.setTabChangesFocus(True)
        self.hostaddress.hide()
        self.username=QtWidgets.QPlainTextEdit(self)
        self.username.setPlaceholderText('Enter the username')
        self.layout.addWidget(self.username)
        self.username.setTabChangesFocus(True)
        self.username.hide()
        self.hostport=QtWidgets.QPlainTextEdit(self)
        self.hostport.setPlaceholderText('Enter the port')
        self.layout.addWidget(self.hostport)
        self.hostport.setTabChangesFocus(True)
        self.hostport.hide()
        self.password=QtWidgets.QPlainTextEdit(self)
        self.password.setPlaceholderText('Enter the password')
        self.layout.addWidget(self.password)
        self.password.setTabChangesFocus(True)
        self.password.hide()
        self.keyButton=QtWidgets.QPushButton(self)
        self.keyButton.clicked.connect(self.openFile)
        self.keyButton.setText('Open a key file')
        self.layout.addWidget(self.keyButton)
        self.keyButton.hide()
        self.key=QtWidgets.QFileDialog(self)
        self.connecter=QtWidgets.QPushButton(self)
        self.connecter.setText('Connect')
        self.connecter.clicked.connect(self.normalconnect)
        self.layout.addWidget(self.connecter)

    def openFile(self):
        self.key.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        self.key=QtWidgets.QFileDialog.getOpenFileUrl()
        print(self.key)

    def normalmenu(self):
        self.quickbox.show()
        self.advanced.setText('Advanced')
        self.advanced.clicked.connect(self.advancedmenu)
        self.connecter.clicked.connect(self.normalconnect)
        self.nick.hide()
        self.hostaddress.hide()
        self.username.hide()
        self.hostport.hide()
        self.password.hide()
        self.keyButton.hide()
        sshtech.setFixedSize(codecwidth*1.15,codecwidth/2.65)

    def advancedmenu(self):
        self.quickbox.hide()
        self.advanced.setText('Normal')
        self.advanced.clicked.connect(self.normalmenu)
        self.connecter.clicked.connect(self.advancedconnect)
        self.nick.show()
        self.hostaddress.show()
        self.username.show()
        self.hostport.show()
        self.password.show()
        self.keyButton.show()
        sshtech.setFixedSize(codecwidth*1.15,codecwidth)

    def normalconnect(self):
        text=sshtech.quickbox.toPlainText()
        os.system(text)

    def advancedconnect(self):
        address=self.hostaddress.toPlainText()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(hostname='sdf.org',port=22,username='new',timeout=500,)
            print("I'm in!")
        except paramiko.SSHException as error:
            widgetdva.show()
            widgetdva.subtext.setText(f"There seems to be an error... [{error}]")
            widgetdva.subsdecay(4)
            speechtech.speech()
            print(f"There seems to be an error...\nSSH Error: {error}")

sshtech=SSHAgent()
sshtech.setFixedSize(codecwidth*1.15,codecwidth/2.65)


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

    if conf.value('animated') == 'False' or conf.value('animated') == 'false':
        pass
    if conf.value('animated') == 'True' or conf.value('animated') == 'true':
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
widget.hide()
sshtech.show()
sys.exit(app.exec())