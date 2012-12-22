#  urlDialog.py: -*- Python -*-  DESCRIPTIVE TEXT.


from PyQt4 import QtCore, QtGui
from modules.urlDialogUi import *
import urllib

class UrlDialog(QtGui.QDialog):
    def __init__(self, parent=None, url=None):
        super(UrlDialog, self).__init__(parent)
        self.ui = Ui_urlDialog()
        self.ui.setupUi(self)
        if url:
          self.ui.txtURL.setText(url)
        
    def accept(self):
      url = str(self.ui.txtURL.text())
      try:
        fp = urllib.urlopen(url)
        lines = fp.readlines()
      except Exception as e:
        QMessageBox.information(None, "Failed to open URL",
                                "Could not open the specified URL. Please check to ensure that you have entered the correct URL.\n\n%s" % str(e))
        return
      
      html = ''.join(lines)
      self.parent.emit(PYSIGNAAL('urlImported()'), (html,url))