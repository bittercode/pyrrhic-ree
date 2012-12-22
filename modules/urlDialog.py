#  urlDialog.py: -*- Python -*-  DESCRIPTIVE TEXT.


from PyQt4 import QtCore, QtGui
from modules.urlDialogUi import *
import urllib.request

class UrlDialog(QtGui.QDialog):
    
    sig = QtCore.pyqtSignal('QString', name='urlImported')
    
    def __init__(self, parent=None):
        super(UrlDialog, self).__init__(parent)
        self.ui = Ui_urlDialog()
        self.ui.setupUi(self)
        
        
    def accept(self):
      url = str(self.ui.txtURL.toPlainText())
      try:
        nurl = urllib.request.urlopen(url)
        mybytes = nurl.read()
        mystr = mybytes.decode("utf8")
        nurl.close()
        
      except Exception as e:
        QtGui.QMessageBox.information(None, "Failed to open URL",
                                "Could not open the specified URL. Please check to ensure that you have entered the correct URL.\n\n%s" % str(e))
        return
      
      html = ''.join(mystr)
      self.sig.emit( html)
      
      self.done(1)
      