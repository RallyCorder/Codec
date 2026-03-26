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

conf=QSettings('Codec','codec')

conf.value('theme')
conf.value('scale')
conf.value('animated')
conf.value('spritesheet')
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
        self.selectedentry=None
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

    def loginpart(self,connection):   

        def connectsequence(self,usernick,hostname):

            usercom=self.combox.toPlainText()
            ssh=paramiko.SSHClient()
            ssh.load_host_keys(conf.value('ssh_known_hosts'))
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(hostname=hostname,key_filename=conf.value('ssh_authorised_keys'),username=usernick,timeout=500)
                self.widgetdva.show()
                self.widgetdva.settext("I'm in!")
                self.widgetdva.subsdecay(2)
                self.speechtech.speech()
                stdin,stdout,stderr=ssh.exec_command(usercom)
                output=stdout.read().decode('utf-8')
                comerror=stderr.read().decode('utf-8')
                if output:
                    self.widgetdva.settext(output)
                    self.widgetdva.subsdecay(2)
                    self.speechtech.speech()
                if comerror:
                    self.widgetdva.settext('Error : '+comerror)
                    self.widgetdva.subsdecay(2)
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
        self.inputer.clicked.connect(connectsequence(self,usernick=self.namebox.toPlainText(),hostname=connection))

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

self.{0}.clicked.connect(self.loginpart(connection='{1}'))
self.layout.addWidget(self.{0})""".format('connection'+str(x),entryname,authkeys)
            code=compile(template,'<string>','exec')
            exec(code)
            x+=1