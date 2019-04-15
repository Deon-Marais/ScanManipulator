'''
Created on 07 Feb 2019

@author: Deon
'''

import sys
import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import traceback

#==================================================
    
vertex_code = """
    #version 130
    attribute vec3 position;
    attribute vec4 color;
    varying vec4 v_color;
    void main()
    {
        gl_Position = vec4(position, 1.0);
        v_color = color;
    }
    """

fragment_code = """
    #version 130
    varying vec4 v_color;
    void main()
    {
      gl_FragColor = v_color;
      
    }
    """
#==================================================   
class GLshaders():
    def __init__(self):
        self.program  = gl.glCreateProgram()
        
#==================================================        
    def __init__2(self):
        # Build & activate program
        # Request a program and shader slots from GPU
        self.program  = gl.glCreateProgram()

        self.vertex   = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(self.vertex, vertex_code)
        gl.glCompileShader(self.vertex)
        if not gl.glGetShaderiv(self.vertex, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(self.vertex).decode()
            print(error)
            raise RuntimeError("Shader compilation error")

        self.fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(self.fragment, fragment_code)
        gl.glCompileShader(self.fragment)
        if not gl.glGetShaderiv(self.fragment, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(self.fragment).decode()
            print(error)
            raise RuntimeError("Shader compilation error")  
        
        # Attach shader objects to the program
        gl.glAttachShader(self.program, self.vertex)
        gl.glAttachShader(self.program, self.fragment)
        
        #self.vertexloc = gl.glGetAttribLocation(self.program, "position")
        
        
        # Build program
        gl.glLinkProgram(self.program)
        if not gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS):
            print(gl.glGetProgramInfoLog(self.program))
            raise RuntimeError('Linking error')
    
    
        #    The default openGL attribute locations are as follows:
        # see http://trevorius.com/scrapbook/uncategorized/part-1-drawing-with-pyopengl-using-moden-opengl-buffers/
        #0: position
        #1: tangent
        #2: normal
        #3: color
        #4: uv
        
        #self.vertexloc = gl.glGetAttribLocation(self.program, "position")
        #self.colorloc = gl.glGetAttribLocation(self.program, "color")
        self.vertexloc = 0
        self.colorloc = 3
        
        
        # Get rid of shaders (no more needed)
        gl.glDetachShader(self.program, self.vertex)
        gl.glDetachShader(self.program, self.fragment)
        
        
        True
        


#===============================================================================
    def getAttLoc(self,att):
        return gl.glGetAttribLocation(self.program, att)
    
    
#===============================================================================
    def LoadShaders(self, vertex_file_path, fragment_file_path):
        #Create the shaders
        self.vertex   = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        self.fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        
        #Read the Vertex and Fragment Shader code from files
        try:
            vertex_code = open(vertex_file_path).read()
            fragment_code = open(fragment_file_path).read()
        except:
            traceback.print_exc()    
        
        #Compile Vertex shader
        gl.glShaderSource(self.vertex, vertex_code)
        gl.glCompileShader(self.vertex)
        if not gl.glGetShaderiv(self.vertex, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(self.vertex).decode()
            print(error)
            raise RuntimeError("Vertex Shader compilation error")    
        
        #Compile Fragment shader
        gl.glShaderSource(self.fragment, fragment_code)
        gl.glCompileShader(self.fragment)
        if not gl.glGetShaderiv(self.fragment, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(self.fragment).decode()
            print(error)
            raise RuntimeError("Fragment Shader compilation error")  
    
        #Link the program
        gl.glAttachShader(self.program, self.vertex)
        gl.glAttachShader(self.program, self.fragment)
        gl.glLinkProgram(self.program)
        if not gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS):
            print(gl.glGetProgramInfoLog(self.program))
            raise RuntimeError('Linking error')
    
    

        gl.glUseProgram(self.program)
        #Using the Testvert & Testfrag files
        #self.pMatrixUniform = gl.glGetUniformLocation(self.program, "uPMatrix")
        #self.mvMatrixUniform = gl.glGetUniformLocation(self.program, "uMVMatrix")
        #self.colorU = gl.glGetUniformLocation(self.program, "uColor")
        #self.vertIndex = gl.glGetAttribLocation(self.program, "aVert")
        
        self.vertexloc = gl.glGetAttribLocation(self.program, "position")
        self.colorloc = gl.glGetAttribLocation(self.program, "color")
        self.translateloc = gl.glGetUniformLocation(self.program, "translate")
        self.rotateloc = gl.glGetUniformLocation(self.program, "rotate")
        self.perspectiveloc = gl.glGetUniformLocation(self.program, "perspectiveMatrix")
        self.lookatloc = gl.glGetUniformLocation(self.program, "lookat")
        
        
        
        
        # Get rid of shaders (no more needed)
        gl.glDetachShader(self.program, self.vertex)
        gl.glDetachShader(self.program, self.fragment)
        gl.glDeleteShader(self.vertex)
        gl.glDeleteShader(self.fragment)
    
    
    
        