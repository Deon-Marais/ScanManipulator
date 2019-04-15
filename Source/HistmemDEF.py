from PyQt4.QtGui import QGroupBox as QGroupBox
from PyQt4 import QtCore
from Source.HistmemGUI import Ui_Histmem
import numpy as np
from Source import Srcpar
import os.path
import urllib
import copy
import time
import struct

import mylib

from Source.SourceCommon import SourceCommon

class HistmemDEF(QGroupBox,SourceCommon):
    def __init__(self, ScanmanMain):
        QGroupBox.__init__(self)
        SourceCommon.__init__(self, ScanmanMain)
        
        self.name="Histmem"
        self.ui = Ui_Histmem()
        self.ui.setupUi(self)
        self.scanman = ScanmanMain
        #self.src = Srcpar.Srcpar()
        #self.detdict = {}
        #self.paramdict = {}
        if "histmem" in self.scanman.config["source"]:
            self.ui.servername_edit.setText(self.scanman.config["source"]["histmem"]["IP"])
            if "flipxy" in self.scanman.config["source"]["histmem"]:
                self.flipxy = bool(self.scanman.config["source"]["histmem"]["flipxy"])
            else:
                self.flipxy = False
        
        
        
        
        self.paramdict["DAQ_Status"] = ""
        
        self.password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        #self.serveraddr = 'http://10.0.1.21/admin/'
        #self.password_mgr.add_password(None, self.serveraddr, 'manager','necsa')
        #pwd_handler = urllib2.HTTPBasicAuthHandler(self.password_mgr)
        #proxy_support = urllib2.ProxyHandler({})
        #self.opener = urllib2.build_opener(pwd_handler,proxy_support)
        self.x_mm = self.y_mm = np.array([0.0])
        self.ServerChanged()
        self.autotimer = mylib.RepeatedTimer()
        self.autotimer.updateSignal.connect(self.ReadServer)
        #self.autotimer = mylib.RepeatedTimer(100, self.ReadServer)
        
        #self.autotimer.start()
        #self.mythread=QtCore.QThread()
        True
        

        
    #**************************************************************************************
    def ServerChanged(self):
        self.serveraddr = str(self.ui.servername_edit.text()) + "/admin/"
        self.password_mgr.passwd.clear()
        self.password_mgr.add_password(None, self.serveraddr, 'manager','necsa')
        pwd_handler = urllib.request.HTTPBasicAuthHandler(self.password_mgr)
        proxy_support = urllib.request.ProxyHandler({})
        self.opener = urllib.request.build_opener(pwd_handler,proxy_support)
        
        self.detdict["det_ymin"] = self.scanman.config["source"]["detector"]["det_ymin"]
        self.detdict["det_ymax"] = self.scanman.config["source"]["detector"]["det_ymax"]
        try:
            response = self.opener.open(self.serveraddr+'readconfig.egi', timeout=2)
            histstatus = response.read()
            response.close()
            
            idx1 = histstatus.find("<X>")+19
            idx2 = histstatus.find("</X>",idx1)
            xaxis = histstatus[idx1 : idx2].split()
            self.nrx = len(xaxis)-1
            #self.detdict["det_xmin"] = float(xaxis[0])
            #self.detdict["det_xmax"] = float(xaxis[-1])
            idx1 = histstatus.find("<Y>",idx2)+19
            idx2 = histstatus.find("</Y>",idx1)
            yaxis = histstatus[idx1 : idx2].split()
            self.nry = len(yaxis)-1
            #self.detdict["det_ymin"] = float(yaxis[0])
            #self.detdict["det_ymax"] = float(yaxis[-1])

            #if self.flipxy == True:
            #    newnrx = self.nry
            #    newnry = self.nrx
            #    self.nry = newnry
            #    self.nrx = newnrx
        except:
            True
        True
        
        
        
        
    #**************************************************************************************
    def ReadServer(self):
        tic=time.time()
        wasrunning = False
        try:
            src = Srcpar.Srcpar(self.config)
            
            #wasrunning = self.autotimer.is_running
            #if wasrunning: self.autotimer.stop()
            #if wasrunning: self.autotimer.halt()
            
            self.detdict["sam_to_det"] = float(self.scanman.ui.sam2det_edit.text())
            self.detdict["stth"] = float(self.scanman.ui.stth_edit.text())
            self.detdict["lambda"] = float(self.scanman.ui.wavelength_edit.text())
            self.detdict["det_xmin"] = float(self.scanman.ui.detDim_xmin_edit.text())
            self.detdict["det_xmax"] = float(self.scanman.ui.detDim_xmax_edit.text())
           
            #--------------------------------
            response = self.opener.open(self.serveraddr+'textstatus.egi')
            histstatus = response.read()
            response.close()

            idx1 = histstatus.find("HM-Host") + 9
            idx2 = histstatus.find('\n',idx1)
            self.paramdict["HM-Host"] = histstatus[idx1 : idx2]
    
            idx1 = histstatus.find("DAE_type",idx2) + 10
            idx2 = histstatus.find('\n',idx1)
            self.paramdict["DAE_type"] = histstatus[idx1 : idx2]
            
            idx1 = histstatus.find("DAQ:",idx2) + 5
            idx2 = histstatus.find('\n',idx1)
            self.paramdict["DAQ_Status"] = histstatus[idx1 : idx2]                
            
            idx1 = histstatus.find("DAQ_dirname",idx2) + 13
            idx2 = histstatus.find('\n',idx1)
            self.paramdict["DAQ_dirname"] = histstatus[idx1 : idx2]
            fname = self.paramdict["DAQ_dirname"]
            
            idx1 = histstatus.find("acq_dataset_active_sec",idx2) + 24
            idx2 = histstatus.find('\n',idx1)
            self.paramdict["time"] = histstatus[idx1 : idx2]
            
            idx1 = histstatus.find("num_events_to_hfp",idx2) + 18
            idx2 = histstatus.find('\n',idx1)
            self.paramdict["events"] = histstatus[idx1 : idx2]
            
                #-------------------------------- 
            response = self.opener.open(self.serveraddr+'readconfig.egi', timeout=2)
            histstatus = response.read()
            response.close()
            
            idx1 = histstatus.find("COUNT_METHOD") + 14
            idx2 = histstatus.find('"',idx1)
            self.paramdict["COUNT_METHOD"] = histstatus[idx1 : idx2]
            idx1 = histstatus.find("COUNT_SIZE") + 12
            idx2 = histstatus.find('"',idx1)
            self.paramdict["COUNT_SIZE"] = histstatus[idx1 : idx2]
            #print "Time is %f" % (time.time()-tic)
                        
            #-------------------------------- 1D data read       
            #r1 = self.opener.open(self.serveraddr+'readdataselectdatatype.egi?read_data_type=TOTAL_HISTOGRAM_X&read_data_format=CSV')
            #response = self.opener.open(self.serveraddr+'readdataselected.egi?read_data_uncal_cal=CALIBRATED&read_data_order_flip_x=DISABLE&read_data_order_flip_y=DISABLE&read_data_order_transpose_xy=DISABLE&start=&end=')
            #dataparsed = response.read().split(',')
            #self.src.Clear()
            #y = np.array([float(dataparsed[i]) for i in range(len(dataparsed))])
            #self.src.x_chan = np.arange(0, len(dataparsed), 1)
            #self.src.nchan = len(self.src.x_chan)
            #self.src.AddData(y,self.paramdict, self.detdict, "ANSTO Histmem", fname)
            
            #-----------------------------------2D data read
            #r1 = self.opener.open(self.serveraddr+'readdataselectdatatype.egi?read_data_type=TOTAL_HISTOGRAM_XY&read_data_format=CSV')
            #response = self.opener.open(self.serveraddr+'readdataselected.egi?read_data_uncal_cal=CALIBRATED&read_data_order_flip_x=DISABLE&read_data_order_flip_y=DISABLE&read_data_order_transpose_xy=DISABLE&start=&end=')
            nrvals=self.nrx*self.nry
            response = self.opener.open(self.serveraddr+'readhmdata.egi?bank=1&start=0&end='+str(nrvals)+'&read_data_period_number=0&read_data_type=HISTOPERIOD_XYT')
            textdata = response.read()
            response.close()
            
            data = struct.unpack(str(nrvals)+'i',textdata)
            n = np.asarray(data,dtype=float).reshape((self.nrx,self.nry))
            if self.flipxy:
                n=n.transpose()
            #tic=time.time()
            #dataparsed = textdata.split('\n')
            #n = []
            #for yline in dataparsed[:-2]:
            #    n.append(yline.split(","))
            #n=np.asarray(n,dtype=float)
            #print "Time is %f" % (time.time()-tic)
            src.AddData(n,self.paramdict, self.detdict, "ANSTO Histmem 2D", fname, twod = True)
            src.crmap = copy.deepcopy(self.src.crmap) #Use the previous geometry correction map if it exists. Saves a lot of time
            self.src=src
            self.srcp = Srcpar.Srcpar(self.config)     #Source post process
            self.srcsplit = Srcpar.Srcpar(self.config)     #Source with detector splitted
            
            #tic=time.time()
            self.src.CalcAllAxis()
            self.src.x_chan = self.src.dataset[-1].x_chan
            self.src.nchan = len(self.src.x_chan)
            self.src.CalcSumSetCommon("")
            self.src.CalcSumSet(["raw"])
            self.src.SelectFrame("raw")
            self.src.SelectDataSet(-1)
            
        
            self.scanman.datasrc = self.src         #We have to do this because the linking is broken when assigning different file's datasets
            
            if self.src.data2D == False:
                self.srcsplit = self.src
            
            self.scanman.Generate()
            #print "Time is %f" % (time.time()-tic)
            QtCore.QCoreApplication.instance().processEvents()      #This, together with stopping and starting the timer again seems to keep the program from crashing in Qt4lib.dll
            
        except:
            True
        #if wasrunning: self.autotimer.start()
        #if wasrunning: self.autotimer.begin(2.0)
    
    #**************************************************************************************
    def ARSelected(self,checked):
        try:
            if (checked == True):
                time = float(self.ui.autoreadtime_edit.text())
                self.autotimer.interval = time
                self.autotimer.begin()
                if self.autotimer.isRunning() == False:
                    self.autotimer.start()
                True
            else:
                self.autotimer.halt()
        except:
            True
            
        #try:
        #    if (checked == True):
        #        time = float(self.ui.autoreadtime_edit.text())
        #        self.autotimer.interval = float(self.ui.autoreadtime_edit.text())
        #        #self.autotimer = mylib.RepeatedTimer(time, self.ReadServer())
        #        self.autotimer.start()
        #        
        #    else:
        #        self.autotimer.stop()
        #except:
        #    True
            
        
    
