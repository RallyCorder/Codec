import sys
import os
import paramiko
import socket
from PySide6 import QtCore,QtWidgets
from PySide6.QtWidgets import QWidget, QStyle
from PySide6.QtCore import QSettings

conf=QSettings('Codec','codec')

conf.value('ssh_known_hosts')
conf.value('ssh_authorised_keys')
conf.sync()

class SSHCAgent(QtWidgets.QWidget):

    def __init__(self,codecwidth):
        super().__init__()

        self.layout=QtWidgets.QGridLayout(self)
        self.codecwidth=codecwidth
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
        url,_=QtWidgets.QFileDialog.getOpenFileUrl(self,'Select a file')
        if not url.isValid():
            return 
        self.key.setPlainText(url.toLocalFile())

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
        self.setFixedSize(self.codecwidth*1.15,self.codecwidth/2.65)

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
        self.setFixedSize(self.codecwidth*1.15,self.codecwidth*0.90)

    def normalconnect(self):
        text=self.quickbox.toPlainText()
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
            main.main.widgetdva.show()
            main.widgetdva.settext("I'm in!")
            main.widgetdva.subsdecay(2)
            main.speechtech.speech()
            ssh.save_host_keys(conf.value('known_hosts'))
            ssh.close()
        except paramiko.SSHException as error:
            main.widgetdva.show()
            main.widgetdva.settext(f"There seems to be an error... [{error}]")
            main.widgetdva.subsdecay(4)
            main.speechtech.speech()
            ssh.close()

class SSHPAgent(QtWidgets.QWidget):

    def __init__(self,codecwidth,widgetdva,speechtech):
        super().__init__()

        self.layout=QtWidgets.QGridLayout(self)
        self.codecwidth=codecwidth
        self.widgetdva=widgetdva
        self.speechtech=speechtech
        self.knownhostsButton=QtWidgets.QPushButton(self)
        self.knownhostsButton.setText("Open known hosts file")
        self.knownhostsButton.clicked.connect(self.openKHFile)
        self.layout.addWidget(self.knownhostsButton)
        self.authorisedkeysButton=QtWidgets.QPushButton(self)
        self.authorisedkeysButton.setText("Open authorised keys file")
        self.authorisedkeysButton.clicked.connect(self.openAKFile)
        self.layout.addWidget(self.authorisedkeysButton)
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
        self.selectedentry=None
        self.knownhostsValue=None
        self.authorisedkeysValue=None
        if conf.value('ssh_known_hosts') != '' and conf.value('ssh_authorised_keys') != '':
            self.addUp()
            self.knownhostsValue=conf.value('ssh_known_hosts')
            self.authorisedkeysValue=conf.value('ssh_authorised_keys')
            self.authorisedkeysButton.hide()
            self.knownhostsButton.hide()
        style=self.style()
        good_icon=style.standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)
        if conf.value('ssh_known_hosts') != '':
            self.knownhostsButton.setIcon(good_icon)
        if conf.value('ssh_authorised_keys') != '':
            self.authorisedkeysButton.setIcon(good_icon)

    def openKHFile(self):
        url,_=QtWidgets.QFileDialog.getOpenFileUrl(self,'Select a known hosts file')
        if not url.isValid():
            return 
        conf.setValue('ssh_known_hosts',url.toLocalFile())
        conf.sync()
        os.execv(sys.executable, ['Codec'] + sys.argv)

    def openAKFile(self):
        url,_=QtWidgets.QFileDialog.getOpenFileUrl(self,'Select a authorised keys file')
        if not url.isValid():
            return 
        conf.setValue('ssh_authorised_keys',url.toLocalFile())
        conf.sync()
        os.execv(sys.executable, ['Codec'] + sys.argv)

    def loginpart(self,connection):   

        def connectsequence(self,usernick,hostname):

            usercom=self.combox.toPlainText()
            ssh=paramiko.SSHClient()
            ssh.load_host_keys(conf.value('ssh_known_hosts'))
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(hostname=hostname,key_filename=conf.value('ssh_authorised_keys'),username=usernick,timeout=500)
                self.widgetdva.show()
                stdin,stdout,stderr=ssh.exec_command(usercom)
                output=stdout.read().decode('utf-8')
                comerror=stderr.read().decode('utf-8')
                if output:
                    self.widgetdva.settext(output)
                    self.widgetdva.subsdecay(len(usercom)/3)
                    self.speechtech.speech()
                if comerror:
                    self.widgetdva.settext('Error : '+comerror)
                    self.widgetdva.subsdecay(len(usercom)/3)
                    self.speechtech.speech()
                ssh.close()
            except paramiko.SSHException as error:
                self.widgetdva.show()
                self.widgetdva.settext(f"There seems to be an error... ["+str(error)+" ]")
                self.widgetdva.subsdecay(4)
                self.speechtech.speech()
                ssh.close()

        self.namebox.show()
        self.combox.show()
        self.inputer.show()
        self.inputer.clicked.connect(lambda:connectsequence(self,usernick=self.namebox.toPlainText(),hostname=connection))

    def addUp(self):
        style=self.style()
        online_icon=style.standardIcon(QStyle.StandardPixmap.SP_DialogYesButton)
        offline_icon=style.standardIcon(QStyle.StandardPixmap.SP_DialogNoButton)
        ssh = paramiko.SSHClient()
        ssh.load_host_keys(conf.value('ssh_known_hosts'))
        for x, entry in enumerate(ssh._host_keys._entries):
            entryname = str(entry).split("'")[1]
            entrybutton = QtWidgets.QPushButton(entryname,self)
            entrybutton.clicked.connect(lambda _,host=entryname:self.loginpart(host))
            try:
                with socket.create_connection((entryname,22),timeout=2):
                    entrybutton.setIcon(online_icon)
            except OSError:
                entrybutton.setIcon(offline_icon)
            self.layout.addWidget(entrybutton)