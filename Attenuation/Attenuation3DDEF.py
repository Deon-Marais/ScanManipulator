'''
Created on 07 January 2018

@author: Deon
'''
from PyQt4.QtGui import QGroupBox as QGroupBox
from PyQt4.QtGui import QFileDialog
from Attenuation.Attenuation3DGUI import Ui_Attenuation3D
import PyQt4.QtGui as qt
from PyQt4 import QtCore
import numpy as np
import sys
import mylib
from mylib import ProgressBar
from mylib import Graph
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib as mpl
from os import path 
from functools import partial
from shapely import geometry as shgeom
import shapely
from PIL import Image
import random
import os
#import glm

#import pybullet
#import pybullet_data
import trimesh
#import stl
import Attenuation.PyGLWidget as PyGLWidget
import Attenuation.Component as Component

#import pyglet
#from pyglet import gl as gl
#from itertools import izip
from OpenGL import GL as gl, GL


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
    
try:
    _encoding = qt.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return qt.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return qt.QApplication.translate(context, text, disambig)

def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print ("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print ("Toc: start time not set")

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(np.deg2rad(phi))
    y = rho * np.sin(np.deg2rad(phi))
    return(x, y)

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step


#**************************************************************************************
class MyPyGLWidget(PyGLWidget.PyGLWidget):
    def __init__(self):
        PyGLWidget.PyGLWidget.__init__(self)
        #self.sprite = pyglet.sprite.Sprite(pyglet.resource.image("logo.png"))
        #self.label = pyglet.text.Label(
        #    text="This is a pyglet label rendered in a Qt widget :)")
        #self.config = gl.Config(alpha_size=8)
        
        #self.setContext(self.config)
        self.setMinimumSize(QtCore.QSize(100, 100))
        #self.mesh = ""
        #self.edges = 0
    
    #def paintGL(self):
    #    PyGLWidget.paintGL(self)
        
    #    if self.mesh !="":
    #        self.draw_mesh_faces_flat(self.mesh, self.edges)
    #    if self.edges:
    #        self.draw_edges(self.mesh)
    #    True

    #def draw_edges(self, mesh):
        #self.mesh = mesh
    #    l = len(mesh.edges)
    #    gl.glBegin(gl.GL_LINES)
    #    for n, edge in enumerate(mesh.edges):
    #        gl.glColor3f(n / float(l), 0.5, 0.5)
    #        edge = tuple(edge)
    #        gl.glVertex3f(*mesh.vertices[edge[0]])
    #        gl.glVertex3f(*mesh.vertices[edge[1]])
    #    gl.glEnd()

    #def draw_mesh_faces_flat(self, mesh, will_draw_edges=True):
    #    if will_draw_edges:
            ## This offset guarantees that all polygon faces have a z-buffer value at least 1 greater.
    #        gl.glPolygonOffset(1.0, 1.0)
    #        gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)

    #    gl.glBegin(gl.GL_TRIANGLES)
    #    for face, normal in izip(mesh.faces, mesh.face_normals):
    #        gl.glNormal3f(*normal)
    #        for vertex_index in face:
    #            gl.glVertex3f(*mesh.vertices[vertex_index])
    #    gl.glEnd()
    #    gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)

    #def on_draw(self):
        #gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        #gl.glLoadIdentity()
        #gl.gluLookAt(1, 10, -0.0, 10, 0.0, 0.0, 0.0, 0.0, 0.0)
        #lk = np.concatenate([self.camera.mPos,self.camera.mView,self.camera.mUp])
        #gl.gluLookAt(lk[0],lk[1],lk[2],lk[3],lk[4],lk[5],lk[6],lk[7],lk[8])
        
    #    if self.mesh != "":
            #self.draw_mesh_faces_flat(self.mesh,False)
    #        self.draw_edges(self.mesh)
    #    True
        
        #gl.gluLookAt(1, 10, -0.0, 10, 0.0, 0.0, 0.0, 0.0, 0.0)
        #gl.glBegin(gl.GL_TRIANGLES)
        #gl.glVertex2f(0, 0)
        #gl.glVertex2f(100, 0)
        #gl.glVertex2f(100, 100)
        #gl.glEnd()
    #    True
    #def set_mesh(self,mesh):
    #    self.mesh = mesh

#**************************************************************************************
class prm():
    def __init__(self,name="",description=""):
        # y = mx + c
        self.name=name
        self.description=description
        self.m_val=np.float(0)
        self.x_str=""
        self.x_val=np.float(0)
        self.c_val=np.float(0)
        self.res_val=np.float(0)
        
    def GetVal(self):
        return self.res_val
    
    def SetVal(self,varUI):
        self.c_val = np.double(varUI.const_lineEdit.text())
        self.m_val = np.double(varUI.mult_lineEdit.text())
        self.x_str = ""
        self.res_val= np.double(varUI.eq_lineEdit.text())
        return self.res_val


#**************************************************************************************
class varUI():
    def __init__(self,title,inlayout,ScanmanMain=""):
        self.scanman = ScanmanMain
        sizePolicy = qt.QSizePolicy(qt.QSizePolicy.MinimumExpanding, qt.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        
        self.dvalidator = qt.QDoubleValidator()
        self.hlayout = qt.QHBoxLayout()
        self.hlayout.setContentsMargins(-1, 0, -1, -1)
        self.hlayout.setObjectName(title+"_layout")
        self.varname_label = qt.QLabel()
        self.varname_label.setObjectName(title+"_varname_label")
        self.varname_label.setSizePolicy(sizePolicy)
        self.varname_label.setMinimumSize(QtCore.QSize(50, 0))        
        self.varname_label.setText(_translate("", title, None))
        self.hlayout.addWidget(self.varname_label)
        self.const_lineEdit = qt.QLineEdit()
        self.const_lineEdit.setObjectName(title+"_const_lineEdit")
        self.const_lineEdit.setSizePolicy(sizePolicy)
        self.const_lineEdit.setMinimumSize(QtCore.QSize(20, 0))
        self.const_lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.const_lineEdit.setValidator(self.dvalidator)
        self.const_lineEdit.setText(_translate("", "0", None))
        self.hlayout.addWidget(self.const_lineEdit)
        self.plus_label = qt.QLabel()
        self.plus_label.setObjectName(title+"_plus_label")
        self.plus_label.setText(_translate("", "+", None))
        self.hlayout.addWidget(self.plus_label)
        self.mult_lineEdit = qt.QLineEdit()
        self.mult_lineEdit.setObjectName(title+"_mult_lineEdit")
        self.mult_lineEdit.setSizePolicy(sizePolicy)
        self.mult_lineEdit.setMinimumSize(QtCore.QSize(20, 0))
        self.mult_lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mult_lineEdit.setValidator(self.dvalidator)
        self.mult_lineEdit.setText(_translate("", "0", None))
        self.hlayout.addWidget(self.mult_lineEdit)
        self.mul_label = qt.QLabel()
        self.mul_label.setObjectName(title+"_mul_label")
        self.mul_label.setText(_translate("", "x", None))
        self.hlayout.addWidget(self.mul_label)
        self.vars_comboBox = qt.QComboBox()
        self.vars_comboBox.setObjectName(_fromUtf8(title+"vars_comboBox"))
        self.hlayout.addWidget(self.vars_comboBox)
        self.eq_label = qt.QLabel()
        self.eq_label.setObjectName(title+"_eq_label")
        self.eq_label.setText(_translate("", "=", None))
        self.hlayout.addWidget(self.eq_label)
        self.eq_lineEdit = qt.QLineEdit()
        self.eq_lineEdit.setObjectName(title+"_mult_lineEdit")
        self.eq_lineEdit.setSizePolicy(sizePolicy)
        self.eq_lineEdit.setMinimumSize(QtCore.QSize(40, 0))
        self.eq_lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.eq_lineEdit.setText(_translate("", "0", None))
        self.eq_lineEdit.setReadOnly(True)
        self.hlayout.addWidget(self.eq_lineEdit)
        inlayout.addLayout(self.hlayout)
        self.CalcResult()
        
        pass


    #**************************************************************************************
    def CalcResult(self):
        prmval = 0.0
        try:
            src = self.scanman.datasrc
            prmval = float(src.prm[self.vars_comboBox.currentText()])
        except:
            pass
        
        try:
            c=float(self.const_lineEdit.text())
            a=float(self.mult_lineEdit.text())
            res = c + a * prmval
            self.eq_lineEdit.setText(str(res))
        except:
            self.eq_lineEdit.setText("")


    #**************************************************************************************
    def GetVal(self):
        return np.double(self.eq_lineEdit.text())
    
    #**************************************************************************************
    def SetVals(self,const_line="0", mult_line="0", selparam=""):
        self.const_lineEdit.setText(np.str(const_line))
        self.mult_lineEdit.setText(np.str(mult_line))
        
        curparams=[self.vars_comboBox.itemText(s) for s in range(self.vars_comboBox.count())]
        if "" not in curparams:
            curparams = [""] + curparams
        if selparam not in curparams:
            curparams = curparams+[selparam]
            self.vars_comboBox.clear()
            self.vars_comboBox.addItems(curparams)
        self.vars_comboBox.setCurrentIndex(self.vars_comboBox.findText(selparam))
 
        pass
    
    #**************************************************************************************
    def UpdateCombos(self, paramskeys):
        selparam = self.vars_comboBox.currentText()
        curparams=[self.vars_comboBox.itemText(s) for s in range(self.vars_comboBox.count())]
        
        if "" not in paramskeys:
            paramskeys = [""]+paramskeys
        if selparam not in paramskeys:
            paramskeys = paramskeys+[selparam]
        if curparams == paramskeys:
            True
        else:
            self.vars_comboBox.clear()
            self.vars_comboBox.addItems(paramskeys)

        if selparam in paramskeys:
            self.vars_comboBox.setCurrentIndex(self.vars_comboBox.findText(selparam))
    
        
        
        
                    
#**************************************************************************************
class Attenuation3DDEF(QGroupBox):
    def __init__(self, ScanmanMain=""):
        self.scanman = ScanmanMain
        QGroupBox.__init__(self)
        self.name = "Attenuation3D"
        self.ui = Ui_Attenuation3D()
        self.ui.setupUi(self)
        self.ConstructUI()
        
        self.filedialog = QFileDialog()
        self.filedialog.setAcceptMode(QFileDialog.AcceptSave)
        self.filedialog.setFileMode(QFileDialog.AnyFile)
        self.filedialog.setViewMode(QFileDialog.Detail)
        self.lastdir=""
        
        self.lineseries=[]
        self.lineseries.append(Line2D([], [], color='black', linewidth = 1.0))      #0 = intensity fraction
     
        self.absgraph_line = self.lineseries[0]
        
        self.lineseries.append(Line2D([], [], color='black', linewidth = 1.0))      #1 = Correction multiplier
        self.ui.cor_graphic.figure.axes[0].add_line(self.lineseries[1])
        self.ui.cor_graphic.figure.axes[0].set_ylabel("Correction coefficient")
        self.corgraph = Graph(self.ui.cor_graphic)        
        self.corgraph_line = self.lineseries[1]   
        
        self.expgraph = Graph(self.ui.exp_graphic)
        
        
        self.omega = prm("omega","Sample rotation [degrees] Clockwise from primary beam")
        self.sstth = prm("sstth","Secondary slit 2-theta [degrees] Clockwise from primary beam")
        self.psw = prm("psw","Primary slit width [mm]")
        self.ssw = prm("ssw","Secondary slit width [mm]")
        self.psw_sec = prm("psw_sec","Primary slit divisions for grid")
        self.ssw_sec = prm("ssw_sec","Secondary slit divisions for grid")
        self.psp = prm("psp","Primary slit position")
        self.ssp = prm("ssp","Secondary slit position")
        self.psdiv = prm("psdiv","Primary slit divergence [degrees]")
        self.ssdiv = prm("ssdiv","Secondary slit divergence [degrees]")
        self.sdd = prm("sdd","Sample to detector distance [mm]")
        self.nchi = prm("nchi","Cradle chi rotation angle [degrees]")
        self.nphi = prm("nphi","Cradle phi rotation angle [degrees]")
        
        
        self.cor_x = prm("cor_x","Center of rotation x-offset in sample [mm]")
        self.cor_y = prm("cor_y","Center of rotation y-offset in sample [mm]")
        self.cor_z = prm("cor_z","Center of rotation z-offset in sample [mm]")
        self.s_len_x = prm("s_len_x","Sample length in x-direction [mm]")
        self.s_len_y = prm("s_len_y","Sample length in y-direction [mm]")
        self.s_len_y = prm("s_len_z","Sample length in y-direction [mm]")
        self.att_coef = prm("att_coef","Attenuation coefficient [cm^-1]")
        
        self.LoadPrmFile("./Session/att_corr.txt")
 
            
        self.InitExpFigure()

    #**************************************************************************************
    def ConstructUI(self):
        self.instvar_names=["omega", "sstth","psw","ssw","psw_sec","ssw_sec","psp","ssp","psdiv","ssdiv","sdd","nchi","nphi"]
        self.vars_inst = {}
        for vari in self.instvar_names:
            self.vars_inst[vari] = varUI(vari,self.ui.inst_param_layout, self.scanman)
            self.vars_inst[vari].const_lineEdit.textChanged.connect(partial(self.UpdateUI,vari))
            self.vars_inst[vari].mult_lineEdit.textChanged.connect(partial(self.UpdateUI,vari))
            self.vars_inst[vari].vars_comboBox.currentIndexChanged.connect(partial(self.UpdateUI,vari))
        self.vars_samp_rect ={}
        self.samp_rect_names=["cor_x","cor_y","cor_z","s_len_x","s_len_y","s_len_z","att_coef"]
        for vari in self.samp_rect_names:
            self.vars_samp_rect[vari] = varUI(vari,self.ui.samp_param_layout, self.scanman)
            self.vars_samp_rect[vari].const_lineEdit.textChanged.connect(partial(self.UpdateUI,vari))
            self.vars_samp_rect[vari].mult_lineEdit.textChanged.connect(partial(self.UpdateUI,vari))
            self.vars_samp_rect[vari].vars_comboBox.currentIndexChanged.connect(partial(self.UpdateUI,vari))
        self.samp_cyl_names=[""]
        
        self.ui_vars = a=dict(self.vars_inst, **self.vars_samp_rect)    #concatenate the dictionaries
    
        self.glwidget = MyPyGLWidget()
        self.ui.pyglet_layout.addWidget(self.glwidget)
        #self.pygletwidget = MyPygletWidget()
        #self.ui.pyglet_layout.addWidget(self.pygletwidget)
    #**************************************************************************************
    def PopulateParamCombos(self):
        #paramskeys=self.scanman.datasrc.prm.keys()
        #paramskeys.sort()
        paramskeys=sorted(self.scanman.datasrc.prm.keys())
        for vari in self.ui_vars.keys():
            self.ui_vars[vari].UpdateCombos(paramskeys)
         
    #**************************************************************************************
    def InitExpFigure(self):
        axis = self.ui.exp_graphic.figure.axes[0]
        axis.set_xlim(-7,7);axis.set_ylim(-7,7);
        self.expgraph.graph.draw()
        axis.relim(True)
        axis.autoscale(True, 'both', False)
        axis.set_aspect('equal')
        self.viewLim = [axis.get_xbound(),axis.get_ybound()]
        
    #**************************************************************************************
    def UpdateUI(self,vari="",sig=""):
        try:
            self.ui_vars[vari].CalcResult()
        except:
            if vari=="all":
                for vari in self.ui_vars:
                    self.ui_vars[vari].CalcResult()
        
    #**************************************************************************************

    
    #**************************************************************************************
    def Save(self):
        fname = self.filedialog.getSaveFileName(self, "Save as *.txt", filter="Text (*.txt)")
        if fname == "": return
        self.filedialog.setDirectory(path.dirname(str(fname)))
        txt_file = open(fname,"w")
        for uiprm in self.ui_vars:
            c_val = self.ui_vars[uiprm].const_lineEdit.text()
            m_val = self.ui_vars[uiprm].mult_lineEdit.text()
            x_str = self.ui_vars[uiprm].vars_comboBox.currentText()
            s = uiprm + " = " + c_val + " + " + m_val
            if x_str != "":
                s = s + " * " + x_str
            s = s +"\r\n"
            txt_file.write(s)
        txt_file.close()
        
    #**************************************************************************************
    def Load(self):
        fname = self.filedialog.getOpenFileName(self, "Select absorption correction parameter file", self.lastdir,"AbsCor (*.txt)")
        if fname == "": return
        self.lastdir = path.dirname(str(fname))
        self.LoadPrmFile(fname)
        
    #**************************************************************************************
    def LoadPrmFile(self,fname):
        loadedprms = []
        with open(fname) as fh:
            for line in fh:
                s = line.split()
                try:
                    thisprm = eval("self."+s[0])
                    loadedprms.append(s[0])
                except:
                    continue
                try:
                    thisprm.c_val = np.float(s[2])
                except:
                    thisprm.c_val = np.float(0)
                try:
                    thisprm.m_val = np.float(s[4])
                except:
                    thisprm.m_val = np.float(0)
                try:
                    thisprm.x_str = s[6]
                except:
                    thisprm.x_str = ""
        
                if thisprm.name in self.ui_vars:
                    self.ui_vars[thisprm.name].SetVals(thisprm.c_val, thisprm.m_val, thisprm.x_str)
    
    #**************************************************************************************
    def SampleTypeChanged(self):
        if self.ui.cylRadioButton.isChecked() == True:
            self.vars_samp_rect["s_len_y"].varname_label.setEnabled(False)
            self.vars_samp_rect["s_len_x"].varname_label.setText("d")
        elif self.ui.rectRadioButton.isChecked() == True:
            self.vars_samp_rect["s_len_y"].varname_label.setEnabled(True)
            self.vars_samp_rect["s_len_x"].varname_label.setText("s_len_x")            

    #**************************************************************************************
    def ClearDrawing(self):
        axis = self.ui.exp_graphic.figure.axes[0]
        self.viewLim = [axis.get_xbound(),axis.get_ybound()]
        axis.clear()
        self.expgraph.graph.draw()
        pass
    
    def LockAxis_clicked(self):
        axis = self.ui.exp_graphic.figure.axes[0]
        self.viewLim = [axis.get_xbound(),axis.get_ybound()]
        
    #**************************************************************************************
    def RefreshSet(self,stth=np.linspace(0,180,50)):
        self.UpdateUI("all")
        self.Refresh(stth)
    
    #**************************************************************************************
    def Refresh(self,stth=np.linspace(0,180,50)):
        if self.ui.autoclear_check.isChecked() == True:
            self.ClearLayout()
        omega = self.omega.SetVal(self.vars_inst["omega"])
        sstth = self.sstth.SetVal(self.vars_inst["sstth"])
        psw = self.psw.SetVal(self.vars_inst["psw"])
        ssw = self.ssw.SetVal(self.vars_inst["ssw"])
        psw_sec = self.psw_sec.SetVal(self.vars_inst["psw_sec"])
        ssw_sec = self.ssw_sec.SetVal(self.vars_inst["ssw_sec"])
        psp = self.psp.SetVal(self.vars_inst["psp"])
        ssp = self.ssp.SetVal(self.vars_inst["ssp"])
        psdiv = self.psdiv.SetVal(self.vars_inst["psdiv"])
        ssdiv = self.ssdiv.SetVal(self.vars_inst["ssdiv"])
        sdd = self.sdd.SetVal(self.vars_inst["sdd"])
        cor_x = self.cor_x.SetVal(self.vars_samp_rect["cor_x"])
        cor_y = self.cor_y.SetVal(self.vars_samp_rect["cor_y"])
        s_len_x = self.s_len_x.SetVal(self.vars_samp_rect["s_len_x"])
        s_len_y = self.s_len_y.SetVal(self.vars_samp_rect["s_len_y"])
        att_coef = self.att_coef.SetVal(self.vars_samp_rect["att_coef"])
 
        stth, comb_atten = self.CalcAbs()
        
        self.absgraph_line.set_data(stth,comb_atten)
        ymin=min(comb_atten)
        ymax=max(comb_atten)
        ybuf = abs(ymax - ymin) * 0.1
        if ybuf == 0: ybuf = 1.0
 
        inten_corr = 1.0/comb_atten
        self.corgraph_line.set_data(stth,inten_corr)
        ymin=min(inten_corr)
        ymax=max(inten_corr)
        ybuf = abs(ymax - ymin) * 0.1
        if ybuf == 0: ybuf = 1.0
        cor_graph_axes= self.ui.cor_graphic.figure.axes[0]
        cor_graph_axes.set_xlim(min(stth), max(stth))
        cor_graph_axes.set_ylim(ymin - ybuf, ymax + ybuf)
        cor_graph_axes.set_title("")
        self.corgraph.graph.draw()       
        
        self.DrawLayout()
       
    #**************************************************************************************
    def CalcAbs(self):
        axis = self.ui.exp_graphic.figure.axes[0]

        ssw = self.ssw.GetVal()
        psw = self.psw.GetVal()
        sstth = self.sstth.GetVal()
        psp = self.psp.GetVal()
        ssp = self.ssp.GetVal()
        cor_x = self.cor_x.GetVal()
        cor_y = self.cor_y.GetVal()
        sdd = self.sdd.GetVal()
        s_len_x = self.s_len_x.GetVal()
        s_len_y = self.s_len_y.GetVal()
        omega = self.omega.GetVal()
        psw_sec = self.psw_sec.GetVal()
        ssw_sec = self.ssw_sec.GetVal()
        mu = self.att_coef.GetVal()/10.0   #now in mm-1  
        
        try:
            stth = self.scanman.datasrc.dataset[self.scanman.datasrc.currset].currframe.x_2th
        except:
            stth = np.linspace(0,180,50)

        try:
            sec_beam_x_proj = ssw/np.cos(np.deg2rad(90.0-sstth))
        except:
            sec_beam_x_proj = 0.0

        randomgrid = 0

        #Sample
        if self.ui.rectRadioButton.isChecked() == True:
            s1 = [cor_x, -cor_y]
            s2 = [cor_x,  s_len_y-cor_y]
            s3 = [-(s_len_x - cor_x), s_len_y - cor_y]
            s4 = [-(s_len_x - cor_x), -cor_y]
            sample_points = np.array([s1,s2,s3,s4])
        elif self.ui.cylRadioButton.isChecked() == True:
            s1 = [cor_x, -cor_y]
            cylsample = shgeom.Point(s1).buffer(s_len_x/2.0)
            cylextpts = cylsample.exterior.xy
            sample_points = np.array(cylextpts).transpose()
            randomgrid = 1
        sample_trans = mpl.transforms.Affine2D().rotate_deg_around(0.0, 0.0, omega)
        self.sample = plt.Polygon(sample_trans.transform(sample_points), alpha=0.3, color="black")
        sh_sample = shgeom.Polygon(self.sample.get_xy())        

        #Gauge volume
        xmin, xmax, ymin, ymax =  [-0.5*sec_beam_x_proj,0.5*sec_beam_x_proj,-0.5*psw,0.5*psw]
        sh_gridbound = shgeom.Polygon([[xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax],[xmin,ymin]])
        sh_gridbound_skew = shapely.affinity.skew(sh_gridbound, xs = 90-sstth,ys=0, origin = 'center')
        if sh_sample.contains(sh_gridbound_skew) != True: randomgrid = 1
        sh_sgvol = sh_sample.intersection(sh_gridbound_skew)
        gridbound_points = np.array(sh_sgvol.exterior.xy).transpose()
        self.gvol =  plt.Polygon(gridbound_points, color="red", linewidth=0.0)
        
        
        #Grid points
        pointspatches = []
        r = np.min([psw,sec_beam_x_proj])/np.max([psw_sec, ssw_sec])/3.0    #radius of displayed point
        if False:
            nrgridpoints = int(ssw_sec*psw_sec)
            N=10*nrgridpoints
            xmin,ymin = gridbound_points.min(0); xmax,ymax = gridbound_points.max(0)
            randomPoints=[]
            i=0
            while i < N:
                newxy = [random.uniform(xmin, xmax),random.uniform(ymin, ymax)]
                if sh_sgvol.contains(shgeom.Point(newxy)):
                    randomPoints.append(newxy)
                    i=i+1
            X = np.array(randomPoints)
            gridpts = mylib.find_centers(X, nrgridpoints)[0]
            self.sh_gridpoints = shgeom.MultiPoint(gridpts)
            for pt in gridpts:
                pointspatches.append(plt.Circle(np.array(pt),r))
        else:
            xdelta = (sec_beam_x_proj)/(ssw_sec)
            ydelta = (psw)/(psw_sec) 
            gridpoints = []
            for xpt in frange(xmin+0.5*xdelta, xmax, xdelta):
                for ypt in frange(ymin+0.5*ydelta, ymax, ydelta):
                    gridpoints.append([xpt,ypt])
            sh_allgridpoints = shgeom.MultiPoint(gridpoints)
            sh_allgridpoints_skew =  shapely.affinity.skew(sh_allgridpoints, xs = 90-sstth,ys=0, origin = [0,0])
            self.sh_gridpoints = []
            for pt in sh_allgridpoints_skew:
                if sh_sgvol.contains(pt):
                    self.sh_gridpoints.append(pt)
                    xypt = plt.Circle(np.array(pt),r)
                    pointspatches.append(xypt)
        self.gridcollection = mpl.collections.PatchCollection(pointspatches, color="yellow", alpha=None)

        #primary beam path lengths
        pb_len = []
        for pt in self.sh_gridpoints:
            ptxy = np.array(pt.xy)
            pbproj = shgeom.LineString([ptxy,[psp,ptxy[1]]])
            intpt = sh_sample.boundary.intersection(pbproj)
            pb_len.append(intpt.distance(pt))
            intpt.distance(pt)
        self.pb_len=np.array(pb_len)    
            
        #secondary beam path lengths for each detector angle
        nrgridpts = len(self.sh_gridpoints)
        sample_bounddary = sh_sample.boundary
        stth_pts = np.array(pol2cart(sdd,stth+180.0)).transpose()
        lenstth = len(stth_pts)
        self.sb_len = np.zeros((lenstth,nrgridpts))
        sblenperstth = np.zeros(nrgridpts)
        if self.ui.drawonly_check.isChecked() == True:
            return [stth,np.array(lenstth*[1.0])]
        progressstth = ProgressBar(str(nrgridpts) + " points per angle", lenstth)
        for stth_i in range(lenstth):
            progressstth.setinfo("2-theta = " + str(round(stth[stth_i],1)))
            stth_pt = stth_pts[stth_i]
            for pti in range(nrgridpts):
                ptxy = np.array(self.sh_gridpoints[pti].xy)
                sbproj = shgeom.LineString([ptxy,stth_pt])
                intpt = sample_bounddary.intersection(sbproj)
                sblenperstth[pti] = intpt.distance(self.sh_gridpoints[pti])
                a= intpt
                pass
            self.sb_len[stth_i] = sblenperstth
            if progressstth.wasCanceled(): break
            progressstth.step()
        #calculate combined attenuation
        ss_i = []  
        pb_i = np.exp(-mu*self.pb_len)
        for k in range(len(stth)):
            ss_i.append(pb_i*np.exp(-mu*self.sb_len[k]))
            pass
        self.ss_i = np.array(ss_i)  
        self.comb_atten = np.sum(self.ss_i,1)/len(pb_i)  
        
        return [stth,self.comb_atten]
    
    #**************************************************************************************
    def ClearLayout(self):
        try:
            self.prim_beam.remove()
        except:
            pass
        try:
            self.sec_beam.remove()
        except:
            pass
        try:
            self.sample.remove()
        except:
            pass
        try:
            self.gvol.remove()
        except:
            pass
        try:
            self.gridcollection.remove()
        except:
            pass        
        try:
            self.cor.remove()
        except:
            pass
        try:
            self.pb_plen_collection.remove()
        except:
            pass
        try:
            self.det_cone.remove()
        except:
            pass
        try:
            self.contour_cone.remove()
        except:
            pass
        try:
            for ctr in self.contour.collections:
                ctr.remove()
        except:
            pass
        try:
            for ctrpatch in self.contourgrp:
                for ctr in ctrpatch.collections:
                    try: ctr.remove()
                    except: pass
            self.contourgrp = []
        except:
            pass
        
    #**************************************************************************************
    def ConfigureRadPlot(self, x,y,z,rstart,rseclen,xshift,yshift, nmin, nmax, nlevels):
        delta_r = rseclen/float(len(y))
        r_lengths = rstart + np.arange(len(y))*delta_r
        R, th = np.meshgrid(r_lengths, x+180)
        theta_rad = np.deg2rad(-th+90)
        Rt_x = R * np.sin(theta_rad)  + xshift# turn radial grid points into (x, y)
        Rt_y = R * np.cos(theta_rad) + yshift
        levels = np.linspace(nmin, nmax, nlevels)
        return np.array([Rt_x,Rt_y,z,levels])
                    
    
    #**************************************************************************************
    def DrawLayout(self):
        ssw = self.ssw.GetVal()
        psw = self.psw.GetVal()
        sstth = self.sstth.GetVal()
        psp = self.psp.GetVal()
        ssp = self.ssp.GetVal()
        cor_x = self.cor_x.GetVal()
        cor_y = self.cor_y.GetVal()
        sdd = self.sdd.GetVal()
        s_len_x = self.s_len_x.GetVal()
        s_len_y = self.s_len_y.GetVal()
        omega = self.omega.GetVal()
        psw_sec = self.psw_sec.GetVal()
        ssw_sec = self.ssw_sec.GetVal()
        mu = self.att_coef.GetVal()/10.0   #now in mm-1    
        opacity = float(self.ui.opacity_edit.text())      
        #Primary beam
        try:
            sec_beam_x_proj = ssw/np.cos(np.deg2rad(90.0-sstth))
            b = 0.5*psw/np.tan(np.deg2rad(sstth))
            a = 0.5*sec_beam_x_proj - b
            c = psw/np.tan(np.deg2rad(sstth))
        except:
            sec_beam_x_proj = 0.0
            b = 0.0
            a = 0.0
            c = 0.0
        prim_beam_points = np.array([[-(c+a),-psw/2.0], [psp,-psw/2.0], [psp, psw/2.0], [-a,psw/2.0]])
        self.prim_beam = plt.Polygon(prim_beam_points, alpha=opacity, color="blue", linewidth=0.0)
        
        #Secondary beam
        a0 = np.array(pol2cart(ssw/2.0, 180-(180-90-sstth)))
        a1 = [-a,psw/2.0]
        a2 = a0 +  np.array(pol2cart(ssp, sstth+180))
        a3 = a2 +  np.array(pol2cart(ssw, 180+sstth + 90.0))
        a4 = [-a+sec_beam_x_proj,psw/2.0]
        sec_beam_points = np.array([a1, a2, a3, a4])
        self.sec_beam = plt.Polygon(sec_beam_points, alpha=opacity, color="green", linewidth=0.0)
        
        #Center of rotation
        self.cor = plt.Circle((0, 0), radius=0.5*np.max([psw,ssw]), fill = False, fc='none', ec='yellow', linestyle='dotted', alpha=opacity)
 
        
        #Detector cone
        try:
            stth = self.scanman.datasrc.dataset[self.scanman.datasrc.currset].currframe.x_2th
        except:
            stth = np.linspace(0,180,50)
        stth_pts = np.array(pol2cart(sdd,stth+180.0)).transpose()
        stth_pt_low = stth_pts[0]
        stth_pt_high = stth_pts[-1]
        minpt = [0.0, 0.0]
        maxpt = [0.0, 0.0]
        grpoints=np.array([np.array(m.xy).transpose()[0] for m in self.sh_gridpoints])
        grx=grpoints.transpose()[0]
        gry=grpoints.transpose()[1]
        m_low = (stth_pt_low[1]-gry)/(stth_pt_low[0]-grx)
        m_high = (stth_pt_high[1]-gry)/(stth_pt_high[0]-grx)
        if cart2pol(stth_pt_low[0],stth_pt_low[1])[1] < 0:
            minpt = grpoints[m_low.argmax()]
        else:
            minpt = grpoints[m_low.argmin()]
        if cart2pol(stth_pt_high[0],stth_pt_high[1])[1] < 0:
            maxpt = grpoints[m_high.argmin()]
        else:
            maxpt = grpoints[m_high.argmax()]
        self.det_cone_proj = plt.Polygon([minpt, stth_pt_low, stth_pt_high, maxpt],  alpha=opacity, color="orange", linewidth=0.0)
        sh_cone_proj = shgeom.Polygon(self.det_cone_proj.get_xy()) 
        
        cone_r1ssp_frac = 1.05
        cone_r2ssp_frac = 1.20
        conecircle = shgeom.Point([0,0]).buffer(ssp*cone_r1ssp_frac)
        sh_cone = conecircle.intersection(sh_cone_proj)
        cone_points = np.array(sh_cone.exterior.xy).transpose()
        self.det_cone = plt.Polygon(cone_points,  alpha=opacity, color="orange", linewidth=0.0)
        
        
        
        #Intensity fraction overlay
        currframe = self.scanman.datasrc.dataset[self.scanman.datasrc.currset].currframe
        outerconecircle = shgeom.Point([0,0]).buffer(ssp*cone_r2ssp_frac)
        sh_outercone = outerconecircle.intersection(sh_cone_proj)
        sh_contourcone = sh_outercone.difference(sh_cone)
        outercone_points = np.array(sh_contourcone.exterior.xy).transpose()
        self.contour_cone = plt.Polygon(outercone_points,  fill=False, linewidth=0.0)
        cone_r1_low = np.array(conecircle.intersection(shgeom.LineString([minpt, stth_pt_low])))[1]
        cone_r1_high = np.array(conecircle.intersection(shgeom.LineString([maxpt, stth_pt_high])))[1]
        cone_r1_ang_low = np.rad2deg(cart2pol(cone_r1_low[0],cone_r1_low[1])[1])
        cone_r1_ang_high = np.rad2deg(cart2pol(cone_r1_high[0],cone_r1_high[1])[1])
        cone_ang1_range = np.linspace(cone_r1_ang_low,cone_r1_ang_high,len(stth),True)
        cone_r2_low = np.array(outerconecircle.intersection(shgeom.LineString([minpt, stth_pt_low])))[1]
        cone_r2_high = np.array(outerconecircle.intersection(shgeom.LineString([maxpt, stth_pt_high])))[1]
        cone_r2_ang_low = np.rad2deg(cart2pol(cone_r2_low[0],cone_r2_low[1])[1])
        cone_r2_ang_high = np.rad2deg(cart2pol(cone_r2_high[0],cone_r2_high[1])[1])
        cone_ang2_range = np.linspace(cone_r2_ang_low,cone_r2_ang_high,len(stth),True)
        
        m_low = (cone_r1_low[1]-cone_r2_low[1])/(cone_r1_low[0]-cone_r2_low[0])
        c_low = cone_r1_low[1]-m_low*cone_r1_low[0]
        m_high = (cone_r1_high[1]-cone_r2_high[1])/(cone_r1_high[0]-cone_r2_high[0])
        c_high = cone_r1_high[1]-m_high*cone_r1_high[0]
        x_intersect = (c_high-c_low)/(m_low-m_high)
        y_intersect = m_low*x_intersect+c_low
        x_intersect=0.0
        y_intersect=0.0
        r_to_origen, th = cart2pol(x_intersect, y_intersect)

        
        
        rbounds = []
        rbounds.append(ssp*cone_r1ssp_frac + r_to_origen)
        rseclen = ssp*cone_r2ssp_frac-ssp*cone_r1ssp_frac
        contourgroups = []
        
        nmin1d = min([dset.currframe.y_2th.min() for dset in self.scanman.datasrc.dataset[1:]])
        nmax1d = max([dset.currframe.y_2th.max() for dset in self.scanman.datasrc.dataset[1:]])
        if self.ui.dpattern_check.isChecked() == True:
            if len(currframe.vc_2th)>1: #2D
                nmin = min([dset.currframe.n.min() for dset in self.scanman.datasrc.dataset[1:]])
                nmax = max([dset.currframe.n.max() for dset in self.scanman.datasrc.dataset[1:]])
                contourgroups.append(self.ConfigureRadPlot(currframe.hc_2th, currframe.vc_2th, currframe.n.transpose() ,
                                                           rbounds[-1], rseclen, x_intersect, y_intersect, nmin, nmax,8))
                rbounds.append(rbounds[-1]+rseclen)
            #1D data
            x1d=currframe.x_2th
            y1d=np.arange(2)
            n1d=np.concatenate([[currframe.y_2th], [currframe.y_2th]]).transpose()
            contourgroups.append(self.ConfigureRadPlot(x1d, y1d, n1d ,rbounds[-1], rseclen, 
                                                       x_intersect, y_intersect,nmin1d,nmax1d,128))
            rbounds.append(rbounds[-1]+rseclen/2.0)        #1D data only uses 2 lines        
            
            

        #Attenuation correction coefficient
        attcor_coeff = 1.0/self.comb_atten
        if self.ui.colourScaleAuto_check.isChecked() == True:
            nminifac = attcor_coeff.min(); nmaxifac = attcor_coeff.max()
        else:
            nminifac = float(self.ui.colourScaleMin_edit.text()); nmaxifac = float(self.ui.colourScaleMax_edit.text())
        if len(self.comb_atten) == len(stth) and self.ui.ifrac_check.isChecked() == True:
            n1d=np.concatenate([[attcor_coeff], [attcor_coeff]]).transpose()
            contourgroups.append(self.ConfigureRadPlot(stth, np.arange(2), n1d ,rbounds[-1], rseclen/2.0, x_intersect, y_intersect, nminifac, nmaxifac,128))
            rbounds.append(rbounds[-1]+rseclen/4.0)
            
        #corrected 1D
        if self.ui.dpattern_check.isChecked() == True:
            n1d=currframe.y_2th * attcor_coeff / nmaxifac
            nmin = n1d.min(); nmax = n1d.max()
            n1d=np.concatenate([[n1d], [n1d]]).transpose()
            contourgroups.append(self.ConfigureRadPlot(stth, np.arange(2), n1d ,rbounds[-1], rseclen, x_intersect, y_intersect, nmin1d, nmax1d,128))
            rbounds.append(rbounds[-1]+rseclen/2.0)
            
        axis = self.ui.exp_graphic.figure.axes[0]
        #DM: axis.hold is now deprecated.  axis.hold(True)   
        
        #Add everything to the axis
        if self.ui.ifrac_check.isChecked() == True: #or self.ui.dpattern_check.isChecked() == True:
            self.contour_cone.set_zorder(3)
            axis.add_patch(self.contour_cone)   
 
        if  self.ui.dpattern_check.isChecked() == True or self.ui.ifrac_check.isChecked() == True:
            self.contourgrp=[]
            for ctr in contourgroups:
                self.contourgrp.append(axis.contourf(ctr[0], ctr[1], ctr[2], levels = ctr[3]))
        if self.ui.pb_check.isChecked() == True:
            self.prim_beam.set_zorder(2)
            axis.add_patch(self.prim_beam)
        if self.ui.sb_check.isChecked() == True:
            self.sec_beam.set_zorder(4)
            axis.add_patch(self.sec_beam) 
        if self.ui.sample_check.isChecked() == True: 
            self.sample.set_zorder(1)        
            axis.add_patch(self.sample)
        if self.ui.gvol_check.isChecked() == True:  
            self.gvol.set_zorder(5)
            axis.add_patch(self.gvol)
        if self.ui.gpoints_check.isChecked() == True:  
            self.gridcollection.set_zorder(6)
            axis.add_collection(self.gridcollection)    
        if self.ui.cor_check.isChecked() == True:  
            self.cor.set_zorder(7) 
            axis.add_patch(self.cor)
        if self.ui.dcone_check.isChecked() == True: 
            self.det_cone.set_zorder(3) 
            axis.add_patch(self.det_cone)

        axis.relim(False)
        if self.ui.lock_axis_check.isChecked() == False:
            axis.autoscale(True, 'both', False)

        else:
            axis.autoscale(False, 'both', False)
            axis.set_xbound(self.viewLim[0])
            axis.set_ybound(self.viewLim[1])

                      
            
            
        self.expgraph.graph.draw()
        self.viewLim = [axis.get_xbound(),axis.get_ybound()]
        self.PopulateParamCombos()

    #**************************************************************************************
    def Animate(self):
        selectionsettings = mylib.Getexportsettings(self)
        dirname = self.filedialog.getExistingDirectory(self, "Select export dir", self.lastdir)
        if dirname == "": return
        self.lastdir = dirname
        imagepathlist = []
        fnamebase="default"
        progressfiles = ProgressBar("Animating files...", selectionsettings.numfiles)
        for filei in selectionsettings.flistidx:
            progressfiles.setinfo(self.scanman.datasrc.filename)
            fnamebase = path.join(dirname,str.split(path.basename(self.scanman.datasrc.filename),".")[0]  + self.scanman.modext)
            self.scanman.ui.sourceGroupBox.SelectDataFile(filei)
            
            f = open(fnamebase+"_a.xy", 'w')        #_a indicates attenuation corrected data 
            src = self.scanman.datasrc
            self.scanman.exportparams.sort()
            axistype = self.scanman.axistype
            
            
            
            if self.ui.all_radio.isChecked():
                selectionsettings.setend = len(self.scanman.datasrc.dataset)
            numsets = selectionsettings.setend - selectionsettings.setstart
            progressdataset = ProgressBar("Calculate and animate datasets...", numsets)
            for nr in range(selectionsettings.setstart,selectionsettings.setend):
                progressdataset.setinfo(self.scanman.datasrc.filename)
                fname = fnamebase +"_"+str(nr)+ ".png"
                fcorr = open(fnamebase+"_corrcoef_"+str(nr)+".txt", 'w')
                self.scanman.SelectData(nr,display=False)
                self.ui.exp_graphic.figure.savefig(fname,format="png", dpi=300, transparent=False)
                if axistype == 'Channel':
                    x = np.array(src.dataset[nr].currframe.x_chan).astype(float)
                    y = src.dataset[nr].currframe.y.astype(float)
                elif axistype == 'Position':
                    x = src.dataset[nr].currframe.x_mm.astype(float)
                    y = src.dataset[nr].currframe.y.astype(float)
                elif axistype == 'Angle':
                    x = src.dataset[nr].currframe.x_2th.astype(float)
                    y = src.dataset[nr].currframe.y_2th.astype(float)
                elif axistype == 'd-spacing':
                    x = src.dataset[nr].currframe.x_d.astype(float)
                    y = src.dataset[nr].currframe.y_2th.astype(float)
                nrpoints = len(y)
                f.write('XYDATA\n')
                f.write("File name: %s\n" %(src.dataset[nr].filename))
                f.write("| Dataset: %s| Type: %s\n" %(nr, src.ylabel))
                detstr = ""
                for param in src.dataset[nr].detprm: detstr = detstr + "| " + param +":" + str(src.dataset[nr].detprm[param])
                f.write("%s\n" %(detstr))
                paramstr = ""
                for param in self.scanman.exportparams: 
                    try:
                        paramstr = paramstr + "| " + param +":" + src.dataset[nr].prm[param]
                    except:
                        True
                if paramstr == "": paramstr = "| set:"+str(nr)      #No parameters were selected to export, but we need some text in that line
                f.write("%s\n" %(paramstr))
                f.write("%s Intensity\n" %(axistype))
                for i in np.arange(nrpoints):
                    f.write('%f %f\n' % (x[i], y[i]*1/self.comb_atten[i]))
                    fcorr.write('%f %f\n' % (x[i], 1.0/self.comb_atten[i]))
                f.write("\n")
                fcorr.write("\n")
                imagepathlist.append(fname)
                if progressdataset.wasCanceled(): break
                progressdataset.step()
            
            
            f.truncate(f.tell()-2)      #Removes the last extra newline
            fcorr.truncate(f.tell()-2)      #Removes the last extra newline
            f.close()
            fcorr.close()
            if progressfiles.wasCanceled(): break
            progressfiles.step()
        images = [Image.open(image) for image in imagepathlist]
        gifname = fnamebase+".gif"
        gif = images[0]
        gif.save(fp=gifname, format='gif', save_all=True, append_images=images[1:])
        try:
            execmd = '"' + os.getcwd()+'\Attenuation\gif2mp4.bat" "' + gifname + '"'
            os.system('"' + execmd + '"')
        except:
            pass
        
    
    def OutputXY(self,fname="default.xy", nr = -1):
            f = open(fname, 'w')
            src = self.scanman.datasrc
            self.scanman.exportparams.sort()
            axistype = self.scanman.axistype

            if axistype == 'Channel':
                x = np.array(src.dataset[nr].currframe.x_chan).astype(float)
                y = src.dataset[nr].currframe.y.astype(float)
            elif axistype == 'Position':
                x = src.dataset[nr].currframe.x_mm.astype(float)
                y = src.dataset[nr].currframe.y.astype(float)
            elif axistype == 'Angle':
                x = src.dataset[nr].currframe.x_2th.astype(float)
                y = src.dataset[nr].currframe.y_2th.astype(float)
            elif axistype == 'd-spacing':
                x = src.dataset[nr].currframe.x_d.astype(float)
                y = src.dataset[nr].currframe.y_2th.astype(float)
            nrpoints = len(y)
                
            f.write('XYDATA\n')
            f.write("File name: %s\n" %(src.dataset[nr].filename))
            f.write("| Dataset: %s| Type: %s\n" %(nr, src.ylabel))
            detstr = ""
            for param in src.dataset[nr].detprm: detstr = detstr + "| " + param +":" + str(src.dataset[nr].detprm[param])
            f.write("%s\n" %(detstr))
            paramstr = ""
            for param in self.scanman.exportparams: 
                try:
                    paramstr = paramstr + "| " + param +":" + src.dataset[nr].prm[param]
                except:
                    True
            if paramstr == "": paramstr = "| set:"+str(nr)      #No parameters were selected to export, but we need some text in that line
            f.write("%s\n" %(paramstr))
            f.write("%s Intensity\n" %(axistype))
            for i in np.arange(nrpoints):
                f.write('%f %f\n' % (x[i], y[i]))
            f.write("\n")
                
                
            y_2th = self.scanman.datasrc.dataset[self.scanman.datasrc.currset].currframe.y_2th
            self.comb_atten
            a=1    

#**************************************************************************************
    def Test2 (self):
        #self.widget = MyPygletWidget()
        #self.ui.pyglet_layout.addWidget(self.widget)
        self.pygletwidget.setSizePolicy(self.ui.cor_graphic.sizePolicy())
        self.pygletwidget.setMinimumSize(QtCore.QSize(200, 200))
        self.trm_cyl=trimesh.creation.cylinder(100,50,32)
        self.trm_cyl2=trimesh.creation.cylinder(50,60,100)
        self.trm_cyl2.apply_translation([80,150,30])
        self.trm_new=self.trm_cyl.difference(self.trm_cyl2)
        self.pygletwidget.mesh= self.trm_cyl2
        
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glLoadIdentity()
        
        if self.pygletwidget.mesh != "":
            self.pygletwidget.draw_mesh_faces_flat(self.pygletwidget.mesh,False)
            True
        #self.pygletwidget.draw_mesh_faces_flat(self.trm_new, will_draw_edges=True)
        #self.pygletwidget.graphics.draw(2, pyglet.gl.GL_POINTS,('v3f', (10.0, 15.0, 0.0, 30.0, 35.0, 0.0)))
        #self.trm_new.show()

        pass
    
#**************************************************************************************
    def Test (self):
        self.glwidget.setSizePolicy(self.ui.cor_graphic.sizePolicy())
        self.glwidget.setMinimumSize(QtCore.QSize(640, 480))
        self.trm_positioner = trimesh.load("D:/home/deon/Develop/BulletTest/models/positioner_base.stl")
        self.trm_detector = trimesh.load("D:/home/deon/Develop/BulletTest/models/detector.stl")

        self.componentlist = []
        #self.glwidget.set_projection(0.01,10000,45)
        #self.glwidget.set_radius(1000)
        
        
        #component_positioner = Component.Component("positioner")
        #component_positioner.setcolor('red',0.50)
        #component_positioner.loadstl("D:/home/deon/Develop/BulletTest/models/positioner_base.stl")
        #self.glwidget.AddComponent(component_positioner)
        
        #component_detector = Component.Component("detector")
        #component_detector.setcolor('blue',0.5)
        #component_detector.loadstl("D:/home/deon/Develop/BulletTest/models/detector.stl")
        #self.glwidget.AddComponent(component_detector)
        
        meshgen = Component.MeshGen()
        
        component_sample = Component.Component("sample")
        mesh_sample = trimesh.primitives.Cylinder(height = 1.0, radius = 0.5, sections = 32)
        component_sample.setcolor('pink',0.5)
        component_sample.loadtrimesh(mesh_sample)
        
                
        component_primbeam = Component.Component("primbeam")
        mesh_primbeam = meshgen.primarybeam(psw = 4, psh = 10, cor_to_slit = 25, cor_to_stop = 50, wdiv = 15, hdiv = 10)
        component_primbeam.setcolor('green',0.5)
        component_primbeam.loadtrimesh(mesh_primbeam)
        

        component_secbeam = Component.Component("secbeam")
        mesh_secbeam = meshgen.secondarybeam(ssw=5, ssh=100, cor_to_slit=25, cor_to_det=1149, detw=300, deth=300, stth=90, extends=50)
        component_secbeam.setcolor('blue',0.5)
        component_secbeam.loadtrimesh(mesh_secbeam)
        
        
        #component_instgvol = Component.Component("instgvol")
        #mesh_instgvol = mesh_primbeam.intersection(mesh_secbeam)
        #component_instgvol.setcolor('red',0.5)
        #component_instgvol.loadtrimesh(mesh_instgvol)
        
        
        #smesh_gvol.show()
        
        
        self.glwidget.AddComponent(component_sample)
        #self.glwidget.AddComponent(component_primbeam)
        #self.glwidget.AddComponent(component_secbeam)
        #self.glwidget.AddComponent(component_instgvol)
        

        centroid = mesh_sample.centroid
        self.glwidget.set_center(centroid)
        # self.glwidget.getLookAt(np.array([0,0,-1000]), self.center, np.array([0,1,0]))
        self.glwidget.radius =self.glwidget.comps.absmax*1.1
        a = self.glwidget.getLookAt(np.array([0,0,-self.glwidget.radius]), centroid, np.array([0,1,0]))
        #b = glm.lookAt(np.array([0,0,-self.glwidget.radius]), centroid, np.array([0,1,0]))
        
         
        
        self.glwidget.getPerspective(self.glwidget.fovdeg, 0.1, 1000)

        #testmesh = mesh_primbeam + mesh_secbeam + mesh_sample
        #testmesh.show()


        
        True
        #self.glwidget.AddComponent(component_primbeam)
        

        #component_cyl = Component.Component("cyl")
        #mesh = trimesh.primitives.Cylinder(height = 2.0, radius = 1.5, sections = 32)
        #component_cyl.setcolor('purple',0.5)
        #component_cyl.position = [1.0, 2.0, 0.0]
        #component_cyl.loadtrimesh(mesh)
        #self.glwidget.AddComponent(component_cyl)
        
        #component_test = Component.Component("test")
        #mesh = meshgen.plane()
        #component_test.loadtrimesh(mesh)
        #component_test.setcolor('black',0.5)
        #component_test.updatevertexdata()
        #self.glwidget.AddComponent(component_test)
        
        #component_test2 = Component.Component("test2")
        #mesh2 = meshgen.plane2()
        #component_test2.loadtrimesh(mesh2)
        #component_test2.setcolor('green',0.5)
        #component_test2.updatevertexdata()
        #self.glwidget.AddComponent(component_test2)
        
        component_test3 = Component.Component("test3")
        mesh3 = meshgen.orthocube()
        component_test3.setcolor('pink',0.5)
        component_test3.position = [1.0, 2.0, 0.0]
        component_test3.loadtrimesh(mesh3)
        #self.glwidget.AddComponent(component_test3)
        
        #c1 = Component.Component("c1")
        #vertices = [[0., 0., 0.],  [0., 0., 1.],  [0., 1., 0.],  [0., 1., 1.],  [1., 0., 0.],  [1., 0., 1.],  [1., 1., 0.],  [1., 1., 1.]]
        #m1 = meshgen.hexahedron(vertices)
        
                
        #self.glwidget.AddTrimesh(self.trm_cyl)
        #self.glwidget.UploadVertices(mesh.vertices.flatten(),mesh.faces.flatten())
        
        True
    
#**************************************************************************************
if __name__ == '__main__':
    
    app = qt.QApplication(sys.argv)
    window=Attenuation3DDEF()
    window.show()
    sys.exit(app.exec_())