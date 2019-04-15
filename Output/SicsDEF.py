'''
Created on 08 May 2014

@author: Deon
'''
from PyQt4.QtGui import QGroupBox as QGroupBox
#from GenPeaksGUI import Ui_GenPeaks
from Output.SicsGUI import Ui_Sics
import PyQt4.QtGui as qt
#from pylab import np
import sys
import PyQt4.QtCore as qtCore
#from PyQt4.QtGui import *
from PyQt4.QtNetwork import QTcpServer, QHostAddress
import numpy as np
#from time import gmtime, strftime
import datetime
import time
import mylib


SIZEOF_UINT32 = 4

class DeviceParams(object):
    def __init__(self):
        self.state = 'S'    #idle = 'I'; Stopped ='S'; Running = 'R'; Paused = 'P'
        self.terminal_due = ' '     #? 'T' : ' '
        self.range_error = ' '     #? ' ' : 'R'
        self.range_gated = ' '     #? 'G' : ' '
        self.timestamp = datetime.datetime.now()
        self.accumulated_time = float(0)
        self.counter_value = float(0)
        self.count_delta = float(0)
        self.counter_rate = float(0)
        self.time_delta = float(0)
        self.average_rate = float(0)
        
class CmpItem(object):
    #def __init__(self, name = '', row=0, req=float(0), cur=float(0)):
    def __init__(self, name = '', default=0.0, row=0, greaterorless = "less"):
        self.row = row
        self.cur = 0.0
        self.req = default
        self.percent = float(0)
        self.colour = 'black'
        if greaterorless =="greater":  self.ineq = np.greater_equal
        elif greaterorless == "less":  self.ineq = np.less
        self.name = name
        self.tblitem_cur = qt.QTableWidgetItem()
        self.tblitem_cur.setFlags(self.tblitem_cur.flags()  & ~qtCore.Qt.ItemIsEditable)
        self.tblitem_cur.setTextAlignment(qtCore.Qt.AlignRight)
        self.tblitem_cur.setForeground(qt.QBrush(qt.QColor("red")))
        self.tblitem_cur.setText("0")
        self.tblitem_req = qt.QTableWidgetItem()
        self.tblitem_req.setText(str(self.req))
        self.tblitem_req.setTextAlignment(qtCore.Qt.AlignRight)
        self.tblitem_header = qt.QTableWidgetItem()
        self.tblitem_header.setText(self.name)
        
        
        
    def Compare(self,curval):
        self.cur = abs(curval)
        if self.ineq(curval,self.req):      #not done
            self.colour = 'black'
        else:
            self.colour = 'red'
            
        if self.ineq == np.greater_equal:
            self.percent = self.cur/self.req*100.0 if self.req != 0 else 0.0
        else:
            self.percent = self.req/self.cur*100.0 if self.cur != 0 else 0.0
        
        self.tblitem_cur.setForeground(qt.QBrush(qt.QColor(self.colour)))
        self.tblitem_cur.setText('{0:.5f}'.format(self.cur))
            
        True
            
    

#**************************************************************************************
#**************************************************************************************
class SicsDEF(QGroupBox):
    def __init__(self, ScanmanMain=""):
        QGroupBox.__init__(self)
        self.name = "Sics"
        self.ui = Ui_Sics()
        self.ui.setupUi(self)
        self.scanman = ScanmanMain
        self.ui.inbuffer_Edit.setText("Hello\n")
        self.prm = DeviceParams()
        
        self.cmplist = []
        self.cmplist.append(CmpItem("inten2bgnd",0))
        self.cmplist.append(CmpItem("inten",1))
        self.cmplist.append(CmpItem("rho_inten",2))
        self.cmplist.append(CmpItem("rho_pos",3))
        self.cmplist.append(CmpItem("rho_fwhm",4))
        self.cmplist.append(CmpItem("rho_bgnd",5))
        
        self.compareprms = {}
        self.compareprms["inten2bgnd"]=CmpItem("Minimum Intensity to Background", 2.0, 0, "greater")
        self.compareprms["inten"]=CmpItem("Minimum Intensity", 20.0, 1, "greater")
        self.compareprms["rho_inten"]=CmpItem("Maximum %Rel StDev Intensity", 2.0, 2, "less")
        self.compareprms["rho_pos"]=CmpItem("Maximum %Rel StDev Position", 2.0, 3, "less")
        self.compareprms["rho_fwhm"]=CmpItem("Maximum %Rel StDev FWHM", 2.0, 4, "less")
        self.compareprms["rho_bgnd"]=CmpItem("Maximum %Rel StDev Background", 2.0, 5, "less")
        self.compareprms["err_ustrain"]=CmpItem("Maximum error in u-strain", 50.0, 6, "less")
        
        
        
        self.reqcol = 0
        self.curcol = 1
        self.prevevents = float(0)
        self.prevstatus = ""
        self.worstpercent = float(0)

        cmptbl = self.ui.compare_tbl
        #for i in range(cmptbl.rowCount()):
        #    someitem = qt.QTableWidgetItem()
        #    someitem.setFlags(someitem.flags()  & ~qtCore.Qt.ItemIsEditable)
        #    someitem.setTextAlignment(qtCore.Qt.AlignRight)
        #    someitem.setText("0")
        #    cmptbl.setItem(i,self.curcol,someitem)
        
        cmptbl.setRowCount(len(self.compareprms))
        cmptbl.setColumnCount(2)
        #for item in self.compareprms.itervalues():    CDM itervalues depricated
        for item in self.compareprms.values():
            cmptbl.setItem(item.row, self.curcol, item.tblitem_cur)
            cmptbl.setItem(item.row, self.reqcol, item.tblitem_req)
            cmptbl.setVerticalHeaderItem(item.row, item.tblitem_header)

            True
        True
        
        self.compare_tbl = mylib.Table(self.ui.compare_tbl)
        
        
    #**************************************************************************************
    def ClearValues(self):
        self.prm.counter_value = float(0)
        self.prm.counter_rate  = float(0)
        self.prm.accumulated_time = float(0)
        self.prm.time_delta = float(0)
        self.worstpercent = float(0)
        #for item in self.cmplist:
        #    item.percent = float(0)
        #    item.cur = float(0)
        for item in self.compareprms.itervalues():
            item.percent = float(0)
            item.cur = float(0)
          
              
    #**************************************************************************************
    def UpdateValues(self):
        #paramdict = copy.deepcopy(self.scanman.ui.sourceGroupBox.paramdict)
        paramdict = self.scanman.ui.sourceGroupBox.paramdict
        try:
            status = paramdict["DAQ_Status"]
        except:
            return False
        if status == "Started":
            if self.prevstatus != "Started":
                self.ClearValues()
                #self.prevstatus = status
                #return True
                
            #self.prevevents = float(paramdict["events"])
            curtime = datetime.datetime.now()
            delta = curtime - self.prm.timestamp
            self.prm.time_delta = delta.total_seconds()
            self.prm.accumulated_time+=delta.total_seconds()
            self.prm.timestamp = curtime
            
            self.prm.count_delta = float(1.0)
            
        
            #if paramdict.has_key("COUNT_METHOD"):
            if "COUNT_METHOD" in paramdict.keys():
                if paramdict["COUNT_METHOD"][:-2]=="MONITOR" and self.worstpercent >= 100.0:         #Required precision reached
                        self.prm.counter_value = float(paramdict["COUNT_SIZE"])                     #So stop count by setting time as the preset time
                else: 
                    self.prm.counter_value = float(paramdict["time"])
            else: 
                self.prm.counter_value = self.prm.accumulated_time
            
            self.prm.counter_rate = self.worstpercent
            
            if (self.prm.accumulated_time !=0):
                self.average_rate =self.prm.counter_value/self.prm.accumulated_time
             
            self.prevstatus = status
            return True
        
        elif (status == "Stopped" or status == 'Paused'):
            self.ClearValues()
            self.prevstatus = status
            return False
        
    
    #**************************************************************************************
    def GetCurrent(self):
        if "DAQ_Status" in self.scanman.ui.sourceGroupBox.paramdict:        #This is data comming in from Histogram Server
            if(self.UpdateValues() == False): return
        cmptbl = self.ui.compare_tbl

        rngList = self.scanman.ui.fitGroupBox.rangeList
        rng = rngList[0]
        if (rng.intensity == 0  or rng.fwhm == 0):
            #self.ClearValues()
            self.ui.worstprm_label.setText("N/A")
            self.ui.worstval_edit.setText("%.4f" %(self.worstpercent))
            return 
        
        for item in self.compareprms.itervalues():
            item.req = float(cmptbl.item(item.row, self.reqcol).text())
        
        self.compareprms["inten2bgnd"].Compare(rng.intensity / rng.background)
        self.compareprms["inten"].Compare(rng.intensity)
        self.compareprms["rho_inten"].Compare(rng.intensity_stdev / rng.intensity * 100)
        self.compareprms["rho_pos"].Compare(rng.position_stdev / rng.position * 100)
        self.compareprms["rho_fwhm"].Compare(rng.fwhm_stdev / rng.fwhm * 100)
        self.compareprms["rho_bgnd"].Compare(rng.background_stdev / rng.background * 100)
        self.compareprms["err_ustrain"].Compare(rng.errustrain)
        
        itemkey = "inten2bgnd"
        self.worstpercent = self.compareprms[itemkey].percent
        worstitem = itemkey
        #for itemkey in self.compareprms.iterkeys():
        for itemkey in self.compareprms.keys():
            item=self.compareprms[itemkey]
            if item.percent < self.worstpercent:
                self.worstpercent = item.percent
                worstitem = itemkey
        if self.worstpercent < 0: self.worstpercent = float(0)
        self.ui.worstprm_label.setText(worstitem)
        self.ui.worstval_edit.setText("%.4f" %(self.worstpercent))
            
        True
       
    #**************************************************************************************
    def Device_print(self):
        outstring = "Time: %s, Count: %10d, Delta: %6d, Time: %8.6f, Rate: %8.2f, Ave: %8.2f\r\n" % (str(self.prm.timestamp.time()),
                                                                                                       self.prm.counter_value,
                                                                                                       self.prm.count_delta,
                                                                                                       self.prm.time_delta,
                                                                                                       self.prm.counter_rate,
                                                                                                       self.prm.average_rate)
        return outstring
        
    #**************************************************************************************
    def Device_read(self):
        outstring = "READ %c%c%c%c %s %.6f %10d %8.2f\r\n" % (self.prm.state,
                                                                self.prm.terminal_due,
                                                                self.prm.range_error,
                                                                self.prm.range_gated,
                                                                str(self.prm.timestamp.time()),
                                                                self.prm.accumulated_time,
                                                                self.prm.counter_value,
                                                                self.prm.counter_rate)
        paramdict = self.scanman.ui.sourceGroupBox.paramdict
        if self.prm.counter_value >= float(paramdict["COUNT_SIZE"]) and paramdict["COUNT_METHOD"].find("MONITOR") > -1: #Only do a quick clear when performing a scan with the monitor.
            self.prm.counter_value = float(0)
            self.worstpercent = float(0)
            True
        return outstring
    
    #**************************************************************************************

    def ReadFromServer(self):
        True
    #**************************************************************************************
    def StartServer(self):
        self.host = "localhost"
        self.port = int(self.ui.port_Edit.text())
        self.ui.inbuffer_Edit.append("ServerStart on port:" + str(self.port))
        
        self.timestamp  = datetime.datetime.now()
        self.tcpServer = QTcpServer(self)               
        self.tcpServer.listen(QHostAddress(self.host), self.port)
        curtime = datetime.datetime.now()
        delta = curtime - self.timestamp
        self.time_delta = delta.total_seconds()
        
        self.scanman.ui.fitGroupBox.fittedsignal.connect(self.GetCurrent)
        
        self.connections = []
        self.connect(self.tcpServer, qtCore.SIGNAL("newConnection()"), self.addConnection)
        self.ui.status_Edit.setText("On")

        
        
        True

    #**************************************************************************************
    def addConnection(self):
        try:
            clientConnection = self.tcpServer.nextPendingConnection()
            clientConnection.nextBlockSize = 0
            self.connections.append(clientConnection)
    
            self.connect(clientConnection, qtCore.SIGNAL("readyRead()"), self.receiveMessage)
            self.connect(clientConnection, qtCore.SIGNAL("disconnected()"), self.removeConnection)
            self.connect(clientConnection, qtCore.SIGNAL("error()"), self.socketError)
        except:
            self.ui.inbuffer_Edit.append("Failed to add connection")
            True
    #**************************************************************************************
    def receiveMessage(self):
        try:
            s = self.sender()
            reply = ""
            #self.disconnect(s, qtCore.SIGNAL("readyRead()"), self.receiveMessage)       #Histogram server polls very quickly, rather let a request be completed before starting another one
            if s.bytesAvailable() > 0:
                textFromClient = s.readAll()
                textFromClient = textFromClient.toLower()
                #outstring = "%s - %s:%d -> %s" % (datetime.datetime.now().time(), s.peerAddress().toString(), s.peerPort(), textFromClient)
                #self.ui.inbuffer_Edit.append(outstring)
                
                if textFromClient.contains("pause"):
                    self.prm.state='P'
                    reply = "OK\r\n"
                elif textFromClient.contains("continue"):
                    self.prm.state='R'
                    reply = "OK\r\n"
                elif textFromClient.contains("resume"):
                    self.prm.state='R'
                    reply = "OK\r\n"
                elif textFromClient.contains("start"):
                    self.prm.state='R'
                    reply = "OK\r\n"
                elif textFromClient.contains("stop"):
                    self.prm.state='S'
                    #self.ClearValues()
                    reply = "OK\r\n"
                elif textFromClient.contains("read"):
                    time.sleep(0.0001)
                    reply = self.Device_read()
                elif textFromClient.contains("test"):
                    True
                else: 
                    reply = self.Device_print()
                self.sendMessage(reply, s.socketDescriptor())
                
            #self.connect(s, qtCore.SIGNAL("readyRead()"), self.receiveMessage)
        except:
            self.ui.inbuffer_Edit.append("Failed read message and send response")
            True
            

    #**************************************************************************************
    def sendMessage(self, text, socketId):
        try:
            for s in self.connections:
                if s.socketDescriptor() == socketId:
                    s.write(text)              
        except:
            self.ui.inbuffer_Edit.append("Failed send response")
            True  

    #**************************************************************************************
    def removeConnection(self):
        s=self.sender()
        self.connections.remove(s)
        True

    #**************************************************************************************
    def socketError(self):
        self.ui.inbuffer_Edit.append("Socket Error...\n")
        True
    
    
    #**************************************************************************************
    def StopServer(self):
        for i in range(len(self.connections)):
            self.connections[0].close() #Once removed, all will shift forward in the array
        self.tcpServer.close()
        self.scanman.ui.fitGroupBox.fittedsignal.disconnect(self.GetCurrent)
        self.ui.status_Edit.setText("Off")


        
    def DoIt(self,astr=""):
        self.ui.inbuffer_Edit.setText(astr)

   
  
   
       

if __name__ == '__main__':
    
    app = qt.QApplication(sys.argv)
    window=SicsDEF()
    window.show()
    sys.exit(app.exec_())

        