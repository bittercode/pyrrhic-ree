
from PyQt4 import QtCore, QtGui
from aboutui import *

class About(Ui_dlgAbout):
    def __init__(self):
        Ui_dlgAbout.__init__(self)
        myPixmap = QtGui.QPixmap(_fromUtf8('logo.phg'))
        myScaledPixmap = myPixmap.scaled(self.lblLogo.size(), Qt.KeepAspectRatio)
        self.lblLogo.setPixmap(myScaledPixmap)