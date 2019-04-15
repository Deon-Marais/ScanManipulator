'''
Created on 26 Mar 2014

@author: Deon
'''
from PyQt4.QtGui import QMainWindow as QMainWindow
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QFileDialog
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtCore
from ScanmanGUI import Ui_MainWindow
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
#from matplotlib.patches import Ellipse
#from mpl_toolkits import mplot3d
import numpy as np
import os
from shutil import copyfile
import pickle
import yaml
from mylib import ProgressBar
from mylib import Graph
from mylib import Table
from Source import NeXus_hdf

class ScanmanDEF (QMainWindow):
    #signal={}
    
    signalxtypechanged = qtCore.pyqtSignal(str)
    
        
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.attentuation3D_check.setEnabled(False)
        self.ui.att_cor_3D_btn.setEnabled(False)
        
        self.signal={}
        self.signal["xtypechanged"] = self.signalxtypechanged
        
        #self.config = yaml.load(open("Session/config.yml"), Loader=yaml.FullLoader)
        self.config = yaml.load(open("Session/config.yml"))
        self.setWindowTitle("Scanman - %s" %(self.config["instrument"]))
        
        iconpath = os.path.abspath(os.path.curdir + os.sep + "icons" + os.sep)
        app_icon = qt.QIcon()
        #app_icon.addFile(iconpath + '16x16.ico', qtCore.QSize(16,16))
        #app_icon.addFile(iconpath + '24x24.ico', qtCore.QSize(24,24))
        #app_icon.addFile(iconpath + '32x32.ico', qtCore.QSize(32,32))
        #app_icon.addFile(iconpath + '48x48.ico', qtCore.QSize(48,48))
        #app_icon.addFile(iconpath + '256x256.ico', qtCore.QSize(256,256))
        app_icon.addFile(iconpath + '256x256.png', qtCore.QSize(256,256))
        self.setWindowIcon(app_icon)
        
        self.axistype = "Channel"
                 
        self.lineseries=[]
        self.lineseries.append(Line2D([], [], color='grey', linewidth = 0.5))
        self.ui.graph.figure.axes[0].add_line(self.lineseries[0])
        self.error_collection=[]
        self.error_collection.append(mpl.collections.LineCollection([],linewidth = 0.5, color='grey'))
        self.ui.graph.figure.axes[0].add_collection(self.error_collection[0])
        
        
        self.ui.diffgraph.figure.axes[0].tick_params(axis='x', labelbottom=False)
        self.ui.diffgraph.figure.axes[0].yaxis.set_major_locator(MaxNLocator(4))
        
        
        self.xlowmask = self.ui.graph.figure.axes[0].axvspan(0,0, facecolor = 'g', alpha = 0.5)
        self.xupmask = self.ui.graph.figure.axes[0].axvspan(0,0, facecolor = 'g', alpha = 0.5)

        
        self.graph_main = Graph(self.ui.graph)
        self.graph_diff = Graph(self.ui.diffgraph)
        self.graph_2d = Graph(self.ui.graph_2d)
               
        ax = self.ui.graph_2d.figure.add_subplot(111)

        self.im2d = mpl.image.NonUniformImage(ax, extent=(0, 0, 1, 1))

        self.im2d.set_data([0,1],[0,1],[[1,2],[1,2]])
        ax.images.append(self.im2d)

        self.graph_2d.colorbar2d=self.ui.graph_2d.figure.colorbar(self.im2d)
        self.ui.graph_2d.figure.tight_layout()
        #self.ui.graph_2d.figure.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08, rect=(0, 0, 1, 1))
        self.ui.graph_2d.figure.subplots_adjust(bottom=0.05)

        

        from Attenuation import AttenuationDEF
        self.attenuationgui = AttenuationDEF.AttenuationDEF(self)
        
        from Attenuation import Attenuation3DDEF
        self.attenuation3Dgui = Attenuation3DDEF.Attenuation3DDEF(self)


        from Manipulate import ManipulateDEF
        self.manipulategui = ManipulateDEF.ManipulateDEF(self)
        
        self.fitlist=[]
        self.Fit=[]
        from Fit import PeakProfilesDEF as PeakProfilesDEF
        #self.Fit.append(PeakProfilesDEF.PeakProfilesDEF(self))
        #self.fitlist.append("PeakProfiles")
        from Fit import PeakDEF
        self.Fit.append(PeakDEF.PeakDEF(self))
        self.fitlist.append("Peak")
        from Fit import EntryCurveDEF
        self.Fit.append(EntryCurveDEF.EntryCurveDEF(self))
        self.fitlist.append("EntryCurve")
        from Fit import VoigtDEF
        self.Fit.append(VoigtDEF.VoigtDEF(self))
        self.fitlist.append("Voigt")
        #self.fitlist = self.GetPlugins("Fit",self)
        for fit in self.fitlist:
            self.ui.fitComboBox.addItem(fit)
        #for fit in self.Fit:            #There is only one
        #    self.ui.fitGroupBox.hide()
        #    self.ui.fitLayout.removeWidget(self.ui.fitGroupBox)
        #    self.ui.fitGroupBox = fit
        #    break

        fffname = self.config["flatfield_cor"]["file"]
        self.ui.fffname_edit.setText(fffname)
        self.flatfieldsrc = NeXus_hdf.NeXus_hdf_read(fffname, self.config)

        self.sourcelist=[]
        self.Source=[]
        from Source import SourceFileDEF
        self.Source.append(SourceFileDEF.SourceFileDEF(self))
        self.sourcelist.append("SourceFile")
        from Source import GenPeaksDEF
        self.Source.append(GenPeaksDEF.GenPeaksDEF(self))
        self.sourcelist.append("GenPeaks")
        from Source import HistmemDEF
        self.Source.append(HistmemDEF.HistmemDEF(self))
        self.sourcelist.append("Histmem")
        #self.sourcelist = self.GetPlugins("Source",self)
        for src in self.sourcelist: 
            self.ui.sourceComboBox.addItem(src)
        self.datasrc = self.ui.sourceGroupBox.src
        
        self.outputlist=[]
        self.Output=[]
        from Output import FiguresDEF
        self.Output.append(FiguresDEF.FiguresDEF(self))
        self.outputlist.append("Figures")
        from Output import Intensity_mapDEF
        self.Output.append(Intensity_mapDEF.Intensity_mapDEF(self))
        self.outputlist.append("Intensity_map")
        from Output import ExcelDEF
        self.Output.append(ExcelDEF.ExcelDEF(self))
        self.outputlist.append("Excel")
        from Output import AsciiDEF
        self.Output.append(AsciiDEF.AsciiDEF(self))
        self.outputlist.append("Ascii")
        from Output import SicsDEF
        self.Output.append(SicsDEF.SicsDEF(self))
        self.outputlist.append("Sics")
        #self.outputlist = self.GetPlugins("Output",self)
        for export in self.outputlist:
            self.ui.outputComboBox.addItem(export)
        #self.export = self.ui.outputGroupBox.export
        self.exportparams = []
             

        #self.ui.fitGroupBox.AddRange()
        #self.ui.fitLayout.addWidget(self.ui.fitGroupBox)
        #self.ui.fitLayout.update()
        #self.ui.fitGroupBox.show()
        
        self.misclist=[]
        self.Misc=[]
        from Misc import NeuralNetDEF
        self.Misc.append(NeuralNetDEF.NeuralNetDEF(self))
        self.misclist.append("NeuralNet")
        for msc in self.misclist: 
            self.ui.miscComboBox.addItem(msc)
        
        
        self.Scanmanfiledialog = QFileDialog()
        self.Scanmanfiledialog.setDirectory("Session")
        self.Scanmanfiledialog.setViewMode(QFileDialog.Detail)
  
        self.prm_table = Table(self.ui.prm_table)


    #**************************************************************************************
    def GetPlugins(self,plugtype,parent):
        filelist = os.listdir(plugtype)
        pluginList = []
        for afile in filelist:
            if afile[-6:] == "DEF.py": pluginList.append(afile[:-6])
            
        exec("self." + plugtype + "=[]")
        for plugin in pluginList:
            exec("from "+ plugtype+" import "+ plugin + "DEF")
            exec("self."+ plugtype + ".append("+ plugin + "DEF."+ plugin + "DEF(parent))")
        
        return pluginList
        
    #**************************************************************************************
    def OpenScanman(self):
        self.Scanmanfiledialog.setFileMode(QFileDialog.ExistingFiles)
        file_types = "Configuration (*.yml)"
        fnames = self.Scanmanfiledialog.getOpenFileNames(self, 'Open file', '', file_types)
        if (fnames==''): return
        self.config = yaml.load(open(fnames[0]))
        self.Scanmanfiledialog.setDirectory(os.path.dirname(str(fnames[0])))
        
        self.setWindowTitle("Scanman - %s" %(self.config["instrument"]))
        
        self.ui.detDim_xmin_edit.setText(str(self.config['source']['detector']['det_xmin']))
        self.ui.detDim_xmax_edit.setText(str(self.config['source']['detector']['det_xmax']))
        self.DetSizeChanged()
        
        self.ui.sam2det_edit.setText(str(self.config['source']['detector']['sam_to_det']))
        self.SampleToDetectorChanged()
        
        self.ui.stth_edit.setText(str(self.config['source']['detector']['stth']))
        self.StthChanged()
        
        self.ui.wavelength_edit.setText(str(self.config['source']['detector']['lambda']))
        self.DSpacingChanged()
        
        fffname = self.config["flatfield_cor"]["file"]
        self.ui.fffname_edit.setText(fffname)
        self.flatfieldsrc = NeXus_hdf.NeXus_hdf_read(fffname, self.config)
        
        copyfile(fnames[0], "Session" + os.path.sep + "config.yml")
        
        True
        

    #**************************************************************************************
    def SaveScanman(self):
        self.Scanmanfiledialog.setFileMode(QFileDialog.AnyFile)
        file_types = "Configuration (*.yml)"
        fname = self.Scanmanfiledialog.getSaveFileName(self, 'Open file', '', file_types)
        if (fname==''): return
        self.Scanmanfiledialog.setDirectory(os.path.dirname(str(fname[0])))
        f = open(fname, 'w')
        
        yaml.dump(self.config, f)
        f.close()
        
    #**************************************************************************************
    def SelectNewSource(self):
        newsrc = str(self.ui.sourceComboBox.currentText()) + "DEF"
        srcplugin = str(self.ui.sourceComboBox.currentText())
        self.ui.sourceGroupBox.hide()
        self.ui.sourceLayout.removeWidget(self.ui.sourceGroupBox)
        for plugin in self.Source:
            if plugin.name == srcplugin:
                self.ui.sourceGroupBox = plugin
                break
        self.ui.sourceLayout.addWidget(self.ui.sourceGroupBox)
        self.datasrc = self.ui.sourceGroupBox.src
        self.ui.sourceLayout.update()
        self.ui.sourceGroupBox.show()
        self.Generate()
    
    #**************************************************************************************
    def SelectNewFit(self):
        newfit = str(self.ui.fitComboBox.currentText()) + "DEF"
        fitplugin = str(self.ui.fitComboBox.currentText())
        self.ui.fitGroupBox.hide()
        try:
            self.ui.fitGroupBox.HideGraphlines()
        except:
            True
        
        #self.ui.var_slider.valueChanged.disconnect()
        try:
            self.signal["xtypechanged"].disconnect()
        except:
            True
        self.ui.fitLayout.removeWidget(self.ui.fitGroupBox)
        for plugin in self.Fit:
            if plugin.name == fitplugin:
                self.ui.fitGroupBox = plugin
                break
        self.signal["xtypechanged"].connect(self.ui.fitGroupBox.xTypeChanged)
        self.ui.fitLayout.addWidget(self.ui.fitGroupBox)
        try:
            self.ui.fitGroupBox.ShowGraphlines()
        except:
            True
        self.ui.fitLayout.update()
        self.ui.fitGroupBox.show()
 
        
    #**************************************************************************************
    def SelectNewExport(self):
        newexp = str(self.ui.outputComboBox.currentText()) + "DEF"
        expplugin = str(self.ui.outputComboBox.currentText())
        self.ui.outputGroupBox.hide()
        self.ui.outputLayout.removeWidget(self.ui.outputGroupBox)
        for plugin in self.Output:
            if plugin.name == expplugin:
                self.ui.outputGroupBox = plugin
                break
        self.ui.outputLayout.addWidget(self.ui.outputGroupBox)
        #self.datasrc = self.ui.sourceGroupBox.src
        self.ui.outputLayout.update()
        self.ui.outputGroupBox.show()

    #**************************************************************************************
    def SelectNewMisc(self):
        newmisc = str(self.ui.miscComboBox.currentText()) + "DEF"
        miscplugin = str(self.ui.miscComboBox.currentText())
        self.ui.miscGroupBox.hide()
        self.ui.miscLayout.removeWidget(self.ui.miscGroupBox)
        for plugin in self.Misc:
            if plugin.name == miscplugin:
                self.ui.miscGroupBox = plugin
                break
        self.ui.miscLayout.addWidget(self.ui.miscGroupBox)
        self.ui.miscLayout.update()
        self.ui.miscGroupBox.show()
                
    #**************************************************************************************
    def AdjustSliderScale(self):
        #wedisconnected = False
        #try:
        #    self.ui.minSlider.valueChanged.disconnect()
        #    self.ui.maxSlider.valueChanged.disconnect()
        #    wedisconnected = True
        #except:
        #        True
        self.ui.minSlider.setMaximum(self.datasrc.nchan)
        self.ui.maxSlider.setMaximum(self.datasrc.nchan)
        #if (wedisconnected):
        #    self.ui.minSlider.valueChanged.connect(self.MinChanged)
        #    self.ui.maxSlider.valueChanged.connect(self.MaxChanged)
            
        True
         
    
    
    #**************************************************************************************
    def MinChanged(self,minrng):        #Peak range minimum
        rngtbl=self.ui.fitGroupBox.ui.range_tbl
        rangenum = np.floor_divide(rngtbl.currentColumn(),2)
        if rangenum == -1:
            self.ui.fitGroupBox.AddRange()
            rangenum = 0
        valcol = (rangenum)*2
        self.ui.minvalLabel.setText(str(minrng))
        try: #old way
            if (self.ui.fitGroupBox.rangeList[rangenum].start==minrng): return
            self.ui.fitGroupBox.rangeList[rangenum].start = minrng
        except: #new way
            if (self.ui.fitGroupBox.rangeList[rangenum].rangeparams["Range_start"].value==minrng): return
            self.ui.fitGroupBox.rangeList[rangenum].rangeparams["Range_start"].value = minrng
        rngtbl.item(0, valcol).setText(str(minrng))
        True
    
    #**************************************************************************************
    def MaxChanged(self,maxrng):    #Peak range maximum
        rngtbl=self.ui.fitGroupBox.ui.range_tbl
        rangenum = np.floor_divide(rngtbl.currentColumn(),2)
        if rangenum == -1:
            self.ui.fitGroupBox.AddRange()
            rangenum = 0
        valcol = (rangenum)*2
        self.ui.maxvalLabel.setText(str(maxrng))
        try:
            if (self.ui.fitGroupBox.rangeList[rangenum].stop==maxrng): return
            self.ui.fitGroupBox.rangeList[rangenum].stop = maxrng
        except:
            if (self.ui.fitGroupBox.rangeList[rangenum].rangeparams["Range_end"].value==maxrng): return
            self.ui.fitGroupBox.rangeList[rangenum].rangeparams["Range_end"].value = maxrng
        rngtbl.item(1, valcol).setText(str(maxrng))
        True
    
    #**************************************************************************************
    def UpdateMask(self):
        
        if self.ui.postprocessGroupBox.isChecked():
            return
        
        if self.ui.maskLower_slider.maximum() == self.datasrc.nchan and self.ui.maskUpper_slider.maximum() == self.datasrc.nchan: return     #Dimensions did not change
        
        wedisconnected = False
        try:
            self.ui.maskLower_edit.textChanged.disconnect()     #otherwise this function might be called recursively
            self.ui.maskUpper_edit.textChanged.disconnect()
            self.ui.maskLower_slider.valueChanged.disconnect()
            self.ui.maskUpper_slider.valueChanged.disconnect()
            wedisconnected = True
        except:
            True
            
        masklow = self.ui.maskLower_slider.value()
        oldmax = self.ui.maskLower_slider.maximum()
        newmax = self.datasrc.nchan
        newmasklow = int(masklow*newmax/oldmax)
        self.ui.maskLower_slider.setMaximum(newmax)
        self.ui.maskLower_edit.setText("%s" %newmasklow)
        self.ui.maskLower_slider.setValue(newmasklow)
        self.datasrc.lowerchan=newmasklow
        
        maskup = self.ui.maskUpper_slider.value()
        diff = self.ui.maskUpper_slider.maximum() - maskup
        self.ui.maskUpper_slider.setMaximum(newmax)
        newmaskup = newmax - int(diff*newmax/oldmax)
        self.ui.maskUpper_edit.setText(str(newmaskup))
        self.ui.maskUpper_slider.setValue(newmaskup)
        self.datasrc.upperchan=newmaskup
        
        self.datasrc
        
        if (wedisconnected):                                    #Reconnect the signal
            self.ui.maskLower_edit.textChanged.connect(self.MaskEditChanged)
            self.ui.maskUpper_edit.textChanged.connect(self.MaskEditChanged)
            self.ui.maskLower_slider.valueChanged.connect(self.MaskChanged)
            self.ui.maskUpper_slider.valueChanged.connect(self.MaskChanged)
        
    #**************************************************************************************
    def MaskEditChanged(self):
        lower = int(self.ui.maskLower_edit.text())
        upper = int(self.ui.maskUpper_edit.text())
        self.ui.maskLower_slider.setValue(lower)
        self.ui.maskUpper_slider.setValue(upper)
        
    #**************************************************************************************
    def MaskChanged(self, display=True):
        lower = self.ui.maskLower_slider.value()
        upper = self.ui.maskUpper_slider.value()
        if (self.datasrc.lowerchan==lower) and (self.datasrc.upperchan==upper): 
            if display == False:
                return
        else:
            self.ui.sourceGroupBox.PostprocessDirty(lower,upper)
        
        if self.ui.postprocessGroupBox.isChecked():
            return
            
        if len(self.datasrc.x)==1: return
        
        maxx = self.datasrc.x_max
        minx = self.datasrc.x_min
        self.xlowmask.set_xy([[minx,0],[self.datasrc.x[lower],0],[self.datasrc.x[lower],1],[minx,1]])
        self.xupmask.set_xy([[self.datasrc.x[upper-1],0],[maxx,0],[maxx,1],[self.datasrc.x[upper-1],1]])
        
        wedisconnected = False
        try:
            self.ui.maskLower_edit.textChanged.disconnect()     #otherwise this function might be called recursively
            self.ui.maskUpper_edit.textChanged.disconnect()
            wedisconnected = True
        except:
            True
        self.ui.maskLower_edit.setText(str(lower))
        self.ui.maskUpper_edit.setText(str(upper))
        if (wedisconnected):                                    #Reconnect the signal
            self.ui.maskLower_edit.textChanged.connect(self.MaskEditChanged)
            self.ui.maskUpper_edit.textChanged.connect(self.MaskEditChanged)   

        self.datasrc.lowerchan=lower
        self.datasrc.upperchan=upper
        #nr =self.datasrc.currset
        #rangelist = self.ui.fitGroupBox.rangeList
        
        #for irng in range(len(rangelist)):
        #    if rangelist[irng].start< lower : self.ui.fitGroupBox.NewTableValue(irng, "range_start", str(lower))
        #    if rangelist[irng].stop< lower : self.ui.fitGroupBox.NewTableValue(irng, "range_end", str(lower))
        #    if rangelist[irng].start> upper : self.ui.fitGroupBox.NewTableValue(irng, "range_start", str(upper))
        #    if rangelist[irng].stop> upper : self.ui.fitGroupBox.NewTableValue(irng, "range_end", str(upper))
        
        #self.circle.center = (90,0)
        #self.circle.width= (90-self.datasrc.dataset[nr].x_2th[lower])*2
        #self.circle.height= self.circle.width*2
        #ax = self.imcorr2d.get_axes()
        #ax.get_figure().canvas.draw()
        
        self.ui.graph.draw()
        
    #**************************************************************************************
    def PostPrecChanged(self,row,col):
        if col != 2: return
        prmtbl = self.ui.prm_table
        item = str(prmtbl.item(row, 0).text())
        try:
            val = prmtbl.item(row, col).text()
        except:
            val = ""
        if val == "": #and self.datasrc.precparams.has_key(item): 
            for afile in self.ui.sourceGroupBox.filelist:
                #if afile.src.precparams.has_key(item): afile.src.precparams.pop(item)
                #if afile.srcsplit.precparams.has_key(item): afile.srcsplit.precparams.pop(item)
                #if afile.srcp.precparams.has_key(item): afile.srcp.precparams.pop(item)
                if item in afile.src.precparams.keys(): afile.src.precparams.pop(item)
                if item in afile.srcsplit.precparams.keys(): afile.srcsplit.precparams.pop(item)
                if item in afile.srcp.precparams.keys(): afile.srcp.precparams.pop(item)
        else:
            try:
                for afile in self.ui.sourceGroupBox.filelist:
                    afile.src.precparams[item] = float(val)
                    afile.srcsplit.precparams[item] = float(val)
                    afile.srcp.precparams[item] = float(val)
                    
                #self.ui.sourceGroupBox.srcp.precparams[item] = float(val)
                #self.ui.sourceGroupBox.src.precparams[item] = float(val)
                #self.ui.sourceGroupBox.srcsplit.precparams[item] = float(val)
            except:
                True
    
    #**************************************************************************************
    def ExportSelectionChanged(self, item):
        if item.column() != 0: return
        name = str(item.text())
        #if (item.checkState() == 0) and (name in self.datasrc.exportparams):
        #    self.datasrc.exportparams.remove(name)
        if (item.checkState() == 0) and (name in self.exportparams):
            self.exportparams.remove(name)
             
        #elif (item.checkState() !=0) and (name not in self.datasrc.exportparams):
        #    self.datasrc.exportparams.append(name)
        elif (item.checkState() !=0) and (name not in self.exportparams):
            self.exportparams.append(name)

            
        
    #**************************************************************************************
    def UpdatePrmTable(self,setnr):
        prmtbl = self.ui.prm_table
        prmtbllist = []
        for prmi in range(prmtbl.rowCount()):
            prmtbllist.append(str(prmtbl.item(prmi,0).text()))
        #prmtbllist.sort()        #should already be sorted
        self.ui.cursource_label.setText(self.datasrc.origin)
        self.ui.filename_edit.setText(self.datasrc.filename)
        
        paramskeys=[x for x in self.datasrc.prm.keys()]
        paramskeys.sort()
        if prmtbllist == paramskeys:        #The parameters in the dataset are the same as in the current table, so only update the values, not the whole table
            params = [x for x in self.datasrc.prm.items()]
            params.sort()
            for i in range(len(params)):
                prmtbl.item(i, 1).setText(str(params[i][1]))
            return
        
        prmtbl.setRowCount(len(self.datasrc.prm))
        #params = self.datasrc.prm.items()
        #params.sort()
        params = sorted(self.datasrc.prm.items())
        
        
        
        oldnorm = self.ui.normalise_combo.currentText()
        self.ui.normalise_combo.clear()
        self.ui.normalise_combo.addItem("")
        self.ui.normalise_combo.addItem("Maximum_n")
        oldsum = self.ui.sum_combo.currentText()
        self.ui.sum_combo.clear()
        self.ui.sum_combo.addItem("")
        
        wedisconnected = False
        try:
            prmtbl.cellChanged.disconnect()     #otherwise this function might be called recursively
            wedisconnected = True
        except:
            True
         
        for i in range(len(params)):
            item = str(params[i][0])
            nameitem = qt.QTableWidgetItem()
            nameitem.setFlags((nameitem.flags() | qtCore.Qt.ItemIsUserCheckable) & ~qtCore.Qt.ItemIsEditable)
            nameitem.setTextAlignment(qtCore.Qt.AlignLeft)
            nameitem.setText(item)
            #if item in self.datasrc.exportparams:
            if item in self.exportparams:
                nameitem.setCheckState(qtCore.Qt.Checked)
            else:
                nameitem.setCheckState(qtCore.Qt.Unchecked)
            prmtbl.setItem(i,0,nameitem)
        
            valitem = qt.QTableWidgetItem()
            valitem.setTextAlignment(qtCore.Qt.AlignRight)
            valitem.setFlags(nameitem.flags() & ~qtCore.Qt.ItemIsEditable)
            valitem.setText(params[i][1])
            prmtbl.setItem(i,1,valitem)
            
            precitem = qt.QTableWidgetItem()
            precitem.setFlags(precitem.flags() | qtCore.Qt.ItemIsEditable)
            precitem.setTextAlignment(qtCore.Qt.AlignRight)
            if item in self.datasrc.precparams.keys():
                precitem.setText(str(self.datasrc.precparams[item]))
            else:
                precitem.setText("")
            prmtbl.setItem(i,2,precitem)
            
            self.ui.normalise_combo.addItem(item)
            self.ui.sum_combo.addItem(item)
            True
        
        if(wedisconnected): prmtbl.cellChanged.connect(self.PostPrecChanged)   #Reconnect the signal
        
        if self.ui.normalise_combo.findText(oldnorm) : self.ui.normalise_combo.setCurrentIndex(self.ui.normalise_combo.findText(oldnorm))
        if self.ui.sum_combo.findText(oldsum) : self.ui.sum_combo.setCurrentIndex(self.ui.sum_combo.findText(oldsum))
        
        for plugin in self.Output:
            if plugin.name == "Figures":
                plugin.PopulateParamCombos()
                break
        
        self.manipulategui.PopulateParamCombos()
        if self.ui.absorption_check.isChecked()==True:
            self.absorptiongui.PopulateParamCombos()
        True
        
        
    #**************************************************************************************
    def UpdateDetInfo(self,setnr):
        prm = self.datasrc.detprm
        #self.ui.detDim_xmin_edit.setText(str(prm["det_xmin"]))
        #self.ui.detDim_xmax_edit.setText(str(prm["det_xmax"]))
        #self.ui.sam2det_edit.setText(str(prm["sam_to_det"]))
        #self.ui.stth_edit.setText("{0:.2f}".format(prm["stth"]))
        #self.ui.wavelength_edit.setText(str(prm["lambda"]))
        
        self.ui.detDim_xmin_edit.setText("%s" %prm["det_xmin"])
        self.ui.detDim_xmax_edit.setText("%s" %prm["det_xmax"])
        self.ui.sam2det_edit.setText("%s" %prm["sam_to_det"])
        self.ui.stth_edit.setText("%0.2f" %prm["stth"])
        self.ui.wavelength_edit.setText("%s" %prm["lambda"])
        
        
                                         
    def ClearData(self):
        self.datasrc.Clear()
        self.ui.sourceGroupBox.src.Clear()
        self.ui.sourceGroupBox.srcp.Clear()
        self.ui.sourceGroupBox.srcsplit.Clear()
        self.datasrc.AddData(np.array([0.0]))
        self.datasrc.CalcAllAxis()
        self.Generate()
        
    
    #**************************************************************************************
    def SelectData(self,setnr, display=True):
        if setnr == 0:
            #Turn off the upper and lower sliders here
            True
        
        lenold = self.ui.minSlider.maximum()    
        self.datasrc.SelectDataSet(setnr, self.axistype)
        lennew = self.datasrc.nchan    
        #self.ApplyAdditionalParams()
        
        #if lenold != lennew:
        self.AdjustSliderScale()
        #self.lineseries[0].set_xdata(self.datasrc.x)
        #self.lineseries[0].set_ydata(self.datasrc.y)
        self.UpdatePrmTable(setnr)
        self.UpdateDetInfo(setnr)
        self.UpdateMask()
        self.MaskChanged(display)
        self.ui.fitGroupBox.UpdateRangeData()
        self.ui.fitGroupBox.FitRange()
        if display == True:
            self.UpdateGraph()
            self.ui.graph.draw()
            self.ui.diffgraph.draw()
        if self.ui.absorption_check.isChecked():
            self.attenuationgui.RefreshSet()
        
    
    #**************************************************************************************
    def NewXType(self):
        if self.ui.channel_radio.isChecked(): self.axistype = 'Channel'; self.modext = "-ch"
        elif self.ui.position_radio.isChecked(): self.axistype = 'Position'; self.modext = "-pos"
        elif self.ui.angle_radio.isChecked(): self.axistype = 'Angle'; self.modext = "-ang"
        elif self.ui.dspacing_radio.isChecked(): self.axistype = 'd-spacing'; self.modext = "-d"
        self.signal["xtypechanged"].emit(self.axistype)
        
        corrext = ""
        if self.ui.flatfield_check.isChecked(): corrext = corrext + "f"           
        if self.ui.geometry_check.isChecked(): corrext = corrext + "g"
        if corrext !="": self.modext = self.modext + "_" + corrext
        
        postpext = ""
        if self.ui.postprocessGroupBox.isChecked():
            postpext = postpext + "_PP"
            if self.ui.normalise_combo.currentText() !="": postpext = postpext + "_Norm(" + self.ui.normalise_combo.currentText() + ")"
            if self.ui.sum_combo.currentText() !="": postpext = postpext + "_Sum(" + self.ui.sum_combo.currentText() + ")"
            if self.ui.scale_edit.text() != "1": postpext = postpext + "_Scale(" + self.ui.scale_edit.text() + ")"
            #if self.datasrc.lowerchan != 0 or (self.datasrc.upperchan != self.datasrc.nchan and self.datasrc.upperchan != -1):
            #    postpext = postpext + "_Mask-" + str(self.datasrc.lowerchan) + "-" + str(self.datasrc.upperchan)
            if self.ui.stthoffset_edit.text() != "0" and self.ui.stthoffset_edit.text() !="": postpext = postpext + "_Stthoffset(" + self.ui.stthoffset_edit.text() + ")"
            if self.ui.justsum_check.isChecked(): postpext = postpext + "_NoAvgOverlap"
            if (self.ui.maskLower_slider.minimum() != int(self.ui.maskLower_edit.text())) or (self.ui.maskUpper_slider.maximum() != int(self.ui.maskUpper_edit.text())):
                postpext = postpext + "_Mask(" + self.ui.maskLower_edit.text() + "_" + self.ui.maskUpper_edit.text() + ")"
            if postpext !="": self.modext = self.modext+postpext    
        
        True
        
        
    #**************************************************************************************
    def XTypeChanged(self):
        self.NewXType()
        self.SelectData(self.datasrc.currset)

    
    #**************************************************************************************
    def UpdateGraph(self):
        self.lineseries[0].set_data(self.datasrc.x, self.datasrc.y)
        
        plot1d =self.ui.graph.figure.axes[0]
        
        try:#if len(self.datasrc.y == self.datasrc.y_err):
            x=self.datasrc.x; y=self.datasrc.y; y_err=self.datasrc.y_err
            y_err_min = y-y_err; y_err_max = y+y_err
            segments =[[(x[i],y_err_min[i]),(x[i],y_err_max[i])] for i in range(len(x))]
            self.error_collection[0].set_segments(segments)
            self.error_collection[0].set_visible(True)
            ymin = y_err_min.min(); ymax = y_err_max.max()
            True
        except: #no stdev data
            self.error_collection[0].set_visible(False)
            ymin = self.datasrc.y_min; ymax= self.datasrc.y_max
        
        
        ybuf = abs(ymax - ymin) * 0.1
        if ybuf == 0: ybuf = 1.0
        xminlim = self.datasrc.x_min; xmaxlim = self.datasrc.x_max
        if xminlim == xmaxlim:
            xminlim = xminlim -1; xmaxlim = xmaxlim + 1;
        plot1d.set_xlim(xminlim, xmaxlim)
        plot1d.set_ylim(ymin - ybuf, ymax + ybuf)
        plot1d.set_ylabel(self.datasrc.ylabel)
        plot1d.set_title(self.datasrc.ylabel + " vs. " + self.axistype)
        self.ui.graph.figure.tight_layout()
        
        self.ui.diffgraph.figure.axes[0].set_xlim(xminlim, xmaxlim)
        self.ui.diffgraph.figure.tight_layout()
        
        src_curr = self.datasrc.dataset[self.datasrc.currset].currframe
        self.Set2D(self.im2d, src_curr.hc_2th,src_curr.vc_2th,src_curr.n, src_curr.h_2th[0], src_curr.h_2th[-1], src_curr.v_2th[0], src_curr.v_2th[-1])
        
        #src_cor = self.datasrc.dataset[self.datasrc.currset].corframe
        #self.Set2D(self.imcorr2d, src_cor.hc_2th,src_cor.vc_2th,src_cor.n, src_cor.h_2th[0], src_cor.h_2th[-1], src_cor.v_2th[0], src_cor.v_2th[-1])
        #self.Set2D(self.imcorr2d, src.hc_cor_2th, src.vc_cor_2th, src.n_cor, src.h_cor_2th[0], src.h_cor_2th[-1], src.v_cor_2th[0], src.v_cor_2th[-1])
        
        
        
        
    #**************************************************************************************
    def DetSizeChanged(self):
        curset = self.datasrc.currset
        dtsrc = self.ui.sourceGroupBox.src
        for src in dtsrc.dataset:
        #for src in self.datasrc.dataset:
            src.detprm["det_xmin"] = float(self.ui.detDim_xmin_edit.text())
            src.detprm["det_xmax"] = float(self.ui.detDim_xmax_edit.text())
            for frm in src.frame:
                src.frame[frm].x_mm = np.array([0.0])
                src.frame[frm].x_2th = np.array([0.0])
                src.frame[frm].x_d = np.array([0.0])
                                    
        dtsrc.CalcAllAxis(frames=[])
        dtsrc.x_chan = dtsrc.dataset[-1].x_chan
        dtsrc.nchan = len(dtsrc.x_chan)
        dtsrc.CalcSumSetCommon()
        dtsrc.CalcSumSet(frames=[])
    
        dtsrc.preps["geom_cor"] = False      #If the flat field changed, the geometric correction will have to be redone
        dtsrc.preps['split'] = -1     #Also redo the splitting
            
        self.Generate(curset)
        True
        
    #**************************************************************************************
    def SampleToDetectorChanged(self):
        curset = self.datasrc.currset
        dtsrc = self.ui.sourceGroupBox.src
        
        for src in dtsrc.dataset:
            src.detprm["sam_to_det"] = float(self.ui.sam2det_edit.text())
            for frm in src.frame:
                src.frame[frm].x_2th = np.array([0.0])
                src.frame[frm].x_d = np.array([0.0])

        dtsrc.CalcAllAxis(frames=[])
        dtsrc.x_chan = dtsrc.dataset[-1].x_chan
        dtsrc.nchan = len(dtsrc.x_chan)
        dtsrc.CalcSumSetCommon()
        dtsrc.CalcSumSet(frames=[])
    
        dtsrc.preps["geom_cor"] = False      #If the flat field changed, the geometric correction will have to be redone
        dtsrc.crmap=[]
        dtsrc.preps['split'] = -1     #Also redo the splitting
            
        self.Generate(curset)
        True
        
    #**************************************************************************************
    def StthChanged(self):
        src = self.ui.sourceGroupBox.src.dataset[self.datasrc.currset]
        src.detprm["stth"] = float(self.ui.stth_edit.text())
        src.currframe.x_2th = np.array([0.0])
        src.currframe.x_d = np.array([0.0])
        #self.ui.sourceGroupBox.src.dataset.pop(0)
        self.ui.sourceGroupBox.src.CalcAllAxis()
        self.ui.sourceGroupBox.src.CalcSumSetCommon()
        self.ui.sourceGroupBox.src.CalcSumSet()
        
        if self.datasrc == self.ui.sourceGroupBox.srcp:
            self.PostProcess()
        self.SelectData(self.datasrc.currset)
        True
        
    #**************************************************************************************
    def DSpacingChanged(self):
        for src in self.ui.sourceGroupBox.src.dataset:
            src.detprm["lambda"] = float(self.ui.wavelength_edit.text())
            src.currframe.x_d = np.array([0.0])
        #self.ui.sourceGroupBox.src.dataset.pop(0)
        self.ui.sourceGroupBox.src.CalcAllAxis()
        self.ui.sourceGroupBox.src.CalcSumSetCommon()
        self.ui.sourceGroupBox.src.CalcSumSet()
        
        if self.datasrc == self.ui.sourceGroupBox.srcp:
            self.PostProcess()
        self.SelectData(self.datasrc.currset)
        True


    #**************************************************************************************
    def PostProcessApply(self):
        self.ui.sourceGroupBox.PostprocessDirty()
        self.PostProcessChanged()
        
        
    
    #**************************************************************************************
    def PostProcessUpdateWidgets(self,state):
        self.xlowmask.set_visible(state)
        self.xupmask.set_visible(state)
        self.ui.maskLower_slider.setEnabled(state)
        self.ui.maskUpper_slider.setEnabled(state)
        self.ui.maskLower_edit.setEnabled(state)
        self.ui.maskUpper_edit.setEnabled(state)
        self.ui.maskLower_label.setEnabled(state)
        self.ui.maskUpper_label.setEnabled(state)
        self.ui.graph_2d.setEnabled(state)
        # self.ui.graphcorr_2d.setEnabled(state)
        self.ui.geometry_check.setEnabled(state)
        self.ui.flatfield_check.setEnabled(state)
        self.ui.detectorsplit_label.setEnabled(state)
        self.ui.vsplit_combo.setEnabled(state)
        
        
    #**************************************************************************************
    def PostProcessChanged(self):
        currset = self.datasrc.currset
        if self.ui.postprocessGroupBox.isChecked():
            self.PostProcessUpdateWidgets(False)
            if self.ui.sourceGroupBox.srcp.preps["postdirty"] == True:
                self.PostProcess()
            self.ui.sourceGroupBox.srcp.precparams = self.ui.sourceGroupBox.srcsplit.precparams
            #self.ui.sourceGroupBox.srcp.precparams = self.ui.sourceGroupBox.src.precparams
            #self.ui.sourceGroupBox.srcp.exportparams = self.ui.sourceGroupBox.src.exportparams
            if (len(self.ui.sourceGroupBox.srcp.x)>1):
                self.datasrc = self.ui.sourceGroupBox.srcp
            self.Generate(selectnr = currset)
        else:
            self.PostProcessUpdateWidgets(True)
            self.ui.sourceGroupBox.srcsplit.precparams = self.ui.sourceGroupBox.srcp.precparams
            #self.ui.sourceGroupBox.src.precparams = self.ui.sourceGroupBox.srcp.precparams
            #self.ui.sourceGroupBox.src.exportparams = self.ui.sourceGroupBox.srcp.exportparams
            
            #if self.ui.sourceGroupBox.src.data2D == False:
            #    self.datasrc = self.ui.sourceGroupBox.src
            #else:
            self.datasrc = self.ui.sourceGroupBox.srcsplit
            

            if currset > len(self.datasrc.dataset): currset = -1 
            self.Generate(selectnr = currset)
            
        
        
        

    #**************************************************************************************
    def PostProcess(self):
        nums = 8    #Number of different post process events

        if self.ui.sourceGroupBox.src.data2D == False:
            srcp = self.ui.sourceGroupBox.src.PreparePost()
        else:
            srcp = self.ui.sourceGroupBox.srcsplit.PreparePost()
        currset = srcp.currset
        if len(srcp.dataset[currset].y) ==1: return

        progress = ProgressBar("Post Processing...", nums)
        progress.setinfo("Prepare post processing datastructures")        
        progress.step()

        progress.setinfo("Ofsetting stth")
        srcp = srcp.StthOffset(self.ui.stthoffset_edit.text())
        #srcp.CalcSumSet(["raw"])
        #srcp.SelectFrame("raw")
        progress.step()
        
        progress.setinfo("Performing crop")
        srcp.SelectFrame("raw")
        srcp = srcp.Crop()
        srcp.CalcSumSet(["raw"])
        srcp.SelectFrame("raw")
        progress.step()
        

        
        progress.setinfo("Normalising data")    
        srcp.Normalise(self.ui.normalise_combo.currentText())
        progress.step()
        
        progress.setinfo("Summing by parameter")
        srcp = srcp.SumWith(self.ui.sum_combo.currentText())
        progress.step()
        
        progress.setinfo("Combining two theta sets")
        srcp.preps["just_sum"] = True if self.ui.justsum_check.isChecked() else False 
        srcp = srcp.Combine2thSets()
        srcp.CalcSumSetCommon()
        srcp.CalcSumSet()
        srcp.SelectFrame("raw")
        progress.step()
        
        progress.setinfo("Scaling data")
        srcp.Scale(float(self.ui.scale_edit.text()))
        progress.step()
        
        
        
        progress.setinfo("Wrapping up")
        srcp.preps['postdirty'] = False
        self.ui.sourceGroupBox.srcp = srcp
        self.datasrc = srcp
        if currset > len(self.datasrc.dataset): currset = -1
        for findex in range(len(self.ui.sourceGroupBox.filelist)):
            if self.ui.sourceGroupBox.filelist[findex].location == self.datasrc.dataset[-1].filename:
                fileinfo = self.ui.sourceGroupBox.filelist[findex]
                fileinfo.srcp = srcp
                self.ui.sourceGroupBox.filelist[findex] = fileinfo
                break
        self.ApplyAdditionalParams()    
        progress.step()
        
        True   

    #**************************************************************************************
    def FlatFieldChanged(self):
        self.ui.sourceGroupBox.postdirty = True #Redo the postprocessing
        self.Generate(selectnr = self.datasrc.currset, pretype = "flatfield")
                     
    #**************************************************************************************
    def GeomCorrChanged(self):
        self.ui.sourceGroupBox.postdirty = True
        self.Generate(selectnr = self.datasrc.currset, pretype = "geom")
        
    #**************************************************************************************
    def PreProcess(self, pretype):
        
        currset = self.datasrc.currset
        self.datasrc = self.ui.sourceGroupBox.src
        if pretype == "flatfield":
            self.datasrc.preps["geom_cor"] = False      #If the flat field changed, the geometric correction will have to be redone
            self.ui.sourceGroupBox.srcsplit.preps['split'] = -1     #Also redo the splitting
            
            
        #flat field
        if self.ui.flatfield_check.isChecked():
            fffname = str(self.ui.fffname_edit.text())
            if (self.flatfieldsrc.dataset[-1].filename != fffname):
                from Source import NeXus_hdf
                self.flatfieldsrc = NeXus_hdf.NeXus_hdf_read(fffname, self.config["source"])
            self.ui.sourceGroupBox.src.CalcFlatFieldCorrection(self.flatfieldsrc.dataset)
            
        else:
            self.datasrc.SelectFrame("raw")
         
        nrsplits = float(self.ui.vsplit_combo.currentText())
        if self.ui.sourceGroupBox.srcsplit.preps['split'] == nrsplits:
            self.datasrc = self.ui.sourceGroupBox.srcsplit
        else:
            splitted = self.ui.sourceGroupBox.src.SplitDetector(nrsplits)
            self.ui.sourceGroupBox.srcsplit = splitted
            self.datasrc = self.ui.sourceGroupBox.srcsplit
            #self.ui.sourceGroupBox.postdirty = True #Redo the postprocessing
        
        #splitted = self.ui.sourceGroupBox.src.SplitDetector(nrsplits)
        #if splitted != False:
        #    self.ui.sourceGroupBox.srcsplit = splitted
        #self.datasrc = self.ui.sourceGroupBox.srcsplit
        if self.ui.flatfield_check.isChecked():
            self.datasrc.SelectFrame("ff_cor")
        else:
            self.datasrc.SelectFrame("raw")
        
        #geometry correction
        if self.ui.geometry_check.isChecked():
            self.datasrc.CalcGeomCorrection(self.config["geom_cor"])
        True
        
        
        for findex in range(len(self.ui.sourceGroupBox.filelist)):
            if self.ui.sourceGroupBox.filelist[findex].location == self.datasrc.dataset[-1].filename:
                fileinfo = self.ui.sourceGroupBox.filelist[findex]
                fileinfo.srcsplit = self.datasrc
                self.ui.sourceGroupBox.filelist[findex] = fileinfo
                break
                
        #self.SelectData(currset)
        #self.Generate(currset)
    
    
    #**************************************************************************************
    def ApplyAdditionalParams(self):
        #if self.datasrc.data2D == True:
        if self.ui.sourceGroupBox.src.data2D == True:
            for src in self.datasrc.dataset:
            #for src in self.ui.sourceGroupBox.src.dataset + self.ui.sourceGroupBox.srcp.dataset + self.ui.sourceGroupBox.srcsplit.dataset:
                if self.ui.geometry_check.isChecked():
                    src.prm["Geom_corr"]="True"
                else:
                    src.prm["Geom_corr"]="False"
                
                if self.ui.flatfield_check.isChecked():
                    src.prm["Flat_field"]=self.flatfieldsrc.filename
                else:
                    src.prm["Flat_field"]="False"
                    
                nrsplit = self.ui.vsplit_combo.currentText()
                if nrsplit == "1":
                    if "Split" in self.datasrc.prm.keys():
                        src.prm.pop("Split")
                else:
                    src.prm["Split"]=nrsplit
            
            
    
        True    
    
    #**************************************************************************************
    def Generate(self, selectnr = -1, pretype = ""):
        #self.ui.sourceGroupBox.GetData()
        nrsets = len(self.datasrc.dataset)
        if selectnr == -1:
            selectnr = nrsets-1
        if nrsets != 0:
            #if self.ui.geometry_check.isChecked():
            #    self.datasrc.CalcGeomCorrection(self.config["geom_cor"])
            if self.datasrc.data2D == True:
                self.PreProcess(pretype)
                

            
            if self.ui.postprocessGroupBox.isChecked():
                if(self.ui.sourceGroupBox.srcp.preps['postdirty']) == True:
                    self.PostProcess()
                   
                else:
                    self.datasrc = self.ui.sourceGroupBox.srcp

            nrsets = len(self.datasrc.dataset)
            if selectnr > len(self.datasrc.dataset):
                selectnr = len(self.datasrc.dataset)-1
            
            self.ApplyAdditionalParams()
            self.SelectData(selectnr)
            self.NewXType()
            self.ui.nrdatasets_label.setText(str(nrsets-1))
            self.ui.dataset_spin.setMaximum(nrsets-1)
            
            self.ui.dataset_spin.valueChanged.disconnect()
            self.ui.dataset_spin.setValue(selectnr)
            self.ui.dataset_spin.valueChanged.connect(self.SelectData)
            
            self.AdjustSliderScale()
        else:
            self.ui.nrdatasets_label.setText("0")
            self.ui.dataset_spin.setMaximum(0)
            self.ui.dataset_spin.setValue(0)
        
        
    #**************************************************************************************
    def FitRange(self):
        try:
            self.ui.fitGroupBox.ui.range_tbl.cellChanged.disconnect()
        except:
            True
        self.ui.fitGroupBox.FitRange()
        self.ui.graph.draw()
        self.ui.diffgraph.draw()
        self.ui.fitGroupBox.ui.range_tbl.cellChanged.connect(self.ui.fitGroupBox.CellValueChanged)   #Reconnect the signal

    #**************************************************************************************
    def About(self):
        QMessageBox.about(self, "About...",  "Scan manipulator Version 2.0.0\nCreated by Deon Marais\nNecsa SOC Limited\ndeon.marais@necsa.co.za")
        
    #**************************************************************************************
    def Set2D(self,im,x,y,z,xmin,xmax,ymin,ymax):
        if len(x) == 1: 
            im.set_data([-1,1],[-1,1],[[1,0],[0,1]])
        else: 
            im.set_data(x,y,z)
        #DM: depricated: ax = im.get_axes()
        ax=im.axes  
        if xmin == xmax:
            xmin = xmin -1.0; xmax=xmax+1.0
        if ymin == ymax:
            ymin = ymin -1.0; ymax=ymax+1.0
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        im.autoscale()
        ax.get_figure().canvas.draw() 
        
        pass
    
    
    #**************************************************************************************
    def ManparamPressed(self):
        self.manipulategui.show()
        #self.update()
        True

    #**************************************************************************************
    def AbscorconfigurePressed(self):
        self.attenuationgui.show()
    #self.update()
        True
    
    #**************************************************************************************
    def Attcor3DconfigurePressed(self):
        self.attenuation3Dgui.show()
    #self.update()
        True
    
    #**************************************************************************************
    def SelectAllChanged(self):
        checkstate = self.ui.selectall_check.checkState()
        nrprms = self.ui.prm_table.rowCount()
        for i in range(nrprms):
            item = self.ui.prm_table.item(i,0)
            item.setCheckState(checkstate)
            self.ExportSelectionChanged(item)
        if checkstate == qtCore.Qt.Unchecked:   #Just make sure everything is removed from the exporting parameter list
            self.exportparams = []
            
    #**************************************************************************************
    def Test(self):
        plot =self.ui.graph.figure.axes[0]
        oldlines = plot.get_lines()
        plot.set_autoscalex_on(False)
        if 1:
            #self.erbar = plot.errorbar(self.datasrc.x, self.datasrc.y, yerr=self.datasrc.y_err)
            self.erbar =mpl.pyplot.errorbar(self.datasrc.x, self.datasrc.y, yerr=self.datasrc.y_err)
        if 0:
            children = self.erbar.get_children()
            children[0].remove()
            children[1].remove()
            children[2].remove()
            children[3].remove()
        #plot.add_line(self.lineseries[0])    
        #plot.add_line(children[1])
        #plot.add_line(children[2])
        #plot.add_collection(children[3])
        #plot.add_line(children[3])
        #plot.set_autoscalex_on(False)
        #plot.set_xbound(self.datasrc.x.min(), self.datasrc.x.max())
        self.ui.graph.draw()
        True

        
    