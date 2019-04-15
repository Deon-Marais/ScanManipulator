
#from PyQt4.QtGui import QApplication, QDialog
import os
#from codetools.util.cbook import Null
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt'
from pyface.qt import QtGui as qt       #Cannot use the normal PyQt4 as it conflicts with Mayavi
#import PyQt4.QtGui as qt
from ScanmanDEF import ScanmanDEF
#import copy
import sys

class MyApplication(qt.QApplication):
    def __init__(self,args):
        super(MyApplication,self).__init__(args)
        #self.qtnotify = copy.deepcopy(self.notify)
        #sys.excepthook = self.my_excepthook
        True
    
    #def my_excepthook(self,atype,value,tback):
    #    sys.__excepthook__(atype, value, tback)
    def notify(self,thereceiver, theevent):
        try:
            return qt.QApplication.notify(self,thereceiver,theevent)
        except:
            True
        
        #try:
            #a= self.qtnotify(thereceiver,theevent)
        #    a= qt.QApplication.notify(thereceiver,theevent)
        #    True
        #except:
        #    a=False
        #    True
        #return a
    #    True




if __name__ == '__main__':
    #app = qt.QApplication(sys.argv)
    app = MyApplication(sys.argv)
    window = ScanmanDEF()
    window.show()
    sys.exit(app.exec_())

