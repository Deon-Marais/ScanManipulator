'''
Created on 06 Feb 2015

@author: Deon
'''
from PyQt4.Qt import QDialog
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtCore

from Source.ScanmanPeakFit_pkfGUI import Ui_ScanmanPeakFit_pkf
import copy
import numpy as np

class ScanmanPeakFit_pkfDEF(QDialog):
    def __init__(self):
        '''
        Constructor
        '''
        QDialog.__init__(self)

        self.name = "ScanmanPeakFit_pkf"
        self.ui = Ui_ScanmanPeakFit_pkf()
        self.ui.setupUi(self)
        self.setWindowFlags(qtCore.Qt.WindowSystemMenuHint or qtCore.Qt.WindowTitleHint)
        #self.windowFlags() &  
        #~qtCore.Qt.WindowContextHelpButtonHint
        self.selectedparams = []
        self.selectedpeaks = []
        #self.scanman = ScanmanMain


    #**************************************************************************************
    def Selectallparams_pressed(self):
        prmtbl = self.ui.prm_table
        checkstate = self.ui.params_check.checkState()
        for i in range(prmtbl.rowCount()): prmtbl.item(i, 0).setCheckState(checkstate)
            
    #**************************************************************************************
    def Selectallpeaks_pressed(self):
        pktbl = self.ui.peak_table
        checkstate = self.ui.peaks_check.checkState()
        for i in range(pktbl.rowCount()): pktbl.item(i, 0).setCheckState(checkstate)
        
    #**************************************************************************************
    def ParamSelectionChanged(self, item):
        if item.column() != 0: return
        name = str(item.text())
        if (item.checkState() == 0) and (name in self.selectedparams):
            self.selectedparams.remove(name)
        #elif (item.checkState() !=0) and (name not in self.selectedparams):
        elif (item.checkState() >0) and (name not in self.selectedparams):
            self.selectedparams.append(name)

    #**************************************************************************************
    def PeakSelectionChanged(self, item):
        if item.column() != 0: return
        #name = str(item.text())
        name = int(item.text())
        if (item.checkState() == 0) and (name in self.selectedpeaks):
            self.selectedpeaks.remove(name)
        elif (item.checkState() !=0) and (name not in self.selectedpeaks):
            self.selectedpeaks.append(name)
            
    #**************************************************************************************
    def settableoptions(self,paroptions,prmtbl):
        prmtbl.setRowCount(len(paroptions))
        if type(paroptions) == dict: 
            #params = paroptions.items()
            params = sorted(paroptions.items())
        elif type(paroptions) == list:
            #params = paroptions
            params = sorted(paroptions)
        #params.sort()
        for i in range(len(params)):
            item = str(params[i][0])
            nameitem = qt.QTableWidgetItem()
            nameitem.setFlags((nameitem.flags() | qtCore.Qt.ItemIsUserCheckable) & ~qtCore.Qt.ItemIsEditable)
            nameitem.setTextAlignment(qtCore.Qt.AlignLeft)
            nameitem.setText(item)
            if item == "Records": nameitem.setCheckState(~qtCore.Qt.Checked)
            else: nameitem.setCheckState(qtCore.Qt.Checked)
            prmtbl.setItem(i,0,nameitem)
            
    
    
    
    #**************************************************************************************
    def setparoptions(self,paroptions):
        if "Mods" in paroptions.keys():
            paroptions.pop("Mods")
        self.settableoptions(paroptions,self.ui.prm_table)
           
        
    #**************************************************************************************
    def setdataoptions(self, dataoptions):
        #dataoptions.sort()
        self.ui.datavals_combo.clear()
        #self.ui.datavals_combo.addItems(dataoptions)
        self.ui.datavals_combo.addItems(sorted(dataoptions))
        True
        
    #**************************************************************************************
    def setpeakoptions(self,peakoptions):
        self.settableoptions(peakoptions,self.ui.peak_table)
        True
    
    #**************************************************************************************
    def ok_pressed(self):
        self.selectedfit = self.ui.datavals_combo.currentText()
        self.precision = float(self.ui.precision_edit.text())
        self.permutate = self.ui.permutate_check.isChecked()
        self.close()
        True
        
    def close_pressed(self):
        self.selectedfit = ""
        self.close()
        True
               
        
    