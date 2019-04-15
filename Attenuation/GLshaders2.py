'''
Created on 07 Feb 2019

@author: Deon
'''

import sys
import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut

#==================================================
# see http://www.lighthouse3d.com/tutorials/glsl-12-tutorial/directional-lights-i/
vertex_code3 = """
    void main() {
        vec3 normal, lightDir, viewVector, halfVector;
        vec4 diffuse, ambient, globalAmbient, specular = vec4(0.0);
        float NdotL,NdotHV;
        
        /* first transform the normal into eye space and normalize the result */
        normal = normalize(gl_NormalMatrix * gl_Normal);
        
        /* now normalize the light's direction. Note that according to the
        OpenGL specification, the light is stored in eye space. Also since 
        we're talking about a directional light, the position field is actually 
        direction */
        lightDir = normalize(vec3(gl_LightSource[0].position));
        
        /* compute the cos of the angle between the normal and lights direction. 
        The light is directional so the direction is constant for every vertex.
        Since these two are normalized the cosine is the dot product. We also 
        need to clamp the result to the [0,1] range. */
        
        NdotL = max(dot(normal, lightDir), 0.0);
        
        /* Compute the diffuse, ambient and globalAmbient terms */
        diffuse = gl_FrontMaterial.diffuse * gl_LightSource[0].diffuse;
        ambient = gl_FrontMaterial.ambient * gl_LightSource[0].ambient;
        globalAmbient = gl_LightModel.ambient * gl_FrontMaterial.ambient;
        
        /* compute the specular term if NdotL is  larger than zero */
        if (NdotL > 0.0) {
    
            NdotHV = max(dot(normal, normalize(gl_LightSource[0].halfVector.xyz)),0.0);
            specular = gl_FrontMaterial.specular * gl_LightSource[0].specular * pow(NdotHV,gl_FrontMaterial.shininess);
        }
        
        gl_FrontColor = globalAmbient + NdotL * diffuse + ambient + specular;
        
        gl_Position = ftransform();
    }
    """

fragment_code3 = """
    void main() 
    {
        
        gl_FragColor = gl_Color;
    }
    """
#==================================================
    
vertex_code = """
    attribute vec4 color;
    attribute vec3 position;
    varying vec4 v_color;
    void main()
    {
        gl_Position = vec4(position, 1.0);
        v_color = color;
    }
    """

fragment_code = """
    varying vec4 v_color;
    void main() {
        gl_FragColor = v_color;
    }
    """
#==================================================   
#==================================================
    
vertex_code = """
    in vec4 position;
    void main()
    {
       gl_Position = position;
    }"""

fragment_code = """
    out vec4 outputColor;
    void main()
    {
      outputColor = vec4(0.0f, 1.0f, 0.0f, 1.0f);
    }
    """
#==================================================   

vertex_code2 = """
    // use a varying value to pass information
    // about color from the vertex to the fragment
    varying vec4 vertex_color;
    void main(){
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        vertex_color = gl_Color;
    }
    """
        
fragment_code2 = """
        varying vec4 vertex_color;
        void main(){
            // interpolates values set into
            // vertex_color from the vertex
            // shader
            gl_FragColor = vertex_color;
        }
        """


#==================================================

class GLshaders():
    def __init__(self):
        # Build & activate program
        # Request a program and shader slots from GPU
        self.program  = gl.glCreateProgram()
        self.vertex   = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        self.fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        # Set shaders source
        gl.glShaderSource(self.vertex, vertex_code)
        gl.glShaderSource(self.fragment, fragment_code)
        # Compile shaders
        gl.glCompileShader(self.vertex)
        if not gl.glGetShaderiv(self.vertex, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(self.vertex).decode()
            print(error)
            raise RuntimeError("Shader compilation error")
        
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
    
    
        self.vertexloc = gl.glGetAttribLocation(self.program, "position")
        self.colorloc = gl.glGetAttribLocation(self.program, "color")
        #self.colorloc =3
        
        
        # Get rid of shaders (no more needed)
        gl.glDetachShader(self.program, self.vertex)
        gl.glDetachShader(self.program, self.fragment)
        
        
        True
        


#===============================================================================
    def getAttLoc(self,att):
        return gl.glGetAttribLocation(self.program, att)
    
    
    
    
    
    
    
    
    
        