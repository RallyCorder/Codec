import sys
import threading
import random
import os
import platform
import subprocess
import re
import paramiko
from PySide6 import QtCore,QtWidgets,QtGui
from PySide6.QtWidgets import QApplication, QWidget, QStyle
from PySide6.QtGui import QPixmap, QAction, QWindow, QScreen, QIcon
from PySide6.QtCore import Qt, QSize, QObject, QSettings

app=QtWidgets.QApplication([])
codecwidth=int(QtWidgets.QApplication.primaryScreen().size().width()/5.33)

conf=QSettings('Codec','codec')

conf.value('animated')
conf.value('spritesheet')
conf.value('ssh_known_hosts')
conf.value('ssh_authorized_keys')
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

        sshcact=QtGui.QAction('Add an SSH connection',self)
        sshcact.triggered.connect(sshctech.show)
        actiondd.addAction(sshcact)

        sshpact=QtGui.QAction('Check your SSH connections',self)
        sshpact.triggered.connect(sshptech.show)
        actiondd.addAction(sshpact)

        quitact=QtGui.QAction('Quit',self)
        quitact.triggered.connect(self.quitter)
        actiondd.addAction(quitact)
        quitact.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_Q)

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
        helphelp.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_H)

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

    def quitter(self):
        sys.exit(app.exec())

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

class SSHCAgent(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout=QtWidgets.QGridLayout(self)
        self.quickbox=QtWidgets.QTextEdit(self)
        self.quickbox.setPlaceholderText("Insert a ssh command 'ssh -p 2222 foo@bar.org'")
        self.layout.addWidget(self.quickbox)
        self.quickbox.setTabChangesFocus(True)
        self.advanced=QtWidgets.QPushButton(self)
        self.advanced.setText('Advanced')
        self.advanced.clicked.connect(self.advancedmenu)
        self.layout.addWidget(self.advanced)
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
        self.key=None
        self.connecter=QtWidgets.QPushButton(self)
        self.connecter.setText('Connect')
        self.connecter.clicked.connect(self.normalconnect)
        self.layout.addWidget(self.connecter)

    def openFile(self):
        self.key=QtWidgets.QFileDialog()
        self.key.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        self.key=QtWidgets.QFileDialog.getOpenFileUrl().__str__()
        clear=re.split("'",self.key)
        clear.pop(0)
        for x in range(3):
            clear.pop(1)
        self.key=''.join(clear)
        clearer=re.split('//',self.key)
        clearer.pop(0)
        self.key=''.join(clearer)
        if platform.system()=='Windows':
            cleared=self.key.replace('/','C:\\',1)
        else:
            cleared=self.key

    def normalmenu(self):
        self.quickbox.show()
        self.advanced.setText('Advanced')
        self.advanced.clicked.connect(self.advancedmenu)
        self.connecter.clicked.connect(self.normalconnect)
        self.hostaddress.hide()
        self.username.hide()
        self.hostport.hide()
        self.password.hide()
        self.keyButton.hide()
        sshctech.setFixedSize(codecwidth*1.15,codecwidth/2.65)

    def advancedmenu(self):
        self.quickbox.hide()
        self.advanced.setText('Normal')
        self.advanced.clicked.connect(self.normalmenu)
        self.connecter.clicked.connect(self.advancedconnect)
        self.hostaddress.show()
        self.username.show()
        self.hostport.show()
        self.password.show()
        self.keyButton.show()
        sshctech.setFixedSize(codecwidth*1.15,codecwidth*0.90)

    def normalconnect(self):
        text=sshctech.quickbox.toPlainText()
        os.system(text)

    def advancedconnect(self):
        address=self.hostaddress.toPlainText()
        usernick=self.username.toPlainText()
        passw=self.password.toPlainText()
        portu=self.hostport.toPlainText()
        keyf=self.key
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if portu=='' and keyf=='':
                ssh.connect(hostname=address,username=usernick,password=passw,timeout=3)
            elif keyf=='':
                ssh.connect(hostname=address,username=usernick,password=passw,port=portu,timeout=3)
            elif portu=='':
                ssh.connect(hostname=address,username=usernick,password=passw,key_filename=keyf,timeout=3)
            else:
                ssh.connect(hostname=address,username=usernick,password=passw,port=portu,key_filename=keyf,timeout=3)
            widgetdva.show()
            widgetdva.subtext.setText("I'm in!")
            widgetdva.subsdecay(2)
            speechtech.speech()
            ssh.save_host_keys(conf.value('known_hosts'))
            ssh.close()
        except paramiko.SSHException as error:
            widgetdva.show()
            widgetdva.subtext.setText(f"There seems to be an error... [{error}]")
            widgetdva.subsdecay(4)
            speechtech.speech()
            ssh.close()
            
sshctech=SSHCAgent()
sshctech.setFixedSize(codecwidth*1.15,codecwidth/2.65)

class SSHPAgent(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout=QtWidgets.QGridLayout(self)
        self.knownhostsButton=QtWidgets.QPushButton(self)
        self.knownhostsButton.setText("Open 'known_hosts' file")
        self.knownhostsButton.clicked.connect(self.openKHFile)
        self.layout.addWidget(self.knownhostsButton)
        self.authorizedkeysButton=QtWidgets.QPushButton(self)
        self.authorizedkeysButton.setText("Open 'authorized_keys' file")
        self.authorizedkeysButton.clicked.connect(self.openAKFile)
        self.layout.addWidget(self.authorizedkeysButton)
        self.namebox=QtWidgets.QTextEdit(self)
        self.namebox.setPlaceholderText("Enter a username")
        self.namebox.setTabChangesFocus(True)
        self.layout.addWidget(self.namebox)
        self.namebox.hide()
        self.combox=QtWidgets.QTextEdit(self)
        self.combox.setPlaceholderText("Enter a command to send")
        self.combox.setTabChangesFocus(True)
        self.layout.addWidget(self.combox)
        self.combox.hide()
        self.inputer=QtWidgets.QPushButton(self)
        self.inputer.setText('Login')
        self.layout.addWidget(self.inputer)
        self.inputer.hide()
        self.knownhostsValue=None
        self.authorizedkeysValue=None
        if conf.value('ssh_known_hosts') != '' and conf.value('ssh_authorized_keys') != '':
            self.addUp()
            self.knownhostsValue=conf.value('ssh_known_hosts')
            self.authorizedkeysValue=conf.value('ssh_authorized_keys')

    def openKHFile(self):
        self.authorizedkeysValue=QtWidgets.QFileDialog()
        self.authorizedkeysValue.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        self.authorizedkeysValue=QtWidgets.QFileDialog.getOpenFileUrl().__str__()
        clear=re.split("'",self.authorizedkeysValue)
        clear.pop(0)
        for x in range(3):
            clear.pop(1)
        self.authorizedkeysValue=''.join(clear)
        clearer=re.split('//',self.authorizedkeysValue)
        clearer.pop(0)
        self.authorizedkeysValue=''.join(clearer)
        if platform.system()=='Windows':
            cleared=self.authorizedkeysValue.replace('/','C:\\',1)
        else:
            cleared=self.authorizedkeysValue
        conf.setValue('ssh_known_hosts',self.authorizedkeysValue)
        conf.sync
        os.execv(sys.executable, ['Codec'] + sys.argv)

    def openAKFile(self):
        self.authorizedkeysValue=QtWidgets.QFileDialog()
        self.authorizedkeysValue.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        self.authorizedkeysValue=QtWidgets.QFileDialog.getOpenFileUrl().__str__()
        clear=re.split("'",self.authorizedkeysValue)
        clear.pop(0)
        for x in range(3):
            clear.pop(1)
        self.authorizedkeysValue=''.join(clear)
        clearer=re.split('//',self.authorizedkeysValue)
        clearer.pop(0)
        self.authorizedkeysValue=''.join(clearer)
        if platform.system()=='Windows':
            cleared=self.authorizedkeysValue.replace('/','C:\\',1)
        else:
            cleared=self.authorizedkeysValue
        conf.setValue('ssh_authorized_keys',self.authorizedkeysValue)
        conf.sync
        os.execv(sys.executable, ['Codec'] + sys.argv)

    def addUp(self):
        ssh=paramiko.SSHClient()
        ssh.load_host_keys(conf.value('ssh_known_hosts'))
        x=0
        authkeys=conf.value('ssh_authorized_keys')
        for element in range(len(ssh._host_keys._entries)):
            entryname=ssh._host_keys._entries[x].__str__()
            clearname=re.split("'",entryname)
            clearname.pop(0)
            clearname.pop(1)
            entryname=''.join(clearname)
            entrypkey=ssh._host_keys._entries[x].__str__()
            template="""style=self.style()
online_icon=style.standardIcon(QStyle.StandardPixmap.SP_DialogYesButton)
offline_icon=style.standardIcon(QStyle.StandardPixmap.SP_DialogNoButton)
self.{0}=QtWidgets.QPushButton(self)
check=os.system('ping -c 1 -W 5 {1}')
if check==0:
    self.{0}.setIcon(online_icon)
else:
    self.{0}.setIcon(offline_icon)
self.{0}.setText("{1}")

def loginpart(self):

    def connectsequence(self):

        usernick=sshptech.namebox.toPlainText()
        usercom=sshptech.combox.toPlainText()
        ssh=paramiko.SSHClient()
        ssh.load_host_keys(conf.value('ssh_known_hosts'))
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname='{1}',key_filename='{2}',username=usernick,timeout=500)
            widgetdva.show()
            widgetdva.subtext.setText("I'm in!")
            widgetdva.subsdecay(2)
            speechtech.speech()
            stdin,stdout,stderr=ssh.exec_command(usercom)
            output=stdout.read().decode('utf-8')
            comerror=stderr.read().decode('utf-8')
            if output:
                widgetdva.subtext.setText(output)
                widgetdva.subsdecay(2)
                speechtech.speech()
            if comerror:
                widgetdva.subtext.setText('Error : '+comerror)
                widgetdva.subsdecay(2)
                speechtech.speech()
            ssh.close()
        except paramiko.SSHException as error:
            widgetdva.show()
            widgetdva.subtext.setText(f"There seems to be an error... ["+str(error)+" ]")
            widgetdva.subsdecay(4)
            speechtech.speech()
            ssh.close()

    sshptech.namebox.show()
    sshptech.combox.show()
    sshptech.inputer.show()
    sshptech.inputer.clicked.connect(connectsequence)


self.{0}.clicked.connect(loginpart)
self.layout.addWidget(self.{0})""".format('connection'+str(x),entryname,authkeys)
            code=compile(template,'<string>','exec')
            exec(code)
            x+=1

sshptech=SSHPAgent()
sshptech.setFixedWidth(codecwidth)


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
widget.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint|QtCore.Qt.WindowType.FramelessWindowHint)
widget.setWindowTitle('Codec')
widget.show()
sys.exit(app.exec())