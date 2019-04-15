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
        #self.bufs = ""
        #self.positions = np.array([])
        #self.elements = np.array([])
        #self.vertexdata = np.array([])
        #self.databuffer = np.array([])
        #self.normals = np.array([])
        #self.nrpositions = 0
        #self.nrelements = 0
        #self.coloroffset = 0
        self.glelementsbuffer = ""
        self.glcolorbuffer = ""
        self.glvertexbuffer = ""
        self.primitive_type = GL_TRIANGLES      #GL_LINES
        #self.primitive_type = GL_LINES
        
    def setprimitive(self,prim):
        self.primitive_type = prim

#**************************************************************************************
class MeshGen(): 
    def __init__(self):
        True
    
#**************************************************************************************
    def primarybeam(self, psw, psh, cor_to_slit, cor_to_stop, wdiv = 0.0, hdiv = 0.0):
        #wdiv and hdiv in degrees
        totl = cor_to_slit + cor_to_stop
        dely = np.tan(np.radians(wdiv)) * totl
        delz = np.tan(np.radians(hdiv)) * totl
        p4 = [cor_to_slit, -psw/2.0, -psh/2.0]
        p6 = [cor_to_slit, +psw/2.0, -psh/2.0]
        p5 = [cor_to_slit, -psw/2.0, +psh/2.0]
        p7 = [cor_to_slit, +psw/2.0, +psh/2.0]
        p0 = [-cor_to_stop, -psw/2.0 -dely, -psh/2.0 - delz]
        p2 = [-cor_to_stop, +psw/2.0 +dely, -psh/2.0 - delz]
        p1 = [-cor_to_stop, -psw/2.0 -dely, +psh/2.0 + delz]
        p3 = [-cor_to_stop, +psw/2.0 +dely, +psh/2.0 + delz]
        vertices = [p0,p1,p2,p3,p4,p5,p6,p7]
        mesh = self.hexahedron(vertices)
        return mesh
    
#**************************************************************************************
    def secondarybeam(self, ssw, ssh, cor_to_slit, cor_to_det, detw, deth, stth, extends = 10.0):
        det_to_slit = cor_to_det - cor_to_slit
        det_dely = detw/2.0 - ssw/2.0
        alpha = np.arctan(det_dely/det_to_slit)
        det_to_intercept_x = (detw/2.0)/np.tan(alpha)
        cor_to_intercept_x = -cor_to_det+det_to_intercept_x
        
        det_delz = deth/2.0 - ssh/2.0
        beta = np.arctan(det_delz/det_to_slit)
        det_delz2 = np.tan(beta)*det_to_intercept_x
        inetecept_delz = (deth/2.0-det_delz2)
        
        p0 = [-cor_to_det, -detw/2.0, -deth/2.0]
        p2 = [-cor_to_det, +detw/2.0, -deth/2.0]
        p1 = [-cor_to_det, -detw/2.0, +deth/2.0]
        p3 = [-cor_to_det, +detw/2.0, +deth/2.0]
        p4 = [cor_to_intercept_x, 0, -inetecept_delz]
        p6 = [cor_to_intercept_x, 0, -inetecept_delz]
        p5 = [cor_to_intercept_x, 0, +inetecept_delz]
        p7 = [cor_to_intercept_x, 0, +inetecept_delz]
        vertices = [p0,p1,p2,p3,p4,p5,p6,p7]
        detside_mesh = self.hexahedron(vertices)
        
        
        det_to_extends_x = det_to_intercept_x+extends
        ext_y = np.tan(alpha)*extends
        det_delz3 = np.tan(beta)*(det_to_extends_x)
        exetends_delz = (deth/2.0 - det_delz3)
        p0 = [cor_to_intercept_x, 0, -inetecept_delz]
        p2 = [cor_to_intercept_x, 0, -inetecept_delz]
        p1 = [cor_to_intercept_x, 0, +inetecept_delz]
        p3 = [cor_to_intercept_x, 0, +inetecept_delz]
        p6 = [extends, +ext_y, -exetends_delz]
        p7 = [extends, +ext_y, +exetends_delz]
        p4 = [extends, -ext_y, -exetends_delz]
        p5 = [extends, -ext_y, +exetends_delz]
        vertices = [p0,p1,p2,p3,p4,p5,p6,p7]
        extended_mesh = self.hexahedron(vertices)
        
        #Penumbra
        det_ext_y = detw/2.0 + ssw/2.0
        gamma = np.arctan(det_ext_y/det_to_slit)
        y_ext = np.tan(gamma)*det_to_extends_x - detw/2.0
        det_ext_z = deth/2.0 + ssh/2.0
        eta = np.arctan(det_ext_z/det_to_slit)
        z_ext = np.tan(eta)*det_to_extends_x - deth/2.0

        p0 = [-cor_to_slit, -ssw/2.0, -ssh/2.0]
        p2 = [-cor_to_slit, +ssw/2.0, -ssh/2.0]
        p1 = [-cor_to_slit, -ssw/2.0, +ssh/2.0]
        p3 = [-cor_to_slit, +ssw/2.0, +ssh/2.0]
        p6 = [extends, +y_ext, -z_ext]
        p7 = [extends, +y_ext, +z_ext]
        p4 = [extends, -y_ext, -z_ext]
        p5 = [extends, -y_ext, +z_ext]
        vertices = [p0,p1,p2,p3,p4,p5,p6,p7]
        penumbra_mesh = self.hexahedron(vertices)

        
        #mesh = detside_mesh + extended_mesh + penumbra_mesh
        mesh = detside_mesh.union(penumbra_mesh)
        
        ang = np.radians(stth)
        rotmat = trimesh.transformations.rotation_matrix(angle = ang, direction = [0,0,1], point = [0,0,0])
        mesh.apply_transform(rotmat)
        return mesh

#**************************************************************************************
    def hexahedron(self, vertices = [0,0,0,0,0,1,0,1,0,0,1,1,1,0,0,1,0,1,1,1,0,1,1,1],  transform = None ):
        #vertices = [0,0,0,0,0,1,0,1,0,0,1,1,1,0,0,1,0,1,1,1,0,1,1,1] 
        vertices = np.array(vertices, dtype=np.float32).reshape((-1,3))
        #vertices -= 0.5

        faces = [1,3,0,4,1,0,0,3,2,2,4,0,1,7,3,5,1,4,5,7,1,3,7,2,6,4,2,2,7,6,6,5,4,7,5,6] 
        faces = np.array(faces, dtype=np.int64).reshape((-1,3))
     
        face_normals = [-1,0,0,0,-1,0,-1,0,0,0,0,-1,0,0,1,0,-1,0,0,0,1,0,1,0,0,0,-1,0,1,0,1,0,0,1,0,0]
        face_normals = np.array(face_normals, dtype=np.float32).reshape(-1,3)

        box = trimesh.Trimesh(vertices     = vertices, 
              faces        = faces,
              face_normals = face_normals,
              process      = False)
               
        if transform is not None:
            box.apply_transform(transform)
        return box
    
    def plane(self):
        vertices = [0.75, 0.75, 0.0,
                    0.75, -0.75, 0.0,
                    -0.75, -0.75, 0.0]
        vertices = np.array(vertices, dtype=np.float32).reshape((-1,3)) 
        mesh = trimesh.Trimesh(vertices = vertices)
        return mesh
    
    def plane2(self):
        z=.99
        vertices = [-0.75, -0.75, z,
                    -0.1, 1.75, z,
                    0.75, -0.75, z,
                    0.75, 0.75, z,
                    0.75, -0.75, z,
                    -0.75, -0.75, z]
        vertices = np.array(vertices, dtype=np.float32).reshape((-1,3)) 
        faces = range(1,len(vertices)+1)
        faces = np.array(faces, dtype=np.int32).reshape((-1,3))
        mesh = trimesh.Trimesh(vertices = vertices,
                               faces        = faces,
                               process      = False)
        return mesh
    
    def orthocube(self):
        #z1=1.25
        #z2=2.75
        #z1=0.25
        #z2=0.75
        z1 = -0.1
        z2 = -0.6
        vertices = [0.25,0.25,z1,
                    0.25,-0.25,z1,
                    -0.25,0.25,z1,
                    0.25,-0.25,z1,
                    -0.25,-0.25,z1,
                    -0.25,0.25,z1,
                    0.25,0.25,z2,
                    -0.25,0.25,z2,
                    0.25,-0.25,z2,
                    0.25,-0.25,z2,
                    -0.25,0.25,z2,
                    -0.25,-0.25,z2,
                    -0.25,0.25,z1,
                    -0.25,-0.25,z1,
                    -0.25,-0.25,z2,
                    -0.25,0.25,z1,
                    -0.25,-0.25,z2,
                    -0.25,0.25,z2,
                    0.25,0.25,z1,
                    0.25,-0.25,z2,
                    0.25,-0.25,z1,
                    0.25,0.25,z1,
                    0.25,0.25,z2,
                    0.25,-0.25,z2,
                    0.25,0.25,z2,
                    0.25,0.25,z1,
                    -0.25,0.25,z1,
                    0.25,0.25,z2,
                    -0.25,0.25,z1,
                    -0.25,0.25,z2,
                    0.25,-0.25,z2,
                    -0.25,-0.25,z1,
                    0.25,-0.25,z1,
                    0.25,-0.25,z2,
                    -0.25,-0.25,z2,
                    -0.25,-0.25,z1]
        vertices = np.array(vertices, dtype=np.float32).reshape((-1,3)) 
        faces = range(len(vertices))
        faces = np.array(faces, dtype=np.int32).reshape((-1,3))
        mesh = trimesh.Trimesh(vertices = vertices,
                               faces        = faces,
                               process      = True)
        return mesh
    

#**************************************************************************************
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
        
#**************************************************************************************
    def setcolor(self,colorname='white', opacity=0.0):
        colorlist = colors.get_named_colors_mapping().keys()
        if colorname not in colorlist:
            colorname = "xkcd:"+colorname
            if colorname not in colorlist:
                colorname = 'white'
        self.color = np.array(colors.to_rgb(colorname))
        self.opacity = opacity
        True
        
    
    
#**************************************************************************************
    def loadtrimesh(self,mesh):
        self.trimeshobj = mesh
        self.trimeshobj.apply_translation(self.position)
        self.glfromtrimesh()
        
#**************************************************************************************
    def loadstl(self,filename):
        self.stlpath = filename
        self.trimeshobj = trimesh.load(self.stlpath)
        self.trimeshobj.apply_translation(self.position)
        self.glfromtrimesh()
        
         
#**************************************************************************************
    def glfromtrimesh(self):
        r,g,b = self.color
        self.glnfo.colorbuf = np.array([r,g,b,self.opacity]*len(self.trimeshobj.vertices)).astype(np.float32)
        self.glnfo.posbuf = np.array(self.trimeshobj.vertices).flatten().astype(np.float32)
        self.glnfo.elementsbuf = np.array(self.trimeshobj.faces.flatten()).astype(np.int32)
        self.glnfo.nrelements = self.glnfo.elementsbuf.size
        self.glnfo.nrpositions = self.glnfo.posbuf.size
       
        

        
           