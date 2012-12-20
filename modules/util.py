

import os
import os.path
import sys
from PyQt4.QtGui import *

def getAppPath():
    "Convenience function so that we can find the necessary images"
    fullpath = os.path.abspath(sys.argv[0])
    path = os.path.dirname(fullpath)
    return path


def getPixmap(fileStr, fileType="PNG", dir="images"):
    """Return a QPixmap instance for the file fileStr relative
    to the binary location and residing in it's 'images' subdirectory"""

    image = getAppPath() + os.sep + dir + os.sep + fileStr
    
    pixmap = QPixmap(image, fileType)
    #pixmap.setMask(pixmap.createHeuristicMask(1))
    
    return pixmap