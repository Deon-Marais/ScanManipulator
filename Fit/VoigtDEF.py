'''
Created on 08 May 2014

@author: Deon
'''
from PyQt4.QtGui import QGroupBox as QGroupBox
#from EntryCurveGUI import Ui_EntryCurve
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtCore
from pylab import np
import sys
from matplotlib.lines import Line2D
from scanlib import gauss
#from pyspec import fit, fitfuncs
from thirdparty.pyspec import fitfuncs
from thirdparty.pyspec import fit      #This is the exact one from pyspec, but modified in the way that the stdev is calculated for mpfit


from Fit.FitCommon import *


def voigt(x, p, mode='eval'):
    """Pearson Type VII
    From Hutchings et al. 2005. Introduction to the characterisation of residual stress by neutron diffraction.2005. Page 160

    Function:
       :math:`f(x) = k + m*x + p_2 \exp\left(\\frac{-(x - p_0)^2}{2p_1^2}\\right)`

    """
    try:
        if mode == 'eval':
            #cent=p[0];wid=p[1];amp=p[2];const=p[3];slope=p[4]
            x0=p[0]; ux=p[1]; H0=p[2]; const=p[3];slope=p[4]; m=p[5]
            
            out = H0*(1+(x-x0)**2.0/((1.0/m)*(0.5*ux)**2))**-(1.0/m) + const+slope*x
        elif mode == 'params':
            out = ['cent', 'sigma', 'amp', 'const', 'slope', 'shape']
        elif mode == 'name':
            out = "Voigt"
        elif mode == 'guess':
            g = fitfuncs.peakguess(x, p)
            out = [g[0], g[1], g[3],g[5], g[4], 0.5]
        else:
            out = []
    except:
        out = [0,0,0,0,0,0]

    return np.array(out)

#**************************************************************************************
#**************************************************************************************
class VoigtDEF(FitCommon,QGroupBox):
    def __init__(self, ScanmanMain):
        FitCommon.__init__(self, ScanmanMain)
        
        #self.ui.moreOptionsGroupBox.hide()
        #self.ui.moreOptionsLayout.removeWidget(self.ui.moreOptionsGroupBox)
        #self.ui.moreOptionsGroupBox=EntryCurveOptionsDEF.EntryCurveOptionsDEF(self)
        #self.ui.moreOptionsLayout.addWidget(self.ui.moreOptionsGroupBox)
        #self.ui.moreOptionsLayout.update()
        #self.ui.moreOptionsGroupBox.show()
        
        self.name = "Voigt"
        #self.paramxy.update({'Channel':"x", 'Intensity':"del_y", 'Slit':"min=0.0 max=10.0", 'Theta':"min=0.0 max=180.0", 'Background':"y", 
        #                     'Thickness':"del_x", 'Absorption':"min=0.0 max=2.0"})
        #self.iterparams = ['Channel', 'Intensity', 'Slit', 'Theta', 'Background', 'Thickness', 'Absorption']
        #self.iterparams_values_format = {'Channel':'{0:.2f}', 'Position':'{0:.2f}', 'Angle':'{0:.2f}', 'd-spacing':'{0:.5f}', 
        #                                'Intensity':"{0:.2f}", 'Slit':"{0:.2f}", 'Theta':"{0:.2f}", 
        #                                'Background':"{0:.2f}", 'Thickness':"{0:.3f}", 'Absorption':"{0:.4f}"}
        #self.iterparams_stdev_format = {'Channel':'{0:.2f}', 'Position':'{0:.2f}', 'Angle':'{0:.2f}', 'd-spacing':'{0:.5f}', 
        #                               'Intensity':"{0:.2f}", 'Slit':"{0:.2f}", 'Theta':"{0:.2f}", 
        #                               'Background':"{0:.2f}", 'Thickness':"{0:.2f}", 'Absorption':"{0:.4f}"}
        self.paramxy.update({'Channel':"x", 'FWHM':"del_x", 'Intensity':"del_y", 'Background':"y", 'Slope':"min=-10.0 max=10.0",'Shape':"min=0.0001 max=1.0"})
        self.iterparams = ['Channel', 'FWHM', 'Intensity', 'Background', 'Slope', 'Shape']
        self.iterparams_values_format = {'Channel':'{0:.4f}', 'Position':'{0:.4f}', 'Angle':'{0:.4f}', 'd-spacing':'{0:.4f}', 
                                        'FWHM':"{0:0.4f}", 'Intensity':"{0:.4f}", 'Background':"{0:.4f}",'Slope':"{0:.4f}", 'Shape':"{0:.4f}"}
        self.iterparams_stdev_format = {'Channel':'{0:.3e}', 'Position':'{0:.3e}', 'Angle':'{0:.3e}', 'd-spacing':'{0:.3e}', 
                                        'FWHM':"{0:.3e}", 'Intensity':"{0:.3e}", 'Background':"{0:.3e}",'Slope':"{0:.3e}", 'Shape':"{0:.3e}"}
         
       
        self.miscparams = ['Intensity_sum','Intensity_area','Counts']

        self.SetVLables(self.rangeparams, self.iterparams, self.miscparams, self.fitparams) #Also creates the rownumbers list
        self.axislinked[str(self.rownumbers["Channel"])] = "Channel"
        True
        
        
    #**************************************************************************************
    
    def FitRange(self, rngnum=-1):
        #FitCommon.FitRange(self, rngnum=rngnum)
        rngtbl=self.ui.range_tbl
        start = rngnum
        end = rngnum +1
        if (rngnum == -1):
            start = 0
            end = len(self.rangeList)

        #self.CalcBG()
        
        #wedisconnected = False
        #try:
        #    rngtbl.cellChanged.disconnect()     #otherwise this function might be called recursively
        #    wedisconnected = True
        #except:
        #    True
        
        for i in range(start, end): 
            rng = self.rangeList[i]
            #xdata = rng.line.get_xdata(True)
            #ydata = rng.line.get_ydata(True)
            xdata = np.asfarray(self.scanman.datasrc.x[rng.rangeparams["Range_start"].value:rng.rangeparams["Range_end"].value])
            ydata = np.asfarray(self.scanman.datasrc.y[rng.rangeparams["Range_start"].value:rng.rangeparams["Range_end"].value])
            xwidth = xdata[1:]-xdata[:-1]
            xmin, xmax, ymin, ymax = np.asfarray([xdata.min(), xdata.max(), ydata.min(), ydata.max()])
             
            if ((len(xdata) < 4) or (len(ydata) < 4)): continue                 #break out if the range was chosen wrong
            #if (min(ydata) == max(ydata)): continue                             #break out is there is no difference in values
            
            fitfunct = voigt
                          
            gparams = fitfunct(xdata, ydata, 'guess')
            gparamsfix = [0]*len(gparams)

            #if rng.iterparams.has_key("Channel"): xkey = "Channel"
            #elif rng.iterparams.has_key("Position"): xkey = "Position"
            #elif rng.iterparams.has_key("Angle"): xkey = "Angle"
            #elif rng.iterparams.has_key("d-spacing"): xkey = "d-spacing"
            if "Channel" in rng.iterparams.keys(): xkey = "Channel"
            elif "Position" in rng.iterparams.keys(): xkey = "Position"
            elif "Angle" in rng.iterparams.keys(): xkey = "Angle"
            elif "d-spacing" in rng.iterparams.keys(): xkey = "d-spacing"

            #iterkeys = [xkey, 'Intensity', 'Slit', 'Theta', 'Background', 'Thickness', 'Absorption']
            iterkeys = [xkey]+self.iterparams[1:]
            for i in range(len(iterkeys)):
                if rng.iterparams[iterkeys[i]].fix == True or rng.iterparams[iterkeys[i]].enabled == False:
                    gparams[i] = rng.iterparams[iterkeys[i]].value
                    gparamsfix[i] = 1
            
            
            fitob = fit.fit(x=xdata, y=ydata, guess=gparams, ifix=gparamsfix ,quiet=True, 
                            funcs=[fitfunct], optimizer = "mpfit", r2min=-1000000)
            minbgnd = -100.0
            if gparamsfix[4] == 1 and gparams[4] == 0.0:
                minbgnd = 0.0
                
            limits = ([xmin,xmax],[0.0,xmax-xmin],[0.0,ymax],[minbgnd,ymax],[-100.0,100.0],[0.0001, 0.9999])
            fitob.ilimits = np.array(limits)
            limited = np.array([[1,1]]*len(limits))
            fitob.ilimited = limited
#mpfit
            if 1:#else:
                fitob.go(interactive=False)
                gparams=fitob.result
                stdev=fitob.stdev
                #rng.bgndfitparms[1] = gparams[3]
                #rng.bgndfitparms[0] = gparams[4]
                xexpanded = np.linspace(xdata.min(), xdata.max(), 50)
                fittedexpanded = fitfunct(xexpanded,gparams)
                fitted = fitfunct(xdata,gparams)

            rng.fittedline.set_data(xexpanded, fittedexpanded)
            rng.diffline.set_data(xdata, ydata - fitted)
            
            for i in range(len(iterkeys)):
                rng.iterparams[iterkeys[i]].value = gparams[i]
                rng.iterparams[iterkeys[i]].stdev = stdev[i]
            
            self.asignfitparamvalues(rng.fitparams,fitob)
            
            ybgnd = fitfuncs.linear(xdata, [gparams[4],gparams[3]],"eval") 
            rng.miscparams['Intensity_sum'].value = np.sum(fitted-ybgnd) 
            rng.miscparams['Intensity_area'].value = np.sum(abs((fitted-ybgnd)[:-1]*xwidth))
            rng.miscparams['Counts'].value = np.sum(ydata)
            
            
            #Determine if the calculated fits are valid based on some 'obvious' rules
            rng.iterparams["Intensity"].valid = False if rng.iterparams["Intensity"].value < 0 else True
            for key in iterkeys:
                curkey = rng.iterparams[key]
                curkey.valid = True
                if curkey.stdev / curkey.value > 1 or (curkey.stdev == 0.0 and curkey.fix == False): curkey.valid = False
            
            
            self.ReflectInTable(rng.iterparams,self.iterparams_values_format,self.iterparams_stdev_format)
            self.ReflectInTable(rng.miscparams)
            self.ReflectInTable(rng.fitparams)
                
        #self.scanman.ui.graph.draw()
        
        ymin = y = 0.0
        ymax = x = 0.0
        for rng in self.rangeList:
            if (len(rng.diffline._y) > 0):
                y = min(rng.diffline.get_ydata(True))
                if (y < ymin): ymin = y
                y = max(rng.diffline.get_ydata(True))
                if (y > ymax): ymax = y
        ybuf = (ymax - ymin) * 0.1
        self.scanman.ui.diffgraph.figure.axes[0].set_ylim(ymin - ybuf, ymax + ybuf)
            
                 
        #self.scanman.ui.diffgraph.draw()
        
    
        #if (wedisconnected): rngtbl.cellChanged.connect(self.CellValueChanged)   #Reconnect the signal
        #self.fittedsignal.emit()        #To call any listeners
        True
    
    
    
    #**************************************************************************************
    def Test(self):
        print ("yeye")
        self.FitRange(-1)
        
        
    #**************************************************************************************
if __name__ == '__main__':
    
    app = qt.QApplication(sys.argv)
    window=EntryCurveDEF()
    window.show()
    sys.exit(app.exec_())

        