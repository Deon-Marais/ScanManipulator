'''
Created on 10 Mar 2015

@author: Deon
'''

from PyQt4.QtGui import QGroupBox as QGroupBox
from Fit.EntryCurveOptionsGUI import Ui_EntryCurveOptions

class EntryCurveOptionsDEF(QGroupBox):
    def __init__(self, myparent=""):
        QGroupBox.__init__(self)
        self.name = "EntryCurveOptions"
        self.ui = Ui_EntryCurveOptions()
        self.ui.setupUi(self)
        self.scanman = myparent.scanman
        
    def typeChanged(self):
        fitbox = self.scanman.ui.fitGroupBox
        
        notenable = []
        if self.ui.wall_check.isChecked():
            if self.ui.reflection_radio.isChecked():  notenable = []
            elif self.ui.transmission_radio.isChecked():  notenable = ['Absorption']
            elif self.ui.zscan_radio.isChecked(): notenable = ['Absorption', 'Theta']
        else:
            if self.ui.reflection_radio.isChecked():  notenable = ['Thickness']
            elif self.ui.transmission_radio.isChecked():  notenable = ['Thickness', 'Absorption']
            elif self.ui.zscan_radio.isChecked(): notenable = ['Thickness', 'Absorption', 'Theta']
 
        iterkeys = fitbox.iterparams
        for rng in fitbox.rangeList:
            for i in range(len(iterkeys)):
                rng.iterparams[iterkeys[i]].enabled = True
            for akey in notenable:
                rng.iterparams[akey].enabled = False
                rng.iterparams[akey].fix = True
                        
            True
                    #gparams[i] = rng.iterparams[iterkeys[i]].value
                    #gparamsfix[i] = 1
                    
            True
            
        fitbox.FitRange()
        self.scanman.ui.graph.draw()
        True
        