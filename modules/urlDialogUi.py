# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './modules/urlDialog.ui'
#
# Created: Sat Dec 22 22:05:29 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_urlDialog(object):
    def setupUi(self, urlDialog):
        urlDialog.setObjectName(_fromUtf8("urlDialog"))
        urlDialog.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(urlDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(urlDialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.txtURL = QtGui.QTextEdit(self.groupBox)
        self.txtURL.setObjectName(_fromUtf8("txtURL"))
        self.verticalLayout.addWidget(self.txtURL)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(urlDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(urlDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), urlDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), urlDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(urlDialog)

    def retranslateUi(self, urlDialog):
        urlDialog.setWindowTitle(QtGui.QApplication.translate("urlDialog", "Open URL", None, QtGui.QApplication.UnicodeUTF8))

