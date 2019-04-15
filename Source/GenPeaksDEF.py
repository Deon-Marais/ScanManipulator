'''
Created on 08 May 2014

@author: Deon
'''
from PyQt4.QtGui import QGroupBox as QGroupBox
from Source.GenPeaksGUI import Ui_GenPeaks
import PyQt4.QtGui as qt
from pylab import np
import sys
from Source import Srcpar
from Source.SourceCommon import SourceCommon
import mylib

class GenPeaksDEF(QGroupBox,SourceCommon):
    def __init__(self, ScanmanMain):
        QGroupBox.__init__(self)
        SourceCommon.__init__(self, ScanmanMain)
        
        self.name = "GenPeaks"
        self.ui = Ui_GenPeaks()
        self.ui.setupUi(self)
        #self.scanman = ScanmanMain
        #self.src = Srcpar.Srcpar(self.config)
        #self.paramdict = {}
        self.peaks_tbl = mylib.Table(self.ui.peaks_tbl)
        self.paramdict["DAQ_Status"] = ""

        
        
        
    #**************************************************************************************
    def AddPeak(self):
        pktbl=self.ui.peaks_tbl
        pktbl.setRowCount(pktbl.rowCount()+1)
        

    #**************************************************************************************
    def DelPeak(self):
        pktbl=self.ui.peaks_tbl
        pktbl.removeRow(pktbl.currentRow())
            
    
    '***************************************************************'
    def GenSinPeak(self, x, begin, end, amp):
        """Generates a sinusoid peak between 'begin' and 'end' on the [x] axis with the amplitude 'amp'"""
        index = range(len(x))
        y = [0]*len(x)
        for i in index:
            if (x[i] < end) and (x[i] > begin):
                y[i] = amp* np.sin(x[i]*np.pi/(end-begin) - np.pi*begin/(end-begin))
        return y
    
    '***************************************************************'
    def GenMultiPeak(self, x, centers, widths, amps):
        numpeaks = len(centers)
        if (numpeaks != len(widths) and (numpeaks != len(amps))) : return x
        y = [0]*len(x)
        index = range(numpeaks)
        for i in index:
            begin = centers[i] - widths[i]/2.0
            end = begin + widths[i]
            y = np.add(y,self.GenSinPeak(x, begin, end, amps[i]))
        return y

    '***************************************************************'
    def GetData(self):
        pktbl=self.ui.peaks_tbl
        centers = [float(pktbl.item(i,0).text()) for i in range(pktbl.rowCount())]
        widths = [float(pktbl.item(i,1).text()) for i in range(pktbl.rowCount())]
        amps = [float(pktbl.item(i,2).text()) for i in range(pktbl.rowCount())]
        #xmin = float(self.ui.xmin_edit.text())
        xmin = 0
        xmax = float(self.ui.nchannels_edit.text())
        step = 1 #(xmax - xmin) #(xmax - xmin) / (float(self.ui.points_edit.text()) - 1.0)
        x = np.arange(xmin, xmax+step, step)
        y = [float(self.ui.background_edit.text())]*len(x)
        y = np.add(y, self.GenMultiPeak(x,centers, widths, amps) + float(self.ui.noise_edit.text())*np.random.rand(len(x)))

        self.src.x_chan = np.arange(0, xmax+1, 1)
        self.src.nchan = len(self.src.x_chan)
        self.src.AddData(y)
        self.src.dataset.pop(0)     #This is the accumulated (sum)  set which we will recalculate
        self.src.CalcAllAxis()
        self.src.CalcSumSetCommon("")
        self.src.CalcSumSet(["raw"])
        self.src.SelectFrame("raw")
        self.src.SelectDataSet(-1)
        self.scanman.Generate()
       

if __name__ == '__main__':
    
    app = qt.QApplication(sys.argv)
    window=GenPeaksDEF()
    window.show()
    sys.exit(app.exec_())

        