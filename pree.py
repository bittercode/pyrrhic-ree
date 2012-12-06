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
    
    
  def process_regex(self):
    compile_obj = re.compile(self.regex, self.flags)
    allmatches = compile_obj.findall(self.matchstring)
    
    match_obj = compile_obj.search(self.matchstring)
    if match_obj is None:
      self.ui.tebMatch.setPlainText("No Match")
    else:
      self.populate_match_textbrowser(match_obj.start(), match_obj.end())
      
    spans = self.findAllSpans(compile_obj)
    #self.populate_matchAll_textbrowser(spans)
    self.populate_matchAll_textbrowser(spans)

    self.populate_match_textbrowser(match_obj.start(), match_obj.end())
    
    #This is where I am at - getting the groups to work
    # I need to figure out match_num and match_index so that I can go through the groups
    # Though I may not need to be that indirect. This is where to pick up.
    
    match_index = len(allmatches) - 1 
        
    if match_index > 0:
      for i in range(match_index):
        match_obj = compile_obj.search(self.matchstring,match_obj.end())
                
    

    self.group_tuples = []
    
    
    if match_obj.groups():
      #print match_obj.groups()
      s = "<font color=blue>"
      num_groups = len(match_obj.groups())

      group_nums = {}
      if compile_obj.groupindex:
        keys = compile_obj.groupindex.keys()
        for key in keys:
          group_nums[compile_obj.groupindex[key]] = key

      if self.debug:
        print( "group_nums:", group_nums)                         
        print( "grp index: ", compile_obj.groupindex)
        print( "groups:", match_obj.groups())
        print( "span: ", match_obj.span())

      # create group_tuple in the form: (group #, group name, group matches)
      g = allmatches[match_index]
      if type(g) == types.TupleType:
        for i in range(len(g)):
          group_tuple = (i+1, group_nums.get(i+1, ""), g[i])
          self.group_tuples.append(group_tuple)
        else:
          self.group_tuples.append( (1, group_nums.get(1, ""), g) )
                        
      #print group_tuples
      self.populate_group_textbrowser(self.group_tuples)


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
    

    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  sys.exit(app.exec_())
