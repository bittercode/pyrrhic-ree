#  about.py: -*- Python -*-  DESCRIPTIVE TEXT.


from PyQt4 import QtCore, QtGui
from modules.aboutui import *
from modules.util import getPixmap
import os,sys


class About(QtGui.QDialog):
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.ui = Ui_dlgAbout()
        self.ui.setupUi(self)
        
        
        image = getPixmap("logo.png")
        myPixmap = QtGui.QPixmap(image)
        self.ui.lblLogo.setPixmap(myPixmap)
        