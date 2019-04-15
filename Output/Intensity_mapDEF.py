'''
Created on 08 May 2014

@author: Deon
'''
from PyQt4.QtGui import QGroupBox as QGroupBox
from PyQt4.QtGui import QFileDialog
from Output.Intensity_mapGUI import Ui_Intensity_map
import PyQt4.QtGui as qt
import numpy as np
import sys
from os import path 
        
class Intensity_mapDEF(QGroupBox):
    def __init__(self, ScanmanMain=""):
        QGroupBox.__init__(self)
        self.name = "Intensity_map"
        self.ui = Ui_Intensity_map()
        self.ui.setupUi(self)
        self.scanman = ScanmanMain
        
        self.filedialog = QFileDialog()
        self.filedialog.setAcceptMode(QFileDialog.AcceptSave)
        self.filedialog.setFileMode(QFileDialog.AnyFile)
        self.filedialog.setViewMode(QFileDialog.Detail)
        self.lastdir=""
        
        
    
    #**************************************************************************************
    def CreateMap(self):
        True
    
    
    #**************************************************************************************
    def ExportPeak(self):
        self.Getexportsettings()
        try:
            self.sh=self.wb.Worksheets("Peakfit")
            self.sh.Activate()
        except:
            self.excel = Dispatch("Excel.Application")
            self.excel.Visible=1
            #excel.ScreenUpdating = False
            self.wb = self.excel.Workbooks.Add()
            self.sh=self.excel.ActiveSheet
            self.sh.Name = "Peakfit"
        
        self.includeEmptyRow = 1
        thicklines = []
        self.colnr = {'File name':1, 'Records':2}
        thicklines.append(len(self.colnr))
        
        lastrow = self.sh.UsedRange.Rows.Count
        src = self.scanman.datasrc
        rangelist = self.scanman.ui.fitGroupBox.rangeList
        
        for i in range(len(src.exportparams)):  self.colnr[src.exportparams[i]] = len(self.colnr) + 1
        thicklines.append(len(self.colnr))
        
        for i in range(len(rangelist)):
            rid = "_"+str(i)
            self.colnr["Channel_range"+rid] = len(self.colnr) + 1
            self.colnr["Position"+rid] = len(self.colnr) + 1
            self.colnr["StDev_Position"+rid] = len(self.colnr) + 1
            self.colnr["FWHM"+rid] = len(self.colnr) + 1
            self.colnr["StDev_FWHM"+rid] = len(self.colnr) + 1
            self.colnr["Intensity"+rid] = len(self.colnr) + 1
            self.colnr["StDev_Intensity"+rid] = len(self.colnr) + 1
            self.colnr["Background"+rid] = len(self.colnr) + 1
            self.colnr["StDev_Background"+rid] = len(self.colnr) + 1
            self.colnr["Chi^2"+rid] = len(self.colnr) + 1
            self.colnr["Intensity_sum"+rid] = len(self.colnr) + 1
            thicklines.append(len(self.colnr))  
            True
        
        if self.includeHeader == True:
            if lastrow == 1 and self.sh.Cells(1,1).Value == None:
                headerrow = 1
            else:
                headerrow = lastrow + 1
            
            #for item in self.colnr.iterkeys():
            for item in self.colnr.keys():
                self.sh.Cells(headerrow,self.colnr[item]).Value = item
                
            lastcol = self.sh.UsedRange.Columns.Count
            range_header = self.sh.Range(self.sh.Cells(headerrow,1),self.sh.Cells(headerrow, lastcol))
            range_header.Font.FontStyle="Bold"
            for col in thicklines:
                range_header.Cells(1,col).Borders(c.xlEdgeRight).LineStyle = c.xlContinuous   
            
        rowdatabegin = self.sh.UsedRange.Rows.Count + self.includeEmptyRow
        row = rowdatabegin
        for setnr in range(self.setstart,self.setend):
            self.scanman.ui.dataset_spin.setValue(setnr)        #Selects the next dataset - Hopefully the callback will be completed before the next statements are executed
            self.sh.Cells(row,self.colnr["File name"]).Value = src.dataset[setnr].filename
            self.sh.Cells(row,self.colnr["Records"]).Value = setnr
            for exportprm in src.exportparams:
                self.sh.Cells(row,self.colnr[exportprm]).Value = src.dataset[setnr].prm[exportprm]
            
            for irng in range(len(rangelist)):
                rid = "_"+str(irng)
                rng = rangelist[irng]
                self.sh.Cells(row,self.colnr["Channel_range"+rid]).Value = str(rng.start)+" - "+ str(rng.stop)
                
                self.sh.Cells(row,self.colnr["Position"+rid]).Value = str(rng.position)
                self.sh.Cells(row,self.colnr["StDev_Position"+rid]).Value = str(rng.position_stdev)
                if rng.position_valid == False: self.sh.Cells(row,self.colnr["Position"+rid]).Font.ColorIndex = 3     #3 is red

                self.sh.Cells(row,self.colnr["FWHM"+rid]).Value = str(rng.fwhm)
                self.sh.Cells(row,self.colnr["StDev_FWHM"+rid]).Value = str(rng.fwhm_stdev)
                if rng.fwhm_valid == False: self.sh.Cells(row,self.colnr["FWHM"+rid]).Font.ColorIndex = 3     #3 is red

                self.sh.Cells(row,self.colnr["Intensity"+rid]).Value = str(rng.intensity)
                self.sh.Cells(row,self.colnr["StDev_Intensity"+rid]).Value = str(rng.intensity_stdev)
                if rng.intensity_valid == False: self.sh.Cells(row,self.colnr["Intensity"+rid]).Font.ColorIndex = 3     #3 is red
                
                self.sh.Cells(row,self.colnr["Background"+rid]).Value = str(rng.background)
                self.sh.Cells(row,self.colnr["StDev_Background"+rid]).Value = str(rng.background_stdev)
                self.sh.Cells(row,self.colnr["Chi^2"+rid]).Value = str(rng.chi2)
                self.sh.Cells(row,self.colnr["Intensity_sum"+rid]).Value = str(rng.intensity_sum)
                True
            row = row+1
            True
        rowdataend = self.sh.UsedRange.Rows.Count
        for col in thicklines:
            range_col = self.sh.Range(self.sh.Cells(rowdatabegin,col),self.sh.Cells(rowdataend, col))
            range_col.Borders(c.xlEdgeRight).LineStyle = c.xlContinuous
        lastcol = self.sh.UsedRange.Columns.Count
        range_data = self.sh.Range(self.sh.Cells(rowdatabegin,1),self.sh.Cells(rowdataend, lastcol))
        range_data.HorizontalAlignment = c.xlHAlignRight
        True

   
    #**************************************************************************************
    def ExportGraph(self):
        src = self.scanman.datasrc
        guessfname = str.split(path.basename(path.splitext(src.dataset[1].filename)[0]),".")[0]
        
        file_types = "Fullprof XYDATA (*.xy);;All (*.*)"
        fname = self.filedialog.getSaveFileName(self, 'Save file', self.lastdir+guessfname, file_types)
        if (fname==''): return
        self.lastdir=path.dirname(str(fname))+"/"
        fstr=path.splitext(str(fname))
        if fstr[0] =="": return
        self.Getexportsettings()
        
        src.exportparams.sort()
        axistype = self.scanman.axistype
        filemod = ""
        for nr in range(self.setstart,self.setend):
            f = open(fstr[0]+filemod+fstr[1], 'w')
            
            if axistype == 'Channel':
                x = np.array(src.dataset[nr].currframe.x_chan).astype(float)
                y = src.dataset[nr].currframe.y.astype(float)
            elif axistype == 'Position':
                x = src.dataset[nr].currframe.x_mm.astype(float)
                y = src.dataset[nr].currframe.y.astype(float)
            elif axistype == 'Angle':
                x = src.dataset[nr].currframe.x_2th.astype(float)
                y = src.dataset[nr].currframe.y_2th.astype(float)
            elif axistype == 'd-spacing':
                x = src.dataset[nr].currframe.x_d.astype(float)
                y = src.dataset[nr].currframe.y_2th.astype(float)
            nrpoints = len(y)
            f.write('XYDATA\n')
            f.write("File name: %s\n" %(src.dataset[nr].filename))
            f.write("Dataset: %s\n" %(nr))
            f.write("Type: %s\n" %(src.ylabel))
            paramstr = ""
            for param in src.exportparams: paramstr = paramstr + ", " + param +":" + src.dataset[nr].prm[param]
            f.write("%s\n" %(paramstr))
            f.write("%s Intensity\n" %(axistype))
            for i in np.arange(nrpoints):
                f.write('%f %f\n' % (x[i], y[i]))
            f.close()
            filemod = "_"+str(nr+1)
        True    
    
    #**************************************************************************************
    def Getexportsettings(self):
        if self.ui.all_radio.isChecked():
            self.setstart = 1
            self.setend = len(self.scanman.datasrc.dataset)
        elif self.ui.current_radio.isChecked():
            self.setstart = self.scanman.datasrc.currset
            self.setend = self.setstart+1
        elif self.ui.range_radio.isChecked():
            self.setstart = self.ui.rangemin_spin.value()
            self.setend = self.ui.rangemax_spin.value() + 1
        #self.includeHeader = self.ui.headers_check.isChecked()
        
        True
       

if __name__ == '__main__':
    
    app = qt.QApplication(sys.argv)
    window=Intensity_mapDEF()
    window.show()
    sys.exit(app.exec_())

        