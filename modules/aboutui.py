# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './modules/about.ui'
#
# Created: Thu Dec 20 16:31:09 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dlgAbout(object):
    def setupUi(self, dlgAbout):
        dlgAbout.setObjectName(_fromUtf8("dlgAbout"))
        dlgAbout.resize(600, 422)
        dlgAbout.setMinimumSize(QtCore.QSize(0, 75))
        dlgAbout.setWindowTitle(QtGui.QApplication.translate("dlgAbout", "About Pree", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(dlgAbout)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblLogo = QtGui.QLabel(dlgAbout)
        self.lblLogo.setMinimumSize(QtCore.QSize(300, 300))
        self.lblLogo.setText(QtGui.QApplication.translate("dlgAbout", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.lblLogo.setObjectName(_fromUtf8("lblLogo"))
        self.gridLayout.addWidget(self.lblLogo, 0, 0, 4, 1)
        self.widget = QtGui.QWidget(dlgAbout)
        self.widget.setMinimumSize(QtCore.QSize(267, 0))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_7 = QtGui.QLabel(self.widget)
        self.label_7.setText(QtGui.QApplication.translate("dlgAbout", "Version:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_2.addWidget(self.label_7)
        self.lblVersion = QtGui.QLabel(self.widget)
        self.lblVersion.setText(QtGui.QApplication.translate("dlgAbout", "0.5", None, QtGui.QApplication.UnicodeUTF8))
        self.lblVersion.setObjectName(_fromUtf8("lblVersion"))
        self.verticalLayout_2.addWidget(self.lblVersion)
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setText(QtGui.QApplication.translate("dlgAbout", "Written by:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setText(QtGui.QApplication.translate("dlgAbout", "JR Peck", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_2.addWidget(self.label_5)
        self.gridLayout.addWidget(self.widget, 0, 1, 1, 2)
        self.label = QtGui.QLabel(dlgAbout)
        self.label.setText(QtGui.QApplication.translate("dlgAbout", "bittercode@gmail.com", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 2)
        self.widget_2 = QtGui.QWidget(dlgAbout)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 75))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.widget_2)
        self.label_2.setText(QtGui.QApplication.translate("dlgAbout", "Pyrhicc Ree is free and open software", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(self.widget_2)
        self.label_3.setText(QtGui.QApplication.translate("dlgAbout", "<a href=\"https://github.com/bittercode/pyrrhic-ree\">https://github.com/bittercode/pyrrhic-ree</a>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.gridLayout.addWidget(self.widget_2, 2, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 238, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(322, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(dlgAbout)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 2, 1, 1)

        self.retranslateUi(dlgAbout)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dlgAbout.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dlgAbout.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgAbout)

    def retranslateUi(self, dlgAbout):
        pass

