'''
Created on 17 Jul 2014

@author: Deon
'''

from Source import Srcpar
from thirdparty.pyparsing import *
import numpy as np
import time

def Gumtree_xyd_read(fname,config):
    src = Srcpar.Srcpar(config)
    #src.dataset.pop()       #Remove the {0,0} dataset
    paramdictcmn = {}
    paramdict = {}
    detdictcmn = {}
    detdict = {}
    
    f = open(fname, 'r')
    filecontent = f.read()
    f.close()
    
    line1end = filecontent.find("\n")
    paramdictcmn['Nexus file'] = filecontent[19:line1end]
    scanStartIdx = filecontent.find("# Scan variable")
    cmnContent = filecontent[line1end +1: scanStartIdx]
    cmnContentLines = cmnContent.split("\n")
    for aline in cmnContentLines:
        tabsplit = aline[2:].split("\t")
        for itemstr in tabsplit:
            eqsplit = itemstr.split("=")
            if len(eqsplit) > 1:
                paramdictcmn[eqsplit[0]] = eqsplit[1]
            True 
        True
    True
    sampletodetector = paramdictcmn.pop("Processed with: calculating two theta on LDS")
    paramdictcmn["cor_to_det"] = sampletodetector
    detdictcmn["det_xmin"] =  float(paramdictcmn["active_width"][:-3]) /(-2.0)
    detdictcmn["det_xmax"] =  float(paramdictcmn["active_width"][:-3]) /(2.0)
    detdictcmn["sam_to_det"] = float(paramdictcmn["cor_to_det"][:-3])
    detdictcmn["stth"] = float(paramdictcmn["stth"][:-7])       #-7 removes the 'degrees'
    detdictcmn["lambda"] = 1.659       #Only valid for MPISI, should do this more cleverly later on
    
    datasections = filecontent[scanStartIdx:-1].split("\n\n")
    for section in datasections:
        paramdict = paramdictcmn.copy()
        detdict = detdictcmn.copy()
        
        #Get the Scan variable
        prmnamestart = section.find(":") + 2
        lnend = section.find("\n")
        eqsplit = section[prmnamestart:lnend].split("=")
        paramdict[eqsplit[0]] = eqsplit[1].strip()
        if eqsplit[0] == "stth":    detdict["stth"] = float(eqsplit[1].strip())
        
        #Get the time and counts line
        varstart = lnend+3  #skip the newline, hash and space
        lnend = section[varstart:].find("\n") + varstart
        splitted = section[varstart:lnend].split(" ")
        for itemstr in splitted:
            eqsplit = itemstr.split("=")
            if len(eqsplit) > 1:
                paramdict[eqsplit[0]] = eqsplit[1].strip()
        
        #Get the intensity data
        datastart = lnend + 57 # Skip the Header line
        y = np.array([])
        tth = np.array([])
        for aline in section[datastart:-1].split("\n"):
            twotheta, intensity, sigma = aline.split()
            y = np.append(y, float(intensity))
            tth = np.append(tth, float(twotheta))
        
        src.AddData(y,paramdict, detdict, "Gumtree_xyd", fname, {"2th":tth})
    return src
    
        