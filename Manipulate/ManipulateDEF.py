'''
Created on 06 Feb 2015

@author: Deon
'''
from PyQt4.Qt import QDialog
from Manipulate.ManipulateGUI import Ui_Manipulate
import copy
import numpy as np
from Source import Srcpar
from Source import SourceFileDEF
from os import path

class ManipulateDEF(QDialog):
    def __init__(self, ScanmanMain):
        '''
        Constructor
        '''
        QDialog.__init__(self)

        self.name = "Manipulate"
        self.ui = Ui_Manipulate()
        self.ui.setupUi(self)
        self.scanman = ScanmanMain
        
        import DatasetsAppliedDEF
        #self.datasetsapplied = DatasetsAppliedDEF.DatasetsAppliedDEF(self,self.scanman)
        self.datasetsapplied = DatasetsAppliedDEF.DatasetsAppliedDEF(self.scanman)
        self.ui.datasetappliedLayout.removeWidget(self.ui.datasetsappliedframe)
        self.ui.datasetsappliedframe=self.datasetsapplied
        self.ui.datasetappliedLayout.addWidget(self.ui.datasetsappliedframe)
        
        
        #self.setParent(self.scanman)
        #self.hide()
        
        
        
    #**************************************************************************************
    def PopulateParamCombos(self):
        xparam = self.ui.vx_combo.currentText()
        yparam = self.ui.vy_combo.currentText()
        
        paramskeys=sorted(self.scanman.datasrc.prm.keys())
        vxparams=[self.ui.vx_combo.itemText(s) for s in range(self.ui.vx_combo.count())]
        if vxparams == paramskeys:
            True
        else:
            self.ui.vx_combo.clear()
            self.ui.vx_combo.addItems(paramskeys)
            self.ui.vy_combo.clear()
            self.ui.vy_combo.addItems(paramskeys)
            
        if xparam in paramskeys:
            self.ui.vx_combo.setCurrentIndex(self.ui.vx_combo.findText(xparam))
        if yparam in paramskeys:
            self.ui.vy_combo.setCurrentIndex(self.ui.vy_combo.findText(yparam))
            
            
    #**************************************************************************************
    def AddVirtualAxes(self):
        xparam = self.ui.vx_combo.currentText()
        yparam = self.ui.vy_combo.currentText()
        rotated = float(self.ui.angle_edit.text())
        
        currfileindex = self.scanman.ui.sourceGroupBox.currfileindex
        currset = self.scanman.datasrc.currset
        
        flistidx, selectstart, selectend =self.ui.datasetsappliedframe.GetSelection()
        for filei in flistidx:
            self.scanman.ui.sourceGroupBox.SelectDataFile(filei)
            setend = copy.copy(selectend)
            setstart = selectstart
            if setend == -1:
                setend = len(self.scanman.datasrc.dataset)
                
            for setnr in range(setstart,setend):
                #self.scanman.ui.dataset_spin.setValue(setnr)        #Selects the next dataset - Hopefully the callback will be completed before the next statements are executed
                self.scanman.SelectData(setnr,display=False)
                src = self.scanman.datasrc
                x = float(src.prm[self.ui.vx_combo.currentText()])
                y = float(src.prm[self.ui.vy_combo.currentText()])
                
                theta = np.rad2deg(np.arctan(y/x))
                if theta <=0: theta = theta+180
                if y < 0: theta = theta+180
                alpha = theta - rotated
                r = np.sqrt(x*x + y*y)
                vx = r * np.cos(np.deg2rad(alpha))
                vy = r * np.sin(np.deg2rad(alpha))                
                src.prm["vsx"]=str(vx)
                src.prm["vsy"]=str(vy)
            #self.scanman.UpdatePrmTable(self.scanman.datasrc.currset)
        True
        self.scanman.ui.sourceGroupBox.SelectDataFile(currfileindex)
        self.scanman.SelectData(currset)
        self.ui.vx_combo.setCurrentIndex(self.ui.vx_combo.findText(xparam))
        self.ui.vy_combo.setCurrentIndex(self.ui.vy_combo.findText(yparam))

    #**************************************************************************************
    def RemoveBelowThreshold(self):
        ythreshold = int(self.ui.ythreshold_edit.text())
        thresholddataset = int(self.ui.thresholddataset_edit.text())
        currset = self.scanman.datasrc.currset
        
        flistidx, selectstart, selectend =self.ui.datasetsappliedframe.GetSelection()
        
        if self.scanman.axistype == "Channel" : axistype = "ch"
        elif self.scanman.axistype == "Position" : axistype = "mm"
        elif self.scanman.axistype == "Angle" : axistype = "2th"
        elif self.scanman.axistype == "d-spacing" : axistype = "d"
        
        
        for filei in flistidx:
            self.scanman.ui.sourceGroupBox.SelectDataFile(filei)
            setend = copy.copy(selectend)
            setstart = selectstart
            if setend == -1:
                setend = len(self.scanman.datasrc.dataset)
            self.scanman.SelectData(thresholddataset,display=False)
            src=self.scanman.datasrc
            validpoints=np.where(src.y>ythreshold)[0]
            dstsrc = Srcpar.Srcpar(src.config)
                
            for setnr in range(setstart,setend):
                self.scanman.SelectData(setnr,display=False)
                src = self.scanman.datasrc
                fname = "threshold_reduced_"+str(thresholddataset)+"_"+str(ythreshold)
                dstsrc.AddData(src.y[validpoints], src.prm, src.detprm, src.origin + "_reduced", 
                               fname, {axistype:src.x[validpoints]})
                True
            #scanman.Source.FileInfo
            finfo = SourceFileDEF.FileInfo(fname,self.scanman.config,dstsrc)
            self.scanman.ui.sourceGroupBox.OpenFile([fname], finfo)
            True
        
        
        #dst.AddData(y[ind],paramdict, detdict, "Gumtree_xyd", fname, {self.scanman.axistype:xaxis[ind]})
        
        #dst.AddData(y[ind],paramdict, detdict, "Gumtree_xyd", fname, {axistype:xaxis[ind]})
        
        True
        
    #**************************************************************************************
    def RemoveEverynth(self):
        nth = int(self.ui.removeevery_edit.text())
        currset = self.scanman.datasrc.currset
        
        flistidx, selectstart, selectend =self.ui.datasetsappliedframe.GetSelection()
        
        if self.scanman.axistype == "Channel" : axistype = "ch"
        elif self.scanman.axistype == "Position" : axistype = "mm"
        elif self.scanman.axistype == "Angle" : axistype = "2th"
        elif self.scanman.axistype == "d-spacing" : axistype = "d"
        
        
        for filei in flistidx:
            self.scanman.ui.sourceGroupBox.SelectDataFile(filei)
            setend = copy.copy(selectend)
            setstart = selectstart
            if setend == -1:
                setend = len(self.scanman.datasrc.dataset)
            #self.scanman.SelectData(thresholddataset,display=False)
            src=self.scanman.datasrc
            #validpoints=np.where(src.y>ythreshold)[0]
            dstsrc = Srcpar.Srcpar(src.config)
            removepoints = range(nth-1, src.nchan, nth)
            validpoints=range(src.nchan)
            for popval in removepoints:
                validpoints.remove(popval)
            
                
            for setnr in range(setstart,setend):
                self.scanman.SelectData(setnr,display=False)
                src = self.scanman.datasrc
                fname = "removed_every_"+str(nth)+"_dataset"
                dstsrc.AddData(src.y[validpoints], src.prm, src.detprm, src.origin + "_removed", 
                               fname, {axistype:src.x[validpoints]})
                True
            #scanman.Source.FileInfo
            finfo = SourceFileDEF.FileInfo(fname,self.scanman.config,dstsrc)
            self.scanman.ui.sourceGroupBox.OpenFile([fname], finfo)
            True
        
        True

    #**************************************************************************************
    def Transposexy(self):
        True
        src = self.scanman.datasrc
        
    #**************************************************************************************
    def ExtractDetectorLines(self):
        currset = self.scanman.datasrc.currset
        flistidx, selectstart, selectend =self.ui.datasetsappliedframe.GetSelection()
        
        #if self.scanman.axistype == "Channel" : axistype = "ch"
        #elif self.scanman.axistype == "Position" : axistype = "mm"
        #elif self.scanman.axistype == "Angle" : axistype = "2th"
        #elif self.scanman.axistype == "d-spacing" : axistype = "d"
        axistype = "mm"
        
        if self.ui.horizontal_radio.isChecked() == True: 
            horizontal = True
            detectoraxis = "detector_y"
        else:
            horizontal = False
            detectoraxis = "detector_x"
        

        
        for filei in flistidx:
            self.scanman.ui.sourceGroupBox.SelectDataFile(filei)
            xbins = int(self.ui.rebinx_edit.text())
            ybins = int(self.ui.rebiny_edit.text())
            if xbins == -1: xbins = len(self.scanman.datasrc.x)
            if ybins == -1: ybins = len(self.scanman.datasrc.y)
            setend = copy.copy(selectend)
            setstart = selectstart
            dstsrc = Srcpar.Srcpar(self.scanman.datasrc.config)
            
            fname = path.basename(self.scanman.datasrc.filename) +"_"+detectoraxis+"_extracted"
            if setend == -1:
                setend = len(self.scanman.datasrc.dataset)-1
            for setnr in range(setstart,setend+1):
                self.scanman.SelectData(setnr,display=False)
                src = self.scanman.datasrc
                cframe=src.dataset[setnr].currframe
                if horizontal ==True:
                    x=cframe.hc_mm
                    y=cframe.vc_mm
                    n = cframe.n
                else:
                    x=cframe.vc_mm
                    y=cframe.hc_mm
                    n = cframe.n.transpose()
                #xx = np.array([[a]*len(y) for a in x])
                #yy=np.array([y]*len(x))                    
                yy = np.array([[a]*len(x) for a in y])
                xx=np.array([x]*len(y))                    
                histn, xedges, yedges = np.histogram2d(x=xx.flatten(), y=yy.flatten(), bins=[xbins,ybins], weights = n.flatten())
                histn = histn.transpose()
                xc = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
                yc = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
                for irow in range(len(yc)):
                    dstprm = copy.copy(src.prm)
                    dstprm[detectoraxis]=str(yc[irow])
                    dstsrc.AddData(histn[irow], dstprm, src.detprm, src.origin + "_"+detectoraxis+"_lines_extracted", 
                               fname, {axistype:xc})
                True
            finfo = SourceFileDEF.FileInfo(fname,self.scanman.config,dstsrc)
            self.scanman.ui.sourceGroupBox.OpenFile([fname], finfo)
            True
            #validpoints=np.where(src.y>ythreshold)[0]

    
    #**************************************************************************************
    def Test(self):
        currset = self.scanman.datasrc.currset