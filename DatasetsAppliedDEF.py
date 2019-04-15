'''
Created on 06 Feb 2015

@author: Deon
'''
from PyQt4.Qt import QFrame
from DatasetsAppliedGUI import Ui_DatasetsApplied

class DatasetsAppliedDEF(QFrame):
    def __init__(self, ScanmanMain):
        '''
        Constructor
        '''
        QFrame.__init__(self)

        self.name = "DatasetsApplied"
        self.ui = Ui_DatasetsApplied()
        self.ui.setupUi(self)
        self.scanman = ScanmanMain
        
    #**************************************************************************************
    def GetSelection(self):
        try:
            if self.ui.allfiles_check.isChecked():
                flistidx = range(len(self.scanman.ui.sourceGroupBox.filelist))
            else:
                flistidx = [self.scanman.ui.sourceGroupBox.ui.file_tbl.currentRow()]
        except:             #This source is probably not a filesource and therefore only one dataset is present
            flistidx = [1]
            
            
        if (self.ui.range_radio.isChecked()):
            setstart = self.ui.rangemin_spin.value()
            setend = self.ui.rangemax_spin.value()
        elif (self.ui.all_radio.isChecked()):
            setstart = 1
            setend = -1
        elif (self.ui.current_radio.isChecked()):
            setstart = self.scanman.datasrc.currset
            setend = self.scanman.datasrc.currset
            
        return flistidx, setstart,setend
                        
        