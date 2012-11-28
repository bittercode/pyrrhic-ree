#!/usr/bin/python3 -d

import sys
import re
import os


try:
    from PyQt4 import *
except:
    print( "Could not locate the PyQt4 module.")
    sys.exit(1)

import os.path
from distutils.sysconfig import get_python_lib

sys.path.insert(0, os.path.join(get_python_lib(), "pyrrhicree"))

from modules.mainWindow import *


class MyForm(QtGui.QMainWindow):
  def __init__(self, parent=None):
    super(MyForm, self).__init__(parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.tedReg.textChanged.connect(self.regChange)
    self.ui.tedString.textChanged.connect(self.strChange)
    self.ui.actionShow_Variables.activated.connect(self.showVariables)
    
    self.regex = ""
    self.matchstring = ""
    self.flags = 0
  
  def regChange(self):
    try:
      self.regex = str(self.ui.tedReg.toPlainText())
      
    except UnicodeError:
      self.regex = unicode(self.ui.tedReg.text())
      
    self.process_regex()
    
    
  def strChange(self):
    try:
      self.matchstring = str(self.ui.tedString.toPlainText())
      
    except UnicodeError:
      self.matchstring = unicode(self.ui.tedString.text())
    
  def process_regex(self):
    compile_obj = re.compile(self.regex, self.flags)
    allmatches = compile_obj.findall(self.matchstring)
    match_obj = compile_obj.search(self.matchstring)
    if match_obj is None:
      self.ui.tedMatch.setText("No Match")
    else:
      self.ui.tedMatch.setText(match_obj.group())
      
      
  def showVariables(self):
    message = "Regex: " + self.regex + "\nString: " + self.matchstring
    self.ui.tedMatch.setText(message)
    
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  sys.exit(app.exec_())