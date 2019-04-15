'''
Created on 09 Mar 2015

@author: Deon
'''
from PyQt4.QtGui import QGroupBox as QGroupBox
from Fit.FitCommonGUI import Ui_FitCommon
import PyQt4.QtCore as qtCore
import PyQt4.QtGui as qt
from matplotlib.lines import Line2D
from pylab import np
import mylib


class FitElement():
    def __init__(self,name):
        self.name = name
        self.value = float(0.0)
        self.fix = False
        self.stdev = float(0.0)
        self.valid = True
        self.enabled = True
        #self.min = float(0.0)
        #self.max = float(0.0)
        self.tableitem = qt.QTableWidgetItem()
        self.tablestditem = qt.QTableWidgetItem()
        self.format = ""
        #self.linkaxis = linkaxis
        

class RangeDataCommon():
    def __init__(self,colorname='red'):
        self.id=1
        #self.start = self.stop = int(0)


        self.color = colorname
        self.line = Line2D([], [], color = colorname, antialiased = False, alpha = 0.5, linestyle=":")
        self.fittedline = Line2D([], [], color = colorname, antialiased = False)
        self.bgrngline = Line2D([], [], color = colorname, antialiased = False, alpha = 0.5, linestyle=" ", marker='.', markersize=2.5)
        self.bgline = Line2D([], [], color = colorname, antialiased = False, alpha = 0.5, linewidth = 0.5, linestyle="-")
        self.diffline = Line2D([], [], color = colorname, antialiased = False, alpha = 0.9, linewidth = 0.2)
        
        self.rangeparams = {}
        self.iterparams = {}
        self.miscparams = {}
        self.fitparams = {}
        self.allparams = {}
        
    def createElem(self, prm, checkable = True, editable = True):
        elem = FitElement(prm)
        editflag = ~qtCore.Qt.ItemIsEditable
        if editable == True: editflag = qtCore.Qt.ItemIsEditable
        checkflag = ~qtCore.Qt.ItemIsUserCheckable
        if checkable == True: checkflag = qtCore.Qt.ItemIsUserCheckable
        
        elem.tableitem.setFlags(elem.tableitem.flags() & editflag & checkflag)
        elem.tableitem.setTextAlignment(qtCore.Qt.AlignRight)
        elem.tableitem.setText("0")
        elem.tablestditem.setFlags(~qtCore.Qt.ItemIsEditable)
        elem.tablestditem.setTextAlignment(qtCore.Qt.AlignRight)
        
        #flags = (elem.tableitem.flags()  & ~qtCore.Qt.ItemIsEditable)
        #if checkable == True:
        #    itemflags = (elem.tableitem.flags() | qtCore.Qt.ItemIsUserCheckable)
        #    elem.tableitem.setCheckState(qtCore.Qt.Unchecked)
        #else:
        #    itemflags = flags
        #elem.tableitem.setFlags(itemflags)
        #elem.tableitem.setTextAlignment(qtCore.Qt.AlignRight)
        #elem.tableitem.setText("0")
        #elem.tablestditem.setFlags(flags)
        #elem.tablestditem.setTextAlignment(qtCore.Qt.AlignRight)
        return elem
    
    def setparams(self,prmdict, prmnamelist, checkable = True, editable = True):
        for prm in prmnamelist:
            elem = FitElement(prm)
            iflag = elem.tableitem.flags()
            editflag = iflag | qtCore.Qt.ItemIsEditable
            if editable == False: editflag = iflag & ~qtCore.Qt.ItemIsEditable
            if checkable == True: 
                elem.tableitem.setCheckState(qtCore.Qt.Unchecked)
            elem.tableitem.setFlags(editflag)
            elem.tableitem.setTextAlignment(qtCore.Qt.AlignRight)
            elem.tableitem.setText("0")
            elem.tablestditem.setFlags(elem.tablestditem.flags() & ~qtCore.Qt.ItemIsEditable)
            elem.tablestditem.setTextAlignment(qtCore.Qt.AlignRight)
            prmdict[prm] = elem
        

#**************************************************************************************
class VarSlider():
    def __init__(self):
        self.min = self.max = self.delta = float(0)
        self.destText = []

#**************************************************************************************
class FitCommon(QGroupBox):
    #fittedsignal = qtCore.pyqtSignal()
    def __init__(self, ScanmanMain):
        self.scanman = ScanmanMain
        self.config = self.scanman.config
        
        QGroupBox.__init__(self)
        self.ui = Ui_FitCommon()
        self.ui.setupUi(self)
        
        self.scanman = ScanmanMain
        
        self.rangeList = []
        self.prevrangeList = []
        self.colornr = 0
        self.colorlist = ['blue','green','cyan','magenta', 'brown']
        self.paramxy = {"Range_start":"x_chan","Range_end":"x_chan"}
        self.rangeparams = ["Range_start","Range_end"]
        self.fitparams = ['Chi^2','R^2','nIter','Time']
        self.iterparams = []
        self.miscparams = []
        self.axislinked = {}
        
        self.myslide = VarSlider()
        self.sliderLinkText = []
        
        self.linesperrange = 4
        
        self.range_tbl = mylib.Table(self.ui.range_tbl)
        
        #self.scanman.signal["xtypechanged"].connect(self.xTypeChanged)
        
        
    #**************************************************************************************   
    def xTypeChanged(self,axistype):
        #self.ui.range_tbl.verticalHeaderItem(2).setText(axistype)
        #oldtype = self.axislinked.values()[0]
        oldtype = list(self.axislinked.values())[0]
        if axistype == oldtype: return
        row = self.rownumbers[oldtype]
        self.rownumbers[axistype] = self.rownumbers.pop(oldtype)
        self.paramxy[axistype] = self.paramxy.pop(oldtype)
        self.axislinked[str(row)] = axistype
        self.iterparams.remove(oldtype)
        self.iterparams.insert(0, axistype)
        self.ui.range_tbl.verticalHeaderItem(row).setText(axistype)
        
        for rng in self.rangeList:
            rng.iterparams[axistype] = rng.iterparams.pop(oldtype)
            rng.iterparams[axistype].name = axistype
            
        True

            
    #**************************************************************************************
    #def Test(self):
    ##    iterparams = ["a","b"]
    #    additionalvalues = ["c","d"]
    #    fitparams  = self.fitparams
    #    self.SetVLables(iterparams, additionalvalues, fitparams)


    #**************************************************************************************
    def AddRange(self):
        self.xTypeChanged(self.scanman.axistype)    #Just make sure the table entry reflects what is chosen
        
        newrange = RangeDataCommon(self.colorlist[self.colornr])
        newrange.setparams(newrange.rangeparams, self.rangeparams, checkable = False, editable = True)
        newrange.setparams(newrange.iterparams, self.iterparams, checkable = True, editable = True)
        newrange.setparams(newrange.miscparams, self.miscparams, checkable = False, editable = False)
        newrange.setparams(newrange.fitparams, self.fitparams, checkable = False, editable = False)
        
        newrange.rangeparams["Range_start"].value = int(0)
        newrange.rangeparams["Range_end"].value = self.scanman.datasrc.nchan
        
        
        self.rangeList.append(newrange)
        self.colornr += 1
        if (self.colornr > len(self.colorlist)-1): self.colornr = 0
        rngnum = len(self.rangeList)-1
        self.ShowGraphlines(rngnum)
          
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
        
        newrange.allparams = {}
        for d in [newrange.rangeparams, newrange.iterparams, newrange.miscparams, newrange.fitparams]:
            newrange.allparams.update(d)
        for elemname in self.rownumbers.keys():
            rngtbl.setItem(self.rownumbers[elemname],nrcols,newrange.allparams[elemname].tableitem)
            rngtbl.setItem(self.rownumbers[elemname],nrcols+1,newrange.allparams[elemname].tablestditem)
             
        
        if(wedisconnected): rngtbl.cellChanged.connect(self.CellValueChanged)   #Reconnect the signal
        rngtbl.setCurrentCell(0,nrcols, qt.QItemSelectionModel.SelectCurrent) 
        rangenum=len(self.rangeList)       
        self.UpdateRangeData(rangenum-1)
        self.scanman.ui.graph.draw()
           
        True
        
    #**************************************************************************************
    def DelRange(self):
        rngtbl=self.ui.range_tbl
        selcol = rngtbl.currentColumn()
        rangenum = np.floor_divide(selcol,2)
        if rangenum <0: return

        if (selcol%2 == 0):
            rngtbl.removeColumn(selcol + 1)
            rngtbl.removeColumn(selcol)
        else:
            rngtbl.removeColumn(selcol)
            rngtbl.removeColumn(selcol - 1)
        headers = [["Val_"+str(i), "Stdev_" + str(i)] for i in range(np.floor_divide(rngtbl.columnCount(),2))]
        flatheader = [item for sublist in headers for item in sublist]
        rngtbl.setHorizontalHeaderLabels(flatheader)
        self.HideGraphlines(rangenum)
        del self.rangeList[rangenum]    

    
    #**************************************************************************************
    def HideGraphlines(self, rngnum = -1):
        start = rngnum
        end = rngnum +1
        if (rngnum == -1):
            start = 0
            end = len(self.rangeList)
        for rangenum in range(start, end): 
            del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #.lines[0] is the main data
            del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #all would have moved up, therefore the fitted line is now in this position 
            del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #background range (bgrngline) is now in this position 
            del self.scanman.ui.graph.figure.axes[0].lines[rangenum*self.linesperrange+1]        #background line is now in this position 
            del self.scanman.ui.diffgraph.figure.axes[0].lines[rangenum]        #the difference graph only has one line per range
        self.scanman.ui.graph.draw()
        self.scanman.ui.diffgraph.draw()
           
    def ShowGraphlines(self, rngnum = -1):
        start = rngnum
        end = rngnum +1
        if (rngnum == -1):
            start = 0
            end = len(self.rangeList)
        for rangenum in range(start, end): 
            self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[rangenum].line)
            self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[rangenum].fittedline)
            self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[rangenum].bgrngline)
            self.scanman.ui.graph.figure.axes[0].add_line(self.rangeList[rangenum].bgline)        
            self.scanman.ui.diffgraph.figure.axes[0].add_line(self.rangeList[rangenum].diffline)
        self.scanman.ui.graph.draw()
        self.scanman.ui.diffgraph.draw()                                                  
            
    #**************************************************************************************
    def SetVLables(self, rangeparams, iterparams, additionalvalues, fitparams):
        headers = rangeparams+iterparams+ additionalvalues+ fitparams
        self.rownumbers = {}
        for i in range(len(headers)):
            self.rownumbers[headers[i]] = i
        self.ui.range_tbl.setRowCount(len(headers))
        self.ui.range_tbl.setVerticalHeaderLabels(headers)
        self.ui.range_tbl.update()
        
        
    #**************************************************************************************
    def LinkSlider(self,xory,curitem, txtstr):
        curval = float(curitem.text())
        self.myslide.destText=curitem.setText
        self.myslide.getdestText=curitem.text
        self.ui.varval_label.setText("{0:.4f}".format(curval))
        self.ui.varname_label.setText(txtstr)
        if (xory == "x"):
            minval = float(self.scanman.datasrc.x_min)
            maxval = float(self.scanman.datasrc.x_max)
        elif(xory == "y"):
            minval = float(self.scanman.datasrc.y_min) 
            maxval = float(self.scanman.datasrc.y_max) 
        elif(xory == "del_y"):
            minval = float(0)
            maxval = abs(float(self.scanman.datasrc.y_max)-float(self.scanman.datasrc.y_min))
        elif(xory == "del_x"):  
            minval = float(0)
            maxval = abs(float(self.scanman.datasrc.x_max)-float(self.scanman.datasrc.x_min))
        elif(xory == "x_chan"):
            minval = float(0)
            maxval = float(self.scanman.datasrc.nchan)   
        else:
            minstr,maxstr = xory.split(" ")
            minval = float(minstr.split("=")[1])
            maxval = float(maxstr.split("=")[1])
        self.myslide.min = minval
        self.myslide.max = maxval
        
        dval = maxval - minval
        if dval == 0: dval = 1
        self.myslide.delta = dval/99
        self.ui.var_slider.setValue(int((curval - minval)/(dval)*99))
        #self.ui.var_slider.setValue(int((max([curval,self.myslide.min])-self.myslide.min)/self.myslide.delta*100))
        
    #**************************************************************************************
    def VarSliderValChanged(self,newval):
        value = newval*self.myslide.delta + self.myslide.min
        oldvalue = float(self.myslide.getdestText())
        if abs(value-oldvalue)/abs(self.myslide.max-self.myslide.min) > 0.1:
            self.myslide.destText("{0:.4f}".format(value))
        self.ui.varval_label.setText("{0:.4f}".format(value))
        self.FitRange()
        True
    
    def VarSliderReleased(self):
        value = self.ui.varval_label.text()
        self.myslide.destText(value)
                        
                               
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
        #minrng = rng.start
        #maxrng = rng.stop        
        minrng = rng.rangeparams["Range_start"].value
        maxrng = rng.rangeparams["Range_end"].value
        
        rngtbl.item(0, valcol).setText(str(minrng))
        rngtbl.item(1, valcol).setText(str(maxrng))
        self.scanman.ui.minSlider.setValue(minrng)
        self.scanman.ui.maxSlider.setValue(maxrng)
        
        if (wedisconnected): rngtbl.cellChanged.connect(self.CellValueChanged)   #Reconnect the signal

        currow = rngtbl.currentRow()
        curitem = rngtbl.item(currow,curcol)
        curitemname = rngtbl.verticalHeaderItem(currow).text()
        #if curitem.checkState() == qtCore.Qt.Unchecked: return
        if curitemname not in self.iterparams or (curcol%2.0 !=0.0): return
        
        wedisconnected = False
        try:
            self.ui.var_slider.valueChanged.disconnect()     #otherwise this function might be called recursively
            wedisconnected = True
        except:
            a=1
        
        varname = rngtbl.verticalHeaderItem(currow).text() + "_" + str(rangenum)
        txtstr = "<font color='" + rng.color+ "'>" +varname+"</font>"   
        
        
        if self.paramxy[curitemname] != "": self.LinkSlider(self.paramxy[curitemname], curitem, txtstr)
        if (wedisconnected): self.ui.var_slider.valueChanged.connect(self.VarSliderValChanged)   #Reconnect the signal
        self.ui.var_slider.valueChanged.connect(self.VarSliderValChanged)   #Reconnect the signal

    
    #**************************************************************************************
    def CellValueChanged(self,row,col):
        rngtbl=self.ui.range_tbl
        varname = rngtbl.verticalHeaderItem(row).text()
        if (varname not in (self.iterparams+self.rangeparams)) or (float(col)%2 != 0): return #skip cells not editable
        
        rangenum = np.floor_divide(col,2)
        valcol = (rangenum)*2
        if (rangenum < 0): return
        rng=self.rangeList[rangenum]
        tableitem = rngtbl.item(row, col)
        
        if varname in self.iterparams:
            if ((tableitem.checkState() == qtCore.Qt.Checked) and (rng.iterparams[varname].fix == False)):
                rng.iterparams[varname].fix = True
            elif ((tableitem.checkState() == qtCore.Qt.Unchecked) and (rng.iterparams[varname].fix == True)):
                rng.iterparams[varname].fix = False
            else:
                rng.iterparams[varname].value = float(tableitem.text())
            True


        wedisconnected = False
        try:
            rngtbl.cellChanged.disconnect()     #otherwise this function might be called recursively
            wedisconnected = True
        except:
            True
            
            
        if varname in self.rangeparams:
            self.UpdateRangeData(rangenum)
            if (varname == "Range_start"): self.scanman.ui.minSlider.setValue(self.rangeList[rangenum].rangeparams[varname].value)
            if (varname == "Range_end"): self.scanman.ui.maxSlider.setValue(self.rangeList[rangenum].rangeparams[varname].value)

        if(wedisconnected): rngtbl.cellChanged.connect(self.CellValueChanged)   #Reconnect the signal

        self.UpdateRangeData(rangenum)
        self.FitRange(rangenum)
        self.scanman.ui.graph.draw()
        #if (row == self.position_row): self.AdjustCheckSate(row,valcol,rangenum,"position")
        
            
                
    #**************************************************************************************
    def NewTableValue(self,rangenum, prop, value):
        rngtbl=self.ui.range_tbl
        valcol = (rangenum)*2
        valrow = self.rownumbers[prop]
        rngtbl.item(valrow, valcol).setText(value)
        True
        
    #**************************************************************************************
    def ReflectInTable(self,params,value_fmt="", stdev_fmt=""):
        rngtbl=self.ui.range_tbl
        paramnames = params.keys()
        if value_fmt=="": value_fmt = {prm:"{0:.4f}" for prm in paramnames}
        #if stdev_fmt=="": stdev_fmt = {prm:"{0:.3e}" for prm in paramnames}
        if stdev_fmt=="": stdev_fmt = {prm:"{}" for prm in paramnames}
        
        wedisconnected = False
        try:
            rngtbl.cellChanged.disconnect()     #otherwise this function might be called recursively
            wedisconnected = True
        except:
            True
        
        for item in params:
            params[item].tableitem.setForeground(qt.QBrush(qt.QColor('Black' if params[item].valid else 'Red')))
            params[item].tableitem.setText(value_fmt[item].format(params[item].value))
            params[item].tablestditem.setForeground(qt.QBrush(qt.QColor('Black')))
            params[item].tablestditem.setText(stdev_fmt[item].format(params[item].stdev))
            iflag = params[item].tableitem.flags()
            enableflag = iflag | qtCore.Qt.ItemIsEnabled
            if params[item].enabled == False: 
                enableflag = iflag & ~qtCore.Qt.ItemIsEnabled
                params[item].tableitem.setForeground(qt.QBrush(qt.QColor('Grey')))
                params[item].tablestditem.setForeground(qt.QBrush(qt.QColor('Grey')))
            params[item].tableitem.setFlags(enableflag)

            
                                    
            True
        if (wedisconnected): rngtbl.cellChanged.connect(self.CellValueChanged)   #Reconnect the signal
        True
    
    
    #**************************************************************************************
    def asignfitparamvalues(self,params,fitob):
        params["R^2"].value = fitob.r2
        params["Time"].value = fitob._lastRunTime
        params["nIter"].value = fitob._niter
        params["Chi^2"].value = fitob.chi2
        
    #**************************************************************************************
    def UpdateFitRange(self,rangenum):
        rngtbl=self.ui.range_tbl
        valcol = (rangenum)*2
        strt = int(rngtbl.item(0, valcol).text())
        stp = int(rngtbl.item(1, valcol).text())
        self.rangeList[rangenum].rangeparams["Range_start"]=strt
        self.rangeList[rangenum].rangeparams["Range_end"]=stp
         

    #**************************************************************************************
    def UpdateRangeData(self, rngnum=-1):
        start = rngnum
        end = rngnum +1
        if (rngnum == -1):
            start = 0
            end = len(self.rangeList)
        for i in range(start, end): 
            rng = self.rangeList[i]
            start = rng.rangeparams["Range_start"].value
            stop = rng.rangeparams["Range_end"].value
            rng.line.set_data(self.scanman.datasrc.x[start:stop], self.scanman.datasrc.y[start:stop])
        
    #**************************************************************************************

        