from PyQt4.QtGui import QGroupBox as QGroupBox
from PyQt4.QtGui import QFileDialog
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtCore
from Source.SourceFileGUI import Ui_SourceFile
import numpy as np
import Source.Srcpar as Srcpar
import os.path
from thirdparty.pyparsing import *
from PyQt4 import QtCore
from mylib import ProgressBar
from mylib import Table

from Source.SourceCommon import SourceCommon as SourceCommon
from Source import Gumtree_xyd
from Source import NeXus_hdf
from Source import AsciiTwoColumn_txt
from Source import FullprofCompat_xy
from Source import McStas_sim
from Source import ScanmanPeakFit_pkf

class FileInfo(object):
    def __init__(self, filepath ,config, src=None):
        self.src=src
        self.selected = False
        filepath = str(filepath)
        if os.path.exists(filepath):
            self.location = os.path.abspath(filepath)
            base, self.ext = os.path.splitext(filepath)
            self.filename = os.path.split(base)[1]
            if self.ext == ".xyd":
                self.type = "Gumtree xyd"
                self.src = Gumtree_xyd.Gumtree_xyd_read(filepath, config)
                True
            elif self.ext ==".hdf":
                self.type = "NeXus hdf"
                self.src = NeXus_hdf.NeXus_hdf_read(filepath, config)
                #self.MotorCorrections(config)
            elif self.ext == ".txt":
                self.type = "ASCII two column"
                self.src = AsciiTwoColumn_txt.AsciiTwoColumn_txt_read(filepath, config)
            elif self.ext == ".xy":
                self.type = "Fullprof compatible"
                self.src = FullprofCompat_xy.FullprofCompat_xy_read(filepath, config)
            elif self.ext == ".sim":
                self.type = "McStas 1D Detector"
                self.src = McStas_sim.McStas_sim_read(filepath, config)
            elif self.ext == ".cmds":
                self.type = "McStas Parameter Study"
                self.src = McStas_sim.McStas_sim_read(filepath, config, paramstudy=True)
            elif self.ext == ".pkf":
                self.type = "Scanman PeakFit"
                self.src = ScanmanPeakFit_pkf.ScanmanPeakFit_pkf_read(filepath,config)
        
        else:
            self.location = "memory_"+filepath
            self.filename = "None"
            self.type = "Modified"
            self.ext = ""

        if self.src == None:
            return
        
        self.srcp = Srcpar.Srcpar(config)     #Source post process
        self.srcsplit = Srcpar.Srcpar(config)     #Source with detector splitted
            
        self.src.CalcAllAxis()
        self.src.x_chan = self.src.dataset[-1].x_chan
        self.src.nchan = len(self.src.x_chan)
        self.src.CalcSumSetCommon("")
        self.src.CalcSumSet(["raw"])
        self.src.SelectFrame("raw")
        self.src.SelectDataSet(-1)
        
        if self.src.data2D == False:
            self.srcsplit = self.src
    
    #**************************************************************************************
    def MotorCorrections(self,config):      #Needed on KOWARI
        if "motor_corrections" not in config: return
        if "echi" not in self.src.dataset[-1].prm: return
        if "ephi" not in self.src.dataset[-1].prm: return
        
        ephi_coupled_echi = 0.0
        echi_offset = 0.0
        echi_offset_sign = 1.0
        if "ephi_coupled_echi" in config["motor_corrections"]:
            ephi_coupled_echi = config["motor_corrections"]["ephi_coupled_echi"]
        if "echi_offset" in config["motor_corrections"]:
            echi_offset = config["motor_corrections"]["echi_offset"]
        if "echi_offset_sign" in config["motor_corrections"]:
            echi_offset_sign = config["motor_corrections"]["echi_offset_sign"]
        for dseti in range(1, len(self.src.dataset)):
            prm = self.src.dataset[dseti].prm
            ephi = float(prm["ephi"])
            echi = float(prm["echi"])
            ephi = round(ephi + (ephi_coupled_echi * echi), 3)
            if ephi < 0: ephi = ephi + 360
            prm["ephi"] = str(ephi)
            
            prm["echi"] = str(round(echi_offset + echi_offset_sign*echi,2))
            
                
        
        True  
            
#**************************************************************************************
#**************************************************************************************            
class SourceFileDEF(QGroupBox,SourceCommon):
    def __init__(self, ScanmanMain):
        QGroupBox.__init__(self)
        SourceCommon.__init__(self, ScanmanMain)
        
        self.name="SourceFile"
        self.ui = Ui_SourceFile()
        self.ui.setupUi(self)

        self.filedialog = QFileDialog()
        self.filedialog.setFileMode(QFileDialog.ExistingFiles)
        self.filedialog.setViewMode(QFileDialog.Detail)
        self.file_tbl = Table(self.ui.file_tbl)

        
        self.curfilter = ""
        self.colnr = {'Filename':0, 'Ext':1, 'Type':2, 'Location':3}
    
    #**************************************************************************************
    def getfileindex(self,location):
        for i in range(len(self.filelist)):
            if self.filelist[i].location == location:
                return i
        return -1
    
            
    #**************************************************************************************
    def OpenFile(self, fnames="", finfo=None):
        if fnames == False:
            file_types = "NeXus (*.hdf);;Fullprof (*.xy);;ASCII Two Column (*.txt);;Gumtree Exported (*.xyd);;MCstas (*.sim);;MCStasPS (*.cmds);;PeakFit (*.pkf);; All (*.*)"
            #self.filedialog.selectFilter(self.curfilter)
            fnames, filters = self.filedialog.getOpenFileNamesAndFilter(self, 'Open file', '', file_types, initialFilter=self.curfilter)
            if (fnames==[]): return
            self.filedialog.setDirectory(os.path.dirname(str(fnames[0])))
            self.curfilter = filters
        
        ftbl = self.ui.file_tbl
        
        wedisconnected = False
        try:
            ftbl.cellChanged.disconnect()     #otherwise this function might be called recursively
            wedisconnected = True
        except:
            True
        #self.src.Clear()
        
        numfiles = len(fnames)
        progress = ProgressBar("Opening files...", numfiles)

        for afile in fnames:
            progress.setinfo(afile)
            if finfo == None:
                finfo = FileInfo(afile, self.config)
            if finfo.src == None:
                progress.close()
                break
            
            ftbl.setRowCount(ftbl.rowCount()+1)
            duplicate = ftbl.findItems(finfo.location, qtCore.Qt.MatchExactly)      #the file is already in the table
            if len(duplicate) > 0:
                row = duplicate[0].row()
                ftbl.removeRow(row)                                #now remove it from the table
                if row == self.getfileindex(finfo.location):  self.filelist.pop(row)      #if it exists in the filelist as well
                #self.src == self.filelist[findex].src
            
            if len(self.filelist)>0:
                finfo.src.lowerchan=self.filelist[-1].src.lowerchan
                finfo.src.upperchan=self.filelist[-1].src.upperchan
                finfo.srcsplit.lowerchan=self.filelist[-1].srcsplit.lowerchan
                finfo.srcsplit.upperchan=self.filelist[-1].srcsplit.upperchan        
            self.filelist.append(finfo)                     #append it to the filelist                 
            #for key in self.colnr.iterkeys():
            for key in self.colnr.keys():
                someitem = qt.QTableWidgetItem()
                someitem.setTextAlignment(qtCore.Qt.AlignRight)
                someitem.setFlags(someitem.flags() & ~qtCore.Qt.ItemIsEditable)
                if key == 'Filename':
                    someitem.setFlags(someitem.flags() | qtCore.Qt.ItemIsUserCheckable)
                    someitem.setCheckState(qtCore.Qt.Checked)
                    someitem.setText(finfo.filename)
                elif key == 'Ext': someitem.setText(finfo.ext)
                elif key == 'Type': someitem.setText(finfo.type)
                elif key == 'Location': someitem.setText(finfo.location)
                ftbl.setItem(ftbl.rowCount()-1,self.colnr[key],someitem)
            if progress.wasCanceled(): break
            finfo=None
            progress.step()
            True
            
        if(wedisconnected): ftbl.cellChanged.connect(self.CellValueChanged)   #Reconnect the signal
        self.ui.nrfiles_label.setText(str(len(self.filelist)))    

        
        try:
            guessexport = self.filelist[-1].src.precparams.keys()
            for parname in guessexport:
                if (parname not in self.scanman.exportparams): self.scanman.exportparams.append(parname)
            
            for i in range(self.scanman.ui.prm_table.rowCount()):
                self.scanman.PostPrecChanged(i,2)                   #Let the newly opened file have the same values for post sets precicion
            self.SelectDataFile(-1)        
            ftbl.setCurrentCell(ftbl.rowCount()-1,1)
        except:
            True

               
    #**************************************************************************************
    def SelectDataFile(self, findex,setnr = -1):
        if (self.src == self.filelist[findex].src):
            return
        elif (self.ui.lim_mem_check.isChecked()):       #Remove the calculated datasets from ram. Useful if a lot of 2D data files needs to be exported
            self.srcp.Clear()
            if self.srcsplit != self.src:
                self.srcsplit.Clear()
            
        self.src = self.filelist[findex].src
        self.paramdict = self.filelist[findex].src.prm
        self.detdict = self.filelist[findex].src.detprm
        
        self.scanman.datasrc = self.src         #We have to do this because the linking is broken when assigning different file's datasets
        self.srcp = self.filelist[findex].srcp
        self.srcsplit = self.filelist[findex].srcsplit
        self.currfileindex = findex
        
        self.scanman.Generate(selectnr = setnr)
        True
    
    #**************************************************************************************
    def RowDoubleClicked(self,row,col):
        self.SelectDataFile(row)
        True

    #**************************************************************************************
    def CellValueChanged(self,row,col):
        ftbl = self.ui.file_tbl
        item = ftbl.item(row, col)
        if (item.checkState() == qtCore.Qt.Checked):
            self.filelist[row].selected = True
        else:
            self.filelist[row].selected = False


    #**************************************************************************************
    def Remove(self):
        ftbl = self.ui.file_tbl
        rowselection = list(set([x.row() for x in ftbl.selectedIndexes()]))     #many items in a row, the 'set' will remove duplicate row numbers
        rowselection.reverse()      #Sort from high to low
        for irow in rowselection:
            try:
                fname = ftbl.item(irow,self.colnr['Location']).text()
            except:
                True
            ftbl.removeRow(irow)
            for afile in self.filelist:
                if afile.location == fname: self.filelist.remove(afile)
        self.ui.nrfiles_label.setText(str(len(self.filelist)))

    #**************************************************************************************
    def Select(self):
        ftbl = self.ui.file_tbl
        rowselection = list(set([x.row() for x in ftbl.selectedIndexes()]))
        for irow in rowselection:
            ftbl.item(irow, self.colnr['Filename']).setCheckState(qtCore.Qt.Checked)
        
    #**************************************************************************************
    def Unselect(self):
        ftbl = self.ui.file_tbl
        rowselection = list(set([x.row() for x in ftbl.selectedIndexes()]))
        for irow in rowselection:
            ftbl.item(irow, self.colnr['Filename']).setCheckState(qtCore.Qt.Unchecked)
        

    #**************************************************************************************
    def PSSelected(self,checked):
        if (checked == True):
            self.ui.filenameps_edit.setEnabled(True)
            self.ui.openps_button.setEnabled(True)
            self.ui.filename_edit.setText(os.path.basename(str(self.ui.filename_edit.text())))
        else:
            self.ui.filenameps_edit.setDisabled(True)
            self.ui.openps_button.setDisabled(True)
            a=2
        
    
    #**************************************************************************************
    def ReadFile(self,fname):
        f = open(fname, 'r')
        filecontent = f.read()
        f.close()
        
        #Get the parameters
        paramStartIdx = filecontent.find("# Param:")
        paramEndIdx = filecontent.find("# type:", paramStartIdx)
        paramDef = filecontent[paramStartIdx:paramEndIdx]
        validch = "".join( [ c for c in printables if c != "," and c != ")" and c != "=" and c != "("] )
        param_str = CaselessLiteral("# Param: ").suppress()
        equal = CaselessLiteral("=").suppress()
        param_name = Word(validch)
        param_value = Word(validch)
        paramsexpr = ZeroOrMore(Group(param_str + param_name + equal + param_value))
        paramsparsed = paramsexpr.parseString(paramDef)
        self.paramdict = {paramsparsed[i][0]:paramsparsed[i][1] for i in range(len(paramsparsed))}
                        
        #Get the detector xmin and xmax
        xlimitsStartIdx = filecontent.find("# xlimits:", paramEndIdx)
        xlimitsEndIdx = filecontent.find("#", xlimitsStartIdx+1)
        xlimitsDef = filecontent[xlimitsStartIdx:xlimitsEndIdx]
        xlimexpr = CaselessLiteral("# xlimits:").suppress() + Word(validch) + Word(validch)
        xlimparsed = xlimexpr.parseString(xlimitsDef)
        
        #Get the actual data
        dataStartIdx = filecontent.find("# Data ", paramEndIdx)
        dataStartIdx = filecontent.find(":", dataStartIdx)
        dataStartIdx = dataStartIdx + 1
        dataEndIdx = filecontent.find("# EndDate",dataStartIdx)
        dataDef = filecontent[dataStartIdx:dataEndIdx]
        x = intensity = intensity_err = ncount = Word(validch)
        dataexpr = ZeroOrMore(Group(x + intensity + intensity_err + ncount))
        self.dataparsed = dataexpr.parseString(dataDef)
        
        #self.detdict = {"det_xmin":-100.0, "det_xmax":100.0, "sam_to_det":1000.0, "stth":90.0, "lambda":1.659}
        self.detdict["det_xmin"] = float(xlimparsed[0])*1000
        self.detdict["det_xmax"] = float(xlimparsed[1])*1000
        self.detdict["sam_to_det"] = float(self.paramdict["cor_to_det"])*1000
        self.detdict["stth"] = float(self.paramdict["det_takeoff"])
        self.detdict["lambda"] = (float(self.paramdict["source_lam_min"]) + float(self.paramdict["source_lam_max"]))/2.0 
        
        
        #self.scanman.Generate()     #Will subsequently call our GetData
        #self.GetData()
        y = np.array([float(self.dataparsed[i][3]) for i in range(len(self.dataparsed))])
        self.src.x_chan = np.arange(0, len(self.dataparsed), 1)
        self.src.nchan = len(self.src.x_chan)
        self.src.AddData(y,self.paramdict, self.detdict, "McStas", fname)
        
    
    #**************************************************************************************
    def ReadPSFile(self,fname):
        f = open(fname, 'r')
        lastdir = os.path.dirname(str(fname))
        self.filedialog.setDirectory(lastdir)
        filecontent = f.read()
        f.close()
        
        #Get a list of the directories
        dirStartIdx = filecontent.find("--dir=")
        detfile = os.path.basename(str(self.ui.filename_edit.text()))
        while dirStartIdx > -1 :
            dirStartIdx = dirStartIdx + 7
            dirEndIdx = filecontent.find('"',dirStartIdx)
            simfilename = filecontent[dirStartIdx:dirEndIdx] + os.path.sep + detfile
            dirStartIdx = filecontent.find("--dir=",dirEndIdx)
            self.ReadFile(simfilename)
        
        self.src.CalcAllAxis()
        self.src.CalcSumSetCommon(fname)
        self.src.CalcSumSet("raw")
        self.src.SelectFrame("raw")
        self.src.SelectDataSet(-1)
        
    
        
    

        
    
    #**************************************************************************************
    def OpenPSFile(self):
        file_types = "MCstasPS (*.cmds);;All (*.*)"
        fname = self.filedialog.getOpenFileName(self, 'Open file', '', file_types)
        if (fname==''): return
        self.src.Clear()
        self.filedialog.setDirectory(os.path.dirname(str(fname)))
        self.ReadPSFile(fname)
        self.ui.filenameps_edit.setText(fname)
        self.scanman.Generate()

    
    #**************************************************************************************
    def GetData(self):
        #y = np.array([float(self.dataparsed[i][3]) for i in range(len(self.dataparsed))])
        #self.src.chan = np.arange(0, len(self.dataparsed), 1)
        #self.src.nchan = len(self.src.chan)
        #self.src.AddData(y,self.paramdict, self.detdict)

        
        True