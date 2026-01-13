from PySide6 import QtCore
from PySide6.QtCore import QSettings

conf=QSettings('Codec','codec')
conf.setValue('animated','True')
conf.setValue('spritesheet','otacondo.png')