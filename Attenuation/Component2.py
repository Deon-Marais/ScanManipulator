'''
Created on 07 Feb 2019

@author: Deon
'''

import numpy as np
import trimesh
from OpenGL.GL import *
from matplotlib import colors


class GLnfo():
    def __init__(self):
        self.vao = ""
        self.bufs = ""
        self.positions = np.array([])
        self.elements = np.array([])
        self.vertexdata = np.array([])
        self.normals = np.array([])
        self.nrpositions = 0
        self.nrelements = 0
        self.primitive_type = GL_TRIANGLES      #GL_LINES
        
    def setprimitive(self,prim):
        self.primitive_type = prim
        


class Component():
    '''
    classdocs
    '''

#**************************************************************************************
    def __init__(self,name):
        '''
        Constructor
        '''
        self.name = name
        self.position = np.array([0.0,0.0,0.0])
        self.color = np.array([255,255,255])
        self.opacity = 0.0
        self.issample = False
        self.stlpath = ""
        self.trimeshobj = ""
        self.glnfo = GLnfo()
        #self.glwidget = glwidget
        
    def setcolor(self,colorname='white', opacity=0.0):
        colorlist = colors.get_named_colors_mapping().keys()
        if colorname not in colorlist:
            colorname = "xkcd:"+colorname
            if colorname not in colorlist:
                colorname = 'white'
        #self.color = (np.array(colors.to_rgb(colorname))*255).astype(int)
        self.color = np.array(colors.to_rgb(colorname))
        self.opacity = opacity
        True
        
    
    
#**************************************************************************************
    def loadstl(self,filename):
        self.stlpath = filename
        self.trimeshobj = trimesh.load(self.stlpath)
        self.glfromstl()
        
         
#**************************************************************************************
    def glfromstl(self):
        self.glnfo.positions = self.trimeshobj.vertices.flatten()
        self.glnfo.elements = self.trimeshobj.faces.flatten().astype(int)
        #self.glnfo.normals = self.trimeshobj.face_normals.flatten()
        self.glnfo.nrpositions = self.glnfo.positions.size
        self.glnfo.nrelements = self.glnfo.elements.size
        True
        
    def updatevertexdata(self):
        #r,g,b = self.color
        #self.glnfo.vertexdata = np.array([[x,y,z,r,g,b,self.opacity] for x,y,z in self.trimeshobj.vertices]).flatten().astype(np.float32)
        True
 
        nrvtx = len(self.trimeshobj.vertices)
        self.glnfo.vertexdata = np.zeros(nrvtx, [("position", np.float32, 3), ("color", np.float32, 4)])
        posbuf = self.trimeshobj.vertices.astype(np.float32)
        r,g,b = self.color.astype(np.float32)
        a = np.float32(self.opacity)
        colorbuf = np.array([[r,g,b,a] for i in range(nrvtx)])
        
        #for i in range(nrvtx):
        #    self.glnfo.vertexdata['position'][i] = posbuf[i]
        #    self.glnfo.vertexdata['color'][i] = colorbuf[i]

        #True
        
        self.glnfo.vertexdata = np.zeros(3, [("position", np.float32, 3),
                    ("color",    np.float32, 4)])
        self.glnfo.vertexdata['position'] = (-100,+100,0),   (+100,+100,0),   (-100,-100,100)
        self.glnfo.vertexdata['color']    = (1,1,0,0.5), (1,0,0,0.5), (0,0,1,0.5)
        self.glnfo.elements = [0,1,2]
        self.glnfo.nrelements = 1
        self.glnfo.nrpositions = 3
         
        
           