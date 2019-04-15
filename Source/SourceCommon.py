'''
Created on 17 Jul 2014

@author: Deon
'''
from Source import Srcpar

class SourceCommon(object):
    '''
    All Source plugins should inherit from this
    '''

    def __init__(self, ScanmanMain):
        self.scanman = ScanmanMain
        #self.config = self.scanman.config["source"]
        self.config = self.scanman.config
        self.src = Srcpar.Srcpar(self.config)
        self.paramdict = {}
        self.detdict = {}
        self.filelist = []
        self.name = ""

        self.srcp = Srcpar.Srcpar(self.config)     #Source post process
        self.srcsplit = Srcpar.Srcpar(self.config)     #Source with detector splitted
        
        
        
    #**************************************************************************************
    def PostprocessDirty(self,lowchan=-1, upchan=-1):
        self.scanman.ui.sourceGroupBox.srcp.preps["postdirty"] = True
        if lowchan == upchan:
            for filei in self.filelist:
                filei.srcp.preps["postdirty"] = True
            return
        else:
            for filei in self.filelist:
                filei.srcp.preps["postdirty"] = True
                filei.srcsplit.lowerchan=lowchan
                filei.srcsplit.upperchan=upchan
        
    #**************************************************************************************
    
                
