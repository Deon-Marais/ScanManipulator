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
import thirdparty.pyspec.fit   as fit   #This is the exact one from pyspec, but modified in the way that the stdev is calculated for mpfit


from Fit.FitCommon import *
import Fit.PeakProfilesOptionsDEF



def Gauss(x, p, mode='eval'):
    """Gaussian defined by amplitide

    Function:
       :math:`f(x) = k + m*x + p_2 \exp\left(\\frac{-(x - p_0)^2}{2p_1^2}\\right)`

    """
    try:
        if mode == 'eval':
            cent=p[0];wid=p[1];amp=p[2];const=p[3];slope=p[4]
            #out = const + amp * np.exp(-1.0 * (x - cent)**2 / (2 * wid**2))
            #Inserted the 0.5* because we want FWHM out, not HWHM
            #out = const + slope*x + amp * np.exp(-1.0 * (x - cent)**2 / (2 * (0.5*wid)**2))
            conversion =2.0*np.sqrt(2.0*np.log(2))      #Hutchings et al. Introduction to the characterisation of residual stress by neutron diffraction.2005. Page 159 
            #conversion = 2.0
            out = const + slope*x + amp * np.exp(-1.0 * (x - cent)**2 / (2 * (wid/conversion)**2))
        elif mode == 'params':
            out = ['cent', 'sigma', 'amp', 'const', 'slope']
        elif mode == 'name':
            out = "Gaussian"
        elif mode == 'guess':
            g = fitfuncs.peakguess(x, p)
            out = [g[0], g[1] / (4 * np.log(2)), g[3], g[4], g[5]]
        else:
            out = []
    except:
        out = [0,0,0,0,0]

    return np.array(out)

#**************************************************************************************
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




def zscan(xvals, p):
    #position=p[0];  intensity=p[1]; slit=p[2];  stth=p[3];  background=p[4];  thickness=p[5];  absorption=p[6]
    x0=p[0];        i0=p[1];        w=p[2];     theta=p[3];  ib=p[4];    thick=p[5];   u=p[6];
    p0 = w/2.0
    
    #b=p[4];     m=p[1];     a=p[2];     x0=p[0]
    #out = b+(m-b)/(1+np.exp(-a*(xvals-x0)))
    out=[]
    for x in xvals:          
        if x < (x0 - p0):
            val = ib
        elif (x > (x0 - p0)) and (x < (x0+p0)):
            val = ib + i0*(x-(x0-p0))/(2*p0)
        else:
            val = ib + i0
        out = out + [val]
    return np.array(out)

def zscanreverse(xvals, p, mode='eval'):
    try:
        if mode == 'eval':
            xvals = xvals * -1.0
            prms = p.copy()
            prms[0] = -prms[0]
            out = zscan(xvals, prms)
            True
        elif mode == 'params':
            #out = ['cent', 'sigma', 'amp', 'const', 'slope']
            out = ['position', 'intensity', 'slit', 'theta', 'background', 'thickness', 'absorption']
        elif mode == 'name':
            out = "ZScan_Reverse"
        elif mode == 'guess':
            xmin, xmax, ymin, ymax = [xvals.min(), xvals.max(), p.min(), p.max()]
            out = [xmin+(xmax-xmin)/2.0, ymax-ymin, (xmax-xmin)/3.0, 45.0, ymin, 0.0, 0.01]
            True
        else:
            out = []
    except:
        out = np.array([0]*len(p))

    return out

#**************************************************************************************
def zscandirect(xvals, p, mode='eval'):
    try:
        if mode == 'eval':
            out = zscan(xvals, p)
            True
        elif mode == 'params':
            #out = ['cent', 'sigma', 'amp', 'const', 'slope']
            out = ['position', 'intensity', 'slit', 'theta', 'background', 'thickness', 'absorption']
        elif mode == 'name':
            out = "Reflection_Direct"
        elif mode == 'guess':
            xmin, xmax, ymin, ymax = [xvals.min(), xvals.max(), p.min(), p.max()]
            out = [xmin+(xmax-xmin)/2.0, ymax-ymin, (xmax-xmin)/3.0, 45.0, ymin, 0.0, 0.01]
            True
        else:
            out = []
    except:
        out = np.array([0]*len(p))

    return out

#**************************************************************************************
def reflection(xvals, p):
    #position=p[0];  intensity=p[1]; slit=p[2];  stth=p[3];  background=p[4];  thickness=p[5];  absorption=p[6]
    x0=p[0];        i0=p[1];        w=p[2];     theta=p[3];  ib=p[4];    thick=p[5];   u=p[6];
    th = np.deg2rad(theta)
    p0 = w * np.sin(th)/np.sin(2*th) 
    out = []
    for x in xvals:          
        if x < (x0 - p0):
            val = ib
        elif ((x >= (x0-p0)) and (x < x0)):
            val = i0*((x-x0+p0)/u) - i0*(np.sin(th)/(2*u*u)) * (1-np.exp((-2*u/np.sin(th))*(x-x0+p0))) + ib
        elif ((x >= x0) and (x < (x0 + p0))):
            val = i0*(np.sin(th)/(2*u*u))*(np.exp((-2*u/np.sin(th))*(x-x0+p0))
                                           -2*np.exp((-2*u/np.sin(th))*(x-x0))+1)  + i0*((x0+p0-x)/u) + ib
        elif (x >= (x0 + p0)):
            val = i0*np.sin(th)/(2*u*u)*(np.exp(-2*u*(x-x0+p0)/np.sin(th))
                                         -2*np.exp(-2*u*(x-x0)/np.sin(th))
                                         +np.exp(-2*u*(x-x0-p0)/np.sin(th))) + ib
        out = out + [val]
    return np.array(out)
            
#**************************************************************************************
def reflection1(xvals, parms):
    #position=p[0];  intensity=p[1]; slit=p[2];  stth=p[3];  background=p[4];  thickness=p[5];  absorption=p[6]
    x0=parms[0];        i0=parms[1];        w=parms[2];     theta=parms[3];  ib=parms[4];
    thick=parms[5];   u=parms[6];
    th = np.deg2rad(theta)
    p = w*np.sin(th)
    Atot = w*w/np.sin(2.0*th)
    out = []
    ni = 5
    irng = np.array(range(1,ni+1))
    
    for x in xvals:          
        if x < (x0 - p):
            val = ib
        elif ((x0-p)<x and x0>x):
            l1 = x-(x0-p);
            nrleft = int(np.ceil(l1/(2*p)*ni));
            if nrleft < 1: nrleft = 1
            irngleft = np.array(range(1, nrleft+1))
            dl1 = l1/float(nrleft);     dl = irngleft * dl1
            triA = dl*dl/np.tan(th)                 #triangle areas
            secA = [triA[0]] + [triA[i]-triA[i-1] for i in range(1,nrleft)]     #section areas
            secA =np.array(secA)
            m1 = np.linspace(x0-p+dl1/2.0, x-dl1/2.0, nrleft)       #section midpoint position - path length calculated from this
            plen = np.abs(2*m1/np.sin(th))
            val = ib + np.sum(i0*secA*np.exp(-u*plen))
            
        elif (x0<=x) and (x0+p >= x):
            l1 = p; 
            nrleft = int(np.ceil(l1/(2*p)*ni));
            if nrleft < 1: nrleft = 1  
            irngleft = np.array(range(1, nrleft+1))
            dl1left = l1/float(nrleft)
            dlleft = irngleft *dl1left
            triAleft = dlleft*dlleft/np.tan(th)                 #triangle areas
            secAleft = [triAleft[0]] + [triAleft[i]-triAleft[i-1] for i in range(1,nrleft)]     #section areas
            secAleft =np.array(secAleft)
            m1left = np.linspace(x0-p+dl1left/2.0, x0-dl1left/2.0, nrleft)+(x-x0)
            plenleft = np.abs(2*m1left/np.sin(th))
            valleft = np.sum(i0*secAleft*np.exp(-u*plenleft))
            
            l2 = x-x0
            nrright = int(np.ceil(x-x0/(2*p)*ni));
            if nrright < 1: nrright = 1 
            irngright = np.array(range(1, nrright+1))
            dl1right = l2/float(nrright)
            dlright = p-np.append(0.0, dl1right*irngright)
            triAright = dlright*dlright/np.tan(th)
            secAright = [triAright[i]-triAright[i+1] for i in range(nrright)]
            secAright = np.array(secAright)
            m1right = np.linspace(x-x0-dl1right/2.0, dl1right/2.0, nrright)
            plenright = np.abs(2*m1right/np.sin(th))
            valright = np.sum(i0*secAright*np.exp(-u*plenright))
            
            val = ib + valleft + valright
        
        elif (x > x0+p):
            l1 = p; 
            #nrleft = int(np.ceil(l1/(x-(x0-p))*ni));  
            nrleft = int(np.ceil(l1/(2*p)*ni));
            if nrleft < 1: nrleft = 1 
            irngleft = np.array(range(1, nrleft+1))
            dl1left = l1/float(nrleft)
            dlleft = irngleft *dl1left
            triAleft = dlleft*dlleft/np.tan(th)                 #triangle areas
            secAleft = [triAleft[0]] + [triAleft[i]-triAleft[i-1] for i in range(1,nrleft)]     #section areas
            secAleft =np.array(secAleft)
            m1left = np.linspace(x0-p+dl1left/2.0, x0-dl1left/2.0, nrleft)+(x-x0)
            plenleft = np.abs(2*m1left/np.sin(th))
            valleft = np.sum(i0*secAleft*np.exp(-u*plenleft))
            
            l2 = p
            nrright = int(np.ceil(l2/(2*p)*ni));
            if nrright < 1: nrright = 1 
            irngright = np.array(range(1, nrright+1))
            dl1right = l2/float(nrright)
            dlright = p-np.append(0.0, dl1right*irngright)
            triAright = dlright*dlright/np.tan(th)
            secAright = [triAright[i]-triAright[i+1] for i in range(nrright)]
            secAright = np.array(secAright)
            m1right = np.linspace(dlright[0]-dl1right/2.0, dlright[-1] + dl1right/2.0, nrright) + (x-(x0+p))
            plenright = np.abs(2*m1right/np.sin(th))
            valright = np.sum(i0*secAright*np.exp(-u*plenright))
            
            val = ib + valleft + valright
            
        out = out + [val]
    return np.array(out)
            
    
    
    
#**************************************************************************************
def reflectionreverse(xvals, p, mode='eval'):
    """ From Brand et al.
    """
    try:
        if mode == 'eval':
            xvals = xvals * -1.0
            prms = p.copy()
            prms[0] = -prms[0]
            out = reflection(xvals, prms)
            True
        elif mode == 'params':
            #out = ['cent', 'sigma', 'amp', 'const', 'slope']
            out = ['position', 'intensity', 'slit', 'theta', 'background', 'thickness', 'absorption']
        elif mode == 'name':
            out = "Reflection_Reverse"
        elif mode == 'guess':
            xmin, xmax, ymin, ymax = [xvals.min(), xvals.max(), p.min(), p.max()]
            out = [xmin+(xmax-xmin)/2.0, ymax-ymin, (xmax-xmin)/3.0, 45.0, ymin, 0.0, 0.01]
            True
        else:
            out = []
    except:
        out = np.array([0]*len(p))

    return out
            

#**************************************************************************************
def reflectiondirect(xvals, p, mode='eval'):
    """ From Brand et al.
    """
    try:
        if mode == 'eval':
            out = reflection(xvals, p)
            True
        elif mode == 'params':
            #out = ['cent', 'sigma', 'amp', 'const', 'slope']
            out = ['position', 'intensity', 'slit', 'theta', 'background', 'thickness', 'absorption']
        elif mode == 'name':
            out = "Reflection_Direct"
        elif mode == 'guess':
            xmin, xmax, ymin, ymax = [xvals.min(), xvals.max(), p.min(), p.max()]
            out = [xmin+(xmax-xmin)/2.0, ymax-ymin, (xmax-xmin)/3.0, 45.0, ymin, 0.0, 0.01]
            True
        else:
            out = []
    except:
        out = np.array([0]*len(p))

    return out


#**************************************************************************************
def transmission(xvals, parms):
#position=p[0];  intensity=p[1]; slit=p[2];  stth=p[3];  background=p[4];  thickness=p[5];  absorption=p[6]
    #x0=p[0];        i0=p[1];        w=p[2];     theta=p[3];  ib=p[4];    thick=p[5];   u=p[6];
    #th = np.deg2rad(theta)
    #p0 = w * np.cos(th)/np.cos(2*th) 
    #out = []
    #for x in xvals:          
    #    if x < (x0 - p0):
    #        val = ib
    #    elif ((x>=x0-p0) and (x < x0)):
    #        val = i0*(x-x0+p0)*(x-x0+p0)+ib
    #    elif ((x>=x0) and (x<(x0+p0))):
    #        val = i0*(2.0*p0*p0-(x0+p0-x)*(x0+p0-x))+ib
    #    elif (x>=x0+p0):
    #        val=2*i0*p0*p0 +ib
    #    out = out + [val]
    x0=parms[0];        i0=parms[1];        w=parms[2];     theta=parms[3];
    ib=parms[4];        thick=parms[5];     u=parms[6];
    th = np.deg2rad(theta)
    p = w*np.cos(th)
    Atot = w*w/np.sin(2.0*th)
    out = []
    for x in xvals:
        if (x <= (x0-p)):
            val = ib
        elif ( (x > (x0-p)) and (x <= x0)):
            val = ib + i0*((x-(x0-p))*((x-(x0-p))*np.tan(th)))/Atot
        elif ((x > x0) and (x <= x0 + p)):
            val = ib + i0*(Atot-(x0+p-x)*(x0+p-x)*np.tan(th))/Atot
        elif (x>x0+p):
            val = ib + i0
        out = out + [val]
    return np.array(out)
            
    
    
#**************************************************************************************
def transmissiondirect(xvals, p, mode='eval'):
    """ From Brand et al.
    """
    try:
        if mode == 'eval':
            out = transmission(xvals, p)
            True
        elif mode == 'params':
            #out = ['cent', 'sigma', 'amp', 'const', 'slope']
            out = ['position', 'intensity', 'slit', 'theta', 'background', 'thickness', 'absorption']
        elif mode == 'name':
            out = "Transmission_Direct"
        elif mode == 'guess':
            xmin, xmax, ymin, ymax = [xvals.min(), xvals.max(), p.min(), p.max()]
            out = [xmin+(xmax-xmin)/2.0, ymax-ymin, (xmax-xmin)/3.0, 45.0, ymin, 0.0, 0.01]
            True
        else:
            out = []
    except:
        out = np.array([0]*len(p))

    return out

#**************************************************************************************
def transmissionreverse(xvals, p, mode='eval'):
    """ From Brand et al.
    """
    try:
        if mode == 'eval':
            xvals = xvals * -1.0
            prms = p.copy()
            prms[0] = -prms[0]
            out = transmission(xvals, prms)
            True
        elif mode == 'params':
            #out = ['cent', 'sigma', 'amp', 'const', 'slope']
            out = ['position', 'intensity', 'slit', 'theta', 'background', 'thickness', 'absorption']
        elif mode == 'name':
            out = "Transmission_Reverse"
        elif mode == 'guess':
            xmin, xmax, ymin, ymax = [xvals.min(), xvals.max(), p.min(), p.max()]
            out = [xmin+(xmax-xmin)/2.0, ymax-ymin, (xmax-xmin)/3.0, 45.0, ymin, 0.0, 0.01]
            True
        else:
            out = []
    except:
        out = np.array([0]*len(p))

    return out


#**************************************************************************************
def wall(xvals, parms):
#position=p[0];  intensity=p[1]; slit=p[2];  stth=p[3];  background=p[4];  thickness=p[5];  absorption=p[6]
    midpoint=parms[0];        i0=parms[1];        w=parms[2];     theta=parms[3];
    ib=parms[4];        thick=parms[5];     u=parms[6];
    midpoint = parms[0]
    x0 = midpoint - thick/2.0
    th = np.deg2rad(theta)
    p = w*np.cos(th)
    Atot = w*w/np.sin(2.0*th)
    out = []
    for x in xvals:
        if (x <= (x0-p)):
                val = ib
        #elif ((x0-p) >= (x-thick)) and ((x0+p) >= x):         #Gauge volume is smaller than thickness
        if ( (x > (x0-p)) and (x0-p>(x-thick)) and (x <= x0)):
            val = ib + i0*((x-(x0-p))*((x-(x0-p))*np.tan(th)))/Atot
        elif ((x > x0) and (x <= x0 + p) and (x0-p > (x-thick))) :
            val = ib + i0*(Atot-(x0+p-x)*(x0+p-x)*np.tan(th))/Atot
        elif (x0-p>(x-thick) and (x0+p < x)):   #Gauge volume is smaller than thickness
            val = ib + i0
        elif (x0-p<(x-thick) and (x0+p > x)):   #Gauge volume is larger than thickness
            A2 = (x0+p-x)*(x0+p-x)*np.tan(th)
            A3 = ((x-thick)-(x0-p))*(((x-thick)-(x0-p))*np.tan(th))
            val = ib + i0*(Atot-A2-A3)/Atot
        elif ((x0-p) < (x-thick)) and ((x0+p) < x) and (x0 >= (x-thick)):
            A3 = ((x-thick)-(x0-p))*(((x-thick)-(x0-p))*np.tan(th))
            val = ib + i0*(Atot-A3)/Atot
        elif (x0<(x-thick) and ((x0+p>=(x-thick)))):
            A2= (x0+p-(x-thick))*((x0+p)-(x-thick))*np.tan(th)
            val = ib + i0*(A2/Atot)
        elif (x0+p < (x-thick)):
            val = ib
            
        #elif ((x0-p) < (x-thick)) and ((x0+p) >= x):         #Gauge volume is larger than thickness
        #    A2 = (x0+p-x)*(x0+p-x)*np.tan(th)
        #    A3 = ((x-thick)-(x0-p))*(((x-thick)-(x0-p))*np.tan(th))
        #    val = ib + i0*(Atot-A2-A3)/Atot
        
        
        out = out + [val]
    return np.array(out)

#**************************************************************************************

def walldirect(xvals, p, mode='eval'):
    """ From Wang et al.
    """
    try:
        if mode == 'eval':
            out = wall(xvals, p)
            True
        elif mode == 'params':
            #out = ['cent', 'sigma', 'amp', 'const', 'slope']
            out = ['position', 'intensity', 'slit', 'theta', 'background', 'thickness', 'absorption']
        elif mode == 'name':
            out = "Wall_Direct"
        elif mode == 'guess':
            xmin, xmax, ymin, ymax = [xvals.min(), xvals.max(), p.min(), p.max()]
            out = [xmin+(xmax-xmin)/2.0, ymax-ymin, (xmax-xmin)/6.0, 45.0, ymin, (xmax-xmin)/3.0, 0.01]
            True
        else:
            out = []
    except:
        out = np.array([0]*len(p))

    return out

#**************************************************************************************
#**************************************************************************************
class PeakProfilesDEF(FitCommon,QGroupBox):
    def __init__(self, ScanmanMain):
        FitCommon.__init__(self, ScanmanMain)
        
        self.ui.moreOptionsGroupBox.hide()
        self.ui.moreOptionsLayout.removeWidget(self.ui.moreOptionsGroupBox)
        self.ui.moreOptionsGroupBox=PeakProfilesOptionsDEF.PeakProfilesOptionsDEF(self)
        self.ui.moreOptionsLayout.addWidget(self.ui.moreOptionsGroupBox)
        self.ui.moreOptionsLayout.update()
        self.ui.moreOptionsGroupBox.show()
        
        #self.ui.moreOptionsGroupBox.ui.backgroundGroupBox.hide()
        #self.ui.moreOptionsGroupBox.ui
        True
        
        self.name = "PeakProfiles"
        self.iterparams_values_format = {}
        self.iterparams_stdev_format = {}
        self.ui.moreOptionsGroupBox.typeChanged(self.ui.moreOptionsGroupBox.ui.profileComboBox.currentText())
        
        

        
        #self.paramxy.update({'Channel':"x", 'FWHM':"del_x", 'Intensity':"del_y", 'Background':"y", 'Slope':"min=-10.0 max=10.0",'Shape':"min=0.0001 max=1.0"})
        #self.iterparams = ['Channel', 'FWHM', 'Intensity', 'Background', 'Slope', 'Shape']
        #self.iterparams_values_format = {'Channel':'{0:.4f}', 'Position':'{0:.4f}', 'Angle':'{0:.4f}', 'd-spacing':'{0:.4f}', 
        #                                'FWHM':"{0:0.4f}", 'Intensity':"{0:.4f}", 'Background':"{0:.4f}",'Slope':"{0:.4f}", 'Shape':"{0:.4f}"}
        #self.iterparams_stdev_format = {'Channel':'{0:.3e}', 'Position':'{0:.3e}', 'Angle':'{0:.3e}', 'd-spacing':'{0:.3e}', 
        #                                'FWHM':"{0:.3e}", 'Intensity':"{0:.3e}", 'Background':"{0:.3e}",'Slope':"{0:.3e}", 'Shape':"{0:.3e}"}
         
       
        #self.miscparams = ['Intensity_sum','Intensity_area','Counts']

        #self.SetVLables(self.rangeparams, self.iterparams, self.miscparams, self.fitparams) #Also creates the rownumbers list
        #self.axislinked[str(self.rownumbers["Channel"])] = "Channel"
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
        if end == 0:
            return

        #self.CalcBG()
        fitfunct = eval(self.ui.moreOptionsGroupBox.ui.profileComboBox.currentText())
        
        
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
            xdata = self.scanman.datasrc.x[rng.rangeparams["Range_start"].value:rng.rangeparams["Range_end"].value]
            ydata = self.scanman.datasrc.y[rng.rangeparams["Range_start"].value:rng.rangeparams["Range_end"].value]
            xmin, xmax, ymin, ymax = [xdata.min(), xdata.max(), ydata.min(), ydata.max()]
             
            if ((len(xdata) < 4) or (len(ydata) < 4)): continue                 #break out if the range was chosen wrong
            #if (min(ydata) == max(ydata)): continue                             #break out is there is no difference in values
            
            #fitfunct=""
            #if method == "reflection":
            #    if ydata[0] < ydata[-1]: fitfunct = reflectiondirect
            #    else: fitfunct = reflectionreverse
            #elif method == "transmission":
            #    if ydata[0] < ydata[-1]: fitfunct = transmissiondirect
            #    else: fitfunct = transmissionreverse
            #elif method == "wall":
            #    fitfunct = walldirect
            #elif method == "zscan":
            #    if ydata[0] < ydata[-1]: fitfunct = zscandirect
            #    else: fitfunct = zscanreverse
            
                
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

            iterkeys = [xkey]+self.iterparams[1:]
            for i in range(len(iterkeys)):
                if rng.iterparams[iterkeys[i]].fix == True or rng.iterparams[iterkeys[i]].enabled == False:
                    gparams[i] = rng.iterparams[iterkeys[i]].value
                    gparamsfix[i] = 1
            
            
            fitob = fit.fit(x=xdata, y=ydata, guess=gparams, ifix=gparamsfix ,quiet=True, 
                            funcs=[fitfunct], optimizer = "mpfit", r2min=-1000000)
            limits = [[xmin,xmax],[0,xmax-xmin],[0,ymax],[0,ymax],[-100.0,100.0]]
            fitob.ilimits = np.array(limits)
            limited = np.array([[1,1]]*len(limits))
            fitob.ilimited = limited
#mpfit
            if 1:#else:
                fitob.go(interactive=False)
                gparams=fitob.result
                stdev=fitob.stdev
                xexpanded = np.linspace(xdata.min(), xdata.max(), 50)
                fittedexpanded = fitfunct(xexpanded,gparams)
                fitted = fitfunct(xdata,gparams)

            rng.fittedline.set_data(xexpanded, fittedexpanded)
            rng.diffline.set_data(xdata, ydata - fitted)
            
            for i in range(len(iterkeys)):
                rng.iterparams[iterkeys[i]].value = gparams[i]
                rng.iterparams[iterkeys[i]].stdev = stdev[i]
            
            self.asignfitparamvalues(rng.fitparams,fitob)
            
            #Determine if the calculated fits are valid based on some 'obvious' rules
            #if  rng.iterparams["Intensity"].value < 0: rng.iterparams["Intensity"].valid = False
            rng.iterparams["Intensity"].valid = False if rng.iterparams["Intensity"].value < 0 else True
            rng.iterparams["Background"].valid = False if rng.iterparams["Background"].value < 0 else True
            
            self.ReflectInTable(rng.iterparams,self.iterparams_values_format,self.iterparams_stdev_format)
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
    window=PeakProfilesDEF()
    window.show()
    sys.exit(app.exec_())

        