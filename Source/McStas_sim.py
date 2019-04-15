'''
Created on 20 Jan 2015

@author: Deon
'''

from Source import Srcpar
import numpy as np
from mylib import ProgressBar
import re
from thirdparty.pyparsing import *
from PyQt4.QtGui import QFileDialog
import os.path

#import time

class McStasReader():
    def __init__(self):
        self.name="McStas"
        self.filedialog = QFileDialog()
        self.filedialog.setFileMode(QFileDialog.ExistingFiles)
        
        
    def ReadFile(self,fname):
        f = open(fname, 'r')
        filecontent = f.read()
        f.close()
        
        paramdict = {}
        params = {}
        detdict = {}
        detdictcmn = {}
    
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
        paramdict = {paramsparsed[i][0]:paramsparsed[i][1] for i in range(len(paramsparsed))}
        

                        
        #Get the detector xmin and xmax
        xlimitsStartIdx = filecontent.find("# xlimits:", paramEndIdx)
        if xlimitsStartIdx >0   :       #Found it, this is 1d data
            xlableStartIdx = filecontent.find("xlabel:", paramEndIdx)
            leftbracketStartIdx = filecontent.find("[", xlableStartIdx)
            rightbracketStartIdx = filecontent.find("]", leftbracketStartIdx)
            xscalestr = filecontent[leftbracketStartIdx+1:rightbracketStartIdx]
            xscale = 1.0
            if xscalestr == "cm": xscale = 10.0
            elif xscalestr == "m": xscale = 1000.0
            elif xscalestr == "AA": xscale = 1000.0 #ughly hack - This is wavelenth data is Angstrom. Very little variation in values makes ScanMan crash for some reason. Remedy is to scale the values
            
            xlimitsEndIdx = filecontent.find("#", xlimitsStartIdx+1)
            xlimitsDef = filecontent[xlimitsStartIdx:xlimitsEndIdx]
            xlimexpr = CaselessLiteral("# xlimits:").suppress() + Word(validch) + Word(validch)
            xlimparsed = xlimexpr.parseString(xlimitsDef)
        
            dataEndIdx = filecontent.rfind("\n#")
            lasthashIdx = filecontent.rfind("\n#",0,dataEndIdx)
            dataStartIdx = filecontent.find("\n",lasthashIdx+1)+1
            dataDef = filecontent[dataStartIdx:dataEndIdx]
            dataparsed=[n.split() for n in dataDef.split("\n")]
            if "cor_to_det" in paramdict :           #NDIFF instruments
                detdict["det_xmin"] = float(xlimparsed[0])*xscale
                detdict["det_xmax"] = float(xlimparsed[1])*xscale
                detdict["sam_to_det"] = float(paramdict["cor_to_det"])*1000
                detdict["stth"] = float(paramdict["det_takeoff"])
                if "source_lam_mean" in paramdict:
                    detdict["lambda"] = float(paramdict["source_lam_mean"])
                else:
                    detdict["lambda"] = (float(paramdict["source_lam_min"]) + float(paramdict["source_lam_max"]))/2.0 
                datatype = "McStas_Constant_wavelength"
                x = np.array([float(dataparsed[i][0])*xscale for i in range(len(dataparsed))])
            else:                                   #EnginX TOF
                detdict["det_xmin"] = float(xlimparsed[0])
                detdict["det_xmax"] = float(xlimparsed[1])
                detdict["sam_to_det"] = 1000.0
                detdict["stth"] = 90.0
                detdict["lambda"] = 1.6
                datatype = "McStas_TOF"
                x = np.array([float(dataparsed[i][0]) for i in range(len(dataparsed))])
            
            y = np.array([float(dataparsed[i][3]) for i in range(len(dataparsed))])
            self.src.x_chan = np.arange(0, len(dataparsed), 1)
            self.src.nchan = len(self.src.x_chan)
            self.src.AddData(y,paramdict, detdict, datatype, fname, {"mm":x})
        
        
        
        
        
        else:           #This is 2d data
            twodim = True
            xlableStartIdx = filecontent.find("xlabel:", paramEndIdx)
            leftbracketStartIdx = filecontent.find("[", xlableStartIdx)
            rightbracketStartIdx = filecontent.find("]", leftbracketStartIdx)
            xscalestr = filecontent[leftbracketStartIdx+1:rightbracketStartIdx]
            leftbracketStartIdx = filecontent.find("[", rightbracketStartIdx)
            rightbracketStartIdx = filecontent.find("]", leftbracketStartIdx)
            yscalestr = filecontent[leftbracketStartIdx+1:rightbracketStartIdx]
            
            xylimitsStartIdx = filecontent.find("# xylimits:", paramEndIdx)
            xylimitsEndIdx = filecontent.find("#", xylimitsStartIdx+1)
            detlimits = filecontent[xylimitsStartIdx:xylimitsEndIdx].split()
            
            xscale = 1.0
            if xscalestr == "cm": xscale = 10.0
            elif xscalestr == "m": xscale = 100.0
            yscale = 1.0
            if yscalestr == "cm": yscale = 10.0
            elif yscalestr == "m": yscale = 100.0
            
            
            detdict["det_xmin"] = float(detlimits[2])*xscale
            detdict["det_xmax"] = float(detlimits[3])*xscale
            detdict["det_ymin"] = float(detlimits[4])*yscale
            detdict["det_ymax"] = float(detlimits[5])*yscale
            
            #dataEndIdx = filecontent.rfind("\n#")
            #lasthashIdx = filecontent.rfind("\n#",0,dataEndIdx)
            #dataStartIdx = filecontent.find("\n",lasthashIdx+1)+1
            #eventsStartIdx = filecontent.find("# Events")
            eventsStartIdx = filecontent.find("# Data")
            dataStartIdx = filecontent.find("\n",eventsStartIdx)+1
            dataEndIdx = filecontent.find("\n#",dataStartIdx)
            #dataStartIdx = filecontent.find("# Events",lasthashIdx+1)+1
            dataDef = filecontent[dataStartIdx:dataEndIdx]
            dataparsed=[n.split() for n in dataDef.split("\n")]
            if "cor_to_det" in paramdict:           #NDIFF instruments
                #detdict["det_xmin"] = float(xlimparsed[0])*1000
                #detdict["det_xmax"] = float(xlimparsed[1])*1000
                detdict["sam_to_det"] = float(paramdict["cor_to_det"])*1000
                detdict["stth"] = float(paramdict["det_takeoff"])
                if "source_lam_mean" in paramdict:
                    detdict["lambda"] = float(paramdict["source_lam_mean"])
                else:
                    detdict["lambda"] = (float(paramdict["source_lam_min"]) + float(paramdict["source_lam_max"]))/2.0 
                datatype = "McStas_Constant_wavelength"
                #x = np.array([float(dataparsed[i][0])*1000 for i in range(len(dataparsed))])
                x = np.linspace(detdict["det_xmin"], detdict["det_xmax"], len(dataparsed[0]))
                True
            else:                                   #EnginX TOF
                True
                #detdict["det_xmin"] = float(xlimparsed[0])
                #detdict["det_xmax"] = float(xlimparsed[1])
                #detdict["sam_to_det"] = 1000.0
                #detdict["stth"] = 90.0
                #detdict["lambda"] = 1.6
                #datatype = "McStas_TOF"
                #x = np.array([float(dataparsed[i][0]) for i in range(len(dataparsed))])
            
            #y = np.array([float(dataparsed[i][3]) for i in range(len(dataparsed))])
            y = np.array(dataparsed).astype(float)
            self.src.x_chan = np.arange(0, len(dataparsed[0]), 1)
            self.src.nchan = len(self.src.x_chan)
            #self.src.AddData(y,paramdict, detdict, datatype, fname, axis = {"mm":x}, twod=twodim)
            self.src.AddData(y,paramdict, detdict, datatype, fname, twod=twodim)
            
               
        #Get the actual data
        #dataStartIdx = filecontent.find("# Data ", paramEndIdx)
        #if dataStartIdx !=-1:                                 #Normal McSats output
        #    dataStartIdx = filecontent.find(":", dataStartIdx)
        #    dataStartIdx = dataStartIdx + 1
        #    dataEndIdx = filecontent.find("# EndDate",dataStartIdx)
        #    detdict["det_xmin"] = float(xlimparsed[0])*1000
        #    detdict["det_xmax"] = float(xlimparsed[1])*1000
        #    detdict["sam_to_det"] = float(paramdict["cor_to_det"])*1000
        #    detdict["stth"] = float(paramdict["det_takeoff"])
        #    detdict["lambda"] = (float(paramdict["source_lam_min"]) + float(paramdict["source_lam_max"]))/2.0 
        #    dataDef = filecontent[dataStartIdx:dataEndIdx]
        #    dataparsed=[n.split() for n in dataDef.split("\n")]
        #    y = np.array([float(dataparsed[i][3]) for i in range(len(dataparsed))])
        #    self.src.x_chan = np.arange(0, len(dataparsed), 1)
        #    self.src.nchan = len(self.src.x_chan)
        #    self.src.AddData(y,paramdict, detdict, "McStas", fname)
        #    
        #else:                       #Used for EnginX time of flight detector
        #    variablesStartIdx = filecontent.find("# variables", paramEndIdx)
        #    variablesStartIdx = filecontent.find(":", variablesStartIdx)
        #    variablesStartIdx = variablesStartIdx + 1
        #    variablesEndIdx = filecontent.find("\n", variablesStartIdx)
        #    variablesDef = filecontent[variablesStartIdx:variablesEndIdx].split()
        #    dataStartIdx=variablesEndIdx+1
        #    dataEndIdx = -1
        #    dataDef = filecontent[dataStartIdx:dataEndIdx]
        #    dataparsed=[n.split() for n in dataDef.split("\n")]
        #    x = np.array([float(dataparsed[i][0]) for i in range(len(dataparsed))])
        #    y = np.array([float(dataparsed[i][3]) for i in range(len(dataparsed))])
        #    self.src.x_chan = np.arange(0, len(dataparsed), 1)
        #    self.src.nchan = len(self.src.x_chan)
        #    self.src.AddData(y,paramdict, detdict, "McStas_TOF", fname, {"mm":x})
        #    True
        
        
    
        #dataDef = filecontent[dataStartIdx:dataEndIdx]
        #x = intensity = intensity_err = ncount = Word(validch)
        #dataexpr = ZeroOrMore(Group(x + intensity + intensity_err + ncount))
        #dataparsed = dataexpr.parseString(dataDef)
        
        
        #self.scanman.Generate()     #Will subsequently call our GetData
        #self.GetData()
        #y = np.array([float(dataparsed[i][3]) for i in range(len(dataparsed))])
        #self.src.x_chan = np.arange(0, len(dataparsed), 1)
        #self.src.nchan = len(self.src.x_chan)
        #self.src.AddData(y,paramdict, detdict, "McStas", fname)
        

    #**************************************************************************************
    def ReadPSFile(self,fname):
        f = open(fname, 'r')
        lastdir = os.path.dirname(str(fname))
        
        filecontent = f.read()
        f.close()
        
        #Get a list of the directories
        dirStartIdx = filecontent.find("--dir=")
        #detfile = os.path.basename(str(self.ui.filename_edit.text()))
        
        dirEndIdx = filecontent.find('"',dirStartIdx+7)
        simdir1 = filecontent[dirStartIdx+7:dirEndIdx]
        if "/" in simdir1: sep = "/"
        elif "\\" in simdir1: sep ="\\"
        if os.path.exists(simdir1) == False:
            simdir1 = os.path.dirname(fname) + sep + simdir1.split(sep)[-1]
            
        self.filedialog.setDirectory(simdir1) 
        
        file_types = "MCstas (*.sim *.dat);; All (*.*)"
        detfilelong = self.filedialog.getOpenFileNames(None, 'Select detector file', '', file_types)
        self.filedialog.setDirectory(lastdir)
        if (detfilelong==[]): return
        
        fnames=[]
        detfile = os.path.basename(detfilelong[0])
        while dirStartIdx > -1 :
            dirStartIdx = dirStartIdx + 7
            dirEndIdx = filecontent.find('"',dirStartIdx)
            detpath = filecontent[dirStartIdx:dirEndIdx] + sep + detfile
            if os.path.exists(detpath) == False:
                detpath = os.path.dirname(fname) + sep + detpath.split(sep)[-2] + sep + detfile
            fnames.append(detpath)
            dirStartIdx = filecontent.find("--dir=",dirEndIdx)
        
        numfiles = len(fnames)
        progress = ProgressBar("Opening McStas PS files...", numfiles)
        for afile in fnames:
            progress.setinfo(afile)
            if (os.path.exists(afile)):
                self.ReadFile(afile)
            if progress.wasCanceled(): break
            progress.step()


#**************************************************************************************
#**************************************************************************************
def McStas_sim_read(fname, config, paramstudy=False):
    
    mcStasob = McStasReader()
    mcStasob.src = Srcpar.Srcpar(config)
    if paramstudy==False:
        mcStasob.ReadFile(fname)
    else:
        mcStasob.ReadPSFile(fname)
    return mcStasob.src
    True
    
        