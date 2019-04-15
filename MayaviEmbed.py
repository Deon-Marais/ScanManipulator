'''
Created on 18 Dec 2014

@author: Deon
'''

import os
#from builtins import False
#from mayavi.tools.helper_functions import Points3d
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt'
import numpy as np
from pyface.qt import QtGui
import PyQt4.QtCore as QtCore
import mylib
from pyface.qt.QtGui import QFileDialog
#import PyQt4.QtGui as QtGui
#from PyQt4 import QtCore

from traits.api import HasTraits, Instance, on_trait_change
#from traitsui.api import View, Item, HGroup
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
import mayavi
import win32clipboard as cb
from win32api import FormatMessage as FormatMessage
from win32api import GetLastError as GetLastError
from scipy.interpolate import griddata
from tvtk.api import tvtk
     
class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=0.9, width=0.9, show_label=False), resizable=True)
 
    def __init__(self, points, **traits):
        super(HasTraits, self).__init__(**traits)

        self.figure = self.scene.mlab.gcf()
        self.figure.scene.background=(1,1,1)
        self.figure.scene.foreground=(0,0,0)
        #self.picker = self.figure.on_mouse_pick(self.contextMenuRequested, button = "right")
        #self.figure = figure(bgcolor=None)
        
    
    #@on_trait_change('meridional,transverse')
    #def update_plot(self):
        #x, y, z, t = curve(self.meridional, self.transverse)
        #self.plot.mlab_source.set(x=x, y=y, z=z, scalars=t)
        #self.plot.mlab_source.set()
    #    True
         
    #@on_trait_change('scene.activated')
    #def update_plot(self):
    #    picker = self.figure.on_mouse_pick(self.onpick)
    #    picker.tolerance = 0.5
    #    self.scene.mlab.points3d(*self.points, scale_factor=0.03)
     
    #def onpick(self, event):
    #    ind = event.point_id/self.np
    #    print (self.points[0][ind], self.points[1][ind], self.points[2][ind])
        
class Waterfall(Visualization):
    
    def __init__(self,x,y,z):
        super(Waterfall,self).__init__(z)
        self.x=x
        self.y=y
        self.z=z
    
    #def update_plot(self):
    
    @on_trait_change('scene.activated')
    def create_plot(self):
        #my_extent = (np.min(self.x), np.max(self.x), np.min(self.y), np.max(self.y), np.min(self.z), np.max(self.z))
        #self.waterfallplot = self.scene.mlab.surf(self.x, self.y, self.z, extent=my_extent)
        #self.waterfallplot.actor.actor.set(origin=[0,0,0], position=[0,0,0], scale = [1,1,1])
        #self.axes = self.scene.mlab.axes(self.waterfallplot, extent=my_extent)
        #self.axes.axes.z_label=""
        
        #my_extent = (np.min(self.x), np.max(self.x), np.min(self.y), np.max(self.y), np.min(self.z), np.max(self.z))
        #self.waterfallplot = self.scene.mlab.points3d(self.x, self.y, self.z, extent=my_extent)
        #self.waterfallplot.actor.actor.set(origin=[0,0,0], position=[0,0,0], scale = [1,1,1])
        #self.axes = self.scene.mlab.axes(self.waterfallplot, extent=my_extent)
        #self.taxes.axes.z_label=""
        
        self.surfextent = (np.min(self.x), np.max(self.x), np.min(self.y), np.max(self.y), np.min(self.z), np.max(self.z))
        self.surfplot = self.scene.mlab.surf(self.x, self.y, self.z, extent=self.surfextent)
        self.surfplot.actor.actor.set(origin=[0,0,0], position=[0,0,0], scale = [1,1,1])
        self.surfaxes = self.scene.mlab.axes(self.surfplot, extent=self.surfextent)
        self.surfaxes.axes.z_label=""
        self.surftype = "regular"
        
        True

        
    def update_xyz(self,x,y,z,z_err,pts=[0,0]):
        interpol = True
        self.scene.mlab.options.offscreen = False
        if pts == [0,0]: interpol = False
        
        xvals = [x[i] for i in range(len(x))]  
        yvals = [y[i][j] for i in range(len(y)) for j in range(len(y[i]))]          #Flatten so that we can get the max and min - np.array and lists dont mix well 
        zvals = [z[i][j] for i in range(len(z)) for j in range(len(z[i]))]
        zerrvals = [z_err[i][j] for i in range(len(z_err)) for j in range(len(z_err[i]))]
        #doerr = False if (min(zerrvals) == max(zerrvals) and min(zerrvals) == 0) else True
        doerr = True
        if len(zerrvals) == 0:
            doerr = False
        elif (min(zerrvals) == max(zerrvals) and min(zerrvals) == 0):
            doerr = False
        
        if doerr:
            zerrminvals = (np.array(zvals) - np.array(zerrvals)).tolist();
            zerrmaxvals = (np.array(zvals) + np.array(zerrvals)).tolist();
            
        xmin, ymin, zmin =[min(xvals), min(yvals), min(zvals)]
        xmax, ymax, zmax =[max(xvals), max(yvals), max(zvals)]
        dx, dy, dz = [xmax - xmin, ymax - ymin, zmax - zmin]
        if dz == 0: 
            from sys import float_info
            dz = float_info.min
        maxlen=max([dx, dy, dz])  

        regular = True
        if (len(xvals) != len(zvals)): regular = False

        ranges = (xmin,xmax,ymin,ymax,zmin,zmax)
        camview = self.scene.mlab.view()
        
        #self.scene.mayavi_scene.children = []   #Remove any figures on the canvas
        if interpol:
            nrptsx = complex(0,pts[0])
            nrptsy = complex(0,pts[1])
            xa=[[x[i]]*len(y[i]) for i in range(len(y))]
            xvals = [xa[i][j] for i in range(len(xa)) for j in range(len(xa[i]))]
            points = np.array([xvals,yvals]).transpose()
            grid_x, grid_y = np.mgrid[xmin:xmax:nrptsx, ymin:ymax:nrptsy]
            grid_z = griddata(points, zvals, (grid_x, grid_y), method='cubic')
            xmin, ymin, zmin =[np.nanmin(grid_x), np.nanmin(grid_y), np.nanmin(grid_z)]
            xmax, ymax, zmax =[np.nanmax(grid_x), np.nanmax(grid_y), np.nanmax(grid_z)]
            dx, dy, dz = [xmax - xmin, ymax - ymin, zmax - zmin]
            ranges = (xmin,xmax,ymin,ymax,zmin,zmax)
            maxlen=max([dx, dy, dz])
            scalex,scaley,scalez = [maxlen/dx, maxlen/dy, maxlen/dz]
            self.surfpts = self.scene.mlab.points3d(grid_x, grid_y, grid_z, grid_z, scale_mode='none', scale_factor=0.01)
            self.surfpts.actor.actor.set(scale = [scalex,scaley,scalez])
            self.surfmesh = self.scene.mlab.pipeline.delaunay2d(self.surfpts)
            self.surfplot = self.scene.mlab.pipeline.surface(self.surfmesh)
            self.surfpts.visible = False
            self.surfpts.actor.mapper.scalar_visibility = 0 #Will result in the glyphs being black  
            True
            if doerr:
                grid_z_err_min = griddata(points, zerrminvals, (grid_x, grid_y), method='cubic')
                self.surferrminpts = self.scene.mlab.points3d(grid_x, grid_y, grid_z_err_min, scale_mode='none', scale_factor=0.01)
                self.surferrminpts.actor.actor.set(scale = [scalex,scaley,scalez])
                self.surferrminpts.visible = False
                self.surfminmesh = self.scene.mlab.pipeline.delaunay2d(self.surferrminpts)
                self.surfminplot = self.scene.mlab.pipeline.surface(self.surfminmesh, opacity=0.1 )
                self.surfminplot.actor.actor.set(origin=[0,0,0], position=[0,0,0], scale=[scalex,scaley,scalez])
                
                grid_z_err_max = griddata(points, zerrmaxvals, (grid_x, grid_y), method='cubic')
                self.surferrmaxpts = self.scene.mlab.points3d(grid_x, grid_y, grid_z_err_max, scale_mode='none', scale_factor=0.01)
                self.surferrmaxpts.actor.actor.set(scale = [scalex,scaley,scalez])
                self.surferrmaxpts.visible = False
                self.surfmaxmesh = self.scene.mlab.pipeline.delaunay2d(self.surferrmaxpts)
                self.surfmaxplot = self.scene.mlab.pipeline.surface(self.surfmaxmesh, opacity=0.1 )
                self.surfmaxplot.actor.actor.set(origin=[0,0,0], position=[0,0,0], scale=[scalex,scaley,scalez])
    
                
        else: #not interpolate
            scalex, scaley, scalez = [maxlen/dx, maxlen/dy, maxlen/dz]
            if regular:
                try:
                    self.surfplot = self.scene.mlab.surf(x, y, z)
                    if doerr:
                        True
                except:
                    scenechil=self.scene.mayavi_scene.children
                    scenechil.pop(-1)            #Remove the 'Array2d' Source
                    regular = False
            #return
            if regular == False:
                xa=[[x[i]]*len(y[i]) for i in range(len(y))]
                xvals = [xa[i][j] for i in range(len(xa)) for j in range(len(xa[i]))]
                try:
                    self.surfpts = self.scene.mlab.points3d(xvals, yvals, zvals, zvals, scale_mode='none', scale_factor=0.01)
                except:
                    True
                self.surfpts.actor.actor.set(scale = [scalex,scaley,scalez])
                self.surfmesh = self.scene.mlab.pipeline.delaunay2d(self.surfpts)
                self.surfplot = self.scene.mlab.pipeline.surface(self.surfmesh)
                self.surfpts.visible = False
                self.surfpts.actor.mapper.scalar_visibility = 0 #Will result in the glyphs being black
                if doerr:
                    self.surferrminpts = self.scene.mlab.points3d(xvals, yvals, zerrminvals, scale_mode='none', scale_factor=0.01)
                    self.surferrminpts.actor.actor.set(scale = [scalex,scaley,scalez])
                    self.surferrminpts.visible = False
                    self.surfminmesh = self.scene.mlab.pipeline.delaunay2d(self.surferrminpts)
                    self.surfminplot = self.scene.mlab.pipeline.surface(self.surfminmesh, opacity=0.1 )
                    self.surfminplot.actor.actor.set(origin=[0,0,0], position=[0,0,0], scale=[scalex,scaley,scalez])
                    
                    self.surferrmaxpts = self.scene.mlab.points3d(xvals, yvals, zerrmaxvals, scale_mode='none', scale_factor=0.01)
                    self.surferrmaxpts.actor.actor.set(scale = [scalex,scaley,scalez])
                    self.surferrmaxpts.visible = False
                    self.surfmaxmesh = self.scene.mlab.pipeline.delaunay2d(self.surferrmaxpts)
                    self.surfmaxplot = self.scene.mlab.pipeline.surface(self.surfmaxmesh, opacity=0.1 )
                    self.surfmaxplot.actor.actor.set(origin=[0,0,0], position=[0,0,0], scale=[scalex,scaley,scalez])
        
            True
        self.surfplot.actor.actor.set(origin=[0,0,0], position=[0,0,0], scale=[scalex,scaley,scalez])
        self.surfaxes = self.scene.mlab.axes(self.surfplot,ranges = ranges)
        self.surfaxes.axes.number_of_labels = 5
        self.surfaxes.axes.label_format = "%-#6.1f"
        try:
            self.scene.mlab.view(*camview)
        except:
            True
        scenechil=self.scene.mayavi_scene.children
        
        vtksrc=self.scene.mlab.pipeline.get_vtk_src(self.surfplot)[0]
        points = vtksrc.trait_get("points")["points"].to_array().transpose()
        self.x=points[0]
        self.y=points[1]
        self.z=points[2]  
              

        if (len(scenechil)) >1: # There already was a figure present
            axis=scenechil[0].children[1].children[0].children[1]
            rxmin, rxmax, rymin, rymax, rzmin, rzmax = axis.axes.get("ranges")["ranges"]
            idxvtk=[]
            for i in range(len(scenechil)):
                if (type(scenechil[i]) == mayavi.sources.vtk_data_source.VTKDataSource):
                    idxvtk=idxvtk+[i]
                    surface=scenechil[i].children[1].children[0].children[0]
                    axis=scenechil[i].children[1].children[0].children[1]
                    rxmint, rxmaxt, rymint, rymaxt, rzmint, rzmaxt = axis.axes.get("ranges")["ranges"]
                    if rxmint <rxmin:rxmin = rxmint
                    if rxmaxt >rxmax:rxmax = rxmaxt
                    if rymint <rymin:rymin = rymint
                    if rymaxt >rymax:rymax = rymaxt
                    if rzmint <rzmin:rzmin = rzmint
                    if rzmaxt >rzmax:rzmax = rzmaxt
                    True
                True
            dx, dy, dz = [rxmax - rxmin, rymax - rymin, rzmax - rzmin]
            maxlen=max([dx, dy, dz]) 
            scalex,scaley,scalez = [maxlen/dx, maxlen/dy, maxlen/dz] 
            #Only adjust and show the axis of the first graph, hide the rest    
            surface=scenechil[0].children[1].children[0].children[0]
            axis=scenechil[0].children[1].children[0].children[1]
            glyphs=scenechil[0].children[0].children[0]
            glyphs.actor.actor.set(scale=[scalex,scaley,scalez])
            surface.actor.actor.set(scale=[scalex,scaley,scalez])
            axis.axes.set(ranges=[rxmin, rxmax, rymin, rymax, rzmin, rzmax])
            axis.axes.set(bounds=[rxmin*scalex, rxmax*scalex, rymin*scaley, rymax*scaley, rzmin*scalez, rzmax*scalez])
            for i in idxvtk[1:]:
                surface=scenechil[i].children[1].children[0].children[0]
                surface.actor.actor.set(scale=[scalex,scaley,scalez])
                axis=scenechil[i].children[1].children[0].children[1]
                axis.visible=False
                glyphs=scenechil[i].children[0].children[0]
                glyphs.actor.actor.set(scale=[scalex,scaley,scalez])
            True
                
        True
        scenechil
        

        True
        
 
class MayaviQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.mylayout = QtGui.QVBoxLayout(self)
        self.mylayout.setContentsMargins(0,0,0,0)
        self.mylayout.setSpacing(0)
        self.visualization = Waterfall([1,2],[1,2], [[1,1],[1,1]])      #Just to get the visualization up, we will remove it again
        self.ui = self.visualization.edit_traits(parent=self, kind='subpanel').control
        self.mylayout.addWidget(self.ui)
        self.ui.setParent(self)
        self.visualization.figure.on_mouse_pick(self.contextMenuRequested, type="point", button="Right")
        
        self.filedialog = QFileDialog()
        self.filedialog.setFileMode(QFileDialog.AnyFile)
        self.filedialog.setViewMode(QFileDialog.Detail)
        self.curfilter = ""
        self.visualization.scene.mayavi_scene.children = []   #Remove any figures on the canvas
        #from PyQt4.QtCore import Qt
        #self.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.customContextMenuRequested.connect(self.contextMenuRequested)
        
        #self.engine = get_engine() #This is the main mayavi engine
        #self.mainscene = self.engine.scenes[0]  #This is the main (first) scene
        
    def setWaterfall(self,x,y,z,y_err,pts):
        self.visualization.update_xyz(x,y,z,y_err,pts)
        
        True
    

    
    def contextMenuRequested(self,picker):
            menu = QtGui.QMenu()
            cpyVTK = menu.addAction("Copy VTK")
            cpyCSV = menu.addAction("Copy CSV")
            cpyBMP = menu.addAction("Copy BMP")
            cpyPNG = menu.addAction("Copy PNG")
            saveAS = menu.addAction("Save as...")
            cpyVTK.triggered.connect(self.copyVTK)
            cpyCSV.triggered.connect(self.copyCSV)
            cpyBMP.triggered.connect(self.copyBMP)
            cpyPNG.triggered.connect(self.copyPNG)
            saveAS.triggered.connect(self.saveAS)
            
            menu.exec_(self.mapFromParent(QtGui.QCursor.pos()))
    
    def saveAS(self):
        fname = self.filedialog.getSaveFileName(self, "Save as *.*", filter="All files (*.*)")
        if fname == "": return
        self.filedialog.setDirectory(os.path.dirname(str(fname)))
        self.visualization.scene.mlab.options.offscreen = True
        self.visualization.scene.save(fname,size=(1280,1280))
        True
    
    
    def copyVTK2(self):
        #from tvtk.api import tvtk, write_data
        #src = mayavi.tools.pipeline.get_vtk_src(self.visualization.scene.mayavi_scene.children[5])
        #write_data(src[0],"test.vtk")
        True

        
        self.visualization.scene.mlab.options.offscreen = True
        fpath=os.path.abspath("clipboard.eps")
        f_prefix, f_ext = os.path.splitext(fpath)
 
        ex = tvtk.GL2PSExporter()
        ex.file_prefix = f_prefix
        ex.file_format = 'eps'
        ex.sort = 'bsp'
        ex.compress = 0
        #ex.write3d_props_as_raster_image = 1
                
        
        
        self.visualization.scene.save(fpath, size=(640,640), exp=ex)
        #self.visualization.scene.mlab.savefig(fpath, exp=ex)
        #self.visualization.scene.mlab.savefig(fpath)
        
        opath=os.path.abspath("clipboard")
        exeln = 'inkscape -z --file "' + fpath + '" --export-emf "' + opath + '"'
        os.system(exeln)
        os.remove(fpath)
        mylib.set_clipboard_file(opath)



    def copyVTK(self):        
        from tvtk.api import tvtk, write_data
        src = mayavi.tools.pipeline.get_vtk_src(self.visualization.scene.mayavi_scene.children[0])
        write_data(src[0],"test")
        True
        
        
        
        
    def copyCSV(self):
        x=self.visualization.x
        y=self.visualization.y
        z=self.visualization.z
        #csvline = " "
        #for yi in y: 
        #    csvline = csvline + "%f " %yi
        #csvline = csvline+"\n"
        #for xi in range(len(x)):
        #    csvline = csvline + "%f " %x[xi]
        #    for yi in range(len(y)): csvline = csvline + "%f " %z[xi][yi]
        #    csvline = csvline+"\n"
        csvline = ""
        for i in range(len(x)):
            if np.isnan(z[i]) == False:
                csvline = csvline + "%f\t %f\t%f\n" %(x[i],y[i],z[i])
        mylib.set_clipboard_text(csvline)
       
    def copyBMP(self):
        self.visualization.scene.mlab.options.offscreen = True
        fpath=os.path.abspath("clipboard.bmp")
        self.visualization.scene.save(fpath)
        newfpath = os.path.abspath("clipboard")
        if (os.path.exists(newfpath)): os.remove(newfpath)
        os.rename(fpath,newfpath)
        mylib.set_clipboard_image(newfpath)
        
    
    def copyPNG(self):
        self.visualization.scene.mlab.options.offscreen = True
        fpath=os.path.abspath("clipboard.png")
        self.visualization.scene.save(fpath,size=(1280,1280))
        im = QtGui.QImage(fpath)
        im2 = im.convertToFormat(QtGui.QImage.Format_ARGB32)
        im3 = im2.createMaskFromColor(QtGui.QColor("white").rgb(), QtCore.Qt.MaskOutColor)
        im2.setAlphaChannel(im3)
        newfpath = os.path.abspath("clipboard")
        im2.save(fpath)
        
        if (os.path.exists(newfpath)): os.remove(newfpath)
        os.rename(fpath,newfpath)
        mylib.set_clipboard_file(newfpath)
        #self.visualization.scene.mlab.options.offscreen = False
        True  
            
    def test(self):
        
        
        
        True
        
    
    
    def clear(self):
        True


       
        
 
