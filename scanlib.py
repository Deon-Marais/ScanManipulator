'''
Created on 18 Mar 2014

@author: Deon
'''
import numpy as np
from thirdparty.pyspec import fit, fitfuncs

def gauss(x, p, mode='eval'):
    """Gaussian defined by amplitide

    Function:
       :math:`f(x) = k + p_2 \exp\left(\\frac{-(x - p_0)^2}{2p_1^2}\\right)`

    """
    if mode == 'eval':
        cent=p[0];wid=p[1];amp=p[2];const=p[3];
        out = const + amp * np.exp(-1.0 * (x - cent)**2 / (2 * wid**2))
    elif mode == 'params':
        out = ['cent', 'sigma', 'amp', 'const']
    elif mode == 'name':
        out = "Gaussian"
    elif mode == 'guess':
        g = fitfuncs.peakguess(x, p)
        out = [g[0], g[1] / (4 * np.log(2)), g[3], g[4]]
    else:
        out = []

    return out


'***************************************************************'
def GenData():
    x = np.arange(0.0, 2.0, 0.01)
    y = np.sin(2.0*np.pi*x) #'+ np.random.normal(size=len(t))'
    return x, y
pass


            
'***************************************************************'
def GenFitData(x,y):
    initial = gauss(x,y,'guess')
    
    fitob = fit.fit(x=x, y=y, guess=initial ,funcs=[gauss])
    fitob.go(interactive=False)
    gparams=fitob.result
    stdev=fitob.stdev
    fitted = gauss(x,gparams)
    return gparams, stdev, fitted
    

'***************************************************************'
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    x = np.arange(0.0, 300, 1)
    centers = [50, 200, 250]
    widths = [10,30, 30]
    amps = [5,10,1]
    
pass