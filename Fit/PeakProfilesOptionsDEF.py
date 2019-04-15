'''
Created on 10 Mar 2015

@author: Deon
'''

from PyQt4.QtGui import QGroupBox as QGroupBox
from Fit.PeakProfilesOptionsGUI import Ui_PeakProfilesOptions
#from BackgroundOptionsGUI import Ui_BackgroundOptions
import Fit.BackgroundOptionsDEF

class ProfileParams():
    def __init__(self,name):
        self.profilename = name
        self.iterparams = ['Channel']
        self.paramxy = {"Range_start":"x_chan","Range_end":"x_chan",'Channel':"x"}
        self.iterparams_values_format = {'Channel':'{0:.4f}', 'Position':'{0:.4f}', 'Angle':'{0:.4f}', 'd-spacing':'{0:.4f}'}
        self.iterparams_stdev_format = {'Channel':'{0:.3e}', 'Position':'{0:.3e}', 'Angle':'{0:.3e}', 'd-spacing':'{0:.3e}'}
        self.miscparams = []
        
    def additerparams(self,iterparams):
        self.iterparams = self.iterparams + iterparams
        
    def addparamxy(self,paramxy):
        self.paramxy.update(paramxy)
    
    def addvaluesformat(self,valuesformat):
        self.iterparams_values_format.update(valuesformat)
        
    def addstdevformat(self,stdevformat):
        self.iterparams_stdev_format.update(stdevformat)
        
    def addmiscparams(self,miscparams):
        self.miscparams = self.miscparams + miscparams
        

class PeakProfilesOptionsDEF(QGroupBox):
    def __init__(self, myparent=""):
        QGroupBox.__init__(self)
        self.name = "PeakProfilesOptions"
        self.ui = Ui_PeakProfilesOptions()
        self.ui.setupUi(self)
        self.scanman = myparent.scanman
        
        self.ui.backgroundGroupBox.hide()
        self.ui.backgroundLayout.removeWidget(self.ui.backgroundGroupBox)
        self.ui.backgroundGroupBox=BackgroundOptionsDEF.BackgroundOptionsDEF(self)
        self.ui.backgroundLayout.addWidget(self.ui.backgroundGroupBox)
        self.ui.backgroundLayout.update()
        self.ui.backgroundGroupBox.show()
        
        self.peaktype = {}
        gauss = ProfileParams("Gauss")
        gauss.additerparams(['FWHM', 'Intensity', 'Background'])
        gauss.addparamxy({'FWHM':"del_x", 'Intensity':"del_y", 'Background':"y"})
        gauss.addvaluesformat({'FWHM':"{0:0.4f}", 'Intensity':"{0:.4f}", 'Background':"{0:.4f}"})
        gauss.addstdevformat({'FWHM':"{0:.3e}", 'Intensity':"{0:.3e}", 'Background':"{0:.3e}"})
        gauss.addmiscparams(['Intensity_sum','Intensity_area','Counts'])
        self.peaktype["Gauss"]=gauss
        
        lorentz = ProfileParams("Lorentz")
        lorentz.additerparams(['FWHM2', 'Intensity', 'Background'])
        lorentz.addparamxy({'FWHM2':"del_x", 'Intensity':"del_y", 'Background':"y"})
        lorentz.addvaluesformat({'FWHM2':"{0:0.4f}", 'Intensity':"{0:.4f}", 'Background':"{0:.4f}"})
        lorentz.addstdevformat({'FWHM2':"{0:.3e}", 'Intensity':"{0:.3e}", 'Background':"{0:.3e}"})
        lorentz.addmiscparams(['Intensity_sum','Intensity_area','Counts'])
        self.peaktype["Lorentz"]=lorentz 
        
        True
        
        
    def typeChanged(self,newselection):
        fitbox = self.scanman.ui.fitGroupBox
        newpeaktype = self.peaktype[str(newselection)]
        #newpeaktype.rangetbl = fitbox.ui.range_tbl
        
        
        parentprofile = self.parent()
        parentprofile.iterparams=newpeaktype.iterparams
        parentprofile.miscparams = newpeaktype.miscparams
        parentprofile.iterparams_values_format = newpeaktype.iterparams_values_format
        parentprofile.iterparams_stdev_format = newpeaktype.iterparams_stdev_format
        parentprofile.paramxy = newpeaktype.paramxy
        

        parentprofile.SetVLables(parentprofile.rangeparams, parentprofile.iterparams, parentprofile.miscparams, parentprofile.fitparams) #Also creates the rownumbers list
        parentprofile.axislinked[str(parentprofile.rownumbers["Channel"])] = "Channel"

        
        #notenable = []
        #if self.ui.reflection_radio.isChecked():  notenable = ['Thickness']
        #elif self.ui.transmission_radio.isChecked():  notenable = ['Thickness', 'Absorption']
        #elif self.ui.zscan_radio.isChecked(): notenable = ['Thickness', 'Absorption', 'Theta']
        #elif self.ui.wall_radio.isChecked():  notenable = ['Absorption']
        #iterkeys = fitbox.iterparams
        #for rng in fitbox.rangeList:
        #    for i in range(len(iterkeys)):
        #        rng.iterparams[iterkeys[i]].enabled = True
        #    for akey in notenable:
        #        rng.iterparams[akey].enabled = False
        #        rng.iterparams[akey].fix = True
                        
        #    True
                    #gparams[i] = rng.iterparams[iterkeys[i]].value
                    #gparamsfix[i] = 1
                    
        #    True
            
        parentprofile.FitRange()
        self.scanman.ui.graph.draw()
        True
        
        