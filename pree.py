#!/usr/bin/python3 -d
#
#pree.py
#This is my Python3/PyQt4 rewrite of Kodos by Phil Schwartz ( http://kodos.sourceforge.net/ )
#A lot of the code is the same - probably the biggest difference other than using new libraries,
#is that I don't use custom controls and do use html in the qtextbrowser objects for formatting
#and creating the group table, etc. I could never have written it without having the original
#as a reference.

import sys
import re
import os
import types

try:
    from PyQt4 import QtGui, QtCore
except:
    print("Could not locate the PyQt4 module.")
    sys.exit(1)

import os.path
from distutils.sysconfig import get_python_lib

#  get the controller and alias it to controller for easier use
from ReeController import controller
controller = controller.Controller

sys.path.insert(0, os.path.join(get_python_lib(), "pyrrhicree"))


from modules.mainWindow import *
from modules.about import *
from modules.urlDialog import *

###################################################################
#
# The Form class that builds the form and inserts logic
#
###################################################################


class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tabResults.setCurrentIndex(0)
        self.ui.tedReg.textChanged.connect(self.regChange)
        self.ui.tedString.textChanged.connect(self.strChange)
        self.ui.tedReplace.textChanged.connect(self.repChange)
        self.ui.actionAbout.triggered.connect(self.showAbout)
        self.ui.actionImport_URL.triggered.connect(self.showImpURL)
        self.ui.actionImport_File.triggered.connect(self.importFile)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.pbPause.clicked.connect(self.clickPause)

        # give a callback to the flag toggles
        # that provides information about which flag was toggled
        # the lambda is used to send information to the callback about
        # who the caller was.
        self.ui.chkCase.toggled.connect(lambda: self.checkChange(re.IGNORECASE))
        self.ui.chkMulti.toggled.connect(lambda: self.checkChange(re.MULTILINE))
        self.ui.chkDot.toggled.connect(lambda: self.checkChange(re.DOTALL))
        self.ui.chkVerbose.toggled.connect(lambda: self.checkChange(re.VERBOSE))
        self.ui.chkLocale.toggled.connect(lambda: self.checkChange(re.LOCALE))
        self.ui.chkAscii.toggled.connect(lambda: self.checkChange(re.ASCII))

        self.is_paused = False
        self.debug = False
        self.group_tuples = None

        self.MNUMBER = self.tr("Match Number")
        self.GNUMBER = self.tr("Group Number")
        self.MATCHNAME = self.tr("Match Name")
        self.MATCHTEXT = self.tr("Match")
        self.MSG_NA = self.tr("Enter a regular expression and a string to match against")
        self.MSG_PAUSED = self.tr("Pree regex processing is paused.  Click the pause icon to unpause")
        self.MSG_FAIL = self.tr("Pattern does not match")

        self.highlightColor = r'#7FFF00'
        self.highlightStart = r'<span style="background-color: ' + self.highlightColor + r'">'
        self.highlightEnd = r'</span>'

        controller.updateView = self.process_regex

    def checkChange(self, toggledFlagValue):
        '''
        Toggles the flags provided by the toggledFlagValue from the flag member.

        Because the re flags are powers of 2 it makes using bitwise operations
        the easiest way to handle them. XOR is used to toggle each flags bit on or
        off without the need for any logic.
        '''
        controller.flags ^= toggledFlagValue

    def clickPause(self):

        self.is_paused = not self.is_paused

        if self.is_paused:
            self.ui.pbPause.setText('UnPause')
            temptext = self.ui.tedReg.toPlainText()
            self.ui.tedReg.setTextColor(QtGui.QColor(255, 0, 0))
            self.ui.tedReg.clear()
            self.ui.tedReg.setPlainText(temptext)
            self.ui.gbReg.setStyleSheet(r'QGroupBox{font-weight: bold; color: red;}')
            self.ui.gbReg.setTitle('Regular Expression Pattern *Processing Paused*')
        else:
            self.ui.pbPause.setText('Pause')
            temptext = self.ui.tedReg.toPlainText()
            self.ui.tedReg.setTextColor(QtGui.QColor(0, 0, 0))
            self.ui.tedReg.clear()
            self.ui.tedReg.setPlainText(temptext)
            self.ui.gbReg.setStyleSheet(r'QGroupBox{font-weight: normal; color: black;}')
            self.ui.gbReg.setTitle('Regular Expression Pattern')

    def regChange(self):
        controller.regex = self.ui.tedReg.toPlainText()

    def strChange(self):
        controller.matchString = self.ui.tedString.toPlainText()

    def repChange(self):
        controller.replaceString = self.ui.tedReplace.toPlainText()

    # The tuple holds two things - the group name and the contents of the match and I can count rows
    def populate_group_textbrowser(self):
        tuples = controller.getGroups()
        self.ui.tebGroup.clear()
        row = 1
        result = (r'<table border=1 cellpadding=7 ><tr><th>' + self.MNUMBER + r'</th>' +
                  r'<th>' + self.GNUMBER + r'</th><th>' + self.MATCHNAME + r'</th><th>' +
                  self.MATCHTEXT + r'</th></tr>')

        for t in tuples:
            if t[0] % 2:
                trow_start = r'<tr style="background-color:lightgreen;">'
            else:
                trow_start = r'<tr>'
            trow = trow_start + (r'<td>' + str(t[0]) + r'</td><td>' + str(t[1]) +
                                 r'</td><td>' + str(t[2]) + r'</td><td>' + str(t[3]) +
                                 r'</td></tr>')
            result = result + trow
            row = row + 1

        self.ui.tebGroup.setHtml(result)

    def populate_matchAll_textbrowser(self):
        spans = controller.getSpans()
        self.ui.tebMatchAll.clear()

        if not spans:
            return

        index = 0
        displayText = ""
        result = ""
        text = controller.matchString

        for span in spans:
            if span[0] != 0:
                result = (text[index:span[0]] + self.highlightStart + text[span[0]:span[1]]
                          + self.highlightEnd)
            else:
                result = self.highlightStart + text[span[0]:span[1]] + self.highlightEnd

            index = span[1]
            displayText = displayText + result
        displayText = displayText + text[index:]

        self.ui.tebMatchAll.setHtml(displayText)

    def clear_results(self):
        self.ui.tebMatch.setHtml("")
        self.ui.tebMatchAll.setHtml("")
        self.ui.tebGroup.setHtml("")
        self.ui.tebRep1.setHtml("")
        self.ui.tebRepAll.setHtml("")
        self.ui.statusbar.clearMessage()

    def should_process_regex(self):
        proceed = True

        if not controller.regex or not controller.matchString:
            self.clear_results()
            proceed = False

        return proceed and not self.is_paused

    def processReplacements(self):
        #  check for the replacement and then
        #  do the subs - both all subs and just first
        if controller.replaceString:
            replaceAll = controller.replaceAll()
            replaceFirst = controller.replaceArbitraryCount(1)
            print('REPL: ', replaceAll)
            self.ui.tebRepAll.setText(replaceAll)
            self.ui.tebRep1.setText(replaceFirst)

    def processFind(self):
        match_obj = controller.search()

        if match_obj is None:
            self.ui.tebMatch.setPlainText("No Match")
            self.ui.tebMatchAll.setPlainText("No Match")
            self.ui.statusbar.showMessage("No Match", 0)
        else:
            self.populate_match_textbrowser()
            self.populate_matchAll_textbrowser()

    def process_regex(self):
        if not self.should_process_regex():
            return

        self.process_embedded_flags()
        self.processReplacements()
        self.processFind()
        self.populate_group_textbrowser()

    def populate_match_textbrowser(self):
        match_obj = controller.search()
        startpos = match_obj.start()
        endpos = match_obj.end()
        pre = post = match = ""

        match = controller.matchString[startpos:endpos]

        # prepend the beginning that didn't match
        if startpos > 0:
            pre = controller.matchString[0:startpos]

        # append the end that didn't match
        if endpos < len(controller.matchString):
            post = controller.matchString[endpos:]

        self.ui.tebMatch.setHtml(pre + self.highlightStart + match + self.highlightEnd + post)

    def process_embedded_flags(self):
        #  determine if the regex contains embedded regex flags.
        #  if not, return False -- inidicating that the regex has no embedded flags
        #  if it does, set the appropriate checkboxes on the UI to reflect the flags that are embedded
        #  and return True to indicate that the string has embedded flags
        flags = controller.embeddedFlags()

        for flag in flags:
            if flag == 'i':
                self.ui.chkCase.setChecked(True)
            elif flag == 'L':
                self.ui.chkLocale.setChecked(True)
            elif flag == 'm':
                self.ui.chkMulti.setChecked(True)
            elif flag == 's':
                self.ui.chkDot.setChecked(True)
            elif flag == 'a':
                self.ui.chkAscii.setChecked(True)
            elif flag == 'x':
                self.ui.chkVerbose.setChecked(True)

        #  Not sure where this is used yet
        return True if flags else False

    def urlImported(self, html):
        controller.matchString = html
        self.ui.tedString.setPlainText(html)

    def showAbout(self):
        self.aboutWindow = About()
        self.aboutWindow.show()

    def showImpURL(self):
        self.impurlWindow = UrlDialog()
        self.impurlWindow.show()
        self.impurlWindow.urlImported.connect(self.urlImported)

    def importFile(self):

        filename = QtGui.QFileDialog.getOpenFileName(self, 'Import File', "All (*)",)

        if filename == "":
            return None

        try:
            inputfile = open(filename, "r")
        except:
            return None

        data = inputfile.read()
        inputfile.close()
        self.ui.tedString.setPlainText(data)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
