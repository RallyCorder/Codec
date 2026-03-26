import sys
import threading
import random
import os
import platform
import subprocess
import re
import paramiko
from PySide6 import QtCore,QtWidgets,QtGui
from PySide6.QtWidgets import QApplication, QWidget, QStyle, QStyleFactory
from PySide6.QtGui import QPixmap, QAction, QWindow, QScreen, QIcon
from PySide6.QtCore import Qt, QSize, QObject, QSettings
import codec_dev

app=QtWidgets.QApplication([])
icon=QIcon(os.path.dirname(os.path.realpath(__file__))+'/assets/logo.png')
app.setApplicationName('Codec')
app.setApplicationDisplayName('Codec')
app.setWindowIcon(icon)

conf=QSettings('Codec','codec')

conf.value('theme')
conf.value('scale')
conf.value('animated')
conf.value('spritesheet')
conf.value('ssh_known_hosts')
conf.value('ssh_authorised_keys')
conf.sync()

codecwidth=int((QtWidgets.QApplication.primaryScreen().size().width()/5.33)*float(conf.value('scale')))

if conf.value('theme')=='system':
    app.setStyle('qt6ct-style')
if conf.value('theme')=='dark':
    app.setStyle('Adwaita-Dark')
if conf.value('theme')=='light':
    app.setStyle('Adwaita')

class Subs(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout=QtWidgets.QGridLayout(self)
        self.subtext=QtWidgets.QLabel("")
        self.subtext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.subtext,0,0)

    def settext(self,text):
        self.subtext.setText(text)

    def subsdecay(self,lifetime):
        hider=threading.Timer(lifetime,widgetdva.hide)
        hider.start()
        if conf.value('animated') == 'True' or conf.value('animated') == 'true':
            stopspeak=threading.Timer(lifetime,speechtech.speechend)
            stopspeak.start()
widgetdva=Subs()
widgetdva.setFixedHeight(35)
widgetdva.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint|QtCore.Qt.WindowType.FramelessWindowHint)
widgetdva.setWindowTitle('CodecSpeech')

class Codec(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.pixmap=QPixmap(conf.value('spritesheet')).scaledToHeight(codecwidth)
        self.label=QtWidgets.QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.height=self.pixmap.height()
        self.width=self.pixmap.width()//5
        
        self.menubar=QtWidgets.QMenuBar(self)

        actiondd=self.menubar.addMenu('&Actions')

        pingact=QtGui.QAction('&Ping',self)        
        pingact.triggered.connect(self.pingsubs)
        actiondd.addAction(pingact)

        blinkact=QtGui.QAction('&Blink',self)
        blinkact.triggered.connect(blinktech.blinker)
        actiondd.addAction(blinkact)
        blinkact.setShortcut(Qt.Key.Key_Space)

        netact=QtGui.QAction('Check &Network',self)
        netact.triggered.connect(self.satcheck)
        actiondd.addAction(netact)

        useract=QtGui.QAction('Add a &command',self)
        useract.triggered.connect(self.usercmd)
        actiondd.addAction(useract)

        sshcact=QtGui.QAction('&Add an SSH connection',self)
        sshcact.triggered.connect(self.sshc)
        actiondd.addAction(sshcact)

        sshpact=QtGui.QAction('&Check your SSH connections',self)
        sshpact.triggered.connect(self.sshp)
        actiondd.addAction(sshpact)

        settingsact=QtGui.QAction('&Settings',self)
        settingsact.triggered.connect(self.settings)
        actiondd.addAction(settingsact)

        quitact=QtGui.QAction('&Quit',self)
        quitact.triggered.connect(self.quitter)
        actiondd.addAction(quitact)
        quitact.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_Q)

        conf.beginGroup('Custom')
        if conf.value('usercmd1')!=None:
            self.customdd=self.menubar.addMenu('&Custom')
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

        helpdd=self.menubar.addMenu('&Help')

        helphelp=QtGui.QAction('&Help',self)
        helphelp.triggered.connect(self.helpdocs)
        helpdd.addAction(helphelp)
        helphelp.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_H)

        abouthelp=QtGui.QAction('&About',self)
        abouthelp.triggered.connect(self.about)
        helpdd.addAction(abouthelp)
        abouthelp.setShortcut(Qt.Modifier.CTRL | Qt.Key_I)

        self.pseudorandomblink=[1000,5101,6767,5849,4224,4015,3141,2722,6945,1334,5213,6014,3687]

        if conf.value('animated') == 'True' or conf.value('animated') == 'true':
            timer=QtCore.QTimer(self)
            timer.timeout.connect(blinktech.blinker)
            for i in range(442108):
                timer.start(self.pseudorandomblink[0+1])

    def about(self):
        self.abouttech=AboutInfo()
        self.abouttech.show()
        self.abouttech.setWindowTitle('About Codec')
        self.abouttech.setWindowIcon(icon)
        self.abouttech.setFixedSize(codecwidth*1.5,codecwidth)

    def usercmd(self):
        self.usertech=UserCmd()
        self.usertech.show()
        self.usertech.setWindowTitle('Add a user command')
        self.usertech.setWindowIcon(icon)
        self.usertech.setFixedSize(codecwidth*2,codecwidth-codecwidth/3)

    def sshc(self):
        self.sshctech=codec_dev.SSHCAgent(codecwidth)
        self.sshctech.show()
        self.sshctech.setWindowTitle('Add an SSH connection')
        self.sshctech.setWindowIcon(icon)
        self.sshctech.setFixedSize(codecwidth*1.15,codecwidth/2.65)

    def sshp(self):
        self.sshptech=SSHPAgent()
        self.sshptech.show()
        self.sshptech.setWindowTitle('Check your SSH connections')
        self.sshptech.setWindowIcon(icon)
        self.sshptech.setFixedWidth(codecwidth)

    def settings(self):
        self.settingstech=Settings()
        self.settingstech.show()
        self.settingstech.setWindowTitle('Settings')
        self.settingstech.setWindowIcon(icon)
        self.settingstech.setFixedSize(codecwidth*2,codecwidth)

    def pingsubs(self):
        if widgetdva.isVisible() == True:
            widgetdva.hide()
        else:
            widgetdva.show()
            widgetdva.settext("Hello User!")
            widgetdva.subsdecay(2)
        if conf.value('animated') == 'True' or conf.value('animated') == 'true':
            speechtech.speech()

    def satcheck(self):
        dishback=os.system("ping -c 1 google.com")
        if dishback == False:
            widgetdva.show()
            widgetdva.settext("Network Online!")
            widgetdva.subsdecay(2)
            speechtech.speech()
        else:
            widgetdva.show()
            widgetdva.settext("Huh, it seems you aren't connected...")
            widgetdva.subsdecay(4)
            speechtech.speech()

    def helpdocs(self):
        if platform.system()=='Darwin':
            subprocess.call(('open',os.path.dirname(os.path.realpath(__file__))+'/docs.md'))
        elif platform.system()=='Windows':
            os.startfile(os.path.dirname(os.path.realpath(__file__))+'/docs.md')
        else:
            subprocess.call(('xdg-open',os.path.dirname(os.path.realpath(__file__))+'/docs.md'))

    def quitter(self):
        sys.exit(app.exec())

class Settings(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        style=self.style()
        select_icon=style.standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)
        null_icon=style.standardIcon(QStyle.StandardPixmap.SP_CustomBase)
        
        self.layout=QtWidgets.QGridLayout(self)
        self.themelabel=QtWidgets.QLabel('<b>Theme</b>')
        self.spritelabel=QtWidgets.QLabel('<b>Spritesheet</b> *')
        self.animatedlabel=QtWidgets.QLabel('<b>Animations</b> *')
        self.sshauthlabel=QtWidgets.QLabel('<b>SSH Authorised keys</b> *')
        self.sshknownlabel=QtWidgets.QLabel('<b>SSH Known hosts</b> *')
        self.sizelabel=QtWidgets.QLabel('<b>Window size</b> *')
        
        self.animatedswitch=QtWidgets.QCheckBox(self)
        if conf.value('animated') == 'True' or conf.value('animated') == 'true':
            self.animatedswitch.setChecked(True)

        self.themeselect=QtWidgets.QComboBox(self)
        self.themeselect.addItem(null_icon,'System')
        self.themeselect.addItem(null_icon,'Light')
        self.themeselect.addItem(null_icon,'Dark')
        if QApplication.styleHints().colorScheme() == Qt.ColorScheme.Light:
            self.themeselect.setItemIcon(1,select_icon)
        if QApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            self.themeselect.setItemIcon(2,select_icon)
        if QApplication.styleHints().colorScheme() == Qt.ColorScheme.Unknown:
            self.themeselect.setItemIcon(0,select_icon)
            
        self.spritebar=QtWidgets.QPlainTextEdit(self)
        self.spritebar.setPlainText(conf.value('spritesheet'))
        self.spritebar.setTabChangesFocus(True)
        self.spriteplus=QtWidgets.QPushButton(self)
        self.spriteplus.setText('...')
        self.spriteplus.clicked.connect(self.spriteselect)
        
        self.sshauthbar=QtWidgets.QPlainTextEdit(self)
        self.sshauthbar.setPlainText(conf.value('ssh_authorised_keys'))
        self.sshauthbar.setTabChangesFocus(True)
        self.sshauthplus=QtWidgets.QPushButton(self)
        self.sshauthplus.setText('...')
        self.sshauthplus.clicked.connect(self.authselect)

        self.sshknownbar=QtWidgets.QPlainTextEdit(self)
        self.sshknownbar.setPlainText(conf.value('ssh_known_hosts'))
        self.sshknownbar.setTabChangesFocus(True)
        self.sshknownplus=QtWidgets.QPushButton(self)
        self.sshknownplus.setText('...')
        self.sshknownplus.clicked.connect(self.knownselect)

        self.sizebar=QtWidgets.QComboBox(self)
        self.sizebar.addItem(null_icon,'1x')
        self.sizebar.addItem(null_icon,'0.75x')
        self.sizebar.addItem(null_icon,'1.25x')
        self.sizebar.addItem(null_icon,'1.5x')
        self.sizebar.addItem(null_icon,'Custom')
        if conf.value('scale')=='1':
            self.sizebar.setItemIcon(0,select_icon)
        elif conf.value('scale')=='0.75':
            self.sizebar.setItemIcon(1,select_icon)
        elif conf.value('scale')=='1.25':
            self.sizebar.setItemIcon(2,select_icon)
        elif conf.value('scale')=='1.5':
            self.sizebar.setItemIcon(3,select_icon)
        else:
            self.sizebar.setItemIcon(4,select_icon)

        
        self.sizecustom=QtWidgets.QDoubleSpinBox(self)

        self.applybutton=QtWidgets.QPushButton(self)
        self.applybutton.setText('Apply')
        self.applybutton.clicked.connect(self.apply)

        self.cancelbutton=QtWidgets.QPushButton(self)
        self.cancelbutton.setText('Cancel')
        self.cancelbutton.clicked.connect(self.cancel)

        self.restartlabel=QtWidgets.QLabel('* a restart may be required to apply this setting')

        self.layout.addWidget(self.themelabel,0,0)
        self.layout.addWidget(self.themeselect,0,1)
        self.layout.addWidget(self.animatedlabel,1,0)
        self.layout.addWidget(self.animatedswitch,1,1)
        self.layout.addWidget(self.spritelabel,2,0)
        self.layout.addWidget(self.spritebar,2,1)
        self.layout.addWidget(self.spriteplus,2,2)
        self.layout.addWidget(self.sshauthlabel,3,0)
        self.layout.addWidget(self.sshauthbar,3,1)
        self.layout.addWidget(self.sshauthplus,3,2)
        self.layout.addWidget(self.sshknownlabel,4,0)
        self.layout.addWidget(self.sshknownbar,4,1)
        self.layout.addWidget(self.sshknownplus,4,2)
        self.layout.addWidget(self.sizelabel,5,0)
        self.layout.addWidget(self.sizebar,5,1)
        self.layout.addWidget(self.sizecustom,5,2)
        self.layout.addWidget(self.cancelbutton,6,0)
        self.layout.addWidget(self.restartlabel,6,1)
        self.layout.addWidget(self.applybutton,6,2)

    def apply(self):
        if self.themeselect.currentIndex()==0:
            conf.setValue('theme','system')
            app.setStyle('qt6ct-style')
        if self.themeselect.currentIndex()==1:
            conf.setValue('theme','light')
            app.setStyle('Adwaita')
        if self.themeselect.currentIndex()==2:
            conf.setValue('theme','dark')
            app.setStyle('Adwaita-Dark')
        if self.animatedswitch.isChecked()==True:
            conf.setValue('animated','True')
        if self.animatedswitch.isChecked()==False:
            conf.setValue('animated','False')
        conf.setValue('spritesheet',self.spritebar.toPlainText())
        conf.setValue('ssh_authorised_keys',self.sshauthbar.toPlainText())
        conf.setValue('ssh_known_hosts',self.sshknownbar.toPlainText())
        if self.sizebar.currentIndex()==0:
            conf.setValue('scale','1')
        if self.sizebar.currentIndex()==1:
            conf.setValue('scale','0.75')
        if self.sizebar.currentIndex()==2:
            conf.setValue('scale','1.25')
        if self.sizebar.currentIndex()==3:
            conf.setValue('scale','1.5')
        if self.sizebar.currentIndex()==4:
            conf.setValue('scale',self.sizecustom.value())

    def cancel(self):
        self.destroy()

    def spriteselect(self):
        self.selectedSprite=QtWidgets.QFileDialog()
        self.selectedSprite=QtWidgets.QFileDialog.getOpenFileUrl().__str__()
        clear=re.split("'",self.selectedSprite)
        clear.pop(0)
        for x in range(3):
            clear.pop(1)
        self.selectedSprite=''.join(clear)
        clearer=re.split('//',self.selectedSprite)
        clearer.pop(0)
        self.selectedSprite=''.join(clearer)
        if platform.system()=='Windows':
            cleared=self.selectedSprite.replace('/','C:\\',1)
        else:
            cleared=self.selectedSprite
        if self.selectedSprite=='':
            pass
        else:
            self.spritebar.setText(self.selectedSprite)

    def authselect(self):
        self.selectedAuth=QtWidgets.QFileDialog()
        self.selectedAuth=QtWidgets.QFileDialog.getOpenFileUrl().__str__()
        clear=re.split("'",self.selectedAuth)
        clear.pop(0)
        for x in range(3):
            clear.pop(1)
        self.selectedAuth=''.join(clear)
        clearer=re.split('//',self.selectedAuth)
        clearer.pop(0)
        self.selectedAuth=''.join(clearer)
        if platform.system()=='Windows':
            cleared=self.selectedAuth.replace('/','C:\\',1)
        else:
            cleared=self.selectedAuth
        if self.selectedAuth=='':
            pass
        else:
            self.sshauthbar.setText(self.selectedAuth)

    def knownselect(self):
        self.selectedKnown=QtWidgets.QFileDialog()
        self.selectedKnown=QtWidgets.QFileDialog.getOpenFileUrl().__str__()
        clear=re.split("'",self.selectedKnown)
        clear.pop(0)
        for x in range(3):
            clear.pop(1)
        self.selectedKnown=''.join(clear)
        clearer=re.split('//',self.selectedKnown)
        clearer.pop(0)
        self.selectedKnown=''.join(clearer)
        if platform.system()=='Windows':
            cleared=self.selectedKnown.replace('/','C:\\',1)
        else:
            cleared=self.selectedKnown
        if self.selectedKnown=='':
            pass
        else:
            self.sshknownbar.setText(self.selectedKnown)

class AboutInfo(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout=QtWidgets.QGridLayout(self)
        self.logo=QPixmap(os.path.dirname(os.path.realpath(__file__))+'/assets/logo.png')
        self.label=QtWidgets.QLabel(self)
        self.label.setPixmap(self.logo)
        self.label.setGeometry(0,0,256,256)
        self.layout.addWidget(self.label,0,0)
        self.abouttext=QtWidgets.QLabel("<h1><a href='https://github.com/RallyCorder/Codec/'>Codec</a></h1>\n developped by <a href='https://github.com/RallyCorder/'>RallyCorder</a><br>Built with <a href='https://www.qt.io/development/qt-framework/python-bindings'>Qt6 PySide</a>")
        self.abouttext.setOpenExternalLinks(True)
        self.layout.addWidget(self.abouttext,0,1)

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
        title=self.titlebox.toPlainText()
        cmd=self.cmdbox.toPlainText()
        cmdin=cmd+'user'
        cmdcleaned=re.sub("\\W","_",cmdin)
        titlecleaned=re.sub("\\W","_",title)
        template= """{1}=QtGui.QAction('&{0}',self)
def {3}():
    os.system("{2}")
{1}.triggered.connect({3})
self.customdd.addAction({1})""".format(title,titlecleaned,cmd,cmdcleaned)
        try:
            code=compile(template,'<string>','exec')
            def miniloop():
                if conf.value('usercmd'+str(self.nbcap))!=None:
                    self.nbcap+=1
                    miniloop()
                else:
                    conf.setValue('usercmd'+str(self.nbcap),template)
            miniloop()
            conf.endGroup()
            conf.sync()
            os.execv(sys.executable, ['Codec'] + sys.argv)
        except SyntaxError:
            print('Invalid Syntax')

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
        if conf.value('ssh_known_hosts') != '' and conf.value('ssh_authorised_keys') != '':
            self.addUp()
            self.knownhostsValue=conf.value('ssh_known_hosts')
            self.authorizedkeysValue=conf.value('ssh_authorised_keys')
        style=self.style()
        good_icon=style.standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)
        if conf.value('ssh_known_hosts') != '':
            self.knownhostsButton.setIcon(good_icon)
        if conf.value('ssh_authorised_keys') != '':
            self.authorizedkeysButton.setIcon(good_icon)

    def openKHFile(self):
        self.knownhostsValue=QtWidgets.QFileDialog()
        self.knownhostsValue=QtWidgets.QFileDialog.getOpenFileUrl().__str__()
        clear=re.split("'",self.knownhostsValue)
        clear.pop(0)
        for x in range(3):
            clear.pop(1)
        self.knownhostsValue=''.join(clear)
        clearer=re.split('//',self.knownhostsValue)
        clearer.pop(0)
        self.knownhostsValue=''.join(clearer)
        if platform.system()=='Windows':
            cleared=self.knownhostsValue.replace('/','C:\\',1)
        else:
            cleared=self.knownhostsValue
        conf.setValue('ssh_known_hosts',self.knownhostsValue)
        conf.sync()
        os.execv(sys.executable, ['Codec'] + sys.argv)

    def openAKFile(self):
        self.authorizedkeysValue=QtWidgets.QFileDialog()
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
        conf.setValue('ssh_authorised_keys',self.authorizedkeysValue)
        conf.sync()
        os.execv(sys.executable, ['Codec'] + sys.argv)

    def addUp(self):
        ssh=paramiko.SSHClient()
        ssh.load_host_keys(conf.value('ssh_known_hosts'))
        x=0
        authkeys=conf.value('ssh_authorised_keys')
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
check=os.system('ping -c 1 -W 1 {1}')
if check==0:
    self.{0}.setIcon(online_icon)
else:
    self.{0}.setIcon(offline_icon)
self.{0}.setText("{1}")

def loginpart(self):

    def connectsequence(self):

        usernick=self.namebox.toPlainText()
        usercom=self.combox.toPlainText()
        ssh=paramiko.SSHClient()
        ssh.load_host_keys(conf.value('ssh_known_hosts'))
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname='{1}',key_filename='{2}',username=usernick,timeout=500)
            widgetdva.show()
            widgetdva.settext("I'm in!")
            widgetdva.subsdecay(2)
            speechtech.speech()
            stdin,stdout,stderr=ssh.exec_command(usercom)
            output=stdout.read().decode('utf-8')
            comerror=stderr.read().decode('utf-8')
            if output:
                widgetdva.settext(output)
                widgetdva.subsdecay(2)
                speechtech.speech()
            if comerror:
                widgetdva.settext('Error : '+comerror)
                widgetdva.subsdecay(2)
                speechtech.speech()
            ssh.close()
        except paramiko.SSHException as error:
            widgetdva.show()
            widgetdva.settext(f"There seems to be an error... ["+str(error)+" ]")
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
    widget.setFixedSize(codecwidth*conf.value('scale'),widget.height)
else:
    widget.setFixedSize(widget.width,widget.height)
widget.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint|QtCore.Qt.WindowType.FramelessWindowHint)
widget.setWindowTitle('Codec')
widget.setWindowIcon(icon)
widget.show()
sys.exit(app.exec())