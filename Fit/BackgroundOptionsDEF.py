from PyQt4.QtGui import QGroupBox as QGroupBox
from Fit.BackgroundOptionsGUI import Ui_BackgroundOptions

class BackgroundOptionsDEF(QGroupBox):
    def __init__(self, myparent=""):
        QGroupBox.__init__(self)
        self.name = "BackgroundOptions"
        self.ui = Ui_BackgroundOptions()
        self.ui.setupUi(self)
        self.scanman = myparent.scanman
        
