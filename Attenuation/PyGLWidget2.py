# -*- coding: utf-8 -*-
#===============================================================================
#
# PyGLWidget.py
#
# A simple GL Viewer.
#
# Copyright (c) 2011, Arne Schmitz <arne.schmitz@gmx.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#===============================================================================

from PyQt4 import QtCore, QtGui, QtOpenGL
import math
import numpy as np
import numpy.linalg as linalg
import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *
from itertools import izip
from Component import Component
from GLshaders import GLshaders


class PyGLWidget(QtOpenGL.QGLWidget):

    # Qt signals
    signalGLMatrixChanged = QtCore.pyqtSignal()
    rotationBeginEvent = QtCore.pyqtSignal()
    rotationEndEvent = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        format = QtOpenGL.QGLFormat()
        format.setSampleBuffers(True)
        QtOpenGL.QGLWidget.__init__(self, format, parent)
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setMouseTracking(True)

        self.modelview_matrix_  = []
        self.translate_vector_  = [0.0, 0.0, 0.0]
        self.viewport_matrix_   = []
        self.projection_matrix_ = []
        self.near_   = 0.1
        self.far_    = 100.0
        self.fovy_   = 45.0
        self.radius_ = 5.0
        self.last_point_2D_ = QtCore.QPoint()
        self.last_point_ok_ = False
        self.last_point_3D_ = [1.0, 0.0, 0.0]
        self.isInRotation_  = False

        self.mesh = ""
        self.edges = 0
        self.nrelements = []

        #self.glshaders = GLshaders()
        #glUseProgram(self.glshaders.program)
        self.direction = [0.0, 2.0, -1.0, 1.0]  # Direction of light
        #self.direction = [100,0,1]  # Direction of light
        
        self.intensity = [0.7, 0.7, 0.7, 1.0] # Intensity of light
        self.ambient_intensity = [0.3, 0.3, 0.3, 1.0] # Intensity of ambient light
        self.components = {}

    @QtCore.pyqtSlot()
    def printModelViewMatrix(self):
        print self.modelview_matrix_

    def initializeGL(self):
        self.glshaders = GLshaders()
        glUseProgram(self.glshaders.program)
        
        glClearColor(0.0, 1.0, 0.0, 1.0)
        #glClearDepth(1.0)
        #glEnable(GL_DEPTH_TEST)
        #glDepthFunc(GL_LEQUAL)
        #glShadeModel(GL_FLAT)
        #glEnable(GL_LIGHTING)
        #glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient_intensity)
        #glEnable(GL_LIGHT0)
        #glLightfv(GL_LIGHT0, GL_POSITION, self.direction)
        #glEnable(GL_COLOR_MATERIAL)
        #glColorMaterial(GL_FRONT,GL_AMBIENT_AND_DIFFUSE)
        self.reset_view()

    def resizeGL(self, width, height):
        glViewport( 0, 0, width, height );
        self.set_projection( self.near_, self.far_, self.fovy_ );
        #self.updateGL()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glColorMaterial(GL_FRONT,GL_AMBIENT_AND_DIFFUSE)
        self.reset_view()
        #for name in self.components.iterkeys():
        for name in self.components.keys():
            glnfo = self.components[name].glnfo
            glBindVertexArray(glnfo.vao)
            
            glDrawElements(glnfo.primitive_type  , glnfo.nrelements, GL_UNSIGNED_INT, None)
            #glDrawArrays(glnfo.primitive_type,0,glnfo.nrelements)
            True
        #self.swapBuffers()
        
            
        
    def paintGL2(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glBindVertexArray(self.__vao)  
        #glDrawElements(GL_TRIANGLES  , self.nrelements, GL_UNSIGNED_INT, None)
        #glDrawElements( GL_TRIANGLES  , self.nrelements.sum(), GL_UNSIGNED_INT, None)
        glDrawElements( GL_LINES  , self.nrelements.sum(), GL_UNSIGNED_INT, None)
        
        #points = np.array([(i,0,0) for i in range( 8 )] + [(i,1,0) for i in range( 8 )], 'd')
        #indices = np.array([[0,8,9,1, 2,10,11,3,],[4,12,13,5,6,14,15,7],],'B')
        #counts = [ len(x) for x in indices ]
                
        #indices = np.array([0])
        #for i in range(len(self.nrelements)-1):
        #    indices = np.append(indices,self.nrelements[i]-1)
            
        #a = [np.append(indices,self.nrelements[i]+1) for i in range(len(self.nrelements)-1)]
        #glMultiDrawElements(GL_TRIANGLES, self.nrelements,  GL_UNSIGNED_INT, indices, self.nrmeshes)        
        #glMultiDrawElements(GL_TRIANGLES, self.nrelements,  GL_UNSIGNED_INT, self.indices, self.nrmeshes)
        True
    
    def set_projection(self, _near, _far, _fovy):
        self.near_ = _near
        self.far_ = _far
        self.fovy_ = _fovy
        self.makeCurrent()
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        gluPerspective( self.fovy_, float(self.width()) / float(self.height()),
                        self.near_, self.far_ )
        self.updateGL()

    def set_center(self, _cog):
        self.center_ = _cog
        self.view_all()

    def set_radius(self, _radius):
        self.radius_ = _radius
        self.set_projection(_radius / 100.0, _radius * 100.0, self.fovy_)
        self.reset_view()
        self.translate([0, 0, -_radius * 2.0])
        self.view_all()
        self.updateGL()

    def reset_view(self):
        # scene pos and size
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity();
        self.modelview_matrix_ = glGetDoublev( GL_MODELVIEW_MATRIX )
        self.set_center([0.0, 0.0, 0.0])

    def reset_rotation(self):
        self.modelview_matrix_[0] = [1.0, 0.0, 0.0, 0.0]
        self.modelview_matrix_[1] = [0.0, 1.0, 0.0, 0.0]
        self.modelview_matrix_[2] = [0.0, 0.0, 1.0, 0.0]
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixd(self.modelview_matrix_)
        self.updateGL()
   
    def translate(self, _trans):
        # Translate the object by _trans
        # Update modelview_matrix_
        self.makeCurrent()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(_trans[0], _trans[1], _trans[2])
        glMultMatrixd(self.modelview_matrix_)
        self.modelview_matrix_ = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.translate_vector_[0] = self.modelview_matrix_[3][0]
        self.translate_vector_[1] = self.modelview_matrix_[3][1]
        self.translate_vector_[2] = self.modelview_matrix_[3][2]
        self.signalGLMatrixChanged.emit()

    def rotate(self, _axis, _angle):
        t = [self.modelview_matrix_[0][0] * self.center_[0] +
             self.modelview_matrix_[1][0] * self.center_[1] +
             self.modelview_matrix_[2][0] * self.center_[2] +
             self.modelview_matrix_[3][0],
             self.modelview_matrix_[0][1] * self.center_[0] +
             self.modelview_matrix_[1][1] * self.center_[1] +
             self.modelview_matrix_[2][1] * self.center_[2] +
             self.modelview_matrix_[3][1],
             self.modelview_matrix_[0][2] * self.center_[0] +
             self.modelview_matrix_[1][2] * self.center_[1] +
             self.modelview_matrix_[2][2] * self.center_[2] +
             self.modelview_matrix_[3][2]]

        self.makeCurrent()
        glLoadIdentity()
        glTranslatef(t[0], t[1], t[2])
        glRotated(_angle, _axis[0], _axis[1], _axis[2])
        glTranslatef(-t[0], -t[1], -t[2])
        glMultMatrixd(self.modelview_matrix_)
        self.modelview_matrix_ = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.signalGLMatrixChanged.emit()

    def view_all(self):
        self.translate( [ -( self.modelview_matrix_[0][0] * self.center_[0] +
                             self.modelview_matrix_[0][1] * self.center_[1] +
                             self.modelview_matrix_[0][2] * self.center_[2] +
                             self.modelview_matrix_[0][3]),
                           -( self.modelview_matrix_[1][0] * self.center_[0] +
                              self.modelview_matrix_[1][1] * self.center_[1] +
                              self.modelview_matrix_[1][2] * self.center_[2] +
                              self.modelview_matrix_[1][3]),
                           -( self.modelview_matrix_[2][0] * self.center_[0] +
                              self.modelview_matrix_[2][1] * self.center_[1] +
                              self.modelview_matrix_[2][2] * self.center_[2] +
                              self.modelview_matrix_[2][3] +
                              self.radius_ / 2.0 )])

    def map_to_sphere(self, _v2D):
        _v3D = [0.0, 0.0, 0.0]
        # inside Widget?
        if (( _v2D.x() >= 0 ) and ( _v2D.x() <= self.width() ) and
            ( _v2D.y() >= 0 ) and ( _v2D.y() <= self.height() ) ):
            # map Qt Coordinates to the centered unit square [-0.5..0.5]x[-0.5..0.5]
            x  = float( _v2D.x() - 0.5 * self.width())  / self.width()
            y  = float( 0.5 * self.height() - _v2D.y()) / self.height()

            _v3D[0] = x;
            _v3D[1] = y;
            # use Pythagoras to comp z-coord (the sphere has radius sqrt(2.0*0.5*0.5))
            z2 = 2.0*0.5*0.5-x*x-y*y;
            # numerical robust sqrt
            _v3D[2] = math.sqrt(max( z2, 0.0 ))

            # normalize direction to unit sphere
            n = linalg.norm(_v3D)
            _v3D = np.array(_v3D) / n

            return True, _v3D
        else:
            return False, _v3D

    def wheelEvent(self, _event):
        # Use the mouse wheel to zoom in/out
        d = - float(_event.delta()) / 500.0 * self.radius_
        self.translate([0.0, 0.0, d])
        self.updateGL()
        _event.accept()

    def mousePressEvent(self, _event):
        self.last_point_2D_ = _event.pos()
        self.last_point_ok_, self.last_point_3D_ = self.map_to_sphere(self.last_point_2D_)

    def mouseMoveEvent(self, _event):
        newPoint2D = _event.pos()

        if ((newPoint2D.x() < 0) or (newPoint2D.x() > self.width()) or
            (newPoint2D.y() < 0) or (newPoint2D.y() > self.height())):
            return
        
        # Left button: rotate around center_
        # Middle button: translate object
        # Left & middle button: zoom in/out

        value_y = 0
        newPoint_hitSphere, newPoint3D = self.map_to_sphere(newPoint2D)

        dx = float(newPoint2D.x() - self.last_point_2D_.x())
        dy = float(newPoint2D.y() - self.last_point_2D_.y())

        w  = float(self.width())
        h  = float(self.height())

        # enable GL context
        self.makeCurrent()

        # move in z direction
        if (((_event.buttons() & QtCore.Qt.LeftButton) and (_event.buttons() & QtCore.Qt.MidButton))
            or (_event.buttons() & QtCore.Qt.LeftButton and _event.modifiers() & QtCore.Qt.ControlModifier)):
            value_y = self.radius_ * dy * 2.0 / h;
            self.translate([0.0, 0.0, value_y])
        # move in x,y direction
        elif (_event.buttons() & QtCore.Qt.MidButton
              or (_event.buttons() & QtCore.Qt.LeftButton and _event.modifiers() & QtCore.Qt.ShiftModifier)):
            z = - (self.modelview_matrix_[0][2] * self.center_[0] +
                   self.modelview_matrix_[1][2] * self.center_[1] +
                   self.modelview_matrix_[2][2] * self.center_[2] +
                   self.modelview_matrix_[3][2]) / (self.modelview_matrix_[0][3] * self.center_[0] +
                                                    self.modelview_matrix_[1][3] * self.center_[1] +
                                                    self.modelview_matrix_[2][3] * self.center_[2] +
                                                    self.modelview_matrix_[3][3])

            fovy   = 45.0
            aspect = w / h
            n      = 0.01 * self.radius_
            up     = math.tan(fovy / 2.0 * math.pi / 180.0) * n
            right  = aspect * up

            self.translate( [2.0 * dx / w * right / n * z,
                             -2.0 * dy / h * up / n * z,
                             0.0] )

    
        # rotate
        elif (_event.buttons() & QtCore.Qt.LeftButton):
            if (not self.isInRotation_):
                self.isInRotation_ = True
                self.rotationBeginEvent.emit()
       
            axis = [0.0, 0.0, 0.0]
            angle = 0.0

            if (self.last_point_ok_ and newPoint_hitSphere):
                axis = np.cross(self.last_point_3D_, newPoint3D)
                cos_angle = np.dot(self.last_point_3D_, newPoint3D)
                if (abs(cos_angle) < 1.0):
                    angle = math.acos(cos_angle) * 180.0 / math.pi
                    angle *= 2.0
                self.rotate(axis, angle)

        # remember this point
        self.last_point_2D_ = newPoint2D
        self.last_point_3D_ = newPoint3D
        self.last_point_ok_ = newPoint_hitSphere

        # trigger redraw
        self.updateGL()

        def mouseReleaseEvent(self, _event):
            if (self.isInRotation_):
                self.isInRotation_ = False
                self.rotationEndEvent.emit()
            last_point_ok_ = False
            
#===============================================================================
#Custom DM
#===============================================================================
    def testGLWidget(self):
        #self.paintGL()
        glBegin(GL_TRIANGLES)
        glColor3f(1,0,0)
        glVertex3f(0,0,0)
        glColor3f(0,1,0)
        glVertex3f(0,1,0)
        glColor3f(0,0,1)
        glVertex3f(1,1,0)
        glEnd()



#===============================================================================
    def AddTrimeshes(self,meshes):
        positions = np.array([])
        elements = np.array([])
        offsets = np.array([])
        self.nrpositions = []
        self.nrelements = []
        self.nrmeshes = len(meshes)
        offset = 0
        for i in range(len(meshes)):
            mesh = meshes[i]
            flatpositions = mesh.vertices.flatten()
            flatelements = mesh.faces.flatten()
            if i > 0 :
                offset = meshes[i-1].faces.max() + offset + 1
            offsetelements = flatelements + offset
            elements = np.append(elements,offsetelements)    
            positions = np.append(positions, flatpositions)        
            self.nrelements = np.append(self.nrelements, len(flatelements))
            self.nrpositions = np.append(self.nrpositions, len(flatpositions))
            
            
        #for mesh in meshes:
        #    flatpositions = mesh.vertices.flatten()
        #    flatelements = mesh.faces.flatten()
        #    positions = np.append(positions, flatpositions)
        #    elements = np.append(elements,flatelements)
        #    self.nrpositions = np.append(self.nrpositions, len(flatpositions))
        #    self.nrelements = np.append(self.nrelements, len(flatelements))
        self.nrelements = self.nrelements.astype(int)
        self.nrpositions = self.nrpositions.astype(int)
        elements = elements.astype(int)
        self.indices=elements
        self.__vao = glGenVertexArrays(1)  
        glBindVertexArray(self.__vao)  
        bufs = glGenBuffers(2)  
        glBindBuffer(GL_ARRAY_BUFFER, bufs[0])  
        glBufferData(GL_ARRAY_BUFFER, sizeof(ctypes.c_float) * len(positions), (ctypes.c_float * len(positions))(*positions), GL_STATIC_DRAW)  
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, bufs[1])  
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(ctypes.c_uint) * len(elements), (ctypes.c_uint * len(elements))(*elements), GL_STATIC_DRAW)  
        glEnableVertexAttribArray(0)  
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        True
        
        
#===============================================================================
    def UploadVertices(self,vert,elem):
        # generate a model  
        # set up the data  
        #vert = [[0,0,100],
        #        [100,0,0],
        #        [0,100,0],
        #        [100,100,0]]
        positions = np.array(vert).flatten()
        #positions = (0, 0, 100, 0, 0, 100, 100, 100)  
        #elements = (0, 1, 2, 1, 3, 2)  
        elements = elem
        self.nrelements = len(elements)
        # apply the data  
        # generate a vertex array object so we can easily draw the resulting mesh later  
        self.__vao = glGenVertexArrays(1)  
        # enable the vertex array before doing anything else, so anything we do is captured in the VAO context  
        glBindVertexArray(self.__vao)  
        # generate 2 buffers, 1 for positions, 1 for elements. this is memory on the GPU that our model will be saved in.  
        bufs = glGenBuffers(2)  
        # set the first buffer for the main vertex data, that GL_ARRAY_BUFFER indicates that use case  
        glBindBuffer(GL_ARRAY_BUFFER, bufs[0])  
        # upload the position data to the GPU  
        # some info about the arguments:  
        # GL_ARRAY_BUFFER: this is the buffer we are uploading into, that is why we first had to bind the created buffer, else we'd be uploading to nothing  
        # sizeof(ctypes.c_float) * len(positions): openGL wants our data as raw C pointer, and for that it needs to know the size in bytes.  
        # the ctypes module helps us figure out the size in bytes of a single number, then we just multiply that by the array length  
        # (ctypes.c_float * len(positions))(*positions): this is a way to convert a python list or tuple to a ctypes array of the right data type  
        # internally this makes that data the right binary format  
        # GL_STATIC_DRAW: in OpenGL you can specify what you will be doing with this buffer, static means draw it a lot but never access or alter the data once uploaded.  
        # I suggest changing this only when hitting performance issues at a time you are doing way more complicated things. In general usage static is the fastest.  
        glBufferData(GL_ARRAY_BUFFER, sizeof(ctypes.c_float) * len(positions), (ctypes.c_float * len(positions))(*positions), GL_STATIC_DRAW)  
        # set the second buffer for the triangulation data, GL_ELEMENT_ARRAY_BUFFER indicates the use here  
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, bufs[1])  
        # upload the triangulation data  
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(ctypes.c_uint) * len(elements), (ctypes.c_uint * len(elements))(*elements), GL_STATIC_DRAW)  
        # because the data is now on the GPU, our python positions & elements can be safely garbage collected hereafter  
        # turn on the position attribute so OpenGL starts using our array buffer to read vertex positions from  
        glEnableVertexAttribArray(0)  
        # set the dimensions of the position attribute, so it consumes 2 floats at a time (default is 4)  
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)  
        
        
    def AddComponent2(self,comp):
        comp.glnfo.vao = glGenVertexArrays(1)  
        glBindVertexArray(comp.glnfo.vao)
        comp.glnfo.bufs = glGenBuffers(2)  
        glBindBuffer(GL_ARRAY_BUFFER, comp.glnfo.bufs[0]) 
        glBufferData(GL_ARRAY_BUFFER, sizeof(ctypes.c_float) * len(comp.glnfo.positions), (ctypes.c_float * len(comp.glnfo.positions))(*comp.glnfo.positions), GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, comp.glnfo.bufs[1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(ctypes.c_uint) * len(comp.glnfo.elements), (ctypes.c_uint * len(comp.glnfo.elements))(*comp.glnfo.elements), GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        self.components[comp.name]=comp

    def AddComponent(self,comp):
        # see: http://www.labri.fr/perso/nrougier/python-opengl/code/glut-quad-varying-color.py
        #glUseProgram(self.glshaders.program)
        comp.glnfo.vao = glGenVertexArrays(1)  
        glBindVertexArray(comp.glnfo.vao)
        data = comp.glnfo.vertexdata
        comp.glnfo.bufs = glGenBuffers(2)           # Request a buffer slot from GPU
        glBindBuffer(GL_ARRAY_BUFFER, comp.glnfo.bufs[0])       # make .bufs[0] the main Vertex data buffer
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)         # Upload vertex data to buffer        
        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, comp.glnfo.bufs[1])   # Element index buffer = [1]
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(ctypes.c_uint) * len(comp.glnfo.elements), (ctypes.c_uint * len(comp.glnfo.elements))(*comp.glnfo.elements), GL_STATIC_DRAW)
        
        #Vertex positions
        stride = data.strides[0]
        offset = ctypes.c_void_p(0)
        #offset = 0
        glEnableVertexAttribArray(self.glshaders.vertexloc)
        loc_position = glGetAttribLocation(self.glshaders.program, "position")
        loc_color = glGetAttribLocation(self.glshaders.program, "color")
        glVertexAttribPointer(self.glshaders.vertexloc, 3, GL_FLOAT, False, stride, offset)
        #glVertexAttribPointer(0, 3, GL_FLOAT, False, stride, offset)
        
        #Vertex colors
        offset = ctypes.c_void_p(data.dtype["position"].itemsize)
        #offset = data.dtype["position"].itemsize
        glEnableVertexAttribArray(self.glshaders.colorloc)
        glVertexAttribPointer(self.glshaders.colorloc, 4, GL_FLOAT, False, stride, offset)
        #glVertexAttribPointer(3, 4, GL_FLOAT, False, stride, offset)
        
        self.components[comp.name]=comp
        

        True
        

        
#===============================================================================
#
# Local Variables:
# mode: Python
# indent-tabs-mode: nil
# End:
#
#===============================================================================
