'''
Created on 17 Jul 2014

@author: Deon
'''

from Source import Srcpar
import numpy as np

def AsciiTwoColumn_txt_read(fname,config):
    validaxistypes = ['Channel','Position','Angle','d-spacing','d','2th','ch','mm']
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
    for section in datasections:
        paramdict = paramdictcmn.copy()
        
        #Get the intensity data
        y = np.array([])
        xaxis = np.array([])
        splittedsections = section.split("\n")
        axis, type = splittedsections[0].split()
        try:
            a=float(axis)
            axistype = "mm"
            paramdict["Type"] = "n"
        except:
            axistype = axis
            if axis not in validaxistypes:
                axistype = "Position"
                paramdict["position"]=axis
            
            paramdict["Type"] = type
            splittedsections=splittedsections[1:]
        for aline in splittedsections:
            x, intensity = aline.split()
            y = np.append(y, float(intensity))
            xaxis = np.append(xaxis, float(x))
        ind = np.lexsort([xaxis])   #sorted indexes
        
        src.AddData(y[ind],paramdict, detdict, "ASCII_2column", fname, {axistype:xaxis[ind]})
        src.ylabel=paramdict["Type"]
    return src
    
        