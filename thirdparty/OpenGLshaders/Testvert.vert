#version 330


//uniform vec3 offset;
layout (location = 0) in vec3 position;
layout (location = 1) in vec4 color;
smooth out vec4 theColor;
//uniform vec3 translate;
uniform mat4 translate;
uniform mat4 rotate;
uniform mat4 lookat;
uniform mat4 perspectiveMatrix;

void main() {
  //vec4 totOffset = vec4(offset, 0.0f);
  vec4 totPosition = vec4(position, 1.0f);
  //vec4 totTranslate = vec4(translate, 0.0f);
  //mat4 cameraPos = translate * perspectiveMatrix;
  

  gl_Position =   lookat * perspectiveMatrix  * rotate * totPosition * translate ;
  //gl_Position =  lookat * perspectiveMatrix  * rotate * totPosition * translate ;
  //gl_Position =  rotate * perspectiveMatrix * totPosition * translate ;

  
  theColor = color;
}
