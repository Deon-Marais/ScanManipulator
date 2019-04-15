'''
Created on 17 Jul 2014

@author: Deon
'''

from Source import Srcpar
import numpy as np
from copy import copy

def ScanmanPeakFit_pkf_read(fname,config):
    
    from Source import ScanmanPeakFit_pkfDEF
    pkfsourcegui = ScanmanPeakFit_pkfDEF.ScanmanPeakFit_pkfDEF()
    #pkfsourcegui.activateWindow()


    src = Srcpar.Srcpar(config)
    paramdictcmn = {}
    params = {}
    paramdict = {}
    detdict = {}
    
    #prec = 0.1             #parameter precision
    #prec = 0.0
    fixnegative = False
    fixmassive = float(2.0)
    
    f = open(fname, 'r')
    filecontent = f.read()
    f.close()
    scanStartIdx = 0
    lines = filecontent[scanStartIdx:-1].split("\n")
    header = lines[0].split("\t")
    i = 0
    ich = []
    for head in header:
        #if "Channel" in head:
        if "Channel_range" in head:
            ich.append(i)
        i=i+1
    ich.append(len(header))
    varpar = {}
    for i in range(1,ich[0]):
        varpar[header[i]] = i
        True
    
    
    pkfsourcegui.setparoptions(varpar)
    pkfsourcegui.setpeakoptions([str(i) for i in range(len(ich)-1)])
        
    #selectedpeaks = [0,1,2]
    #selectedpar = ["sample_x","sample_y","sample_z"]
    #selectedpar = ["sx","sy","sz"]
    #selectedpar = ["vsx","vsy","sz"]
    
    fitparams = {}
    secwidth = ich[1] - ich[0]
    for i in range(ich[0]+1,ich[1]):
        fitparamcol = []
        head = header[i][:header[i].rfind("_")]
        for j in range(len(ich)-1):
            fitparamcol.append(i + secwidth*j)
        fitparams[head] = copy(fitparamcol)
    
    pkfsourcegui.setdataoptions(fitparams.keys())

    if 1:
        result = pkfsourcegui.exec_()     
        if pkfsourcegui.selectedfit == "": return   
        selectedpar = pkfsourcegui.selectedparams
        selectedpeaks = pkfsourcegui.selectedpeaks
        selectedfit = pkfsourcegui.selectedfit  #"Counts"
        src.ylabel = selectedfit
        prec = pkfsourcegui.precision
        permutate = pkfsourcegui.permutate
    
    if 0:       #For testing
        selectedpar = ['sx', 'sz']
        selectedpeaks = [0]
        selectedfit = "Intensity"
        src.ylabel = "Intensity"
        prec = 0.6
        permutate = False
 
    permupar = []
    for parpri in selectedpar:
        perln = [parpri]
        for parsec in selectedpar:
            if parsec != parpri:
                perln.append(parsec) 
        permupar.append(perln)
    if permutate == False:
        permupar = [permupar[0]]   
         
    data = []
    for aline in lines[1:]:
        splitted = aline.split("\t")
        temp = []
        for aval in splitted:
            try:
                temp.append(float(aval))
            except:
                temp.append(aval)
        
        data.append(temp)
        True
    data=np.array(data)
    datat=data.transpose()
    nrdatalns  = len(data)
    
    for parstr in permupar:
        sortedprms = np.array([[0.0]*(1+len(parstr))])
        for i in range(0, len(data)):
            #dset = srcp.dataset[i]
            #expanded = np.array([np.append([[i]], [float(dset.prm[st]) for st in setparams])])
            expanded = np.array([np.append([[i]], [float(datat[varpar[st]][i]) for st in parstr])])
            #expanded = np.array([np.append([[i]], [float(data[varpar[st]][i]) for st in parstr])])
            sortedprms = np.append(sortedprms, expanded,axis=0)
            True
        sortedprms = sortedprms[1:].transpose()
        precparams = []
        #for prm in setparams:  precparams = precparams + [srcp.precparams[prm]]
        #precparams = [0.4,0.4]
        precparams = [prec]*len(parstr)
        
        src.finalblock = np.zeros((len(sortedprms),1))
        src.getsubblock(sortedprms,0,precparams)
       
        sortedidx = [int(a) for a in src.finalblock[0][1:]]
        sorteddata = data[sortedidx]
        
        for pknum in selectedpeaks:
            dataln = 0
            mm = np.array([])
            y = np.array([])
            y_err = np.array([])
            paramdict = {}
            while dataln < nrdatalns:
                for ipar in range(0,len(parstr)-1): paramdict[parstr[ipar]] = str(sorteddata[dataln][varpar[parstr[ipar]]])
                yval = float(sorteddata[dataln][fitparams[selectedfit][pknum]])
                if yval < 0 and fixnegative: yval = 0
                y = np.append(y, yval)
                try:
                    yval_err = float(sorteddata[dataln][fitparams["StDev_"+selectedfit][pknum]])
                    y_err = np.append(y_err, yval_err)
                except: True
                mm = np.append(mm, float(sorteddata[dataln][varpar[parstr[-1]]]))
                dataln = dataln+1
                if len(parstr) == 1: #all values will be given in a single dataset
                    for i in range(nrdatalns-1):
                        yval = float(sorteddata[dataln][fitparams[selectedfit][pknum]])
                        if yval < 0 and fixnegative: yval = 0
                        y = np.append(y, yval)
                        try:
                            yval_err = float(sorteddata[dataln][fitparams["StDev_"+selectedfit][pknum]])
                            y_err = np.append(y_err, yval_err)
                        except: True
                        mm = np.append(mm, float(sorteddata[dataln][varpar[parstr[-1]]]))
                        dataln = dataln+1
                    yfix = y
                    paramdict[parstr[-1]] = " "
                    paramdict["peak_nr"]=str(pknum)
                    paramdict["position"]=parstr[-1]
                    src.AddData(yfix,paramdict.copy(), detdict.copy(), "ScanmanPeakFit_pkf", fname, {"mm":mm}, y_err=y_err)
                    break
                    
                elif dataln < nrdatalns:
                    paramdictcheck = {}
                    paramdictchecknew = {}
                    for ipar in range(len(parstr)-1): 
                        paramdictcheck[parstr[ipar]] = float(sorteddata[dataln-1][varpar[parstr[ipar]]])
                        paramdictchecknew[parstr[ipar]] = float(sorteddata[dataln][varpar[parstr[ipar]]])
                    maxdiff = np.max(np.abs(np.array(paramdictcheck.values()) - np.array(paramdictchecknew.values())))
                    if maxdiff > prec:
                        paramdict[parstr[-1]] = " "
                        yave = []
                        #yfix=np.array([y[i] if y[i]/np.average(np.delete(y,y[i]))<=fixmassive else 0 for i in range(len(y))])
                        #yfix=np.array([y[i] if y[i]<15000 else 0 for i in range(len(y))])
                        yfix = y
                        paramdict["peak_nr"]=str(pknum)
                        paramdict["position"]=parstr[-1]
                        src.AddData(yfix,paramdict.copy(), detdict.copy(), "ScanmanPeakFit_pkf", fname, {"mm":mm}, y_err=y_err)
                        mm = np.array([])
                        y = np.array([])
                        y_err = np.array([])
                        paramdict = {}
                    True
                else:   #Single value
                    paramdict[parstr[-1]] = " "
                    yfix = y
                    paramdict["peak_nr"]=str(pknum)
                    paramdict["position"]=parstr[-1]
                    src.AddData(yfix,paramdict.copy(), detdict.copy(), "ScanmanPeakFit_pkf", fname, {"mm":mm}, y_err=y_err)
                    mm = np.array([])
                    y = np.array([])
                    y_err = np.array([])
                    paramdict = {}
                    
                    
            True
        True
        
    #datasections = filecontent[scanStartIdx:-1].split("\n\n")
    #for section in datasections:
    #    paramdict = paramdictcmn.copy()
        
        #Get the intensity data
    #    y = np.array([])
    #    tth = np.array([])
    #    for aline in section.split("\n"):
    #        x, intensity = aline.split()
    #        y = np.append(y, float(intensity))
    #        mm = np.append(tth, float(x))
        
    #    src.AddData(y,paramdict, detdict, "Gumtree_xyd", fname, {"mm":mm})
    #src.AddData(np.array([0,1,2,3,3,2,1,0]),paramdict, detdict, "ScanmanPeakFit_pkf", fname, {"mm":np.array([-10.2,-9,-8.3,-7.4,-6.9,-5.2,-4,-3.5])})
    
    return src
    
        