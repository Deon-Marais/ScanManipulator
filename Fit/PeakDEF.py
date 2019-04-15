'''
Created on 08 May 2014

@author: Deon
'''
from PyQt4.QtGui import QGroupBox as QGroupBox
from Fit.PeakGUI import Ui_Peak
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtCore
from pylab import np
import sys
from matplotlib.lines import Line2D
from scanlib import gauss
#from pyspec import fit, fitfuncs
from thirdparty.pyspec import fitfuncs
from thirdparty.pyspec import fit      #This is the exact one from pyspec, but modified in the way that the stdev is calculated for mpfit
import mylib


#**************************************************************************************
def gauss(x, p, mode='eval'):
    """Gaussian defined by amplitide

    Function:
       :math:`f(x) = k + m*x + p_2 \exp\left(\\frac{-(x - p_0)^2}{2p_1^2}\\right)`

    """
    try:
        if mode == 'eval':
            cent=p[0];wid=p[1];amp=p[2];const=p[3];slope=p[4]
            #out = const + amp * np.exp(-1.0 * (x - cent)**2 / (2 * wid**2))
            #Inserted the 0.5* because we want FWHM out, not HWHM
            #out = const + slope*x + amp * np.exp(-1.0 * (x - cent)**2 / (2 * (0.5*wid)**2))
            conversion =2.0*np.sqrt(2.0*np.log(2))      #Hutchings et al. Introduction to the characterisation of residual stress by neutron diffraction.2005. Page 159 
            #conversion = 2.0
            out = const + slope*x + amp * np.exp(-1.0 * (x - cent)**2 / (2 * (wid/conversion)**2))
        elif mode == 'params':
            out = ['cent', 'sigma', 'amp', 'const', 'slope']
        elif mode == 'name':
            out = "Gaussian"
        elif mode == 'guess':
            g = fitfuncs.peakguess(x, p)
            out = [g[0], g[1] / (4 * np.log(2)), g[3], g[4], g[5]]
        else:
            out = []
    except:
        out = [0,0,0,0,0]

    return out



#**************************************************************************************
class RangeData():
    def __init__(self,colorname='red'):
        self.id=1
        self.start = self.stop = int(0)
        self.position = self.fwhm = self.intensity = self.background = self.intensity_sum = self.intensity_area = self.counts = self.errustrain = float(0.0)
        self.bgndfitparms = [0,0]
        self.bgndyvals = np.array([])   #will contain the y values of the calculated background over the fit range
        self.position_fix = self.fwhm_fix = self.intensity_fix = self.background_fix = False
        self.position_stdev = self.fwhm_stdev = self.intensity_stdev = self.background_stdev = float(0.0)
        self.chi2 = self.r2 = self.time = float(0.0)
        self.position_valid = self.fwhm_valid = self.intensity_valid = self.background_valid = self.chi2_valid = self.r2_valid = True  #Red for invalid, Black for valid
        self.niter = int(0)
        self.color = colorname
        self.line = Line2D([], [], color = colorname, antialiased = False, alpha = 0.5, linestyle=":")
        self.fittedline = Line2D([], [], color = colorname, antialiased = False)
        self.bgrngline = Line2D([], [], color = colorname, antialiased = False, alpha = 0.5, linestyle=" ", marker='.', markersize=2.5)
        self.bgline = Line2D([], [], color = colorname, antialiased = False, alpha = 0.5, linewidth = 0.5, linestyle="-")
        self.diffline = Line2D([], [], color = colorname, antialiased = False, alpha = 0.9, linewidth = 0.2)
        


#**************************************************************************************
class VarSlider():
    def __init__(self):
        self.min = self.max = self.delta = float(0)
        self.destText = []
        
     



#**************************************************************************************
class PeakDEF(QGroupBox):
    fittedsignal = qtCore.pyqtSignal()
    
    def __init__(self, ScanmanMain):
         
        QGroupBox.__init__(self)
        self.name = "Peak"
        self.ui = Ui_Peak()
        self.ui.setupUi(self)
        self.scanman = ScanmanMain
        self.rangeList = []
        self.prevrangeList = []
        self.colornr = 0
        self.colorlist = ['blue','green','cyan','magenta', 'brown']
        
        self.myslide = VarSlider()
        self.sliderLinkText = []
        
        self.bgmode="Auto"
        self.linesperrange = 4
        
        self.range_start_row = 0
        self.range_end_row = 1
        self.position_row = 2
        self.fwhm_row = 3
        self.intensity_row = 4
        self.background_row = 5
        self.chi2_row = 6
        self.r2_row = 7
        self.niter_row = 8
        self.time_row = 9
        self.intensity_sum_row = 10
        self.intensity_area_row = 11
        self.counts_row = 12
        self.errustrain_row = 13
        
        self.ui.bgstart_edit.installEventFilter(self)
        self.ui.bgend_edit.installEventFilter(self)
        self.ui.bgfix_edit.installEventFilter(self)
        
        #self.scanman.signal["xtypechanged"].connect(self.xTypeChanged)
        self.range_tbl = mylib.Table(self.ui.range_tbl)
        
        True
        
    
    def xTypeChanged(self,axistype):
        self.ui.range_tbl.verticalHeaderItem(2).setText(axistype)
           
    #**************************************************************************************
    def eventFilter(self, widget, event):
        if event.type() == qtCore.QEvent.FocusIn:
            #txtstr = "<font color='black'>" +varname+"</font>"
            wedisconnected = False
            try:
                self.ui.var_slider.valueChanged.disconnect()     #otherwise this function might be called recursively
                wedisconnected = True
            except:
                a=1
            
            if (widget.objectName()=="bgstart_edit"):
                self.LinkSlider("x", widget, "<font color='black'>bg_start</font>")
            elif (widget.objectName()=="bgend_edit"):
                self.LinkSlider("x", widget, "<font color='black'>bg_end</font>")
            elif (widget.objectName()=="bgfix_edit"):
                self.LinkSlider("y", widget, "<font color='black'>All fixed</font>")
            
            if (wedisconnected): self.ui.var_slider.valueChanged.connect(self.VarSliderValChanged)   #Reconnect the signal
            return False
        else:
            return False
        
    #**************************************************************************************
    def NewTableValue(self,rangenum, prop, value):
        rngtbl=self.ui.range_tbl
        valcol = (rangenum)*2
        valrow = eval("self." + prop + "_row")
        rngtbl.item(valrow, valcol).setText(value)
        True
        
        
    #**************************************************************************************
    def UpdateFitRange(self,rangenum):
        rngtbl=self.ui.range_tbl
        valcol = (rangenum)*2
        strt = int(rngtbl.item(0, valcol).text())
        stp = int(rngtbl.item(1, valcol).text())
        self.rangeList[rangenum].start=strt
        self.rangeList[rangenum].stop=stp
         

    #**************************************************************************************
    def AdjustCheckSate(self,row,col,rangenum, name):
        #let the internal data structure reflect what is presented in the table
        rngtbl=self.ui.range_tbl
        item = rngtbl.item(row, col)
        currangefix=False
        exec("currangefix = self.rangeList[rangenum]."+name+"_fix")
        if ((item.checkState() == qtCore.Qt.Checked) and (currangefix == False)):
            exec("self.rangeList[rangenum]."+name+"_fix=True")
            return
        if ((item.checkState() == qtCore.Qt.Unchecked) and (currangefix == True)):
            exec("self.rangeList[rangenum]."+name+"_fix=False")    
            return   
        nameval = 0.0
        tableval = item.text()
        exec("nameval = self.rangeList[rangenum]."+name)
        if ("{0:.4f}".format(nameval) != tableval):
            exec("self.rangeList[rangenum]."+name+"=float(tableval)")
            
           
            
    def UpdateRangeData(self, rngnum=-1):
        start = rngnum
        end = rngnum +1
        if (rngnum == -1):
            start = 0
            end = len(self.rangeList)
        for i in range(start, end): 
            rng = self.rangeList[i]
            rng.line.set_data(self.scanman.datasrc.x[rng.start:rng.stop], self.scanman.datasrc.y[rng.start:rng.stop])
        
        
    #**************************************************************************************
    def CellValueChanged(self,row,col):
        rngtbl=self.ui.range_tbl
        rangenum = np.floor_divide(col,2)
        valcol = (rangenum)*2
        if (rangenum < 0): return

        wedisconnected = False
        try:
            rngtbl.cellChanged.disconnect()     #otherwise this function might be called recursively
            wedisconnected = True
        except:
            a=1
        
        if (row == self.position_row): self.AdjustCheckSate(row,valcol,rangenum,"position")
        if (row == self.fwhm_row): self.AdjustCheckSate(row,valcol,rangenum,"fwhm")
        if (row == self.intensity_row): self.AdjustCheckSate(row,valcol,rangenum,"intensity")
        if (row == self.background_row): self.AdjustCheckSate(row,valcol,rangenum,"background")
        
        if ((row > 1) and (rngtbl.item(row, valcol).flags() == (rngtbl.item(row, valcol).flags() & ~qtCore.Qt.ItemIsEditable))): return     #skip cells not editable
        
        minrng = 0
        maxrng = 0
        try:
            if (rngtbl.item(0, valcol).text() != ""):  minrng = int(rngtbl.item(0, valcol).text())
            if (rngtbl.item(1, valcol).text() != ""):  maxrng = int(rngtbl.item(1, valcol).text())   
        except:
            True
        
        #self.rangeList[rangenum].line.set_data(self.scanman.x[minrng:maxrng], self.scanman.y[minrng:maxrng])
        self.UpdateRangeData(rangenum)
        self.FitRange(rangenum)
        self.scanman.ui.graph.draw()
        
        if(wedisconnected): rngtbl.cellChanged.connect(self.CellValueChanged)   #Reconnect the signal

        if (row == 0 and self.rangeList[rangenum].start==minrng): return
        if (row == 1 and self.rangeList[rangenum].stop==maxrng): return
        
        self.UpdateFitRange(rangenum)
        if (row == 0): self.scanman.ui.minSlider.setValue(self.rangeList[rangenum].start)
        if (row == 1): self.scanman.ui.maxSlider.setValue(self.rangeList[rangenum].stop)       
        
            
    #**************************************************************************************
    def UpdateUIValues(self):
        rngtbl=self.ui.range_tbl
        curcol = rngtbl.currentColumn()
        rangenum = np.floor_divide(curcol,2)
        if (rangenum < 0): return

        wedisconnected = False
        try:
            rngtbl.cellChanged.disconnect()     #otherwise this function might be called recursively
            wedisconnected = True
        except:
            a=1
        
        
        valcol = (rangenum)*2
        rng=self.rangeList[rangenum]
        self.scanman.ui.slideminLabel.setText("<font color='" + rng.color +"'>Min_"+str(rangenum)+"</font>")
        self.scanman.ui.slidemaxLabel.setText("<font color='" + rng.color +"'>Max_"+str(rangenum)+"</font>")
        minrng = rng.start
        maxrng = rng.stop        
        rngtbl.item(0, valcol).setText(str(minrng))
        rngtbl.item(1, valcol).setText(str(maxrng))
        self.scanman.ui.minSlider.setValue(minrng)
        self.scanman.ui.maxSlider.setValue(maxrng)
        
        if (wedisconnected): rngtbl.cellChanged.connect(self.CellValueChanged)   #Reconnect the signal

        currow = rngtbl.currentRow()
        curitem = rngtbl.item(currow,curcol)
        if curitem.checkState() == qtCore.Qt.Unchecked: return
        
        wedisconnected = False
        try:
            self.ui.var_slider.valueChanged.disconnect()     #otherwise this function might be called recursively
            wedisconnected = True
        except:
            a=1
        
        varname = rngtbl.verticalHeaderItem(currow).text() + "_" + str(rangenum)
        txtstr = "<font color='" + rng.color+ "'>" +varname+"</font>"
        #self.ui.varname_label.setText("<font color='" + rng.color+ "'>" +varname+"</font>")

        if (currow == self.position_row or currow == self.fwhm_row): self.LinkSlider("x", curitem, txtstr)
        if (currow == self.intensity_row or currow == self.background_row): self.LinkSlider("y", curitem, txtstr)
        
        if (wedisconnected): self.ui.var_slider.valueChanged.connect(self.VarSliderValChanged)   #Reconnect the signal

        

    #**************************************************************************************
    def LinkSlider(self,xory,curitem, txtstr):
        curval = float(curitem.text())
        self.myslide.destText=curitem.setText
        self.ui.varval_label.setText("{0:.4f}".format(curval))
        self.ui.varname_label.setText(txtstr)
        if (xory == "x"):
            self.myslide.min = 0 #self.scanman.datasrc.x_min
            self.myslide.max = self.scanman.datasrc.nchan #self.scanman.datasrc.x_max
        else:
            self.myslide.min = self.scanman.datasrc.y_min 
            self.myslide.max = self.scanman.datasrc.y_max    
        self.myslide.delta = (self.myslide.max - self.myslide.min)/100
        self.ui.var_slider.setValue(int((curval - self.myslide.min)/(self.myslide.max-self.myslide.min)*100))
        #self.ui.var_slider.setValue(int((max([curval,self.myslide.min])-self.myslide.min)/self.myslide.delta*100))
    
    
    #**************************************************************************************
    def VarSliderValChanged(self,newval):
        value = newval*self.myslide.delta + self.myslide.min
        self.myslide.destText("{0:.4f}".format(value))
        self.ui.varval_label.setText("{0:.4f}".format(value))
        
        

    #**************************************************************************************
    def AddRange(self):
 
        self.rangeList.append(RangeData(self.colorlist[self.colornr]))
        self.colornr += 1 
        if (self.colornr > len(self.colorlist)-1): self.colornr = 0
        self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[len(self.rangeList)-1].line)
        self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[len(self.rangeList)-1].fittedline)
        self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[len(self.rangeList)-1].bgrngline)
        self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[len(self.rangeList)-1].bgline)        
        self.scanman.ui.diffgraph.figure.axes[0].add_line(self.rangeList[len(self.rangeList)-1].diffline)

        
        rngtbl=self.ui.range_tbl
        nrcols = rngtbl.columnCount()
        nrrange = rngtbl.columnCount()/2
        rngtbl.setColumnCount(nrcols+2)
        
        wedisconnected = False
        try:
            rngtbl.cellChanged.disconnect()     #otherwise this function might be called recursively
            wedisconnected = True
        except:
            True
        
        headval = qt.QTableWidgetItem()
        headval.setText("Val_" + str(nrrange))
        headval.setTextColor(qt.QColor(self.rangeList[-1].color))
        rngtbl.setHorizontalHeaderItem(nrcols,headval)
        
        headdev = qt.QTableWidgetItem()
        headdev.setText("Stdev_" + str(nrrange))
        headdev.setTextColor(qt.QColor(self.rangeList[-1].color))
        rngtbl.setHorizontalHeaderItem(nrcols+1,headdev)

        # the Range_start and Range_stop are not checkable
        for i in range(2):
            someitem = qt.QTableWidgetItem()
            someitem.setTextAlignment(qtCore.Qt.AlignRight)
            someitem.setText("0")
            rngtbl.setItem(i,nrcols,someitem)
        for i in range(2, 6):                       #this is the Position, FWHM, Intensity and Background
            someitem = qt.QTableWidgetItem()
            someitem.setFlags(someitem.flags() | qtCore.Qt.ItemIsUserCheckable)
            someitem.setTextAlignment(qtCore.Qt.AlignRight)
            someitem.setText("0")
            someitem.setCheckState(qtCore.Qt.Unchecked)
            rngtbl.setItem(i,nrcols,someitem)
        for i in range(6, rngtbl.rowCount()):       #this is the Chi^2, R^2, nIter and Time, Intensity_sum, Intensity_area, Counts, u_strain
            someitem = qt.QTableWidgetItem()
            someitem = qt.QTableWidgetItem()
            someitem.setFlags(someitem.flags()  & ~qtCore.Qt.ItemIsEditable)
            someitem.setTextAlignment(qtCore.Qt.AlignRight)
            someitem.setText("0")
            rngtbl.setItem(i,nrcols,someitem)
        for i in range(rngtbl.rowCount()):          #this is the standard deviation column
            someitem = qt.QTableWidgetItem()
            someitem.setFlags(someitem.flags()  & ~qtCore.Qt.ItemIsEditable)
            someitem.setTextAlignment(qtCore.Qt.AlignRight)
            rngtbl.setItem(i,nrcols+1,someitem)
            
        if self.ui.background_box.isChecked():
            rngtbl.item(self.background_row, nrcols).setCheckState(qtCore.Qt.Checked)
            self.rangeList[-1].background_fix=True
          

        if(wedisconnected): rngtbl.cellChanged.connect(self.CellValueChanged)   #Reconnect the signal
        rngtbl.setCurrentCell(0,nrcols, qt.QItemSelectionModel.SelectCurrent)        
        
        

    #**************************************************************************************
    def DelRange(self):
        rngtbl=self.ui.range_tbl
        selcol = rngtbl.currentColumn()
        rangenum = np.floor_divide(selcol,2)

        if (selcol%2 == 0):
            rngtbl.removeColumn(selcol + 1)
            rngtbl.removeColumn(selcol)
        else:
            rngtbl.removeColumn(selcol)
            rngtbl.removeColumn(selcol - 1)
        headers = [["Val_"+str(i), "Stdev_" + str(i)] for i in range(np.floor_divide(rngtbl.columnCount(),2))]
        flatheader = [item for sublist in headers for item in sublist]
        rngtbl.setHorizontalHeaderLabels(flatheader)
        
        del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #.lines[0] is the main data
        del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #all would have moved up, therefore the fitted line is now in this position 
        del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #background range (bgrngline) is now in this position 
        del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #background line is now in this position 
        del self.scanman.ui.diffgraph.figure.axes[0].lines[rangenum]        #the difference graph only has one line per range
        del self.rangeList[rangenum]
        #self.FitRange()
        self.scanman.FitRange()
        
    #**************************************************************************************
    def HideGraphlines(self):
        for rangenum in range(len(self.rangeList)):
            del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #.lines[0] is the main data
            del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #all would have moved up, therefore the fitted line is now in this position 
            del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #background range (bgrngline) is now in this position 
            del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #background line is now in this position 
            del self.scanman.ui.diffgraph.figure.axes[0].lines[rangenum]        #the difference graph only has one line per range
            self.scanman.ui.graph.draw()
            self.scanman.ui.diffgraph.draw() 
            
    def ShowGraphlines(self):
        for rangenum in range(len(self.rangeList)):
            self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[rangenum].line)
            self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[rangenum].fittedline)
            self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[rangenum].bgrngline)
            self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[rangenum].bgline)        
            self.scanman.ui.diffgraph.figure.axes[0].add_line(self.rangeList[rangenum].diffline)
            self.scanman.ui.graph.draw()
            self.scanman.ui.diffgraph.draw()                
    
    #**************************************************************************************
    def getKey(self,item):          #used for sorting
        return item[0]
    
    #**************************************************************************************
    def CalcBG(self,rngnum = -1):
        bgrng_x=np.array([])
        bgrng_y=np.array([])
        
        if self.bgmode=="Auto":
            for rng in self.rangeList:
                rng.bgndfitparms = [0,0]
                rng.bgrngline.set_data([0],[0])
                rng.bgline.set_data([0],[0])
            return
        
        if self.bgmode=="All fixed":
            background= float(self.ui.bgfix_edit.text())
            for rng in self.rangeList:
                rng.bgndfitparms = [0,rng.background]       #slope is 0, constant background
                rng.background=background
                rng.bgrngline.set_data([0],[0])
                rng.bgline.set_data([self.scanman.datasrc.x[0],self.scanman.datasrc.x[-1]],[rng.background,rng.background])
            return      #no need to perform fitting routine
        
        elif self.bgmode=="Single fixed":
            for rng in self.rangeList:
                bgrng_x=rng.line.get_xdata(True)
                bgrng_y=[rng.background]*len(bgrng_x)
                #rng.bgrngline.set_data(bgrng_x,bgrng_y)
                rng.bgndfitparms = [0,rng.background]       #slope is 0, constant background
                rng.bgrngline.set_data([0],[0])
                rng.bgline.set_data([self.scanman.datasrc.x[0],self.scanman.datasrc.x[-1]],[rng.background,rng.background])
            return                  #no need to perform fitting routine
            
        elif self.bgmode=="Non-peaks":
            minmax = sorted([[item.start, item.stop] for item in self.rangeList], key=self.getKey)
            #minmax.insert(0, [0,self.scanman.datasrc.lowerchan])
            #minmax.append([self.scanman.datasrc.upperchan,self.scanman.datasrc.nchan])
            flatminmax = []
            flatminmax.append(minmax[0])
            #flatminmax.append([self.scanman.datasrc.upperchan,self.scanman.datasrc.nchan])
            nopeakrng = []
            
            for i in range(1,len(minmax)):
                if (minmax[i][0]-1 <= flatminmax[-1][1]):
                    flatminmax[-1][1] = minmax[i][1]
                else:
                    flatminmax.append(minmax[i])
            if(flatminmax[0][0]!=0): flatminmax.insert(0, [0,0])
            #maxx=int(max(self.scanman.datasrc.x))
            maxx=self.scanman.datasrc.nchan
            if(flatminmax[-1][1]!=maxx): flatminmax.append([maxx,maxx])
            for i in range(len(flatminmax)-1):
                nopeakrng.append([flatminmax[i][1],flatminmax[i+1][0]])

            for rng in nopeakrng:
                bgrng_x = np.append(bgrng_x,self.scanman.datasrc.x[rng[0]:rng[1]])
                bgrng_y = np.append(bgrng_y,self.scanman.datasrc.y[rng[0]:rng[1]])
           
            for rng in self.rangeList:  rng.bgrngline.set_data(bgrng_x, bgrng_y)
                            
            
            
        elif self.bgmode=="Range":
            bg_start = int(float(self.ui.bgstart_edit.text()))
            bg_end = int(float(self.ui.bgend_edit.text()))
            bgrng_x=self.scanman.datasrc.x[bg_start:bg_end]
            bgrng_y=self.scanman.datasrc.y[bg_start:bg_end]
            for rng in self.rangeList:  rng.bgrngline.set_data(bgrng_x, bgrng_y)
                       
        
        
        #not enough data to do a fitting
        if (len(bgrng_x)==0):
            for rng in self.rangeList:
                rng.background=float(0)
                rng.background_stdev=-1
                rng.bgline.set_data([0],[0])
            return

        #masklow = self.scanman.datasrc.lowerchan
        #maskhigh = self.scanman.datasrc.upperchan
        masklow = 0
        maskhigh = self.scanman.datasrc.nchan
        #Now perform the straight line fitting            
        #gparams = fitfuncs.constant(bgrng_x[masklow:maskhigh], bgrng_y[masklow:maskhigh], 'guess')
        gparams = fitfuncs.linear(bgrng_x, bgrng_y, 'guess')
        #fitob = fit.fit(x=bgrng_x[masklow:maskhigh], y=bgrng_y[masklow:maskhigh], guess=gparams, quiet=True, funcs=[fitfuncs.constant], r2min=-1)
        #fitob = fit.fit(x=bgrng_x[masklow:maskhigh], y=bgrng_y[masklow:maskhigh], guess=gparams, quiet=True, funcs=[fitfuncs.linear], r2min=-1)
        fitob = fit.fit(x=bgrng_x, y=bgrng_y, guess=gparams, quiet=True, funcs=[fitfuncs.linear], r2min=-1)
        
        fitob.go(interactive=False)
        #rng.bgndfitparms = fitob.result.copy()
        background=float(rng.bgndfitparms[1])
        stdev=float(fitob.stdev[1])
        for rng in self.rangeList:
                rng.bgndfitparms = fitob.result
                rng.background=background
                rng.background_stdev=stdev
                bgnd_fitted=fitob.evalfitfunc(x=self.scanman.datasrc.x)
                #rng.bgndyvals = bgnd_fitted[1]
                
                #rng.bgline.set_data([self.scanman.datasrc.x[0],self.scanman.datasrc.x[-1]],[rng.background,rng.background])
                rng.bgline.set_data(bgnd_fitted)
                True
        
        
            
    
    #**************************************************************************************
    def BgChanged(self):
        rngtbl=self.ui.range_tbl

        wedisconnected = False
        try:
            rngtbl.cellChanged.disconnect()     #otherwise this function might be called recursively
            wedisconnected = True
        except:
            True

        
        if self.ui.background_box.isChecked():
            for i in range(len(self.rangeList)):
                rngtbl.item(self.background_row, i*2).setCheckState(qtCore.Qt.Checked)
                self.rangeList[i].background_fix=True
            
            if self.ui.bgsinglefixed_radio.isChecked():      self.bgmode="Single fixed"
            if self.ui.bgallfixed_radio.isChecked():       self.bgmode="All fixed"
            if self.ui.bgnonpeaks_radio.isChecked():         self.bgmode="Non-peaks"
            if self.ui.bgrange_radio.isChecked():            self.bgmode="Range"           

        else:   
            self.bgmode="Auto"
            for i in range(len(self.rangeList)):
                rngtbl.item(self.background_row, i*2).setCheckState(qtCore.Qt.Unchecked)
                self.rangeList[i].background_fix=False
                
                   
        

        self.FitRange()
        self.scanman.ui.graph.draw()
        
        if (wedisconnected): rngtbl.cellChanged.connect(self.CellValueChanged)   #Reconnect the signal
        
        
 
        

        
    #**************************************************************************************
    def FitRange(self,rngnum=-1):
        rngtbl=self.ui.range_tbl
        start = rngnum
        end = rngnum +1
        if (rngnum == -1):
            start = 0
            end = len(self.rangeList)

        self.CalcBG()
        
        wedisconnected = False
        try:
            rngtbl.cellChanged.disconnect()     #otherwise this function might be called recursively
            wedisconnected = True
        except:
            True
        
        for i in range(start, end): 
            rng = self.rangeList[i]
            #xdata = rng.line.get_xdata(True)
            #ydata = rng.line.get_ydata(True)
            xdata = self.scanman.datasrc.x[rng.start:rng.stop]
            ydata = self.scanman.datasrc.y[rng.start:rng.stop]
            #xdata_smooth = np.linspace(xdata[0],xdata[-1],100)
            xwidth = xdata[1:]-xdata[:-1]
            
            if ((len(xdata) < 4) or (len(ydata) < 4)): continue                 #break out if the range was chosen wrong
            if (min(ydata) == max(ydata)):                                      #No difference in values detected - cannto fit peak
                gparams = [0.0]*5
                stdev = [0.0]*4
                fitted = ydata
                True
            else:       #Try to fit the data
                gparams = gauss(xdata, ydata, 'guess')
                gparamsfix = [0]*len(gparams)
                gparams[4] = 0.0    #slope
                gparamsfix[4] = 1
                if (rng.position_fix): 
                    gparams[0] = rng.position
                    gparamsfix[0] = 1
                if (rng.fwhm_fix): 
                    gparams[1] = rng.fwhm
                    gparamsfix[1] = 1
                if (rng.intensity_fix): 
                    gparams[2] = rng.intensity
                    gparamsfix[2] = 1
                if (rng.background_fix): 
                    #gparams[3] = rng.background
                    #gparamsfix[3] = 1
                    gparams[3] = rng.bgndfitparms[1]
                    gparamsfix[3] = 1
                    gparams[4] = rng.bgndfitparms[0]
                    gparamsfix[4] = 1
                fitob = fit.fit(x=xdata, y=ydata, guess=gparams, ifix=gparamsfix ,quiet=True, funcs=[gauss], r2min=-100000, optimizer='mpfit')
            
                if ((min(gparams) == max(gparams)) and min(gparams)==0):      #Could not find any possible peak
                    fitted = ydata
                    stdev = gparams
                    rng.r2 = 0
                    rng.niter = 0
                    rng.time = 0
                else:
                    fitob.go(interactive=False)
                    gparams=fitob.result
                    rng.bgndfitparms[1] = gparams[3]
                    rng.bgndfitparms[0] = gparams[4]
                    stdev=fitob.stdev
                    fitted = gauss(xdata,gparams)
                    #fitted_smooth= gauss(xdata_smooth,gparams)
                    rng.chi2 = fitob.chi2
                    rng.r2 = fitob.r2
                    rng.niter = fitob._niter
                    rng.time = fitob._lastRunTime
            
            #rng.fittedline.set_data(rng.line.get_xdata(True), fitted)
            #rng.diffline.set_data(rng.line.get_xdata(True), rng.line.get_ydata(True) - fitted)
            rng.fittedline.set_data(xdata, fitted)
            #rng.fittedline.set_data(xdata_smooth, fitted_smooth)
            rng.diffline.set_data(xdata, ydata - fitted)
            rng.position = gparams[0]
            rng.fwhm = gparams[1]
            rng.intensity = gparams[2]
            rng.background = gparams[3]
            rng.position_stdev = stdev[0]
            rng.fwhm_stdev = stdev[1]
            rng.intensity_stdev = stdev[2]
            if (self.bgmode=="Single fixed" or self.bgmode=="All fixed" or self.bgmode=="Auto"): rng.background_stdev = stdev[3]
            
            
            #Determine if the calculated fits are valid
            rng.position_valid = True
            rng.fwhm_valid = True
            if (rng.fwhm <= 0) or (rng.fwhm_stdev/rng.fwhm >= 0.2) or (rng.fwhm_stdev == 0 and rng.fwhm_fix==False):
                rng.fwhm_valid = False
                rng.position_valid = False
            
            if (rng.intensity <= 0) or (rng.intensity_stdev/rng.intensity >= 0.3) or (rng.intensity_stdev == 0  and rng.intensity_fix==False):
                rng.intensity_valid = False
                rng.position_valid = False 
            else:
                rng.intensity_valid = True
            #if (rng.intensity == False): rng.position_valid = False  
                
            if (rng.background != 0):
                if (rng.intensity / rng.background < 1.1): rng.position_valid = False  
                
            if (rng.position < xdata.min()) or (rng.position > xdata.max()):
                rng.position_valid = False
                
            
            ybgnd = fitfuncs.linear(xdata, rng.bgndfitparms,"eval")    
            rng.intensity_sum = np.sum(fitted-ybgnd)
            rng.intensity_area = np.sum(abs((fitted-ybgnd)[:-1]*xwidth))
            rng.counts = np.sum(ydata)
            #cmnerrterm = np.sqrt(2.0*rng.position_stdev*rng.position_stdev/rng.position/rng.position)*1e6
            if self.scanman.axistype == "d-spacing":
                #rng.errustrain = np.sqrt(2.0*rng.position_stdev*rng.position_stdev/rng.position/rng.position)/rng.position*1e6
                rng.errustrain = np.sqrt(2.0)*rng.position_stdev/rng.position*1e6
            #elif self.scanman.axistype =="Angle":
                #pos = np.sin(np.deg2rad(rng.position/2.0))
                #err = np.sin(np.deg2rad(rng.position_stdev/2.0))
                #rng.errustrain = np.sqrt(2.0*err*err/pos/pos)/pos*1e6
            else:
                rng.errustrain=0.0
                    
            rngtbl.item(self.position_row, i*2).setForeground(qt.QBrush(qt.QColor('Black' if rng.position_valid else 'Red')))
            rngtbl.item(self.position_row, i*2).setText("{0:.4f}".format(rng.position))
            rngtbl.item(self.position_row, i*2 + 1).setText("{0:.3e}".format(rng.position_stdev))
            rngtbl.item(self.fwhm_row, i*2).setForeground(qt.QBrush(qt.QColor('Black' if rng.fwhm_valid else 'Red')))
            rngtbl.item(self.fwhm_row, i*2).setText("{0:.4f}".format(rng.fwhm))
            rngtbl.item(self.fwhm_row, i*2 + 1).setText("{0:.3e}".format(rng.fwhm_stdev))
            rngtbl.item(self.intensity_row, i*2).setForeground(qt.QBrush(qt.QColor('Black' if rng.intensity_valid else 'Red')))
            rngtbl.item(self.intensity_row, i*2).setText("{0:.4f}".format(rng.intensity))
            rngtbl.item(self.intensity_row, i*2 + 1).setText("{0:.3e}".format(rng.intensity_stdev))
            rngtbl.item(self.background_row, i*2).setText("{0:.4f}".format(rng.background))
            rngtbl.item(self.background_row, i*2 + 1).setText("{0:.3e}".format(rng.background_stdev))
            rngtbl.item(self.chi2_row, i*2).setText("{0:.3e}".format(rng.chi2))
            rngtbl.item(self.r2_row, i*2).setText("{0:.4f}".format(rng.r2))
            rngtbl.item(self.niter_row, i*2).setText("{0:.4f}".format(rng.niter))
            rngtbl.item(self.time_row, i*2).setText("{0:.4f}".format(rng.time))
            rngtbl.item(self.intensity_sum_row, i*2).setText("{0:.4f}".format(rng.intensity_sum))
            rngtbl.item(self.intensity_area_row, i*2).setText("{0:.4f}".format(rng.intensity_area))
            rngtbl.item(self.counts_row, i*2).setText("{0:.4f}".format(rng.counts))
            rngtbl.item(self.errustrain_row, i*2).setText("{0:.4f}".format(rng.errustrain))
           
            
        #self.scanman.ui.graph.draw()
        
        ymin = y = 0.0
        ymax = x = 0.0
        for rng in self.rangeList:
            if (len(rng.diffline._y) > 0):
                y = min(rng.diffline.get_ydata(True))
                if (y < ymin): ymin = y
                y = max(rng.diffline.get_ydata(True))
                if (y > ymax): ymax = y
        ybuf = (ymax - ymin) * 0.1
        if ybuf == 0: ybuf = 1.0
        self.scanman.ui.diffgraph.figure.axes[0].set_ylim(ymin - ybuf, ymax + ybuf)
            
                 
        #self.scanman.ui.diffgraph.draw()
        
    
        if (wedisconnected): rngtbl.cellChanged.connect(self.CellValueChanged)   #Reconnect the signal
        self.fittedsignal.emit()        #To call any listeners
        True
    
    #**************************************************************************************
#if __name__ == '__main__':
    
#    app = qt.QApplication(sys.argv)
#    window=FitDEF()
#    window.show()
#    sys.exit(app.exec_())

        