'''
Created on 08 May 2014

@author: Deon
'''
from PyQt4.QtGui import QGroupBox as QGroupBox
from PyQt4.QtGui import QFileDialog
#from GenPeaksGUI import Ui_GenPeaks
from Output.ExcelGUI import Ui_Excel
import PyQt4.QtGui as qt
import numpy as np
import sys
#import Srcpar
#from ScanmanDEF import ScanmanDEF
from win32com.client import Dispatch 
from win32com.client import constants as c
from mylib import get_clipboard_text
from os import path
from mylib import ProgressBar

def ToExcelCol(aList):
    mylist=[]
    for item in aList:
        mylist.append([item])
    return tuple(mylist)

        
class ExcelDEF(QGroupBox):
    def __init__(self, ScanmanMain=""):
        QGroupBox.__init__(self)
        self.name = "Excel"
        self.ui = Ui_Excel()
        self.ui.setupUi(self)
        self.scanman = ScanmanMain
        #self.src = Srcpar.Srcpar()
        self.excel = ""
        self.sh=""
        self.includeHeader = True
        self.includeEmptyRow = 1
        self.colnr = {'File name':1, 'Mods':2, 'Records':3}
        self.setstart = 0
        self.setend = 0
        
        self.filedialog = QFileDialog()
        self.filedialog.setAcceptMode(QFileDialog.AcceptSave)
        self.filedialog.setFileMode(QFileDialog.AnyFile)
        self.filedialog.setViewMode(QFileDialog.Detail)
        self.lastdir=""
        
    
    #**************************************************************************************
    def RangeOpenButtonClicked(self):
        #if self.lastdir == "":
        #    self.lastdir = self.lastdir=path.dirname(self.scanman.ui.sourceGroupBox.filelist[flistidx[0]].location)
        fname = self.filedialog.getOpenFileName(self, "Select range file", self.lastdir,"RangeFile (*.txt)")
        if fname == "": return
        self.ui.rangeFileLineEdit.setText(fname)
        self.lastdir = path.dirname(str(fname))
        #text_file = open(fname,"r")

        
        
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
        rngarray=[[]]
        if self.ui.useRangeCheckBox.isChecked():
            text_file = open(self.ui.rangeFileLineEdit.text(),"r")
            txtrange = text_file.read()
            text_file.close()
            rngarray = np.array([rng.split() for rng in txtrange[:-1].split('\n')]).astype('int')
            True
            
        self.includeEmptyRow = 1
        thicklines = []
        self.colnr = {'File name':1, 'Mods':2, 'Records':3}
        thicklines.append(len(self.colnr))
        
        
        #src = self.scanman.datasrc
        rangelist = self.scanman.ui.fitGroupBox.rangeList
        
        #for i in range(len(self.scanman.datasrc.exportparams)):  self.colnr[self.scanman.datasrc.exportparams[i]] = len(self.colnr) + 1
        for i in range(len(self.scanman.exportparams)):  self.colnr[self.scanman.exportparams[i]] = len(self.colnr) + 1
        thicklines.append(len(self.colnr))
        
        if "allparams" in rangelist[-1].__dict__:    #Generic (new) way
            for i in range(len(rangelist)):
                rid = "_"+str(i)
                self.colnr["Channel_range"+rid] = len(self.colnr) + 1
                for iterprm in rangelist[i].iterparams:
                    self.colnr[iterprm+rid] = len(self.colnr) + 1
                    self.colnr["StDev_"+iterprm+rid] = len(self.colnr) + 1
                for miscprm in rangelist[i].miscparams:
                    self.colnr[miscprm+rid] = len(self.colnr) + 1
                for fitprm in rangelist[i].fitparams:
                    self.colnr[fitprm+rid] = len(self.colnr) + 1
                thicklines.append(len(self.colnr))  
                True
        else:   #old way
            for i in range(len(rangelist)):
                rid = "_"+str(i)
                self.colnr["Channel_range"+rid] = len(self.colnr) + 1
                self.colnr[self.scanman.axistype+rid] = len(self.colnr) + 1
                self.colnr["StDev_"+self.scanman.axistype+rid] = len(self.colnr) + 1
                self.colnr["FWHM"+rid] = len(self.colnr) + 1
                self.colnr["StDev_FWHM"+rid] = len(self.colnr) + 1
                self.colnr["Intensity"+rid] = len(self.colnr) + 1
                self.colnr["StDev_Intensity"+rid] = len(self.colnr) + 1
                self.colnr["Background"+rid] = len(self.colnr) + 1
                self.colnr["StDev_Background"+rid] = len(self.colnr) + 1
                self.colnr["Chi^2"+rid] = len(self.colnr) + 1
                self.colnr["Intensity_sum"+rid] = len(self.colnr) + 1
                self.colnr["Counts"+rid] = len(self.colnr) + 1
                self.colnr["Err_u_strain"+rid] = len(self.colnr) + 1
                thicklines.append(len(self.colnr))  
            True
            
        
        
        if self.scanman.ui.outputGroupBox.ui.allfiles_check.isChecked():
            flistidx = range(len(self.scanman.ui.sourceGroupBox.filelist))
        else:
            flistidx = [self.scanman.ui.sourceGroupBox.ui.file_tbl.currentRow()]
        
        numfiles = len(flistidx)    
        progressfiles = ProgressBar("Fitting files...", numfiles)
        
        lastrow = self.sh.UsedRange.Rows.Count    
        for filei in flistidx:
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
                #for col in thicklines:
                    #range_header.Cells(1,col).Borders(c.xlEdgeRight).LineStyle = c.xlContinuous   
                
            rowdatabegin = self.sh.UsedRange.Rows.Count + self.includeEmptyRow
            row = rowdatabegin
                
            self.scanman.ui.sourceGroupBox.SelectDataFile(filei)
            if self.ui.all_radio.isChecked():
                self.setend = len(self.scanman.datasrc.dataset)
            progressfiles.setinfo(self.scanman.datasrc.filename)
            
            numsets = self.setend - self.setstart
            progresdataset = ProgressBar("Fitting datasets...", numsets)
            
            #rangelist[0].start = 529
            #rangelist[0].stop = 621
            
            if len(rngarray[0]) == 0:
                if "allparams" in rangelist[0].__dict__:
                    rngarray = [[rangelist[0].rangeparams["Range_start"].value,
                                 rangelist[0].rangeparams["Range_end"].value]]
                else:   #old way
                    rngarray = [[rangelist[0].start,rangelist[0].stop]]
            if len(rngarray) !=0:
                True 
            
            for setnr in range(self.setstart,self.setend):
                progresdataset.setinfo(self.scanman.datasrc.filename)
                for nrng in rngarray:
                    if "allparams" in rangelist[0].__dict__:
                        rangelist[0].rangeparams["Range_start"].value = nrng[0]
                        rangelist[0].rangeparams["Range_end"].value = nrng[1]
                    else:   #old way
                        rangelist[0].start = nrng[0]
                        rangelist[0].stop = nrng[1]
                #self.scanman.ui.dataset_spin.setValue(setnr)        #Selects the next dataset - Hopefully the callback will be completed before the next statements are executed
                    self.scanman.SelectData(setnr,display=False)
                    src = self.scanman.datasrc
                    self.sh.Cells(row,self.colnr["File name"]).Value = src.dataset[setnr].filename
                    self.sh.Cells(row,self.colnr["Mods"]).Value = self.scanman.modext
                    self.sh.Cells(row,self.colnr["Records"]).Value = setnr
                    
                    #for exportprm in src.exportparams:
                    for exportprm in self.scanman.exportparams:
                        try:
                            self.sh.Cells(row,self.colnr[exportprm]).Value = src.dataset[setnr].prm[exportprm]
                        except:
                            self.sh.Cells(row,self.colnr[exportprm]).Value = ""
                    
                    for irng in range(len(rangelist)):
                        rid = "_"+str(irng)
                        rng = rangelist[irng]
                        if "allparams" in rangelist[0].__dict__:
                            self.sh.Cells(row,self.colnr["Channel_range"+rid]).Value = str(rng.rangeparams["Range_start"].value)+" - "+ str(rng.rangeparams["Range_end"].value)
                            for iterprm in rng.iterparams:
                                self.sh.Cells(row,self.colnr[iterprm+rid]).Value = str(rng.iterparams[iterprm].value)
                                self.sh.Cells(row,self.colnr["StDev_"+iterprm+rid]).Value = str(rng.iterparams[iterprm].stdev)
                                if rng.iterparams[iterprm].valid == False: self.sh.Cells(row,self.colnr[iterprm+rid]).Font.ColorIndex = 3     #3 is red
                            for miscprm in rangelist[i].miscparams:
                                self.sh.Cells(row,self.colnr[miscprm+rid]).Value = str(rng.miscparams[miscprm].value)
                            for fitprm in rangelist[i].fitparams:
                                self.sh.Cells(row,self.colnr[fitprm+rid]).Value = str(rng.fitparams[fitprm].value)
                            True
                        else:   #old way
                            self.sh.Cells(row,self.colnr["Channel_range"+rid]).Value = str(rng.start)+" - "+ str(rng.stop)
                            self.sh.Cells(row,self.colnr[self.scanman.axistype+rid]).Value = str(rng.position)
                            self.sh.Cells(row,self.colnr["StDev_"+self.scanman.axistype+rid]).Value = str(rng.position_stdev)
                            if rng.position_valid == False: self.sh.Cells(row,self.colnr[self.scanman.axistype+rid]).Font.ColorIndex = 3     #3 is red
            
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
                            self.sh.Cells(row,self.colnr["Counts"+rid]).Value = str(rng.counts)
                            self.sh.Cells(row,self.colnr["Err_u_strain"+rid]).Value = str(rng.errustrain)
                            
                            True
                    row = row+1
                    if progresdataset.wasCanceled(): break
                    progresdataset.step()
                    True
            lastrow = self.sh.UsedRange.Rows.Count
            #for col in thicklines:
            #    range_col = self.sh.Range(self.sh.Cells(rowdatabegin,col),self.sh.Cells(lastrow, col))
            #    range_col.Borders(c.xlEdgeRight).LineStyle = c.xlContinuous
            lastcol = self.sh.UsedRange.Columns.Count
            range_data = self.sh.Range(self.sh.Cells(rowdatabegin,1),self.sh.Cells(lastrow, lastcol))
            #range_data.HorizontalAlignment = c.xlHAlignRight
            
            if self.savetext == True:
                from mylib import get_clipboard_text
                self.sh.Range(self.sh.Cells(headerrow,1),self.sh.Cells(lastrow, lastcol)).Copy()
                data = get_clipboard_text()
                data = data.replace("\r\n", "\n")
                guessfname = path.basename(src.filename).split(".")[0] + self.scanman.modext
                if self.lastdir == "":
                    self.lastdir = self.lastdir=path.dirname(self.scanman.ui.sourceGroupBox.filelist[flistidx[0]].location)
                fname = self.filedialog.getSaveFileName(self, "Save as *.pkf", path.join(self.lastdir,guessfname),"Peakfit (*.pkf)")
                if fname == "": return
                self.lastdir = path.dirname(str(fname))
                text_file = open(fname,"w")
                text_file.write(data)
                text_file.close()
                
                if self.reopen == True:
                    self.scanman.ui.sourceGroupBox.OpenFile([fname])
            
            if progressfiles.wasCanceled(): break
            progressfiles.step()
            True


    #**************************************************************************************
    def ExportGraph(self):
        self.Getexportsettings()
        try:
            self.sh=self.wb.Worksheets.Add()
        except:
            self.excel = Dispatch("Excel.Application")
            self.excel.Visible=1
            #excel.ScreenUpdating = False
            self.wb = self.excel.Workbooks.Add()
            for i in range(1,len(self.wb.Worksheets)):
                self.wb.Worksheets.Item(2).Delete()           #lower index start at 1. Delete all the rest   
            self.sh=self.wb.Worksheets.Item(1)
        
        
        self.includeEmptyRow = 1
        thicklines = []
        self.colnr = {'File name':1, 'Records':2}
        #rownr = {}
        thicklines.append(len(self.colnr))
        
        lastrow = self.sh.UsedRange.Rows.Count
        lastcol = 0
        src = self.scanman.datasrc
        #src.exportparams.sort()
        self.scanman.exportparams.sort()
        rownr = {'File name':1, 'Mods':2, 'Dataset':3, 'Type':4}
        #for i in range(len(src.exportparams)):  rownr[src.exportparams[i]] = len(rownr) + 1
        for i in range(len(self.scanman.exportparams)):  rownr[self.scanman.exportparams[i]] = len(rownr) + 1
        
        rowdatabegin = len(rownr) + 2 
        axistype = self.scanman.axistype
        xprev = np.array([])
        for nr in range(self.setstart,self.setend):
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
            if np.array_equal(x, xprev) == False:
                self.sh.Cells(rownr['File name'],lastcol+1).Value = "File name"
                self.sh.Cells(rownr['Mods'],lastcol+1).Value = "Mods"
                self.sh.Cells(rownr['Dataset'],lastcol+1).Value = "Dataset"
                self.sh.Cells(rownr['Type'],lastcol+1).Value = "Type"
                #for param in src.exportparams: self.sh.Cells(rownr[param],lastcol+1).Value = param
                for param in self.scanman.exportparams: self.sh.Cells(rownr[param],lastcol+1).Value = param
                self.sh.Cells(len(rownr)+1,lastcol+1).Value = axistype
                self.sh.Range(self.sh.Cells(1,lastcol+1),self.sh.Cells(len(rownr)+1, lastcol+1)).Font.FontStyle="Bold"
                range_x = self.sh.Range(self.sh.Cells(rowdatabegin,lastcol+1),self.sh.Cells(rowdatabegin+nrpoints-1, lastcol+1))     
                #range_x.Value = ToExcelCol(x)
                range_x.Value = ToExcelCol(x.astype(np.str))
                lastcol+=1
            
            self.sh.Cells(rownr['File name'],lastcol+1).Value = src.dataset[nr].filename
            self.sh.Cells(rownr['Mods'],lastcol+1).Value = self.scanman.modext
            self.sh.Cells(rownr['Dataset'],lastcol+1).Value = str(nr)
            self.sh.Cells(rownr['Type'],lastcol+1).Value = str(src.ylabel)
            #for param in src.exportparams: self.sh.Cells(rownr[param],lastcol+1).Value = src.dataset[nr].prm[param]
            for param in self.scanman.exportparams: self.sh.Cells(rownr[param],lastcol+1).Value = src.dataset[nr].prm[param]
            range_y = self.sh.Range(self.sh.Cells(rowdatabegin,lastcol+1),self.sh.Cells(rowdatabegin+nrpoints-1, lastcol+1)) 
            #range_y.Value = ToExcelCol(y)
            range_y.Value = ToExcelCol(y.astype(np.str))
            lastcol+=1    
            xprev = x
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
        self.includeHeader = self.ui.headers_check.isChecked()
        self.savetext = self.ui.peaksave_check.isChecked()
        self.reopen = self.ui.peakreopen_check.isChecked() 
        
        True
       

if __name__ == '__main__':
    
    app = qt.QApplication(sys.argv)
    window=ExcelDEF()
    window.show()
    sys.exit(app.exec_())

        