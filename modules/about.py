#  about.py: -*- Python -*-


from PyQt4 import QtCore, QtGui
from modules.aboutui import *
from modules.util import getPixmap
from modules.version import *
import os,sys


class About(QtGui.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_dlgAbout()
        self.ui.setupUi(self)
        
        self.ui.lblVersion.setText(VERSION)
        
        image = getPixmap("logo.png")
        myPixmap = QtGui.QPixmap(image)
        self.ui.lblLogo.setPixmap(myPixmap)
        