import os
from PySide6 import QtCore
from PySide6.QtCore import QSettings

conf=QSettings('Codec','codec')
conf.setValue('theme','system')
conf.setValue('scale','1')
conf.setValue('animated','True')
conf.setValue('spritesheet',os.path.dirname(os.path.realpath(__file__))+'/otacondo.png')
conf.setValue('ssh_known_hosts','')
conf.setValue('ssh_authorised_keys','')