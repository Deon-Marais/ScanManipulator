'''
Created on 17 Jul 2014

@author: Deon
'''

from Source import Srcpar
import numpy as np
from mylib import ProgressBar

def FullprofCompat_xy_read(fname,config):
    src = Srcpar.Srcpar(config)
    #src.dataset.pop()       #Remove the {0,0} dataset
    paramdictcmn = {}
    paramdict = {}
    detdict = {}
    
    f = open(fname, 'r')
    filecontent = f.read()
    f.close()
    scanStartIdx = 0
    datasections = filecontent[scanStartIdx:-1].split("\n\n")
    numruns = len(datasections)    
    progress = ProgressBar("Loading Fullprof compatible xy datasets...", numruns)
    #progress.setinfo(fname)
    for section in datasections:
        progress.setinfo(fname)
        #paramdict = paramdictcmn.copy()
        
        sectionsplitlines = section.split("\n")
        
        params = sectionsplitlines[3].split("| ")
        params.pop(0)
        detdict = {params[s].split(":")[0]:float(params[s].split(":")[1]) for s in range(len(params))}
        
        params = sectionsplitlines[4].split("| ")
        params.pop(0)   #This is the empty one, should improve the exporting so that this isnt needed
        paramdict = {params[s].split(":")[0]:params[s].split(":")[1] for s in range(len(params))}
        if "stth" not in paramdict:
            paramdict["stth"]=str(detdict["stth"])
        True
            
        #Get the intensity data
        #y = np.array([])
        #tth = np.array([])
        axisheader = sectionsplitlines[5].split(" ")
        if axisheader[0] == "Channel" : axistype = "ch"
        elif axisheader[0] == "Position" : axistype = "mm"
        elif axisheader[0] == "Angle" : axistype = "2th"
        elif axisheader[0] == "d-spacing" : axistype = "d"
        
        datalines = sectionsplitlines[6:]
        nrpoints = len(datalines)
        y = np.array([0.0]*nrpoints)
        x = np.array([0.0]*nrpoints)
        
        #for aline in sectionsplitlines[6:]:
        
        for i in range(len(datalines)):
            #x, intensity = aline.split()
            #y = np.append(y, float(intensity))
            #mm = np.append(tth, float(x))
            xstr, intensity = datalines[i].split()
            y[i] = float(intensity)
            x[i] = float(xstr)
        
        src.AddData(y,paramdict, detdict, "FullprofCompat_xy", fname, {axistype:x})
        if progress.wasCanceled(): break
        progress.step()
    
    return src
    
        