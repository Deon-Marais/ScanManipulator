'''
Created on 01 Jul 2014

@author: Deon
'''

from threading import Timer
import PyQt4.QtGui as qt
from PyQt4 import QtCore
from matplotlib.lines import Line2D
import matplotlib as mpl
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
#import StringIO
#import cStringIO
from io import StringIO #cdm: cStringIO no longer exists in 3.7 - from cStringIO import StringIO
import win32clipboard
import win32file
import os
import numpy as np
import copy
import time
#CDM NoneType removed frm Python3 - from types import NoneType
import subprocess
import ctypes
from ctypes import *
import sys

import random

import numpy as np

# Used to get clustered data points
# Taken from: https://datasciencelab.wordpress.com/2013/12/12/clustering-with-k-means-in-python/
def cluster_points(X, mu):
    clusters  = {}
    for x in X:
        bestmukey = min([(i[0], np.linalg.norm(x-mu[i[0]])) \
                    for i in enumerate(mu)], key=lambda t:t[1])[0]
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
    return clusters
 
def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis = 0))
    return newmu
 
def has_converged(mu, oldmu):
    return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))
 
def find_centers(X, K):
    # Initialize to K random centers
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, oldmu):
        oldmu = mu
        # Assign all points in X to clusters
        clusters = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
    return(mu, clusters)



#****************************************************************************************************************************
#****************************************************************************************************************************
def Getexportsettings(mydef):
    class DataSetSelection:
        def __init__(self,mydef):
            if mydef.ui.allfiles_check.isChecked():
                self.flistidx = range(len(mydef.scanman.ui.sourceGroupBox.filelist))
            else:
                self.flistidx = [mydef.scanman.ui.sourceGroupBox.ui.file_tbl.currentRow()]
                
            if mydef.ui.all_radio.isChecked():
                self.setstart = 1
                self.setend = len(mydef.scanman.datasrc.dataset)
                #self.flistidx = range(len(mydef.scanman.ui.sourceGroupBox.filelist))
            #else:
            #    self.flistidx = [mydef.scanman.ui.sourceGroupBox.ui.file_tbl.currentRow()]
            elif mydef.ui.current_radio.isChecked():
                self.setstart = mydef.scanman.datasrc.currset
                self.setend = self.setstart+1
                #self.flistidx = [mydef.scanman.ui.sourceGroupBox.ui.file_tbl.currentRow()]
            elif mydef.ui.range_radio.isChecked():
                self.setstart = mydef.ui.rangemin_spin.value()
                self.setend = mydef.ui.rangemax_spin.value() + 1
            self.numfiles = len(self.flistidx)
            
    return(DataSetSelection(mydef))    





#****************************************************************************************************************************
#****************************************************************************************************************************

#class RepeatedTimer(object):
class RepeatedTimer(QtCore.QThread):
    updateSignal = QtCore.pyqtSignal(int)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.runme = False
        self.interval   = 2.0
        
    #def __init__(self, interval, function, *args, **kwargs):
        #self.timer     = None
    #    self.interval   = interval
    #    self.function   = function
    #    self.args       = args
    #    self.kwargs     = kwargs
    #    self.is_running = False
    #    self.runme = False
        
        
        #self.timer = Timer(self.interval, self.run)
        #self.timer.start()

    def run(self):
        True
        self.runme = True
        while True:
            if self.runme == True:
                self.updateSignal.emit(self.interval)
                time.sleep(self.interval)
            else:
                time.sleep(0.2)
        #else:
        #    time.sleep(0.1)
        #    True
        #try:
        #    self.is_running = False
        #    self.start()
        #    self.function(*self.args, **self.kwargs)
        #except:
        #    True

    #def start(self, interval=2):
    def begin(self):
        self.runme = True
        #try:
        #    if not self.is_running:
        #        self.timer = Timer(self.interval, self.run)
        #        self.timer.start()
        #        self.is_running = True
        #except:
        #    True

    def halt(self):
        self.runme = False

        
    #def stop(self):
    #    self.runme = False
        #try:
        #    if self.timer != None:
        #        self.timer.cancel()
        #        self.is_running = False
        #except:
        #    True
            
#progress2 = mylib.ProgressDiaglog(Title, nrsteps, info)
        #progress2.step(info)
        
#**************************************************************
#**************************************************************
def getprettyduration(seconds):
    if seconds / 3600 > 1.0:
        prettyduration = "%.0fh %.0fmin" %(seconds / 3600, (seconds % 3600)/3600*60)
    elif seconds / 60.0 > 1.0:
        prettyduration = "%.0fmin %.0fsec" %(seconds / 60, seconds % 60)
    else:
        prettyduration = "%.1fsec" %(seconds)
    return prettyduration


#****************************************************************************************************************************
def ErrMessage(msg):
    bx = qt.QMessageBox()
    bx.setIcon(qt.QMessageBox.Critical)
    bx.setText(msg)
    bx.setWindowTitle("Error")
    bx.setInformativeText(str(sys.exc_info()[1]))
    bx.exec_()
    
    True

#****************************************************************************************************************************
class ProgressBar():
    def __init__(self,title, nrofsteps,info=""):
        self.inittime = time.time()
        self.endtime = time.time()
        self.timeln = ""
        self.stepnr = 1
        self.nrofsteps=nrofsteps
        self.progress=qt.QProgressDialog()
        self.progress = qt.QProgressDialog()
        self.progress.setWindowTitle(title)
        self.info = info
        self.setinfo(self.info)
        self.currvalue = 0
        self.progress.setValue(self.currvalue)   
        self.progress.show()
        QtCore.QCoreApplication.instance().processEvents() 
        self.increment = 100.0/float(nrofsteps)

        
        
    def step(self,info=""):
        self.endtime = time.time()
        totrunningtime = self.endtime - self.inittime
        deltatime = totrunningtime/self.stepnr
        predictedtottime = self.nrofsteps * deltatime
        remainingtime = predictedtottime - totrunningtime
        remainingstr = getprettyduration(remainingtime)
        predictedtottimestr = getprettyduration(predictedtottime)
        estendstr = time.ctime(time.time() + remainingtime)
        
        if info != "": self.progress.setLabelText(info)
        self.currvalue = self.currvalue+self.increment
        self.stepnr = self.stepnr + 1
        stepsln = "%i of %i" %(self.stepnr,self.nrofsteps)
        self.timeln = remainingstr + " remaining of " + predictedtottimestr + "\n" + estendstr + "\n"
        self.progress.setLabelText("%s\n%s\n%s" %(stepsln,self.timeln,self.info))
        self.progress.setValue(int(self.currvalue))
        QtCore.QCoreApplication.instance().processEvents()
    
    def setinfo(self,info=""):
        if info !="": self.info = info
        stepsln = "%i of %i\n" %(self.stepnr,self.nrofsteps)
        self.progress.setLabelText("%s\n%s\n%s" %(stepsln,self.timeln,self.info))
        #self.progress.setLabelText("%i of %i\n%s" %(self.stepnr,self.nrofsteps,self.info))
        
    def wasCanceled(self):
        return self.progress.wasCanceled()
    
    def close(self):
        self.progress.close()

#**************************************************************
import pythoncom
from pywin32_testutil import str2bytes
import struct
import win32clipboard as cb
from win32api import FormatMessage as FormatMessage
#from win32api import GetLastError as GetLastError
class DROPFILES(ctypes.Structure):
    _fields_ = (('pFiles', wintypes.DWORD),
                ('pt',     wintypes.POINT),
                ('fNC',    wintypes.BOOL),
                ('fWide',  wintypes.BOOL))

def set_clipboard_file(content):
    offset = ctypes.sizeof(DROPFILES)
    file_list = [content]
    length = sum(len(p) + 1 for p in file_list) + 1
    size = offset + length * ctypes.sizeof(ctypes.c_wchar)
    buf = (ctypes.c_char * size)()
    df = DROPFILES.from_buffer(buf)
    df.pFiles, df.fWide = offset, True
    for path in file_list:
        #path = path.decode('gbk')
        #print "copying to clipboard, filename = " + path
        array_t = ctypes.c_wchar * (len(path) + 1)
        path_buf = array_t.from_buffer(buf, offset)
        path_buf.value = path
        offset += ctypes.sizeof(path_buf)
    stg = pythoncom.STGMEDIUM()
    stg.set(pythoncom.TYMED_HGLOBAL, buf)
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    try:
        win32clipboard.SetClipboardData(win32clipboard.CF_HDROP, stg.data)
        #print "clip_files() succeed"
    finally:
        win32clipboard.CloseClipboard()
    
    

#**************************************************************

def set_clipboard_file_old(content):
    ret_stg = pythoncom.STGMEDIUM()
    fname_buf=str2bytes(content)

    fname_ba=bytearray(fname_buf)
    fname_ba.append('\0')
    fname_ba.append('\0')
    fmt="lllll%ss" %len(fname_ba)
    df=struct.pack(fmt, 20, 0, 0, 0, 0, str(fname_ba))
    ret_stg.set(pythoncom.TYMED_HGLOBAL, df)
    try:
        cb.OpenClipboard()
        cb.EmptyClipboard()
    except:
        print ("open failed, exception=%s"%FormatMessage(GetLastError()))
    else: 
        try:
            cb.SetClipboardData(cb.CF_HDROP, ret_stg.data)
        except:
            print ("set failed, exception = %s"%FormatMessage(GetLastError()))
        finally:
            cb.CloseClipboard()

def set_clipboard_text(content):
        try:
            cb.OpenClipboard()
            cb.EmptyClipboard()
        except:
            print ("open failed, exception=%s"%FormatMessage(GetLastError()))
        else: 
            try:
                cb.SetClipboardText(content, cb.CF_UNICODETEXT)
            except:
                print ("set failed, exception = %s"%FormatMessage(GetLastError()))
            finally:
                cb.CloseClipboard()

def get_clipboard_text():
    data = ""
    try:
        cb.OpenClipboard()
        data = cb.GetClipboardData()
        cb.CloseClipboard()
        data = data[:data.find("\0")]
    except:
        print ("failed to get clipboard data, exception=%s"%FormatMessage(GetLastError()))
    return data

def set_clipboard_image(filepath):
    im = qt.QImage(filepath)
    qt.QApplication.clipboard().setImage(im)
    #clip.setImage(im)
    
    

    True
        


#**************************************************************
class Table(qt.QTableWidget):
    def __init__(self,mplwidget):
        super(Table,self).__init__()
        self.table = mplwidget
        self.superkeyPressEvent = copy.copy(self.table.keyPressEvent)
        self.table.keyPressEvent=self.keyPressEvent    #hijack the event
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.contextMenuRequested)
        self.clip = qt.QApplication.clipboard()
        True
        
    def contextMenuRequested(self,point):
        menu = qt.QMenu()
        cpyTXT = menu.addAction("Copy TXT")
        cpyTXT.triggered.connect(self.copyTXT)
        menu.exec_(self.table.mapToGlobal(point))
        
    def keyPressEvent(self, event):
            if event.matches(qt.QKeySequence.Copy):
                self.copyTXT()
            else:
                self.superkeyPressEvent(event)
        
    def copyTXT(self):
        try:
            selected = self.table.selectedRanges()
            #s = '\t'+"\t".join([str(self.table.horizontalHeaderItem(i).text()) for i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1)])
            s = '\t'+"\t".join([str(self.table.horizontalHeaderItem(i).text()) for i in range(selected[0].leftColumn(), selected[0].rightColumn()+1)])
            s = s + '\n'
            vertheader = True
            #for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
            for r in range(selected[0].topRow(), selected[0].bottomRow()+1):
                try:
                    s += self.table.verticalHeaderItem(r).text() + '\t'
                except:
                    vertheader = False
                    #s += str(r+1) + '\t'
                #for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                for c in range(selected[0].leftColumn(), selected[0].rightColumn()+1):
                    try:
                        s += str(self.table.item(r,c).text()) + "\t"
                    except AttributeError:
                        s += "\t"
                s = s[:-1] + "\n" #eliminate last '\t'
            if vertheader == False:
                s = s[1:]     #eliminate the first '\t'
            self.clip.setText(s)
            True
        except:
            True    
            
        
    True
 

#****************************************************************************************************************************
#****************************************************************************************************************************
class Graph():

    def __init__(self,mplwidget):
        self.graph = mplwidget
        self.graph.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.graph.customContextMenuRequested.connect(self.contextMenuRequested)
        self.toolbar = NavigationToolbar(self.graph.figure.canvas,self.graph)
        self.toolbar.zoom()
        self.toolbar.setMaximumSize(25, 40)
        self.graph.mpl_connect('motion_notify_event',self.mousemove)
        self.ptslabel = qt.QLabel()
        self.annotation = self.graph.axes.annotate("", xy=(0,0), xycoords='data',xytext=(0, 5),
                                                   textcoords='offset points',bbox=dict(boxstyle="round", facecolor="w", edgecolor="0.5", alpha=0.9))
        self.annotation.set_visible(True)
    
    def tighten(self):
        self.graph.tight_layout()
        
    def mousemove(self,event):
        self.annotation.set_visible(False)
        if type(event.inaxes)==type(None):#CDM: NoneType removed from Python 3 - typNoneType:
            self.annotation.set_visible(False)
            self.graph.draw()
            return
            True
        self.annotation.set_text("%.3g , %.3g"%(event.xdata, event.ydata))
        self.annotation.xy=(event.xdata, event.ydata)
        xmid=(event.inaxes.viewLim.xmax-event.inaxes.viewLim.xmin)/2.0+event.inaxes.viewLim.xmin
        if event.xdata > xmid: self.annotation.set_horizontalalignment("right")
        else:
            self.annotation.set_horizontalalignment("left")
        self.annotation.set_visible(True)
        self.graph.draw()
                                 
        True
        
    def contextMenuRequested(self,point):
        self.annotation.set_visible(False)
        self.graph.draw()
        menu = qt.QMenu()
        cpyTXT = menu.addAction("Copy TXT")
        cpyBMP = menu.addAction("Copy BMP")
        cpyPNG = menu.addAction("Copy PNG")
        cpyEMF = menu.addAction("Copy EMF")
        cpySVG = menu.addAction("Copy SVG")
        cpyTXT.triggered.connect(self.copyTXT)
        cpyBMP.triggered.connect(self.copyBMP)
        cpyPNG.triggered.connect(self.copyPNG)
        cpyEMF.triggered.connect(self.copyEMF)
        cpySVG.triggered.connect(self.copySVG)
        menu.exec_(self.graph.mapToGlobal(point))
    
    def get1Dgraphs(self):
        maxlen = 0
        for axis in self.graph.figure.axes:
            for aline in axis.lines:
                linelen = len(aline.get_xdata(True))
                if linelen > maxlen: maxlen = linelen
        axisarr = np.empty((maxlen,0))
        header = ""
        for axis in self.graph.figure.axes:
            title = axis.get_title()
            if title == "":
                ytitle = axis.get_ylabel() 
                xtitle = axis.get_xlabel()
            else:
                ytitle, xtitle = title.split(" vs. ")
            lines = axis.get_lines()
            arr = np.empty((maxlen,0))
            for aline in lines:
                xy = copy.copy(aline.get_xydata())
                if len(xy)>1:
                    xysh =  np.shape(xy)
                    xy.resize((maxlen,2),refcheck=False)
                    if maxlen != xysh[0]:
                        xy[xysh[0]:] = [[np.nan,np.nan]]*(maxlen-xysh[0])
                    header = header + xtitle + "\t" + ytitle + "\t"
                    arr = np.append(arr,xy,1)
            axisarr = np.append(axisarr,arr,1)
        return axisarr, header
    
    def get2Dgraphs(self):
        #cmap=mpl.cm.binary
        #self.colorbar2d.set_cmap(cmap)
        im = self.graph.figure.axes[0].get_images()[0]
        dataarr = im.get_array()
        ax = np.reshape(im._Ax,(1,np.shape(dataarr)[1]))
        x = np.append(ax, dataarr,0)
        y = np.reshape([np.append(np.nan,im._Ay)], (np.shape(x)[0],1))
        data = np.append(y,x,1)
        return data
        True
        
          
    
    def copyTXT(self):
        try:
            test=self.graph.figure.axes[0].get_images()[0].get_array()
            twod=True
            axisarr = self.get2Dgraphs()
            header = ""
        except:
            twod = False
            axisarr, header = self.get1Dgraphs()
            header = header[:-1]+"\n"
        
        npar = np.array(axisarr)
        s = StringIO()
        np.savetxt(s,npar, fmt="%e", delimiter="\t")
        csv=s.getvalue().replace("nan","")
        set_clipboard_text(header + csv[:-1])
    
    def copyBMP(self):
        pixmap = qt.QPixmap.grabWidget(self.graph.figure.canvas)
        qt.QApplication.clipboard().setPixmap(pixmap)
        True
    
    def copyPNG(self, fpath=os.path.abspath("clipboard")):
        #fpath=os.path.abspath("clipboard")
        if fpath==False: fpath=os.path.abspath("clipboard")
        self.graph.figure.set_frameon(False)
        self.graph.figure.savefig(fpath,format="png", dpi=300, transparent=True)
        self.graph.figure.set_frameon(True)
        self.graph.figure.canvas.draw()         #Needed after the 'savefig' command else the center og the graph is the same as the background colour
        set_clipboard_file(fpath)
        True

    def copySVG(self):
        fpath=os.path.abspath("clipboard")
        self.graph.figure.set_frameon(False)
        self.graph.figure.savefig(fpath,format="svg", transparent=True)
        self.graph.figure.set_frameon(True)
        self.graph.figure.canvas.draw()         #Needed after the 'savefig' command else the center og the graph is the same as the background colour
        set_clipboard_file(fpath)
        True
        
    def copyEMF(self):
        fpath=os.path.abspath("clipboard.svg")
        self.graph.figure.set_frameon(False)
        self.graph.figure.savefig(fpath,format="svg", transparent=True)
        self.graph.figure.set_frameon(True)
        self.graph.figure.canvas.draw()         #Needed after the 'savefig' command else the center og the graph is the same as the background colour
        #set_clipboard_file(fpath)
        opath=os.path.abspath("clipboard")
        exeln = 'inkscape -z --file "' + fpath + '" --export-emf "' + opath + '"'
        os.system(exeln)
        set_clipboard_file(opath)
        os.remove(fpath)
        
    def test(self):
        #import MayaviEmbed
        True
        

        
    def addit(self):
        True


