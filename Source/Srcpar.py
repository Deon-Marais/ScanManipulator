'''
Created on 10 Jun 2014

@author: Deon
'''

from pylab import np
import copy
import time
from scipy.interpolate import griddata
import pylab as pl
from mylib import ProgressBar
import mylib
import ctypes
from _ast import Or

class Frame():
    def __init__(self):
        self.y = self.x = self.x_d = self.x_2th = self.x_mm = np.array([0.0])
        self.x_2th_reg = self.x_2th_reg_full2th = np.array([0.0])
        self.y_2th = self.y_reg = self.y_reg_full2th = np.array([0.0])
        self.y_err = self.y_2th_err = self.y_reg_err = self.y_reg_full2th_err = np.array([])
        self.y_min = self.y_max = float(0)
        self.x_chan = np.array([0])
        self.nchan = int(0)
        
        self.twod = False                       #False when no 2D
        self.h = self.v = np.array([0.0])       #horizontal (h) and vertical (v) channel numbers
        self.h_mm = self.v_mm = self.hc_mm = self.vc_mm = np.array([0.0]) #h & v edges and centers distance
        self.h_2th = self.v_2th = self.hc_2th = self.vc_2th = np.array([0.0]) #h & v edges and centers angles (degrees)
        self.n = np.array([[0.0]])      #number of neutrons - v x h array

        self.originalaxis = ""


class SourceData():
    def __init__(self, config):
        self.frame = {}
        self.frame['raw'] = Frame()
        self.frame['ff_cor'] = Frame()
        self.frame['geom_cor'] = Frame()
        self.currframe = self.frame['raw']

        
        #1D
        self.y = self.x = self.x_d = self.x_2th = self.x_mm = np.array([0.0])
        self.x_2th_reg = self.x_2th_reg_full2th = np.array([0.0])
        self.y_err = self.y_2th_err = self.y_reg_err = self.y_reg_full2th_err = np.array([])
        self.y_2th = self.y_reg = self.y_reg_full2th = np.array([0.0])
        self.y_min = self.y_max = float(0)
        self.x_chan = np.array([0])
        
        #2D
        self.twod = False                       #False when no 2D
        self.h = self.v = np.array([0.0])       #horizontal (h) and vertical (v) channel numbers
        self.h_mm = self.v_mm = self.hc_mm = self.vc_mm = np.array([0.0]) #h & v edges and centers distance
        self.h_2th = self.v_2th = self.hc_2th = self.vc_2th = np.array([0.0]) #h & v edges and centers angles (degrees)
        self.h_cor_2th = self.v_cor_2th = self.hc_cor_2th = self.vc_cor_2th = np.array([0.0]) #h & v edges and centers angles (degrees)
        self.n = np.array([[0.0]])      #number of neutrons - v x h array
        self.n_cor = np.array([[0.0]])      #number of neutrons - v x h array
        self.n_y = self.n_cor_y = np.array([0.0])   #collapsed 1D data
        
        self.prm = {}
        self.detprm = config["source"]["detector"]
        self.origin = ""
        self.filename = ""
        
        
        
        #self.detprm = {}
    
class CorMap():
    def __init__(self):
        self.stth = float()
        self.echi = float()
        #self.h_2th = self.v_2th = self.hc_2th = self.vc_2th = np.array([0.0]) #h & v edges and centers angles (degrees)
        self.h_cor_2th = self.v_cor_2th = self.hc_cor_2th = self.vc_cor_2th = np.array([0.0]) #h & v edges and centers angles (degrees)
        self.sam_to_px_theta_flat = self.sam_to_px_gamma_flat = np.array([0.0])
        self.n_cor = np.array([[0.0]])

class Srcpar(object):
    '''
    classdocs
    '''
    


    #**************************************************************************************
    def __init__(self,config):
        '''
        Constructor
        '''
        self.config=config
#        if config == {}:
#            self.config["detector"] = {"det_xmin":-100.0, "det_xmax":100.0,"det_ymin":-100.0, "det_ymax":100.0,
#                                       "sam_to_det":1000, ""}
        
        self.y = self.x = self.x_d = self.x_2th = self.x_mm = np.array([0.0])# []
        self.y_err = self.x_err = np.array([])
        self.y_min = self.y_max = 0.0 #float(0)          #for the current selected dataset
        self.x_min = self.x_max = 0.0 #float(0)          #for the current selected dataset
        self.x_d_min = self.x_d_max = float(0)
        self.x_2th_min = self.x_2th_max = float(0)
        self.x_mm_min = self.x_mm_max = float(0)
        self.x_chan = np.array([0])
        self.nchan = 1
        self.lowerchan = 0
        self.upperchan = -1
        self.currset = int(0)
        self.dataset = []
        self.prm = {}
        self.origin = ""
        self.filename = ""
        #self.exportparams = []
        self.precparams = {}                #Holds the scan variables with their respective precision. Used when performing new set calculations in post processing
        self.ylabel = "n"
        self.preps = {"flat_field":[], "geom_cor":False, "split":0, "postdirty":True, "just_sum":False}
        self.AddData(np.array([0.0]))     #Dataset 0 used as the sum for all others
        self.crmap = []         #add the CorMap structures into this list
        self.data2D = False
        self.ffframe = Frame()
        
        
    #**************************************************************************************
    def Clear(self):
        for i in range(len(self.dataset)):
            self.dataset.pop()
        self.x = self.x_chan = self.x_d = self.x_2th = self.x_mm = [0.0]
        self.y_min = self.y_max = self.x_min = self.x_max = 0.0
        self.x_d_min = self.x_d_max = self.x_2th_min = self.x_2th_max = float(0)
        self.x_mm_min = self.x_mm_max = float(0)
        self.preps = {"flat_field":[], "geom_cor":False, "split":0, "postdirty":True}
        self.data2D = False
    

        
    #**************************************************************************************
    def AddData(self,y,param={}, detprm={}, origin = "", filename = "", axis = {}, twod = False, y_err=np.array([]), x_err=np.array([])):
        src = SourceData(self.config)
        src_raw = src.frame['raw']
        if detprm != {}: src.detprm = detprm
        if twod:
            src_raw.n=y.copy()
            numv = src_raw.n.shape[0]
            numh = src_raw.n.shape[1]
            src_raw.h = np.arange(0, numh, 1)
            src_raw.v = np.arange(0, numv, 1)
            src_raw.h_mm = np.linspace(detprm["det_xmin"], detprm["det_xmax"], numh+1)   #edges
            src_raw.v_mm = np.linspace(detprm["det_ymin"], detprm["det_ymax"], numv+1)
            src_raw.hc_mm = src_raw.h_mm[:-1] + 0.5 * (src_raw.h_mm[1:] - src_raw.h_mm[:-1])            #centers
            src_raw.vc_mm = src_raw.v_mm[:-1] + 0.5 * (src_raw.v_mm[1:] - src_raw.v_mm[:-1])
            
            src_raw.n_y = src_raw.n.sum(axis=0)
            src_raw.y = src_raw.n_y.copy()
            src_raw.twod = True 
            
            try:
                if (axis.keys()[0]=="mm"):
                    src_raw.hc_2th=src_raw.hc_mm
                    src_raw.vc_2th=src_raw.vc_mm
                    src.hc_2th = src_raw.hc_mm
                    src.vc_2th = src_raw.vc_mm
            except:
                True
             
                
                
            #Legacy structure 
            src.n = src_raw.n
            src.h = src_raw.h
            src.v = src_raw.v
            src.h_mm = src_raw.h_mm 
            src.v_mm = src_raw.v_mm
            src.hc_mm = src_raw.hc_mm
            src.vc_mm = src_raw.vc_mm 
            src.n_y = src_raw.n_y
            src.y = src_raw.y
            self.data2D = src_raw.twod 
            
        else:   #1D
            src_raw.y = y.copy()
            src.y = src_raw.y
            src_raw.y_err = y_err.copy()
            src.y_err = src_raw.y_err
            
            
        src_raw.y_min = min(src_raw.y)
        src_raw.y_max = max(src_raw.y)
        src.prm = param
        src.origin = origin
        src.filename = filename
        src_raw.x_chan = np.arange(0, len(src_raw.y), 1)              #create the channel axis
        src_raw.nchan = len(src_raw.x_chan)
        
        if len(axis) == 0:
            src_raw.originalaxis="ch"
        #for axistype in axis.iterkeys():   CDM iterkeys depricated
        for axistype in axis.keys():
            src_raw.originalaxis=axistype
            #src.originalaxis=axistype
            if axistype == "2th"or axistype == "Angle":
                src_raw.x_2th = axis[axistype]
                src.x_2th = src_raw.x_2th
            elif axistype == "mm" or axistype == "Position":
                src_raw.x_mm = axis[axistype]
                src.x_mm = src_raw.x_mm
            elif axistype == "d" or axistype =="d-spacing":
                src_raw.x_d = axis[axistype]
                src.x_d = src_raw.x_d
                
        
        #Legacy datastucture
        src.y_min = src_raw.y_min
        src.y_max = src_raw.y_max
        src.x_chan = src_raw.x_chan
        src.nchan = src_raw.nchan
        
        self.dataset.append(src)


    #**************************************************************************************
    def CalcSumSetCommon(self, setname=""):
        if len(self.dataset) == 1:return
        for i in range(1, len(self.dataset)):
            self.dataset[i].prm = self.dataset[i].prm.copy()
        src_set = SourceData(self.config)
        #src_set.detprm = copy.deepcopy(self.dataset[1].detprm)
        src_set.detprm = copy.copy(self.dataset[1].detprm)
        src_set.prm = self.dataset[1].prm.copy()
        src_set.prm = src_set.prm.copy()    #Have to do this otherwise the order is different form the other sets...
        #src_set.origin = copy.deepcopy(self.dataset[1].origin)
        src_set.origin = copy.copy(self.dataset[1].origin)
        if setname == "" : setname = self.dataset[1].filename
        src_set.filename = "Sum: " + setname
        mintth = self.dataset[1].frame["raw"].x_2th.min()
        maxtth = self.dataset[1].frame["raw"].x_2th.max()
        for i in range(2,len(self.dataset)):
            selfdatasetiframe = self.dataset[i].frame["raw"]
            mintth = selfdatasetiframe.x_2th.min() if selfdatasetiframe.x_2th.min()< mintth else mintth
            maxtth = selfdatasetiframe.x_2th.max() if selfdatasetiframe.x_2th.max()> maxtth else maxtth
            #for parname in src_set.prm.iterkeys(): 
            for parname in src_set.prm.keys():
                #if parname not in self.dataset[i].prm or self.dataset[i-1].prm:
                #    True
                if (self.dataset[i].prm[parname] != self.dataset[i-1].prm[parname]) or src_set.prm[parname] == "" :
                    src_set.prm[parname] = ""
                    #if (parname not in self.exportparams): self.exportparams.append(parname)
        src_set.detprm["stth"] = mintth + (maxtth-mintth)/2.0
        self.dataset[0]=src_set
        True
    
    #**************************************************************************************
    def CalcSumSet(self, frames=[]):
        if len(self.dataset) == 1:return
        if frames == []:
            #for frm_i in self.dataset[-1].frame.iterkeys():
            for frm_i in self.dataset[-1].frame.keys():
                if len(self.dataset[-1].frame[frm_i].y) != 1: frames.append(frm_i)
        
        for frm_i in frames:
            src = Frame()
            selfdataset1frame=self.dataset[1].frame[frm_i]          #1 is The first real dataset, 0 is the sum set now
            src.y = selfdataset1frame.y
            src.x_mm = selfdataset1frame.x_mm
            src.x_d =  selfdataset1frame.x_d
            src.x_chan = range(len(src.y))
            src.y_min = src.y.min()
            src.y_max = src.y.max()
            src.x_mm_min = src.x_mm.min()
            src.x_mm_max = src.x_mm.max()
            src.x_d_min = src.x_d.max()     #min to max in order to reverse the graph axis
            src.x_d_max = src.x_d.min()
            
            for i in range(2,len(self.dataset)):
                try:
                    src.y = src.y + self.dataset[i].frame[frm_i].y
                except:
                    True
            if (len(self.dataset)==2):      #When only one actual dataset is present, such as for the directly read histogram data 
                src.y = self.dataset[1].frame[frm_i].y
            src.y_min=min(src.y)
            src.y_max=max(src.y)
            
            try:
                delth = selfdataset1frame.x_2th[1]-selfdataset1frame.x_2th[0]           #smallest angle are at the sides
                mintth = selfdataset1frame.x_2th.min()
                maxtth = selfdataset1frame.x_2th.max()
                for i in range(1,len(self.dataset)):
                    selfdatasetiframe = self.dataset[i].frame[frm_i]
                    mintth = selfdatasetiframe.x_2th.min() if selfdatasetiframe.x_2th.min()< mintth else mintth
                    maxtth = selfdatasetiframe.x_2th.max() if selfdatasetiframe.x_2th.max()> maxtth else maxtth
                nchansum = np.int(np.floor_divide(maxtth - mintth,delth) + 1)
                fulltth = np.linspace(mintth, maxtth, nchansum)
                sortedprms2th = np.array([[0,0,0]])
                
                for i in range(1,len(self.dataset)):        #Could possibly do this in parallel
                    selfdatasetiframe = self.dataset[i].frame[frm_i]
                    x_2th = selfdatasetiframe.x_2th
                    minch = np.where(fulltth >=x_2th.min())[0][0]
                    maxch = np.where(fulltth <=x_2th.max())[0][-1]
                    selfdatasetiframe.x_2th_reg = fulltth[minch:maxch]
                    selfdatasetiframe.y_reg = np.interp(selfdatasetiframe.x_2th_reg, x_2th, selfdatasetiframe.y)
                    selfdatasetiframe.y_reg_full2th = np.zeros(nchansum)          #creates and array with the full size of 2tth, filled with zeroes
                    selfdatasetiframe.y_reg_full2th[slice(minch,maxch)] = selfdatasetiframe.y_reg
                    sortedprms2th = np.append(sortedprms2th, [[i, selfdatasetiframe.x_2th_reg[0], selfdatasetiframe.x_2th_reg[-1]]],0)
                    True
                sortedprms2th = sortedprms2th[1:]                   #remove the initial [0,0,0] value
                sortedprms2th= sortedprms2th[sortedprms2th[:,1].argsort()]
                src.x_2th = fulltth
                src.y_2th = selfdataset1frame.y_reg_full2th
                for i in range(1,len(self.dataset)):
                    selfdatasetiframe = self.dataset[i].frame[frm_i]
                    src.y_2th += selfdatasetiframe.y_reg_full2th
                src.x_2th_min = src.x_2th.min()
                src.x_2th_max = src.x_2th.max()
                
                #Calculate d-axis
                wavelength = self.dataset[1].detprm["lambda"]
                src.x_d = wavelength/2.0/np.sin(np.deg2rad(src.x_2th/2.0))
                src.x_d_min = src.x_d.max()       #the bigger the angle, the smaller the d-value, therefore reverse min and max in order to have it look the same on the graph
                src.x_d_max = src.x_d.min()
            except:
                True
            self.dataset[0].frame[frm_i] = src
            True
            
        
        #self.dataset.insert(0, src_set)

        
        
    #**************************************************************************************
    def CalcAllAxis(self,frames=[]):
        if frames == []:
            #for frm_i in self.dataset[-1].frame.iterkeys():
            for frm_i in self.dataset[-1].frame.keys():
                #if len(self.dataset[-1].frame[frm_i].y) != 1: frames.append(frm_i)
                if self.dataset[-1].frame[frm_i].originalaxis != "": frames.append(frm_i)
        
        begset = 0
        if ("Sum" in self.dataset[0].filename) or (self.dataset[0].filename==""): begset = 1
        #if ("Sum" in self.dataset[0].filename): begset = 1
        
            
        for i in range(begset,len(self.dataset)):
            for frm_i in frames:
                src_set = self.dataset[i]
                src = self.dataset[i].frame[frm_i]
                sam_to_det = src_set.detprm["sam_to_det"]
                wavelength = src_set.detprm["lambda"]
                
                #Position axis
                #if (len(src.x_mm) == 1) and (len(src.x_2th) != 1):   #Calculate position from stth axis
                if src.originalaxis=="d": #calculate 2th from d
                    stth = src_set.detprm["stth"]
                    src.x_2th = np.rad2deg(np.arcsin(wavelength/2.0/src.x_d))*2.0
                if src.originalaxis=="2th" or src.originalaxis == "Angle" or src.originalaxis == "d":
                    stth = src_set.detprm["stth"]
                    src.x_mm = sam_to_det * np.arctan(np.deg2rad(src.x_2th - stth))
                #elif len(src.x_mm) == 1:
                elif src.originalaxis=="ch":
                    x_mm_min = src_set.detprm["det_xmin"]
                    x_mm_max = src_set.detprm["det_xmax"]
                    if src.nchan==0: src.nchan=len(src.y)
                    delx = (x_mm_max - x_mm_min)/float(src.nchan)
                    src.x_mm = np.array([x_mm_min + j*delx for j in src.x_chan])

                src.x_mm_min = src.x_mm.min()
                src.x_mm_max = src.x_mm.max()
                    
                #2theta angle axis
                stth = src_set.detprm["stth"]
                #if len(src.x_2th) == 1:     #Calculate 2th from x_mm
                #if src.originalaxis != "2th" and src.originalaxis != "Angle" and len(src.hc_2th)==1:  #DM add the len(src.x_2th) part for when the S2D changed and stth must be recalculated
                if (src.originalaxis != "2th" and src.originalaxis != "Angle" and len(src.hc_2th)==1) or (len(src.x_2th) == 1) :
                    src.x_2th =  np.degrees(np.arctan(src.x_mm/sam_to_det))  + stth
                    src.h_2th = np.degrees(np.arctan(src.h_mm/sam_to_det)) + stth
                    src.v_2th = np.degrees(np.arctan(src.v_mm/sam_to_det))
                    src.hc_2th = np.degrees(np.arctan(src.hc_mm/sam_to_det)) + stth
                    src.vc_2th = np.degrees(np.arctan(src.vc_mm/sam_to_det))
                else:   #hack - this is probaly not really a detector to measure in 2th, therefore equate it to the mm axis
                    #src.x_2th =  src.x_mm
                    #src.h_2th = src.h_mm
                    #src.v_2th = src.v_mm
                    #src.hc_2th = src.hc_mm
                    #src.vc_2th = src.vc_mm
                    True
                        
                src.x_2th_min = src.x_2th.min()
                src.x_2th_max = src.x_2th.max()
                #src.y_2th = copy.deepcopy(src.y)
                src.y_2th = copy.copy(src.y)
                
                #d-spacing axis
                
                #if len(src.x_d) == 1:   #Calculate d-spacing from 2th
                #if src.originalaxis!="d":
                if src.originalaxis!="d" or len(src.x_d) == 1:
                    src.x_d = wavelength/2.0/np.sin(np.deg2rad(src.x_2th/2.0))
                src.x_d_min = src.x_d.max()       #the bigger the angle, the smaller the d-value, therefore reverse min and max in order to have it look the same on the graph
                src.x_d_max = src.x_d.min()


    #**************************************************************************************
    #def Select2DType(self, datatype = ""):
        
    #**************************************************************************************
    def CalcFlatFieldCorrection(self,ffset, mode="2th"):
        try:
            src_set = self
            if mode=="none":
                self.SelectFrame("raw")
                return
                
            if ffset == self.preps["flat_field"]:           #The correction was calculated previously, therefore just select it
                self.SelectFrame("ff_cor")
                return
            
            self.preps["flat_field"]=ffset
            stthlist = []
            for srci in range(1, len(ffset)):
                srcff = ffset[srci]
                srcff.frame["ff_cor"] = copy.copy(srcff.frame["raw"])
                srcff.frame["ff_cor"].n = srcff.frame["ff_cor"].n / float(srcff.frame["raw"].n.max())    #Use the 'ff_cor' frame here to store the scaling factors temporarily
                stthlist.append([srci,np.float(srcff.detprm["stth"])])
                True
            
            for i in range(1,len(src_set.dataset)):
                dseti = src_set.dataset[i]
                stth = np.float(src_set.dataset[i].detprm["stth"])
                closeststth = stthlist[0]     #Starting value
                for thpair in stthlist[1:]:
                    if abs(thpair[1]-stth) < abs(closeststth[1]-stth):
                        closeststth = thpair
                src_set.dataset[i].frame["ff_cor"] = copy.copy(src_set.dataset[i].frame["raw"])    
                #resn = src_set.dataset[i].frame["ff_cor"].n
                resn = np.divide(dseti.frame["raw"].n, ffset[closeststth[0]].frame["ff_cor"].n)
                resn[resn == np.inf] = 0
                dseti.frame["ff_cor"].n = np.nan_to_num(resn)
                dseti.frame["ff_cor"].n_y = dseti.frame["ff_cor"].n.sum(axis=0)
                #dseti.frame["ff_cor"].y = dseti.frame["ff_cor"].n_y
                src_set.dataset[i].frame["ff_cor"].y = copy.copy(dseti.frame["ff_cor"].n_y)
                dseti.currframe = dseti.frame["ff_cor"]
                
            self.CalcAllAxis(["ff_cor"])    
            self.CalcSumSet(["ff_cor"])
            self.SelectFrame("ff_cor")
        except:
            mylib.ErrMessage("Incompatible flat field file!")
            
        True
        
       
            
        
    #**************************************************************************************
    def SplitDetector(self,nrsections):
        if self.data2D == False:
            return self
        
        if self.preps['split'] == nrsections:
            return self
            #return False
        
        if nrsections == 1:
            return self
        
        numdsets = len(self.dataset)
        progress = ProgressBar("Splitting detector in %i..." %(nrsections), numdsets,self.filename)

        
        #srcsplit = Srcpar(self.config)
        src = self
        srcsplit = copy.deepcopy(src)
        srcsplit.dataset=[]
        srcsplit.ylabel = src.ylabel
        nrvchan = np.floor_divide(len(src.dataset[-1].frame["raw"].v),nrsections)
        srcsplit.dataset.append(copy.deepcopy(src.dataset[0]))
        for idset in range(1,numdsets):
            progress.setinfo()
            srcsplit.precparams = src.precparams
            
            src_set = self.dataset[idset]
            if "nchi" not in src_set.prm:
                src_set.prm["nchi"] = "0"
            startv=0
            detysplitlen = (src_set.detprm["det_ymax"] - src_set.detprm["det_ymin"])/nrsections
            for vsec in range(int(nrsections)):
                endv=int(startv+nrvchan)
                srcsplit.dataset.append(copy.deepcopy(src_set))
                
                srcsplit.dataset[-1].detprm["det_ymin"]= src_set.detprm["det_ymin"] + vsec*detysplitlen
                srcsplit.dataset[-1].detprm["det_ymax"]=srcsplit.dataset[-1].detprm["det_ymin"] + detysplitlen
                
                frm_raw = srcsplit.dataset[-1].frame["raw"]
                frm_ffcor = srcsplit.dataset[-1].frame["ff_cor"]
                
                #frm_raw.n=src_set.frame["raw"].n[startv:endv].view()
                #frm_ffcor.n=src_set.frame["ff_cor"].n[startv:endv].view()
                
                for frm in[frm_raw, frm_ffcor]:
                    frm.n=frm.n[startv:endv].view()
                    frm.n_y = frm.n.sum(axis=0)
                    frm.v=frm.v[startv:endv+1]
                    frm.v_2th=frm.v_2th[startv:endv+1]
                    frm.v_mm=frm.v_mm[startv:endv+1]
                    frm.vc_2th=frm.vc_2th[startv:endv]
                    frm.vc_mm=frm.vc_mm[startv:endv]
                    frm.y = frm.n_y
                    frm.y_2th = frm.y
                    frm.y_max = frm.y.max()
                    frm.y_min = frm.y.min()
                    True
                srcsplit.dataset[-1].prm["nchi"] = str(round(float(src_set.prm["nchi"]) + (frm_raw.v_2th[-1]+frm_raw.v_2th[0])/2.0 ,2))
                startv = endv
                True
            if progress.wasCanceled(): break
            progress.step()
            True
        True
        srcsplit.preps['geom_cor'] = False
        srcsplit.preps['split'] = nrsections
        srcsplit.crmap=[]
        srcsplit.CalcSumSetCommon()
        srcsplit.CalcSumSet(["raw"])
        return srcsplit    
            

                
            
        
        #srcsum.AddData(dset1.y, dset1_set.prm, dset1_set.detprm, dset1_set.origin+" - Post Process", dset1_set.filename)
                
        #          dset2_set.detprm["stth"] = (max(srcsum.x_2th_reg) - min(srcsum.x_2th_reg))/2.0 + min(srcsum.x_2th_reg)
        #        srcsum.AddData(srcsum.y_reg, dset2_set.prm, dset2_set.detprm, dset2_set.origin+" - Post Process", dset2_set.filename, {"2th":srcsum.x_2th_reg})
        #        True
            
        #srcsplit.CalcAllAxis()
        #srcsplit.precparams = src.precparams
        #srcsplit.exportparams = src.exportparams
        
        
        

    #**************************************************************************************
    def CalcGeomCorrection(self,config=""):
        #Taken from: StressTextureCalculator: a software tool to extract
        #            texture, strain and microstructure information from
        #            area-detector measurements
        #            J. Appl. Cryst. 2011. 44, 641-646
        
        if self.data2D == False:
            return
        elif self.preps['geom_cor'] == True:
            self.SelectFrame("geom_cor")
            return

        if config=="":
            config["hfrac"]=float(1.0)
            config["vfrac"]=float(1.0)
                    
        numdsets = len(self.dataset)
        
        if numdsets > 2:
            progress = ProgressBar("Geometric correction...", numdsets,self.filename)
        #tic=time.time()
    
        for idset in range(1,numdsets):
            #progress.setinfo()
            
            src_set = self.dataset[idset]
            #src_raw = src_set.frame["raw"]
            src_raw = src_set.currframe
            src_cor = src_set.frame["geom_cor"]
            
            stth = src_set.detprm["stth"]
            if "echi" not in src_set.prm:
                src_set.prm["echi"] = "0"
            echi = float(src_set.prm["echi"])
            
            stth_i = -1
            for cmap_i in range(len(self.crmap)):
                if np.abs(self.crmap[cmap_i].stth - stth) < 0.1:
                    if np.abs(self.crmap[cmap_i].echi - echi) < 0.01:
                        stth_i = cmap_i
                        break
            if stth_i > -1:
                mp = self.crmap[stth_i]
                src_cor.h_2th = mp.h_cor_2th
                src_cor.v_2th = mp.v_cor_2th
                src_cor.hc_2th = mp.hc_cor_2th
                src_cor.vc_2th = mp.vc_cor_2th
                src_cor.n, xedges, yedges = np.histogram2d(mp.sam_to_px_theta_flat, mp.sam_to_px_gamma_flat, bins=[mp.h_cor_2th, mp.v_cor_2th], weights=src_raw.n.flatten())
                src_cor.n = src_cor.n.transpose()
                
            else:
                sam_to_det = src_set.detprm["sam_to_det"]
                sam_to_det_sq = np.power(sam_to_det,2.0)
                
                arrshape = src_raw.n.shape
                ctr_to_px_mm = np.empty(arrshape)             #Just to get the correct dimensions
                sam_to_px_mm = np.empty(arrshape)
                sam_to_px_theta = np.empty(arrshape)
                sam_to_px_gamma = np.empty(arrshape)
                r = np.empty(arrshape)
                
                xsq = src_raw.hc_mm * src_raw.hc_mm
                ysq = src_raw.vc_mm * src_raw.vc_mm
                id_midy = np.floor_divide(len(src_raw.vc_mm),2)
                
                j = id_midy
                ctr_to_px_mm[id_midy]=np.sqrt(xsq+ysq[id_midy])
                sam_to_px_mm[id_midy]=np.sqrt(sam_to_det_sq + (ctr_to_px_mm[id_midy]*ctr_to_px_mm[id_midy]))
                sam_to_px_theta[id_midy] = stth + np.rad2deg(np.arctan(src_raw.hc_mm/sam_to_det))
                coneheight=sam_to_px_mm[id_midy]*np.cos(np.deg2rad(sam_to_px_theta[id_midy]))
                
                for j in range(len(ysq)):
                    for i in range(len(xsq)):
                        ctr_to_px_mm[j][i]=np.sqrt(xsq[i]+ysq[j])
                    sam_to_px_mm[j]=np.sqrt(sam_to_det_sq + (ctr_to_px_mm[j]*ctr_to_px_mm[j]))
                    sam_to_px_theta[j]=np.rad2deg(np.arccos(coneheight/sam_to_px_mm[j]))
                    r[j] = np.sqrt((sam_to_px_mm[j] * sam_to_px_mm[j]) - (coneheight * coneheight))
                    sam_to_px_gamma[j] = np.rad2deg(np.arcsin(src_raw.vc_mm[j]/r[j]))

                
                corr = CorMap()
                if 1:       #Done with 'histogram2d' command
                    src_cor.h_2th = np.linspace(sam_to_px_theta.min(),sam_to_px_theta.max(),int(len(xsq)*config["hfrac"]),+1)
                    src_cor.v_2th = np.linspace(sam_to_px_gamma.min(),sam_to_px_gamma.max(),len(ysq)*config["vfrac"]+1)
                    corr.sam_to_px_theta_flat = sam_to_px_theta.flatten()
                    corr.sam_to_px_gamma_flat = sam_to_px_gamma.flatten()
                    
                    src_cor.n, xedges, yedges = np.histogram2d(corr.sam_to_px_theta_flat, corr.sam_to_px_gamma_flat, bins=[src_cor.h_2th, src_cor.v_2th], weights=src_raw.n.flatten())
                    src_cor.n = src_cor.n.transpose()
                    src_cor.hc_2th = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
                    src_cor.vc_2th = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
                    
                    corr.h_cor_2th=src_cor.h_2th
                    corr.hc_cor_2th=src_cor.hc_2th
                    corr.v_cor_2th=src_cor.v_2th
                    corr.vc_cor_2th=src_cor.vc_2th
                    corr.stth = stth
                    corr.echi = echi
                    self.crmap.append(corr)
                
                if 0:   #Done with interpolation
                    nrhc = int(len(xsq)*config["hfrac"])   #number of horisontal centers
                    xmin, xmax = [corr.sam_to_px_theta_flat.min(), corr.sam_to_px_theta_flat.max()]   #new grid horisontal center min and max
                    dhc = (xmax - xmin)/nrhc
                    hc = np.linspace(xmin,xmax, nrhc) #positions of horisontal center grid
                    he = np.linspace(xmin - 0.5 * dhc, xmax + 0.5 * dhc, nrhc + 1)    #positions of horisontal edge grid
                    src_cor.h_2th = he
                    src_cor.hc_2th = hc
                    nrvc = len(ysq)*config["vfrac"]   #number of vertical centers
                    ymin, ymax = [corr.sam_to_px_gamma_flat.min(), corr.sam_to_px_gamma_flat.max()] #new grid vertical center min and max
                    dvc = (ymax - ymin)/nrvc
                    vc = np.linspace(ymin,ymax, nrvc)     #positions of vertical center grid
                    ve = np.linspace(ymin - 0.5 * dvc, ymax + 0.5 * dvc, nrvc + 1)    #positions of vertical edge grid
                    src_cor.v_2th = ve
                    src_cor.vc_2th = vc
                    nrptsx = complex(0,nrhc)
                    nrptsy = complex(0,nrvc)
                    points = np.array([corr.sam_to_px_theta_flat,corr.sam_to_px_gamma_flat]).transpose()
                    grid_x, grid_y = np.mgrid[xmin:xmax:nrptsx, ymin:ymax:nrptsy]
                    grid_z = griddata(points, src_raw.n.flatten(), (grid_x, grid_y), method='linear')
                    src_cor.n = np.nan_to_num(grid_z.transpose())
                    corr.h_cor_2th=he
                    corr.hc_cor_2th=hc
                    corr.v_cor_2th=ve
                    corr.vc_cor_2th=vc
                    corr.stth = stth
                    corr.echi = echi
                    self.crmap.append(corr)
                 
            src_cor.x_d = src_cor.x_mm = np.array([0.0])
            src_cor.x_chan = range(len(src_cor.hc_2th))
            src_cor.x_2th = src_cor.hc_2th
            src_cor.n_y = src_cor.n.sum(axis=0)
            #src_cor.n_y = src_raw.n.sum(axis=0)
            src_cor.y = src_cor.n_y
            src_cor.x_chan = range(len(src_cor.y))
            src_cor.originalaxis="2th"
            try:
                if progress.wasCanceled(): break
                progress.step()
            except:
                True

        self.CalcAllAxis(["geom_cor"])
        self.CalcSumSet(["geom_cor"])
        self.SelectFrame("geom_cor")
        
        #self.CalcAllAxis(frm=["geom_cor"])
        #self.CalcSumSet("", frm=["geom_cor"])
        self.preps['geom_cor'] = True
        
        #toc=time.time()
        #print "Time is %f" % (toc-tic)
            
    
    #**************************************************************************************
    def SelectFrame(self,frm="raw"):
        for nr in range(len(self.dataset)):
            self.dataset[nr].currframe = self.dataset[nr].frame[frm]

    
    #**************************************************************************************
    def SelectDataSet(self,nr,axistype='Channel'):
        
        if axistype == 'Channel':
            self.x = np.array(self.dataset[nr].currframe.x_chan)
            self.x_min = 0       
            self.x_max = len(self.x)-1
            #self.y = copy.deepcopy(self.dataset[nr].y)
            self.y = self.dataset[nr].currframe.y
        elif axistype == 'Position':
            self.x = self.dataset[nr].currframe.x_mm
            self.x_min = self.dataset[nr].currframe.x_mm_min
            self.x_max = self.dataset[nr].currframe.x_mm_max
            #self.y = copy.deepcopy(self.dataset[nr].y)
            self.y = self.dataset[nr].currframe.y
        elif axistype == 'Angle':
            self.x = self.dataset[nr].currframe.x_2th
            self.x_min = self.dataset[nr].currframe.x_2th_min
            self.x_max = self.dataset[nr].currframe.x_2th_max
            #self.y = copy.deepcopy(self.dataset[nr].y_2th)
            self.y = self.dataset[nr].currframe.y_2th
        elif axistype == 'd-spacing':
            self.x = self.dataset[nr].currframe.x_d
            self.x_min = self.dataset[nr].currframe.x_d_min
            self.x_max = self.dataset[nr].currframe.x_d_max
            #self.y = copy.deepcopy(self.dataset[nr].y_2th)
            self.y = self.dataset[nr].currframe.y_2th
            
        self.currset = nr
        self.y_err = self.dataset[nr].currframe.y_err
        self.y_min = min(self.y)
        self.y_max = max(self.y)
        self.nchan = len(self.y)
        #if nr != 0:
        #    self.y[self.dataset[nr].x_chan < self.lowerchan] = np.nan
        #    if self.upperchan == -1: self.upperchan = len(self.y)
        #    self.y[self.dataset[nr].x_chan > self.upperchan] = np.nan

        self.prm = self.dataset[nr].prm
        self.detprm = self.dataset[nr].detprm
        self.origin = self.dataset[nr].origin
        self.filename = self.dataset[nr].filename
        
        
    #**************************************************************************************
    def PreparePost(self):
        srcp = copy.deepcopy(self)
        srcp.data2D = False
        for i in range(len(srcp.dataset)):
            srcp.dataset[i].frame = {}
            srcp.dataset[i].frame["raw"] = copy.copy(srcp.dataset[i].currframe)
            srcp.dataset[i].currframe = srcp.dataset[i].frame["raw"]
        return srcp
            
        #srcp = Srcpar(self.config)
        #for i in range(len(self.dataset)):
        #    srcp.dataset[i].frame = {}
        #    srcp.dataset[i].frame["raw"] = copy.copy(self.dataset[i].currframe)
        #    srcp.dataset[i].currframe = srcp.dataset[i].frame["raw"]
        #    srcp.dataset[i].detprm = self.dataset[i].detprm
        #    srcp.dataset[i].prm = self.dataset[i].prm
        #    srcp.dataset[i].filename = self.dataset[i].filename
        #    True
        #return srcp
        
    
    
    #**************************************************************************************
    def Crop(self):
        #srcp = copy.deepcopy(self)
        srcp = self
        lch = srcp.lowerchan
        uch = srcp.upperchan
        for i in range(1, len(srcp.dataset)):
            #dset = copy.deepcopy(srcp.dataset[i].currframe)
            dset = copy.copy(srcp.dataset[i].currframe)
            dset.y = dset.y[lch:uch]
            dset.y_min = min(dset.y)
            dset.y_max = max(dset.y)
            dset.y_2th = dset.y_2th[lch:uch]
            dset.x_chan = range(len(dset.y))
            dset.x_mm = dset.x_mm[lch:uch]
            dset.x_mm_min = min(dset.x_mm)
            dset.x_mm_max = max(dset.x_mm)
            dset.x_2th = dset.x_2th[lch:uch]
            dset.x_2th_min = min(dset.x_2th)
            dset.x_2th_max = max(dset.x_2th)
            dset.x_d = dset.x_d[lch:uch]
            dset.x_d_min = max(dset.x_d)
            dset.x_d_max = min(dset.x_d)
            
            #srcp.dataset[i].frame = {}
            srcp.dataset[i].frame["raw"] = dset
            srcp.dataset[i].currframe = srcp.dataset[i].frame["raw"]
            True
        
        srcp.lowerchan = 0
        srcp.upperchan = len(srcp.dataset[1].currframe.y)
        return srcp
        True
        
        
    #**************************************************************************************
    def Normalise(self,param):
        #srcp = copy.copy(self)
        srcp=self
        if param == "": return srcp
        sumnorm = float(0)
        for i in range(1, len(srcp.dataset)):
            src_set=srcp.dataset[i]
            src_currframe = srcp.dataset[i].currframe
            if param == "Maximum_n":
                normval = float(src_currframe.y_max)
            else:
                normval = float(src_set.prm[str(param)])
            src_currframe.y = np.asfarray(src_currframe.y)/normval
            src_currframe.y_2th =np.asfarray(src_currframe.y_2th)/ normval
            src_currframe.y_reg =np.asfarray(src_currframe.y_reg)/ normval
            src_currframe.y_reg_full2th =np.asfarray(src_currframe.y_reg_full2th)/ normval
            src_currframe.y_min = min(src_currframe.y)
            src_currframe.y_max = max(src_currframe.y)
            sumnorm+=normval
            True
        src_currframe0 = srcp.dataset[0].currframe
        src_currframe0.y =np.asfarray(src_currframe0.y)/ sumnorm
        src_currframe0.y_2th =np.asfarray(src_currframe0.y_2th)/sumnorm
        src_currframe0.y_reg =np.asfarray(src_currframe0.y_reg)/sumnorm
        #srcp.dataset[0].y_full2th /= sumnorm
        src_currframe0.y_min = min(src_currframe0.y)
        src_currframe0.y_max = max(src_currframe0.y)
        srcp.ylabel = "n / "+param
        #return srcp    

    #**************************************************************************************
    def SumWith(self,sumparam):
        sm = str(sumparam)
        srcp = copy.copy(self)
        if sm == "": return srcp

        srcsum = Srcpar(self.config)
        srcsum.dataset.pop(0)
        srcsum.ylabel = srcp.ylabel
        
        setparams = srcp.precparams.keys()
        sortedprms = np.array([[0.0]*(2+len(setparams))])       #produces something like [[ 0.  0.  0.  0.  0.]]
        
        for i in range(1, len(srcp.dataset)):
            src_set = srcp.dataset[i]
            expanded = np.append([[i]], [float(src_set.prm[st]) for st in setparams])
            expanded = np.array([np.append(expanded,  [float(src_set.prm[sm])])])
            sortedprms = np.append(sortedprms, expanded,axis=0)
        sortedprms = sortedprms[1:].transpose()
        indexes = np.lexsort([sortedprms[s] for s in range(len(sortedprms)-1,0,-1)])        # s will be something like [4, 3, 2, 1]
        sortedprms = sortedprms.transpose()
        sortedprms = sortedprms[indexes]
        
        srcsum.dataset.append(srcp.dataset[0])      #The sum set
        srcsum.dataset.append(srcp.dataset[int(sortedprms[0][0])])      #Append the first dataset in the sortedprms list
        moncounts = [s for s in srcsum.dataset[-1].prm if "counts" in s]
        montime = [s for s in srcsum.dataset[-1].prm if "time" in s]
        for i in range(1, len(sortedprms)):
            src_set = srcp.dataset[i]
            dset = srcp.dataset[int(sortedprms[i][0])]
            sumset = srcsum.dataset[-1]
            dontsum = False in [np.abs(sortedprms[i][s+1] - sortedprms[i-1][s+1]) <= srcp.precparams[setparams[s]] for s in range(len(setparams))]
            if dontsum:
                srcsum.dataset.append(dset)
            else:       #sum
                sumsrc = sumset.frame["raw"]
                sumsrc.y += src_set.currframe.y
                sumsrc.y_2th += src_set.currframe.y_2th
                sumsrc.y_reg += src_set.currframe.y_reg
                sumsrc.y_min += min(sumsrc.y)
                sumsrc.y_max += max(sumsrc.y)
                for item in moncounts: sumset.prm[str(item)] = str(float(sumset.prm[str(item)]) + float(src_set.prm[item]))
                for item in montime: sumset.prm[str(item)] = str(float(sumset.prm[str(item)]) + float(src_set.prm[item]))
            sumset.prm[sm]=""
        srcsum.precparams = copy.copy(srcp.precparams)
        #srcsum.exportparams = copy.copy(srcp.exportparams)
        return srcsum
    
 
    
    
    def getsubblock(self, bigblock, level, precparams):
        indexes = np.lexsort([bigblock[level+1]])
        bigblock = bigblock.transpose()[indexes].transpose()
        if level == len(precparams)-1:
            self.finalblock = np.concatenate((self.finalblock, bigblock), axis = 1)
            return
                
        starti = [0]
        for i in range(1,len(indexes)):
            if abs(bigblock[level+1][i] - bigblock[level+1][i-1]) > precparams[level]:
                starti = starti + [i]
        endi = []
        #for j in range(1,len(starti)-1):
        #    endi = endi + [starti[j]-1]
        #endi = endi + [len(indexes)]
        
        for k in range(len(starti)):
            smallblock = []
            for i in range(len(bigblock)):
                if k < len(starti)-1:
                    smallblock = smallblock + [bigblock[i][starti[k]:starti[k+1]]]
                else:
                    smallblock = smallblock + [bigblock[i][starti[k]:]]
                
            smallblock = np.array(smallblock)
            self.getsubblock(smallblock, level + 1, precparams)
                
        True
            
                
    #**************************************************************************************
    def Combine2thSets(self):
        srcsum = Srcpar(self.config)
        srcp = copy.copy(self)
        #setparams = srcp.precparams.keys()
        setparams = list(srcp.precparams.keys())
        srcsum.ylabel = srcp.ylabel
        
        if "stth" in setparams: setparams.remove("stth")
        setparams.append("stth")            #Make sure it is last in the list
        #if not srcp.precparams.has_key("stth"): srcp.precparams["stth"] = 0.01
        if not "stth" in srcp.precparams.keys(): srcp.precparams["stth"] = 0.01
            
        sortedprms = np.array([[0.0]*(1+len(setparams))])
        
        for i in range(1, len(srcp.dataset)):
            dset = srcp.dataset[i]
            if "stth" not in dset.prm: dset.prm["stth"]="90.0"
            expanded = np.array([np.append([[i]], [float(dset.prm[st]) for st in setparams])])
            sortedprms = np.append(sortedprms, expanded,axis=0)
            True
        sortedprms = sortedprms[1:].transpose()
        #indexes = np.lexsort([sortedprms[s] for s in range(len(sortedprms)-1,0,-1)])        # s will be something like [4, 3, 2, 1]
        #sortedprms = sortedprms[1:]
        precparams = []
        for prm in setparams:  precparams = precparams + [srcp.precparams[prm]]
        
        self.finalblock = np.zeros((len(sortedprms),1))
        self.getsubblock(sortedprms,0,precparams)
       
        sortedprms = self.finalblock.transpose()[1:]
        #sortedprms = sortedprms[indexes]
        
        setidxrange = [0]
        for i in range(1, len(sortedprms)):     #determine the i
            dontsumset = [np.abs(sortedprms[i][s+1] - sortedprms[i-1][s+1]) <= srcp.precparams[setparams[s]] for s in range(len(setparams)-1)]
            #dontsum = False in [np.abs(sortedprms[i][s+1] - sortedprms[i-1][s+1]) <= srcp.precparams[setparams[s]] for s in range(len(setparams)-1)]
            if len(dontsumset) == 0 :
                dontsum = False
            else:
                dontsum = False in dontsumset
            
            if dontsum: setidxrange.append(i)
        setidxrange.append(len(sortedprms))
        datasetrange = []
        for i in range(1, len(setidxrange)):
            aset = sortedprms.transpose()[0][range(setidxrange[i-1],setidxrange[i])]
            datasetrange.append(aset.astype(int))
        x_2th = srcp.dataset[1].currframe.x_2th           #This is the full range
        
        just_sum = srcp.preps["just_sum"]
        if just_sum:
            addlist = []
            for key in srcp.dataset[0].prm.keys():
                if key.rfind("counts")>=0 or key.rfind("time")>=0 : addlist = addlist + [key]
            
        
        for aset in datasetrange:
            dset1_set = srcp.dataset[aset[0]]
            dset1 = dset1_set.currframe
            #if len(aset)==1: aset = np.append(aset,aset[0])
            
            if len(aset)==1:
                #srcsum.AddData(dset1.y, dset1_set.prm, dset1_set.detprm, dset1_set.origin+" - Post Process", dset1_set.filename, {"mm":dset1.x_mm})
                srcsum.AddData(np.asfarray(dset1.y), dset1_set.prm, dset1_set.detprm, dset1_set.origin+" - Post Process", dset1_set.filename, {"2th":dset1.x_2th})
                
            else:
                newprms = copy.copy(dset1_set.prm)
                for i in aset[1:]:
                    dset2_set = srcp.dataset[i]
                    dset2 = dset2_set.currframe
                    idxin1=np.where(np.in1d(dset1.x_2th_reg, dset2.x_2th_reg, True))[0]
                    idxin2=np.where(np.in1d(dset2.x_2th_reg, dset1.x_2th_reg, True))[0]
                    if len(idxin1)>0 and len(idxin2)>0:       #there are some overlap
                        x_2th = dset1.x_2th_reg[0:idxin1[0]]
                        y = dset1.y_reg[0:idxin1[0]]
                        x_2th = np.append(x_2th, dset1.x_2th_reg[idxin1])


                        if just_sum:
                            yave = (dset1.y_reg[idxin1] + dset2.y_reg[idxin2])
                            for key in addlist:         #Add the 'time' and 'count' values of the parameters
                                newprms[key] = str(float(newprms[key]) + float(dset2_set.prm[key]))
                                True
                        else:   #average the overlapping part
                            yave = (dset1.y_reg[idxin1] + dset2.y_reg[idxin2]) / 2.0
                            newprms = dset2_set.prm
                        y = np.append(y, yave)
                        x_2th = np.append(x_2th, dset2.x_2th_reg[idxin2[-1]+1:-1])
                        y = np.append(y, dset2.y_reg[idxin2[-1]+1:-1])
                        
                    else:           #No overlap, will have to stitch together with 'zero' datapoints
                        y = dset1.y_reg
                        dreggrid = dset1.x_2th_reg[1]-dset1.x_2th_reg[0]
                        x_2th_empty = np.linspace(dset1.x_2th_reg[-1]+dreggrid, dset2.x_2th_reg[0]-dreggrid, retstep =dreggrid)[0]
                        y_2th_empty = [0.0]*len(x_2th_empty)
                        x_2th = np.append(dset1.x_2th_reg, x_2th_empty)
                        x_2th = np.append(x_2th, dset2.x_2th_reg)
                        y = np.append(dset1.y_reg,y_2th_empty)
                        y = np.append(y,dset2.y_reg)
                        
                        
                        True
                        
                    
                    srcsum.x_2th_reg=x_2th
                    srcsum.y_reg = y
                    dset1 = srcsum

                    
                    True
                dset2_set.detprm["stth"] = (max(srcsum.x_2th_reg) - min(srcsum.x_2th_reg))/2.0 + min(srcsum.x_2th_reg)
                srcsum.AddData(srcsum.y_reg, newprms, dset2_set.detprm, dset2_set.origin+" - Post Process", dset2_set.filename, {"2th":srcsum.x_2th_reg})
                True
            
        srcsum.CalcAllAxis()
        srcsum.precparams = copy.copy(srcp.precparams)
        return srcsum
    
    
        #**************************************************************************************
    def BackupCombine2thSets(self):
        srcsum = Srcpar(self.config)
        srcp = copy.copy(self)
        setparams = srcp.precparams.keys()
        srcsum.ylabel = srcp.ylabel
        
        if "stth" in setparams: setparams.remove("stth")
        setparams.append("stth")            #Make sure it is last in the list
        #if not srcp.precparams.has_key("stth"): srcp.precparams["stth"] = 0.01
        if "stth" not in srcp.precparams.keys(): srcp.precparams["stth"] = 0.01
            
        sortedprms = np.array([[0.0]*(1+len(setparams))])
        
        for i in range(1, len(srcp.dataset)):
            dset = srcp.dataset[i]
            expanded = np.array([np.append([[i]], [float(dset.prm[st]) for st in setparams])])
            sortedprms = np.append(sortedprms, expanded,axis=0)
            True
        sortedprms = sortedprms[1:].transpose()
        indexes = np.lexsort([sortedprms[s] for s in range(len(sortedprms)-1,0,-1)])        # s will be something like [4, 3, 2, 1]
        sortedprms = sortedprms.transpose()
        sortedprms = sortedprms[indexes]
        
        setidxrange = [0]
        for i in range(1, len(sortedprms)):     #determine the i
            dontsumset = [np.abs(sortedprms[i][s+1] - sortedprms[i-1][s+1]) <= srcp.precparams[setparams[s]] for s in range(len(setparams)-1)]
            #dontsum = False in [np.abs(sortedprms[i][s+1] - sortedprms[i-1][s+1]) <= srcp.precparams[setparams[s]] for s in range(len(setparams)-1)]
            if len(dontsumset) == 0 :
                dontsum = False
            else:
                dontsum = False in dontsumset
            
            if dontsum: setidxrange.append(i)
        setidxrange.append(len(sortedprms))
        datasetrange = []
        for i in range(1, len(setidxrange)):
            aset = sortedprms.transpose()[0][range(setidxrange[i-1],setidxrange[i])]
            datasetrange.append(aset.astype(int))
        x_2th = srcp.dataset[1].currframe.x_2th           #This is the full range
        
        for aset in datasetrange:
            dset1_set = srcp.dataset[aset[0]]
            dset1 = dset1_set.currframe
            #if len(aset)==1: aset = np.append(aset,aset[0])
            if len(aset)==1:
                srcsum.AddData(dset1.y, dset1_set.prm, dset1_set.detprm, dset1_set.origin+" - Post Process", dset1_set.filename)
                
            else:
                for i in aset[1:]:
                    dset2_set = srcp.dataset[i]
                    dset2 = dset2_set.currframe
                    idxin1=np.where(np.in1d(dset1.x_2th_reg, dset2.x_2th_reg, True))[0]
                    idxin2=np.where(np.in1d(dset2.x_2th_reg, dset1.x_2th_reg, True))[0]
                    x_2th = dset1.x_2th_reg[0:idxin1[0]]
                    y = dset1.y_reg[0:idxin1[0]]
                    x_2th = np.append(x_2th, dset1.x_2th_reg[idxin1])
                    yave = (dset1.y_reg[idxin1] + dset2.y_reg[idxin2]) / 2.0
                    y = np.append(y, yave)
                    x_2th = np.append(x_2th, dset2.x_2th_reg[idxin2[-1]+1:-1])
                    y = np.append(y, dset2.y_reg[idxin2[-1]+1:-1])
                    srcsum.x_2th_reg=x_2th
                    srcsum.y_reg = y
                    dset1 = srcsum
                    
                    True
                dset2_set.detprm["stth"] = (max(srcsum.x_2th_reg) - min(srcsum.x_2th_reg))/2.0 + min(srcsum.x_2th_reg)
                srcsum.AddData(srcsum.y_reg, dset2_set.prm, dset2_set.detprm, dset2_set.origin+" - Post Process", dset2_set.filename, {"2th":srcsum.x_2th_reg})
                True
            
        srcsum.CalcAllAxis()
        srcsum.precparams = copy.copy(srcp.precparams)
        return srcsum
    
    
    #**************************************************************************************
    def Scale(self, factor):
        srcp=self
        if (factor == 1) or (factor ==""): return
        for i in range(0, len(srcp.dataset)):
            src_currframe = srcp.dataset[i].currframe
            src_currframe.y *= factor
            src_currframe.y_2th *= factor
            src_currframe.y_reg *= factor
            src_currframe.y_reg_full2th *= factor
            src_currframe.y_min = min(src_currframe.y)
            src_currframe.y_max = max(src_currframe.y)
            True
        srcp.ylabel = srcp.ylabel + " * " + str(factor)
        
    #**************************************************************************************
    def StthOffset(self, shift):
        srcp=self
        if (shift == "0") or (shift ==""): return srcp
        offset = -1.0*float(shift)
        for i in range(1, len(srcp.dataset)):
            #dset = copy.copy(srcp.dataset[i].currframe)
            dset = (srcp.dataset[i].currframe)
            dset.x_2th = dset.x_2th+offset
            dset.x_2th_min = min(dset.x_2th)
            dset.x_2th_max = max(dset.x_2th)
            srcp.dataset[i].frame = {}
            srcp.dataset[i].frame["raw"] = dset
            srcp.dataset[i].currframe = srcp.dataset[i].frame["raw"]
            True
        return srcp
        True        
