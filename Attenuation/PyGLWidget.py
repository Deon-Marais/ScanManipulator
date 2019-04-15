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
#from itertools import izip
from Attenuation.Component import Component as Component
from Attenuation.GLshaders import GLshaders as GLshaders
#import quaternion

#===============================================================================
class ComponentNfo():
    def __init__(self):
        self.list = {}
        self.minx = 0.0
        self.maxx = 0.0
        self.miny = 0.0
        self.maxy = 0.0
        self.minz = 0.0
        self.maxz = 0.0

    def updateMinMax(self):
        objnames = self.list.keys()
        rx, ry, rz = self.list[objnames[0]].trimeshobj.bounds.T
        ox ,oy, oz = self.list[objnames[0]].position
        self.maxx = max(rx+ox)
        self.minx = min(rx+ox)
        self.maxy = max(ry+oy)
        self.miny = min(ry+oy)
        self.maxz = max(rz+oz)
        self.minz = min(rz+oz)
        for i in range(1,len(objnames)):
            rx, ry, rz = self.list[objnames[i]].trimeshobj.bounds.T
            ox ,oy, oz = self.list[objnames[i]].position
            self.maxx = max(np.concatenate([[self.maxx], rx+ox]))
            self.minx = min(np.concatenate([[self.minx], rx+ox]))
            self.maxy = max(np.concatenate([[self.maxy], ry+oy]))
            self.miny = min(np.concatenate([[self.miny], ry+oy]))
            self.maxz = max(np.concatenate([[self.maxz], rz+oz]))
            self.minz = min(np.concatenate([[self.minz], rz+oz]))
            True
        a = np.array([[self.maxx, self.minx], [self.maxy, self.miny ],[self.maxz, self.minz]])
        self.min = a.min()
        self.max = a.max()
        self.absmax = np.abs(a).max()
        self.absmin = -((-np.abs(a)).max())
        return a
    

        
        
#===============================================================================
class PyGLWidget(QtOpenGL.QGLWidget):
    # Qt signals
    signalGLMatrixChanged = QtCore.pyqtSignal()
    rotationBeginEvent = QtCore.pyqtSignal()
    rotationEndEvent = QtCore.pyqtSignal()
    resized = QtCore.pyqtSignal()
#===============================================================================
    def __init__(self, parent = None):
        format = QtOpenGL.QGLFormat()
        format.setSampleBuffers(True)
        QtOpenGL.QGLWidget.__init__(self, format, parent)
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setMouseTracking(True)
        self.resized.connect(self.onResize)

        self.comps = ComponentNfo()
        self.comps.maxz = 0.1
        self.comps.minz = 0.01
        
        self.radius = 5.0
        self.fovdeg = 45.0
        self.isInRotation_ = False
        
        self.rotatemat = np.eye(4).astype(np.float32)
        self.translatemat = np.eye(4).astype(np.float32)
        self.perspectivemat = np.eye(4).astype(np.float32)
        self.lookatmat = np.eye(4).astype(np.float32)
        self.scalemat = np.eye(4).astype(np.float32)
        #self.components = {}
        
#===============================================================================
    def resizeEvent(self,event):
        self.resized.emit()
        #return super(self).resizeEvent(event)
#===============================================================================

    def initializeGL(self):
        self.glshaders = GLshaders()
        shaderpath = "./3rd-party/OpenGLshaders/"
        #self.glshaders.LoadShaders(shaderpath+"TransformVertexShader.vert", shaderpath+"ColorFragmentShader.frag")
        self.glshaders.LoadShaders(shaderpath+"Testvert.vert", shaderpath+"Testfrag.frag")
        glUseProgram(self.glshaders.program)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glDisable(GL_CULL_FACE)
        #glCullFace(GL_BACK)
        glFrontFace(GL_CW)
        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)
        glDepthRange(0.0,1.0)
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #glEnable(GL_POLYGON_STIPPLE)
        self.reset_view()

#===============================================================================
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.glshaders.program)

        #self.matMVP = (matPerspective * matLookat * matModel).astype(np.float32)
        
        imat = np.eye(4,4)
        transform_mat = np.dot(self.rotatemat,self.scalemat).astype(np.float32)

        glUniformMatrix4fv(self.glshaders.rotateloc, 1, GL_FALSE, transform_mat)
        #glUniformMatrix4fv(self.glshaders.rotateloc, 1, GL_FALSE, self.rotatemat)
        glUniformMatrix4fv(self.glshaders.translateloc, 1, GL_FALSE, self.translatemat)
        glUniformMatrix4fv(self.glshaders.perspectiveloc, 1, GL_FALSE, self.perspectivemat);
        glUniformMatrix4fv(self.glshaders.lookatloc, 1, GL_FALSE, self.lookatmat);
        
        


        
        
        
        #for name in self.comps.list.iterkeys():
        for name in self.comps.list.keys():
            comp = self.comps.list[name]
            glBindVertexArray(comp.glnfo.vao)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, comp.glnfo.glelementsbuffer)
         
            #offsetmat = comp.position
            #glUniform3fv(self.glshaders.offsetloc, 1, offsetmat)

            
            glDrawElements(comp.glnfo.primitive_type  , comp.glnfo.nrelements, GL_UNSIGNED_INT, None)
            glBindVertexArray(0)
            True
        #self.swapBuffers()
        glUseProgram(0)

    
#===============================================================================
    def resizeGL(self, width, height):
        #glViewport( 0, 0, width, height );
        #self.set_projection( self.near_, self.far_, self.fovy_ );
        True

    def onResize(self):
        try:
            glUseProgram(self.glshaders.program)
            glViewport( 0, 0, self.width(), self.height())
            #perspective_matrix = self.getPerspective(100.0, 0.5, 3.0)
            #glUniformMatrix4fv(self.glshaders.perspectiveloc, 1, GL_FALSE, perspective_matrix);
            glUseProgram(0)
        except:
            True
        True        
              
#===============================================================================
    def getPerspective(self, field_of_view_y, z_near, z_far):
        aspect = float(self.width())/float(self.height())
        fov_radians = math.radians(field_of_view_y)
        f = math.tan(fov_radians/2)
        a_11 = 1/(f*aspect)
        a_22 = 1/f
        a_33 = (z_near + z_far)/(z_near - z_far)
        a_34 = 2*z_near*z_far/(z_near - z_far)
        
        self.perspectivemat = np.matrix([
            [a_11, 0, 0, 0],       
            [0, a_22, 0, 0],       
            [0, 0, a_33, a_34],    
            [0, 0, -1, 0]          
        ], np.float32)
        return self.perspectivemat

    

#===============================================================================
    def getLookAt(self,eye, lookat, up):
        ez = eye - lookat
        ez = ez / np.linalg.norm(ez)
        
        ex = np.cross(up, ez)
        ex = ex / np.linalg.norm(ex)
        
        ey = np.cross(ez, ex)
        ey = ey / np.linalg.norm(ey)
        
        rmat = np.eye(4)
        rmat[0][0] = ex[0]
        rmat[0][1] = ex[1]
        rmat[0][2] = ex[2]
        
        rmat[1][0] = ey[0]
        rmat[1][1] = ey[1]
        rmat[1][2] = ey[2]
        
        rmat[2][0] = ez[0]
        rmat[2][1] = ez[1]
        rmat[2][2] = ez[2]
        
        tmat = np.eye(4)
        tmat[0][3] = -eye[0]
        tmat[1][3] = -eye[1]
        tmat[2][3] = -eye[2]
        
        # numpy.array * is element-wise multiplication, use dot()
        self.lookatmat = np.dot(rmat, tmat)
        return self.lookatmat
        
#===============================================================================
    def reset_view2(self):
        matPerspective = self.getPerspective(80, 640/480, 0.1, 10000.0)
        matLookat = self.getLookAt(np.array([0,0,-3]), np.array([0,0,0]), np.array([0,1,0]))
        matModel = self.matID
        self.matMVP = (matPerspective * matLookat * matModel).astype(np.float32)
        True
        

#===============================================================================
#===============================================================================        
    def set_projection2(self, _near, _far, _fovy):
        self.near_ = _near
        self.far_ = _far
        self.fovy_ = _fovy
        self.makeCurrent()
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        gluPerspective( self.fovy_, float(self.width()) / float(self.height()),
                        self.near_, self.far_ )
        self.updateGL()
        
    def set_center(self, cog):
        self.center = cog
        #self.view_all()

    def set_radius2(self, radius):
        self.radius = radius
        
        #getPerspective(self, field_of_view_y, z_near, z_far)
        
        self.set_projection(radius / 100.0, radius * 100.0, self.fovdeg)
        self.reset_view()
        self.translate([0, 0, -radius * 2.0])
        #self.view_all()
        self.updateGL()

    def reset_view(self):
        # scene pos and size
        #glMatrixMode( GL_MODELVIEW )
        #glLoadIdentity();
        #self.modelview_matrix_ = glGetDoublev( GL_MODELVIEW_MATRIX )
        self.set_center([0.0, 0.0, 0.0])

    def reset_rotation2(self):
        self.modelview_matrix_[0] = [1.0, 0.0, 0.0, 0.0]
        self.modelview_matrix_[1] = [0.0, 1.0, 0.0, 0.0]
        self.modelview_matrix_[2] = [0.0, 0.0, 1.0, 0.0]
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixd(self.modelview_matrix_)
        self.updateGL()
   
   
    def addscale(self,d):
        self.scalemat[0][0] += d
        self.scalemat[1][1] += d
        self.scalemat[2][2] += d
        self.scalemat = np.abs(self.scalemat)
        True
   
    def addtranslate(self,vec_deltatrans):
        trans = np.array(vec_deltatrans).astype(np.float32)
        self.translatemat[0][3] += trans[0]
        self.translatemat[1][3] += trans[1]
        self.translatemat[2][3] += trans[2]
        True
        
   
    def settranslate(self, vec_trans):
        trans = np.array(vec_trans).astype(np.float32)
        self.translatemat[0][3] = trans[0]
        self.translatemat[1][3] = trans[1]
        self.translatemat[2][3] = trans[2]
        
               
        #self.translatemat = np.array(trans).astype(np.float32)
        #glUniform3fv(self.glshaders.translateloc, 1, self.translatemat)
        
        True
        
    def translate2(self, _trans):
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

    def addrotate(self, axis, angle):
        ang = np.radians(angle) / 2.0 
        x = axis[0] * np.sin(ang)
        y = axis[1] * np.sin(ang)
        z = axis[2] * np.sin(ang)
        w = np.cos(ang)
        
        _FLOAT_EPS = np.finfo(np.float).eps
        Nq = w*w + x*x + y*y + z*z
        if Nq < _FLOAT_EPS:
            return np.eye(4)
        s = 2.0/Nq
        X = x*s
        Y = y*s
        Z = z*s
        wX = w*X; wY = w*Y; wZ = w*Z
        xX = x*X; xY = x*Y; xZ = x*Z
        yY = y*Y; yZ = y*Z; zZ = z*Z
        deltarotate = np.matrix([[ 1.0-(yY+zZ), xY-wZ, xZ+wY, 0 ],
                                 [ xY+wZ, 1.0-(xX+zZ), yZ-wX, 0 ],
                                 [ xZ-wY, yZ+wX, 1.0-(xX+yY), 0 ],
                                 [0, 0, 0, 1]]).astype(np.float32)
        #self.rotatemat = np.eye(4).astype(np.float32)
        #self.rotatemat[3][2] = -1
        #self.rotatemat[3][3] = 0
        #glUniform4fv(self.glshaders.rotateloc, 1, self.rotatemat)
        self.rotatemat = np.dot(self.rotatemat, deltarotate)
        return self.rotatemat
        
    def rotate2(self, _axis, _angle):
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
        True
        #self.translate([-self.center[0], -self.center[1], -(self.center[2]+self.radius/2.0) ])
        #self.translate( [ -( self.modelview_matrix_[0][0] * self.center_[0] +
        #                     self.modelview_matrix_[0][1] * self.center_[1] +
        #                     self.modelview_matrix_[0][2] * self.center_[2] +
        #                     self.modelview_matrix_[0][3]),
        #                   -( self.modelview_matrix_[1][0] * self.center_[0] +
        #                      self.modelview_matrix_[1][1] * self.center_[1] +
        #                      self.modelview_matrix_[1][2] * self.center_[2] +
        #                      self.modelview_matrix_[1][3]),
        #                   -( self.modelview_matrix_[2][0] * self.center_[0] +
        #                      self.modelview_matrix_[2][1] * self.center_[1] +
        #                      self.modelview_matrix_[2][2] * self.center_[2] +
        #                      self.modelview_matrix_[2][3] +
        #                      self.radius / 2.0 )])

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
        d =  float(_event.delta()) / 10000.0 * self.radius
        #self.addtranslate(np.array([0.0, 0.0, d]))
        self.addscale(d)
        #self.getPerspective(self.fovdeg, self.comps.absmin, self.comps.absmax)
        self.updateGL()
        _event.accept()

    def mousePressEvent(self, _event):
        self.last_point_2D_ = _event.pos()
        self.last_point_ok_, self.last_point_3D_ = self.map_to_sphere(self.last_point_2D_)
        True

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

        try:
            dx = float(newPoint2D.x() - self.last_point_2D_.x())
            dy = float(newPoint2D.y() - self.last_point_2D_.y())
        except:
            dx = 0.0
            dy = 0.0
            

        w  = float(self.width())
        h  = float(self.height())

        # enable GL context
        #self.makeCurrent()

        # move in z direction
        if (((_event.buttons() & QtCore.Qt.LeftButton) and (_event.buttons() & QtCore.Qt.MidButton))
            or (_event.buttons() & QtCore.Qt.LeftButton and _event.modifiers() & QtCore.Qt.ControlModifier)):
            value_y = self.radius * dy * 2.0 / h;
            self.translate([0.0, 0.0, value_y])
        # move in x,y direction
        elif (_event.buttons() & QtCore.Qt.MidButton
              or (_event.buttons() & QtCore.Qt.LeftButton and _event.modifiers() & QtCore.Qt.ShiftModifier)):
            True
            #z = - (self.modelview_matrix_[0][2] * self.center_[0] +
            #       self.modelview_matrix_[1][2] * self.center_[1] +
            #       self.modelview_matrix_[2][2] * self.center_[2] +
            #       self.modelview_matrix_[3][2]) / (self.modelview_matrix_[0][3] * self.center_[0] +
            #                                        self.modelview_matrix_[1][3] * self.center_[1] +
            #                                        self.modelview_matrix_[2][3] * self.center_[2] +
            #                                        self.modelview_matrix_[3][3])
            z = 1
            
            
            #fovy   = 45.0
            fovy=self.fovdeg
            aspect = w / h
            n      = 0.01 * self.radius
            up     = math.tan(fovy / 2.0 * math.pi / 180.0) * n
            right  = aspect * up

            x = 1.0 * dx / w * right / n * z
            y = -1.0 * dy / h * up / n * z
            
            self.addtranslate([x, y, 0])

    
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
                    angle *= 4.0
                self.addrotate(axis, angle)

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

 
#===============================================================================        
    def AddComponent(self,compnt):
        if compnt.name not in self.comps.list:
            comp = compnt
            comp.glnfo.vao = glGenVertexArrays(1)  
            glBindVertexArray(comp.glnfo.vao)
            comp.glnfo.glvertexbuffer = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, comp.glnfo.glvertexbuffer)
            glBufferData(GL_ARRAY_BUFFER, comp.glnfo.posbuf.nbytes, comp.glnfo.posbuf, GL_STREAM_DRAW)
            glEnableVertexAttribArray(self.glshaders.vertexloc)
            glVertexAttribPointer(self.glshaders.vertexloc, 3, GL_FLOAT, GL_FALSE, 0, None)
            comp.glnfo.glcolorbuffer = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, comp.glnfo.glcolorbuffer)
            glBufferData(GL_ARRAY_BUFFER, comp.glnfo.colorbuf.nbytes, comp.glnfo.colorbuf, GL_STREAM_DRAW)
            glEnableVertexAttribArray(self.glshaders.colorloc)            
            glVertexAttribPointer(self.glshaders.colorloc, 4, GL_FLOAT, False, 0, None)
            comp.glnfo.glelementsbuffer = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, comp.glnfo.glelementsbuffer)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, comp.glnfo.elementsbuf.nbytes, comp.glnfo.elementsbuf, GL_STREAM_DRAW)
            self.comps.list[comp.name]=comp
        else:
            comp = self.comps.list[compnt.name]
            newcomp = compnt
            comp.glnfo.posbuf = newcomp.glnfo.posbuf
            comp.glnfo.colorbuf = newcomp.glnfo.colorbuf
            comp.position = newcomp.position
            glBindVertexArray(comp.glnfo.vao)
            glBindBuffer(GL_ARRAY_BUFFER, comp.glnfo.glvertexbuffer)
            glBufferSubData(GL_ARRAY_BUFFER, 0, comp.glnfo.posbuf.nbytes, comp.glnfo.posbuf)
            glEnableVertexAttribArray(self.glshaders.vertexloc)
            glVertexAttribPointer(self.glshaders.vertexloc, 3, GL_FLOAT, GL_FALSE, 0, None)
            glBindBuffer(GL_ARRAY_BUFFER, comp.glnfo.glcolorbuffer)
            glBufferSubData(GL_ARRAY_BUFFER, 0, comp.glnfo.colorbuf.nbytes, comp.glnfo.colorbuf)
            glEnableVertexAttribArray(self.glshaders.colorloc)            
            glVertexAttribPointer(self.glshaders.colorloc, 4, GL_FLOAT, False, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER,0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,0)
        
        self.comps.updateMinMax()
        #self.radius =self.comps.absmax*1.1 
        
        #self.getPerspective(self.fovdeg, 0.1, 1000)
        #self.getPerspective(self.fovdeg, 0.1, self.comps.absmax)
        #self.getPerspective(self.fovdeg, self.comps.absmin, self.comps.absmax)
        
        #self.getLookAt(np.array([0,0,1]), np.array([0,0,0]), np.array([0,1,0]))
        
        #compob = self.comps.list['positioner']
        #self.getLookAt(np.array([0,0,self.comps.absmax*1.1]), np.array([0,0,0]), np.array([0,1,0]))
        #self.getLookAt(np.array([0,0,-1000]), self.center, np.array([0,1,0]))

        True
         

  