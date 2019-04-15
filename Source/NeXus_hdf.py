'''
Created on 17 Jul 2014

@author: Deon
'''

from Source import Srcpar
import numpy as np
import h5py
from mylib import ProgressBar
import re

#import time



def NeXus_hdf_read(fname, config):
    src = Srcpar.Srcpar(config)
    #src.dataset.pop()       #Remove the {0,0} dataset
    paramdict = {}
    params = {}
    detdict = {}
    detdictcmn = {}
    twodim = False
    
    f = h5py.File(fname,"r")
    dset = f.get("/")
    #y = dset["/entry1/instrument/detector/hmm_x_corrected"].value.astype('float')
    if "/entry1/instrument/detector/hmm" in dset:
        try:
            #n = dset["/entry1/instrument/detector/hmm"].value.astype('float')
            #CDM .value is depricated: n = dset["/entry1/instrument/detector/hmm"].value
            n = dset["/entry1/instrument/detector/hmm"][()]
            twodim = True
        except ValueError:      #array is too big, try to get the 1D dataset
            #n = dset["/entry1/instrument/detector/hmm_x_corrected"].value.astype('float')
            n = np.array(dset["/entry1/instrument/detector/hmm_x_corrected"])
            twodim = False
    elif "/entry1/instrument/detector/hmm_xy" in dset:
        #n = dset["/entry1/instrument/detector/hmm_xy"].value.astype('float')
        n = dset["/entry1/instrument/detector/hmm_xy"][()].astype('float')
        twodim = True
    elif "/entry1/instrument/detector/hmm_total_xy" in dset:
        #n = dset["/entry1/instrument/detector/hmm_total_xy"].value
        n = dset["/entry1/instrument/detector/hmm_total_xy"][()]
        twodim = True
    
    numruns = len(n)    
    progress = ProgressBar("Loading NeXus hdf datasets...", numruns)

    datakeys = dset["/entry1/data"].keys()
    possiblescanparams = [x for x in datakeys]
    if "run_number" in datakeys:        #Scan was done with Gumtree, therefore use the title to determine the scan variables
        #title = dset["/entry1/experiment/title"].value[0]
        title = str(dset["/entry1/experiment/title"][()])
        possiblescanparams = re.findall(r"[\w']+", title)
    #else:
    #    possiblescanparams = datakeys
    if "time" in possiblescanparams: possiblescanparams.remove("time")
        
    True
    #x_stth = dset["/entry1/instrument/detector/x_stth"]
    try:
        #stth = dset["/entry1/sample/stth"].value
        stth = dset["/entry1/sample/stth"][()]
    except:
        stth = [90.0]*len(n)
    if "/entry1/instrument/detector/sample_to_detector_distance" in dset:
        #sampletodetector = np.float32(dset["/entry1/instrument/detector/sample_to_detector_distance"].value[0])
        sampletodetector = np.float32(dset["/entry1/instrument/detector/sample_to_detector_distance"][0])
    else:
        sampletodetector = np.float32(1000)
    #detwidth = np.float32(dset["/entry1/instrument/detector/active_width"].value[0])
    #detheight = np.float32(dset["/entry1/instrument/detector/active_height"].value[0])
    detwidth = np.float32(dset["/entry1/instrument/detector/active_width"][0])
    detheight = np.float32(dset["/entry1/instrument/detector/active_height"][0])
    if "/entry1/instrument/crystal" in dset:
        crystal = dset["/entry1/instrument/crystal"]
    else:
        crystal = dict([])
    if "/entry1/instrument/monochromator" in dset:
        monochromator = dset["/entry1/instrument/monochromator"]
        if "focus" in monochromator:
            monochromator = dset["/entry1/instrument/monochromator/focus"]
    else:
        monochromator = dict([])
    if "/entry1/instrument/slits" in dset:
        slits = dset["/entry1/instrument/slits"]
    else:
        slits = dict([])
    sample = dset["/entry1/sample"]
    #moncounts = [[s,dset["/entry1/monitor/"+s].value] for s in dset["entry1/monitor"] if "_counts" in s]
    #monrates = [[s,dset["/entry1/monitor/"+s].value] for s in dset["entry1/monitor"] if "_event_rate" in s]
    #montime = [[s,dset["/entry1/monitor/"+s].value] for s in dset["entry1/monitor"] if "_time" in s]
    moncounts = [[s,dset["/entry1/monitor/"+s][()]] for s in dset["entry1/monitor"] if "_counts" in s]
    monrates = [[s,dset["/entry1/monitor/"+s][()]] for s in dset["entry1/monitor"] if "_event_rate" in s]
    montime = [[s,dset["/entry1/monitor/"+s][()]] for s in dset["entry1/monitor"] if "_time" in s]
    
    
    detdictcmn["sam_to_det"] = sampletodetector
    detdictcmn["det_xmin"] =  -detwidth/2.0
    detdictcmn["det_xmax"] =  detwidth/2.0
    detdictcmn["det_ymin"] =  -detheight/2.0
    detdictcmn["det_ymax"] =  detheight/2.0
    detdictcmn["lambda"] = config["source"]["detector"]["lambda"]

    flipit=config["source"]["hdf"]["flipxy"]

    #tic=time.time()
    for run in range(numruns):
        progress.setinfo(fname)
        
        params["RunNr"] = str(run+1)
        
        detdict = detdictcmn.copy()
        detdict["stth"] = stth[run]
        #for itemkey in crystal.iterkeys(): DM iterkeys() depricated
        for itemkey in crystal.keys():
            params[itemkey] = str(dset["/entry1/instrument/crystal/%s" %(itemkey)][run])
        #for itemkey in monochromator.iterkeys():  DM iterkeys() depricated
        for itemkey in monochromator.keys():
            try:
                #params[itemkey] = str(dset["/entry1/instrument/monochromator/%s" %(itemkey)][run])
                params[itemkey] = str(dset[monochromator.name+"/"+itemkey][run])
            except:
                True
        #for itemkey in slits.iterkeys():  DM iterkeys() depricated
        for itemkey in slits.keys():
            try:
                params[itemkey] = str(dset["/entry1/instrument/slits/%s" %(itemkey)][run])
            except:
                True
        #for itemkey in sample.iterkeys(): DM iterkeys() depricated
        for itemkey in sample.keys():
            try:    #if type(sample[itemkey]) == h5py._hl.dataset.Dataset:       #Cannot handle groups at the moment, only Datasets
                #theval = sample[itemkey].value
                theval = sample[itemkey][()]
                ivalnr = run
                if theval.size ==1: ivalnr=0
                params[itemkey]=str(theval[ivalnr])
                #params[itemkey]=theval[ivalnr].astype('str')
                #if sample[itemkey].value.size==1:
                #    params[itemkey]=sample[itemkey].value[0].astype('str')
                #else:
                #    params[itemkey]=sample[itemkey].value[run].astype('str')
            except:
                True
        try:
            #params["time"] = str(dset["/entry1/data/time"].value[run])
            params["time"] = str(dset["/entry1/data/time"][run])
        except:
            True
        for item, value in moncounts:
            params[str(item)] = str(value[run])
        for item, value in monrates:
            params[str(item)] = str(value[run])
        for item, value in montime:
            params[str(item)] = str(value[run])

        paramdict = params.copy()
        #frame = n[run][0]
        #for i in range(len(frame)):
        #    if i != 7:
        #        frame[i]=np.zeros(np.shape(frame[i]))
                
        #src.AddData(frame, paramdict, detdict, "NeXus_hdf", fname, twod=True)     #the [0] is the time channel
        
        if len(n.shape) == 4:   # run, time, x, y
            if flipit:
                src.AddData(np.transpose(n[run][0]), paramdict, detdict, "NeXus_hdf", fname, twod=twodim)     #the [0] is the time channel
            else:
                src.AddData(n[run][0], paramdict, detdict, "NeXus_hdf", fname, twod=twodim)     #the [0] is the time channel
            #src.AddData(np.transpose(n[run][0]), paramdict, detdict, "NeXus_hdf", fname, twod=twodim)     #the [0] is the time channel
        else:   # run, x, y
            src.AddData(np.asfarray(n[run]), paramdict, detdict, "NeXus_hdf", fname, twod=twodim)
        True
        if progress.wasCanceled(): break
        progress.step()
    f.close()
    #toc=time.time()
    #print "Time is %f" % (toc-tic)
    src.filename = fname
    paramkeys = [x for x in params.keys()]
    commonparams = list(set(paramkeys).intersection(possiblescanparams))    #Determine the scan variables from the title and the actual instrument parameters
    for item in commonparams:
        src.precparams[item]=0.01
        True
    return src
    
        