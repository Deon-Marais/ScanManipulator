'''
Created on 08 May 2014

@author: Deon
'''
from PyQt4.QtGui import QGroupBox as QGroupBox
#from GenPeaksGUI import Ui_GenPeaks
from PyQt4.QtGui import QFileDialog
from Output.FiguresGUI import Ui_Figures
import PyQt4.QtGui as qt
import numpy as np
import sys
from mylib import ProgressBar
from mylib import Graph
import os.path
import pickle



#import Srcpar
#from ScanmanDEF import ScanmanDEF
from matplotlib.lines import Line2D
from time import sleep

class Aplot():
    def __init__(self, prm1_name, prm2_name):
        self.prm1_name = prm1_name
        self.prm2_name = prm2_name if prm2_name != "" else "Run_number"
        self.colour = "black"
        self.x = []
        self.y = []
        #self.line = Line2D([], [], color='black', linewidth = 1)
        
        
        
    def addplot(self, axis):
        self.axis = axis
        self.line = Line2D([], [], color=self.colour, linewidth = 1)
        self.axis.add_line(self.line)
        
        #axis.set_title(self.prm1_name + " vs. " + self.prm2_name)
        axis.set_ylabel(self.prm1_name)
        axis.set_xlabel(self.prm2_name)  
        True
        
    def setdata(self, x, y):
        self.x=x
        self.y=y
        self.line.set_data(self.x,self.y)
        self.x_min=min(self.x)
        self.x_max=max(self.x)
        self.y_min=min(self.y)
        self.y_max=max(self.y)
        ybuf = abs(self.y_max - self.y_min) * 0.1
        self.axis.set_xlim(self.x_min, self.x_max)
        self.axis.set_xlim(self.x_min, self.x_max)
        self.axis.set_ylim(self.y_min - ybuf, self.y_max + ybuf)
        #self.axis.set_ylabel(self.datasrc.ylabel)
        #self.axis.set_title(self.datasrc.ylabel + " vs. " + self.axistype)
        


#****************************************************************************************************************************************************************************
#****************************************************************************************************************************************************************************
class FiguresDEF(QGroupBox):
    def __init__(self, ScanmanMain=""):
        QGroupBox.__init__(self)
        self.name = "Figures"
        self.ui = Ui_Figures()
        self.ui.setupUi(self)
        self.scanman = ScanmanMain
        self.setstart = 0
        self.setend = -1
        
        self.ui.graph_scan.figure.delaxes(self.ui.graph_scan.figure.axes[0])
        self.graphlist = []
        self.maxid=-1
        self.graphset={"scan":[],"fit":[]}
        self.loaded = False
        
        self.xlabel = "x"
        self.ylabel = "y"
        self.zlabel = "z"
        #
        #self.ui.widget = self.mywi
        #self.ui.waterfall_container_layout.addWidget(mywi)
        
        
        self.scanparamgraph = Graph(self.ui.graph_scan)
        
        self.filedialog = QFileDialog()
        self.filedialog.setFileMode(QFileDialog.ExistingFiles)
        self.filedialog.setViewMode(QFileDialog.Detail)
        self.curfilter = ""
        
        
        #self.scanparamgraph.graph.tight_layout()
        
    
    #**************************************************************************************
    def LoadMayavi(self):
        if self.loaded == False:
            progress = ProgressBar("Loading Mayavi Library...", 3)
            
            import MayaviEmbed
            progress.step()
            self.ui.waterfall_layout.removeWidget(self.ui.widget)
            self.mayavicontainer = qt.QWidget()
            self.mayaviobj = MayaviEmbed.MayaviQWidget(self.mayavicontainer)
            progress.step()
            self.mayavicontainer.setLayout(self.mayaviobj.mylayout)
            self.ui.waterfall_layout.addWidget(self.mayavicontainer)
            self.mayavicontainer.show()
            progress.step()
            self.loaded =  True
        
        
    #**************************************************************************************
    def Clear(self):
        for axis in self.ui.graph_scan.figure.axes:         #delete the old axes
            self.ui.graph_scan.figure.delaxes(axis)
        
        #self.graphset[gtype] = []
        self.graphlist = []
        self.maxid=-1
        self.ui.graph_scan.draw()
        
    #**************************************************************************************
    def Clear3D(self):
        #self.scene.mayavi_scene.children = [] 
        self.mayaviobj.visualization.scene.mayavi_scene.children = [] 
        True
    #**************************************************************************************
    def ApplyFigure(self):
        #pixmap = qt.QPixmap.grabWidget(self.ui.graph_scan.figure.canvas)
        #qt.QApplication.clipboard().setPixmap(pixmap)
        
        
     
        True
        
    
    #**************************************************************************************
    def Refresh(self):
        True
    
    #**************************************************************************************
    def Test(self):
        True
    
    #**************************************************************************************
    def Read_mvi(self,fname):
        bin_file = open(fname,"rb")
        if sys.version_info.major > 2:
            #data = pickle.load(bin_file, fix_imports=True, encoding='bytes')
            data, bounds = pickle.load(bin_file, fix_imports=True, encoding='bytes')  #For some strange reason the 'bounds' does not get saved in the tree when performing a pickle serialisation. This is a hack to get around that
        else:
            data = pickle.load(bin_file, fix_imports=True, encoding='bytes')
        bin_file.close()
        for item in data:
            self.mayaviobj.visualization.scene.mayavi_scene.children.append(item)
            axis = self.mayaviobj.visualization.scene.mayavi_scene.children[-1].children[1].children[0].children[1]
            axis.axes.set(bounds=bounds)
        True
    
    #**************************************************************************************
    def Read_reggrid(self,fname):
        f = open(fname, 'r')
        filecontent = f.read()
        f.close()
        data = filecontent.split("\n")[:-1]
        griddata = []
        for i in range(len(data)):
            griddata+=[data[i].split("\t")]
            True
        xgrid = griddata[0][1:]
        zgrid = []
        ygrid = []
        for i in range(1,len(griddata)):
            zgrid+=[griddata[i][0]]
            #ygrid+=np.array([griddata[i][1:]])
            ygrid+=[griddata[i][1:]]
        xgrid = np.array(xgrid).astype(np.float)
        y = np.array(ygrid).astype(np.float)
        z = np.array(zgrid).astype(np.float)
        x=np.array([xgrid]*len(zgrid))
        
        
        y_err = np.zeros((len(y),len(y[0])))
        pts = [0,0]
        if self.ui.interp_check.isChecked():
            xpts = int(self.ui.xpts_edit.text())
            ypts = int(self.ui.ypts_edit.text())
            pts = [xpts,ypts]
        self.mayaviobj.setWaterfall(z,x,y,y_err,pts)  #Note the difference in x,y,z assignemnts
    
    
    #**************************************************************************************
    def Read_xyz(self,fname):
        f = open(fname, 'r')
        filecontent = f.read()
        f.close()
        lines = filecontent.split("\n")
        blockidx=[-1]
        for iline in range(len(lines)):
            if len(lines[iline].rstrip()) == 0:     #Determine where whitespace lines are, these will define new datasets
                blockidx =blockidx + [iline]
        datablocks=[]        
        for blocki in range(1,len(blockidx)):
            datablocks = datablocks + [lines[blockidx[blocki-1]+1:blockidx[blocki]]]
        
        progressgraph = ProgressBar("Creating xyz graphs", len(datablocks))          
        for data in datablocks:
            progressgraph.setinfo(fname)
            header = data[0].split()
            readerr=False
            if len(header)==4:readerr=True
            try:
                a=float(header[0])
                datastart = 0
                self.xlabel = "x"
                self.ylabel = "y"
                self.zlabel = "z"
            except:
                datastart = 1
                self.xlabel = header[0]
                self.ylabel = header[1]
                self.zlabel = header[2]
            x = y = z = z_err = []
            for dataln in data[datastart:]:
                if len(dataln.strip())!=0:
                    if readerr:
                        xval,yval,zval,errval = dataln.split()
                        z_err = z_err +  [[float(errval)]]
                    else:
                        xval,yval,zval = dataln.split()
                        z_err = z_err +  [[0.0]]
                        True
                    x = x + [float(xval)]
                    y = y + [[float(yval)]]
                    z = z + [[float(zval)]]

                True
            x = np.array(x)
            y = np.array(y)
            z = np.array(z)
            z_err = np.array(z_err)
            
            #z_err2 = np.zeros((len(z),len(z[0])))
            pts = [0,0]
            if self.ui.interp_check.isChecked():
                xpts = int(self.ui.xpts_edit.text())
                ypts = int(self.ui.ypts_edit.text())
                pts = [xpts,ypts]
            self.mayaviobj.setWaterfall(x,y,z,z_err,pts)  #Note the difference in x,y,z assignemnts
            self.mayaviobj.visualization.surfaxes.axes.x_label=self.xlabel
            self.mayaviobj.visualization.surfaxes.axes.y_label=self.ylabel
            self.mayaviobj.visualization.surfaxes.axes.z_label=self.zlabel
            
            progressgraph.step()               
            True #To be implemented
        
    #**************************************************************************************
    def SetMVIObjName(self,plotname):
        try:
            chil=self.mayaviobj.visualization.figure.children[-1]
            chil.name=plotname
        except:
            True
        #self.mayaviobj.visualization
        True    
    #**************************************************************************************
    def FileOpen(self):
        file_types = ";;Mayavi (*.mvi);;xyz (*.xyz);;reg_grid (*.txt);;All (*.*)"
        #self.filedialog.selectFilter(self.curfilter)
        fnames, filters = self.filedialog.getOpenFileNamesAndFilter(self, 'Open file', '', file_types, initialFilter=self.curfilter)
        if (fnames==[]): 
            #for i in range(10):
            #    self.mayaviobj.visualization.scene.camera.azimuth(10)
            #    self.mayaviobj.visualization.scene.render()
            #    self.mayaviobj.visualization.scene.mlab.draw()
            #    sleep(0.5)
                
            # yield
             
            return
        self.filedialog.setDirectory(os.path.dirname(str(fnames[0])))
        self.curfilter = filters
        self.LoadMayavi()
        
        progressfiles = ProgressBar("Generating 3D Graphs from files", len(fnames))
        for fname in fnames:
            progressfiles.setinfo(fname)
            filetype = os.path.splitext(fname)[1][1:]
            if filetype == "mvi":
                self.Read_mvi(fname)
            elif filetype =="txt":
                self.Read_reggrid(fname)
                self.SetMVIObjName(fname)
            elif filetype =="xyz":
                
                self.Read_xyz(fname)
                self.SetMVIObjName(fname)
            if progressfiles.wasCanceled(): break
            progressfiles.step()
        True
    
    #**************************************************************************************
    
            
    def FileSave(self):
        data = self.mayaviobj.visualization.scene.mayavi_scene.children
        fname = self.filedialog.getSaveFileName(self, "Save as *.mvi", filter="Mayavi (*.mvi)")
        if fname == "": return
        self.filedialog.setDirectory(os.path.dirname(str(fname)))
        bin_file = open(fname,"wb")
        axis = data[0].children[1].children[0].children[1]
        bounds = axis.axes.bounds       #For some strange reason the 'bounds' does not get saved in the tree when performing a pickle serialisation. This is a hack to get around that
        #pickle.dump(data,bin_file, protocol=pickle.HIGHEST_PROTOCOL, fix_imports=True)
        pickle.dump([data,bounds],bin_file, protocol=pickle.HIGHEST_PROTOCOL, fix_imports=True)
        bin_file.close()
        True
        
        
    #**************************************************************************************
    def ApplyWaterfall(self):
        self.LoadMayavi()
        x,y,z,y_err=self.GetWaterFallValues()
        pts = [0,0]
        if self.ui.interp_check.isChecked():
            xpts = int(self.ui.xpts_edit.text())
            ypts = int(self.ui.ypts_edit.text())
            pts = [xpts,ypts]
        self.mayaviobj.setWaterfall(z,x,y,y_err,pts)  #Note the difference in x,y,z assignemnts
        self.mayaviobj.visualization.surfaxes.axes.x_label = self.xlabel
        self.mayaviobj.visualization.surfaxes.axes.y_label = self.ylabel
        self.mayaviobj.visualization.surfaxes.axes.z_label = self.scanman.datasrc.ylabel
        True
        
    
    #**************************************************************************************
    def GraphAdd(self):
        
        self.maxid=self.maxid+1
        for axis in self.ui.graph_scan.figure.axes:         #delete the old axes
            self.ui.graph_scan.figure.delaxes(axis)
            
        nrplots = self.maxid
        for axisi in range(len(self.graphlist)):
            self.ui.graph_scan.figure.add_subplot(self.maxid+1,1,axisi)
            self.graphlist[axisi].addplot(self.ui.graph_scan.figure.axes[axisi])
            self.graphlist[axisi].setdata(self.graphlist[axisi].x,self.graphlist[axisi].y)
            
        prm1=str(self.ui.p1_scan_combo.currentText())
        prm2=str(self.ui.p2_scan_combo.currentText())
        newplot = Aplot(prm1,prm2)
        try:
            self.ui.graph_scan.figure.add_subplot(self.maxid+1,1,self.maxid)
        except:
            self.ui.graph_scan.figure.add_subplot(self.maxid+1,1,self.maxid+1)
        newplot.addplot(self.ui.graph_scan.figure.axes[self.maxid])
        self.graphlist.append(newplot)
        x , y = self.GetParamValues(prm1, prm2)
        self.graphlist[self.maxid].setdata(y,x)
        
        self.ui.graph_scan.figure.tight_layout()
        self.ui.graph_scan.draw()
        True

    
    
    #**************************************************************************************
    def GetWaterFallValues(self):
        
        prm1=str(self.ui.waterfall_scan_combo.currentText())
        if prm1 == "" :
            self.xlabel="Run_number"
        else:
            self.xlabel=prm1
        try:
            if self.scanman.ui.outputGroupBox.ui.allfiles_check.isChecked():
                flistidx = range(len(self.scanman.ui.sourceGroupBox.filelist))
            else:
                flistidx = [self.scanman.ui.sourceGroupBox.ui.file_tbl.currentRow()]
        except:             #This source is probably not a filesource and therefore only one dataset is present
            flistidx = [1]            
        
        x=[]
        y=[]
        #z=[]
        z=np.array([])
        y_err=[]
        run_number = float(1)
        progressfiles = ProgressBar("Retrieving parameters waterfall...", len(flistidx))
        ylabelold = ""
        ylabelnew = ""
        self.ylabel = ""
        for filei in flistidx:
            progressfiles.setinfo(self.scanman.ui.sourceGroupBox.filelist[filei].location)
            try:
                self.scanman.ui.sourceGroupBox.SelectDataFile(filei)
            except:
                True
            
            True
            src = self.scanman.datasrc
            self.setstart = 1
            self.setend = len(src.dataset)-1
            
            if (self.ui.range_radio.isChecked()):
                self.setstart = self.ui.rangemin_spin.value()
                self.setend = self.ui.rangemax_spin.value()
            
            self.scanman.SelectData(self.setstart,display=False)
            if len(y)==0:           #First file
                #y = [src.y]
                y = [src.y.tolist()]
                if (len(src.y)==len(src.y_err)):
                    y_err = [src.y_err.tolist()]
            else:
                y=np.concatenate((y,[src.y]),axis=0)
                if (len(src.y)==len(src.y_err)):
                    y_err=np.concatenate((y_err,[src.y_err]),axis=0)
                
            #x=[src.x]
            x=[src.x.tolist()]
            z_new = run_number if prm1=="" else float(src.prm[prm1])
            #z=np.append(z,z_new)
            z=z+[z_new]
            
            #xp=np.append(xp,[src.x])
            #yp=np.append(yp,[src.y])
            #zp=np.append(zp,[z_new]*len(src.x))
                    
            try:    #Only works with numbers but the parameter value can also be text in which case this will fail
                for setnr in range(self.setstart+1,self.setend+1):
                    run_number = run_number + 1
                    self.scanman.SelectData(setnr,display=False)
                    src = self.scanman.datasrc
                    #if src.prm.has_key("position"):
                    if "position" in src.prm.keys():
                        ylabelnew =src.prm["position"]
                    else:
                        ylabelnew = self.scanman.axistype
                    if  ylabelnew != ylabelold:
                        self.ylabel = self.ylabel + "," + ylabelnew
                        ylabelold = ylabelnew
                    #y=np.concatenate((y,[src.y]),axis=0)
                    y=y+[src.y.tolist()]
                    if (len(src.y)==len(src.y_err)):
                        y_err=y_err+[src.y_err.tolist()]
                    x=x+[src.x.tolist()]
                    z_new = run_number if prm1=="" else float(src.prm[prm1])
                    z=np.append(z,z_new)
                    
                    #xp=np.append(xp,[src.x])
                    #yp=np.append(yp,[src.y])
                    #zp=np.append(zp,[z_new]*len(src.x))
                    True
            except:
                x=[0,0]
                y=[0,0]
                y_err=[0]
            
            if progressfiles.wasCanceled(): break
            progressfiles.step()
        sortedi = z.argsort()
        y=np.array(y)
        y_err=np.array(y_err)
        x=np.array(x)
        self.ylabel = self.ylabel[1:] #remove the ',' at the beginning
        if len(y_err)==0:
            y_err = np.zeros((len(y),len(y[0])))
        try:
            return x[sortedi].tolist(), y[sortedi].tolist(), z[sortedi].tolist(), y_err[sortedi].tolist()
        except:
            
            return z[sortedi], z[sortedi], z[sortedi], z[sortedi]
        
    #**************************************************************************************
    def GetParamValues(self, prm1, prm2):
        try:
            if self.scanman.ui.outputGroupBox.ui.allfiles_check.isChecked():
                flistidx = range(len(self.scanman.ui.sourceGroupBox.filelist))
            else:
                flistidx = [self.scanman.ui.sourceGroupBox.ui.file_tbl.currentRow()]
        except:             #This source is probably not a filesource and therefore only one dataset is present
            flistidx = [1]          
        
        x=np.array([])
        y=np.array([])
        run_number = float(1)
        progressfiles = ProgressBar("Retrieving parameters [%s] and [%s] from files..." %(prm1,prm2), len(flistidx))
        for filei in flistidx:
            progressfiles.setinfo(self.scanman.ui.sourceGroupBox.filelist[filei].location)
            try:
                self.scanman.ui.sourceGroupBox.SelectDataFile(filei)
            except:
                True
            
            True
            src = self.scanman.datasrc
            self.setstart = 1
            self.setend = len(src.dataset)
            try:    #Only works with numbers but the parameter value can also be text in which case this will fail
                for setnr in range(self.setstart,self.setend):
                    self.scanman.SelectData(setnr,display=False)
                    src = self.scanman.datasrc
                    x=np.append(x,[float(src.prm[prm1])])
                    y_new = run_number if prm2=="" else float(src.prm[prm2])
                    y=np.append(y,y_new)
                    run_number = run_number + 1
                    True
            except:
                x=[0,0]
                y=[0,0]
            
            if progressfiles.wasCanceled(): break
            progressfiles.step()
        return x,y
        #    self.scanman.ui.sourceGroupBox.SelectDataFile(filei)
        #    for setnr in range(self.setstart,self.setend):
        #        #self.scanman.ui.dataset_spin.setValue(setnr)        #Selects the next dataset - Hopefully the callback will be completed before the next statements are executed
        #        self.scanman.SelectData(setnr,display=False)
        #        src = self.scanman.datasrc
        
        
    
    #**************************************************************************************
    def PopulateParamCombos(self):
        paramskeys=sorted(self.scanman.datasrc.prm.keys())
        #paramskeys.sort()
        p1params=[self.ui.p1_scan_combo.itemText(s) for s in range(self.ui.p1_scan_combo.count())]
        if p1params == paramskeys:
            True
        else:
            self.ui.p1_scan_combo.clear()
            self.ui.p1_scan_combo.addItems(paramskeys)
            self.ui.p2_scan_combo.clear()
            self.ui.p2_scan_combo.addItem("")
            self.ui.p2_scan_combo.addItems(paramskeys)
            self.ui.waterfall_scan_combo.clear()
            self.ui.waterfall_scan_combo.addItem("")
            self.ui.waterfall_scan_combo.addItems(paramskeys)
            
        
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------        
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
 
    
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
        
        True
       

if __name__ == '__main__':
    
    app = qt.QApplication(sys.argv)
    window=ExcelDEF()
    window.show()
    sys.exit(app.exec_())

        