from OpenGL.GL import *
from OpenGL.GLU import *

class Camera(object):
    def setup(self):
        raise NotImplementedError()

class CameraLookAt(object):
    def __init__(self):
        self.pos = [0, 0, 0]
        self.lookAt = [0, 0, 0]

    def pan_left(self, val):
        self.pos[0] -= val
    def pan_right(self, val):
        self.pos[0] += val
    def pan_up(self, val):
        self.pos[1] += val
    def pan_down(self, val):
        self.pos[1] -= val
    def pan_in(self, val):
        self.pos[2] -= val
    def pan_out(self, val):
        self.pos[2] += val

    def setup(self):
        glLoadIdentity()
        gluLookAt( self.pos[0], self.pos[1], self.pos[2],
                   self.lookAt[0], self.lookAt[1], self.lookAt[2],
                   0,0,1)

class CameraOnSphere(CameraLookAt):
    def __init__(self):
        CameraLookAt.__init__(self)
        self.radius = 40
        self.theta = 0
        self.phi = 0

    def pan_left(self, val):
        self.phi -= val
    def pan_right(self, val):
        self.phi += val
    def pan_up(self, val):
        self.theta += val
    def pan_down(self, val):
        self.theta -= val
    def pan_in(self, val):
        #self.radius -= val
        self.radius /= 1.1**val
    def pan_out(self, val):
        #self.radius += val
        self.radius *= 1.1**val
        
    def setup(self):
        from math import sin, cos, pi
        r = self.radius
        theta = self.theta * pi / 180
        phi = self.phi * pi / 180
        self.pos = [r*cos(phi)*cos(theta),
                    r*sin(phi)*cos(theta),
                    r*sin(theta)]
        CameraLookAt.setup(self)
