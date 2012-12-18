#!/usr/bin/python3 -d
#	pree.py
#	This is my Python3/PyQt4 rewrite of Kodos by Phil Schwartz ( http://kodos.sourceforge.net/ )
#       A lot of the code is the same - probably the biggest difference other than using new libraries,
#       is that I don't use custom controls and do use html in the qtextbrowser objects for formatting
#       and creating the group table, etc. I could never have written it without having the original
#       as a reference.git

import sys
import re
import os
import types

try:
    from PyQt4 import QtGui, QtCore
except:
    print( "Could not locate the PyQt4 module.")
    sys.exit(1)

import os.path
from distutils.sysconfig import get_python_lib

sys.path.insert(0, os.path.join(get_python_lib(), "pree"))


from modules.mainWindow import *

# regex to find special flags which must begin at beginning of line
# or after some spaces
EMBEDDED_FLAGS = r"^ *\(\?(?P<flags>[aiLmsx]*)\)"

###################################################################
#
# The Form class that builds the form and inserts logic
#
###################################################################

class MyForm(QtGui.QMainWindow):
  def __init__(self, parent=None):
    super(MyForm, self).__init__(parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.tedReg.textChanged.connect(self.regChange)
    self.ui.tedString.textChanged.connect(self.strChange)
    self.ui.actionShow_Variables.activated.connect(self.showVariables)
    self.ui.actionExit.activated.connect(self.close)
    self.ui.chkCase.toggled.connect(self.checkChange)
    self.ui.chkMulti.toggled.connect(self.checkChange)
    self.ui.chkDot.toggled.connect(self.checkChange)
    self.ui.chkVerbose.toggled.connect(self.checkChange)
    self.ui.chkLocale.toggled.connect(self.checkChange)
    self.ui.chkAscii.toggled.connect(self.checkChange)
    
    self.regex = ""
    self.matchstring = ""
    self.flags = 0
    self.debug = False
    self.group_tuples = None
    self.embedded_flags_obj = re.compile(EMBEDDED_FLAGS)
    
    self.highlightColor = r'#7FFF00'
    self.highlightStart = r'<span style="background-color: '+ self.highlightColor + r'">'
    self.highlightEnd = r'</span>'
  
  def checkChange(self):
      self.flags = 0
        
      if self.ui.chkCase.isChecked():
        self.flags = self.flags + re.IGNORECASE

      if self.ui.chkMulti.isChecked():
        self.flags = self.flags + re.MULTILINE

      if self.ui.chkDot.isChecked():
        self.flags = self.flags + re.DOTALL

      if self.ui.chkVerbose.isChecked():
        self.flags = self.flags + re.VERBOSE

      if self.ui.chkLocale.isChecked():
        self.flags = self.flags + re.LOCALE

      if self.ui.chkAscii.isChecked():
        self.flags = self.flags + re.ASCII

      self.process_regex()
  
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
      
    self.process_regex()
    

  # The tuple holds two things - the group name and the contents of the match and I can count rows
  def populate_group_textbrowser(self,tuples):
    self.ui.tebGroup.clear()
    result = ""
    row = 1
    htmtable = r'<table border=1>'
    
    for t in tuples:
      trow = r'<tr><td>' + row + r'</td><td>' + t[1] + r'</td><td>' + t[2] + r'</td></tr>'
      result = result + trow
      row = row + 1
      
      
    self.ui.tebGroup.setHtml(result)
    
  def populate_matchAll_textbrowser(self, spans):
    self.ui.tebMatchAll.clear()
    if not spans: return

    idx = 0
    disp = ""
    result = ""
    text = self.matchstring
    
    for span in spans:
      if span[0] != 0:
        result = text[idx:span[0]] + self.highlightStart + text[span[0]:span[1]] + self.highlightEnd
      else:
        result = self.highlightStart + text[span[0]:span[1]] + self.highlightEnd
                
      idx = span[1]
      disp = disp + result
    disp = disp + text[idx:]
    
    self.ui.tebMatchAll.setHtml(disp)
    
  
  def clear_results(self):
    self.ui.tebMatch.setHtml("")
    self.ui.tebMatchAll.setHtml("")
    self.ui.statusbar.clearMessage()
    
  def process_regex(self):
    if not self.regex or not self.matchstring:
        self.clear_results()
        return
    
    self.process_embedded_flags(self.regex)
    
    compile_obj = re.compile(self.regex, self.flags)
    allmatches = compile_obj.findall(self.matchstring)
    
    #This is a big change I"m not updating the spinner
    if allmatches and len(allmatches):
        match_index = len(allmatches) -1
        print('MatchIndex: ' + str(match_index))
    
    match_obj = compile_obj.search(self.matchstring)
    if match_obj is None:
      self.ui.tebMatch.setPlainText("No Match")
      self.ui.tebMatchAll.setPlainText("No Match")
      self.ui.statusbar.showMessage("No Match",0)
    else:
      #This is the single match
      self.populate_match_textbrowser(match_obj.start(), match_obj.end())
      
    spans = self.findAllSpans(compile_obj)
    #This will fill in all matches
    self.populate_matchAll_textbrowser(spans)
    
    #This is the start of groups and right now it goes to the end of process_regex
    #It works right now as long as groups are not named - I think
    print(compile_obj.groupindex)
    
    if match_obj.groups():
      num_groups = compile_obj.groups
      
        
      for m in re.finditer(self.regex,self.matchstring):
        mc =1
        i=1
        while i <= num_groups:
          print('MatchNum:' + str(mc) + ' Group:' + str(i) + ' String:' +str(m.group(i)))
          i=i+1
        mc = mc +1
      
  def findAllSpans(self, compile_obj):
    spans = []
        
    match_obj = compile_obj.search(self.matchstring)

    last_span = None
        
    while match_obj:
      start = match_obj.start()
      end   = match_obj.end()
      span = (start, end)
      if last_span == span: break
            
      spans.append(span)
            
      last_span = span
      match_obj = compile_obj.search(self.matchstring, end)
    
    if self.debug:
      print("FA Spans: ", spans)
    
    return spans

  def populate_match_textbrowser(self, startpos, endpos):
      pre = post = match = ""
        
      match = self.matchstring[startpos:endpos]

      # prepend the beginning that didn't match
      if startpos > 0:
        pre = self.matchstring[0:startpos]
            
      # append the end that didn't match
      if endpos < len(self.matchstring):
        post = self.matchstring[endpos:]
            
      self.ui.tebMatch.setHtml(pre + self.highlightStart + match + self.highlightEnd + post)
        
        
  def showVariables(self):
    message = "Regex: " + self.regex + "\nString: " + self.matchstring + "\nMA: " + self.texttry
    self.ui.tebMatch.setPlainText(message)
    
  def process_embedded_flags(self, regex):
    # determine if the regex contains embedded regex flags.
    # if not, return 0 -- inidicating that the regex has no embedded flags
    # if it does, set the appropriate checkboxes on the UI to reflect the flags that are embedded
    #   and return 1 to indicate that the string has embedded flags
    match = self.embedded_flags_obj.match(regex)
    if not match:
      self.embedded_flags = ""
      self.regex_embedded_flags_removed = regex
      return 0

    self.embedded_flags = match.group('flags')
    self.regex_embedded_flags_removed = self.embedded_flags_obj.sub("", regex, 1)
        
    for flag in self.embedded_flags:
      if flag == 'i':
        self.ui.chkCase.setChecked(1)
      elif flag == 'L':
        self.ui.chkLocale.setChecked(1)
      elif flag == 'm':
        self.ui.chkMulti.setChecked(1)
      elif flag == 's':
        self.ui.chkDot.setChecked(1)
      elif flag == 'a':
        self.ui.chkAscii.setChecked(1)
      elif flag == 'x':
        self.ui.chkVerbose.setChecked(1)

    return 1
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  sys.exit(app.exec_())
