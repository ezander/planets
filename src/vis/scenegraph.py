from OpenGL.GL import *
from OpenGL.GLU import *

image_dir = "../images"

__all__ = ["Node", "Rotation", "Scaling", "Translation", 
           "TexturedSphere", "CoordSystemNode",
           "CircleNode"]

class Node(object):
    def __init__(self, app=None):
        self.children = []
        self.app = app
    def add_child(self, child):
        self.children.append(child)
        return child
    def prerender(self):
        pass
    def postrender(self):
        pass
    def display(self):
        #print self.__class__, self.children
        pass
    def render(self):
        self.prerender()
        for child in self.children:
            child.render()
        self.display()
        self.postrender()

class Rotation(Node):
    def __init__(self, angle, vec, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
        self.angle = angle
        self.vec = vec
    def prerender(self):
        glPushMatrix()
        glRotate(self.angle, *self.vec)
    def postrender(self):
        glPopMatrix()

class Scaling(Node):
    def __init__(self, vec, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
        self.vec = vec
    def prerender(self):
        glPushMatrix()
        glScale(*self.vec)
    def postrender(self):
        glPopMatrix()

class Translation(Node):
    def __init__(self, vec, *args, **kwargs):
        Node.__init__(self)
        self.vec = vec
    def prerender(self):
        glPushMatrix()
        glTranslate(*self.vec)
    def postrender(self):
        glPopMatrix()

class TexturedSphere(Node):

    def __init__(self, filename, radius, mipmap=True, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
        import Image as im
        image = im.open(image_dir + "/" + filename)
        self.ix = image.size[0]
        self.iy = image.size[1]
        self.pixels = image.tostring("raw", "RGBX", 0, -1)
        self.radius = radius
        self.angle = 0

        self.texid = None
        self.listid = None
        self.mipmap = mipmap
        self.transparent = False
        self.color = [1, 1, 1, 1]
        self.inside = False

    def loadTexture(self):
        self.texid = glGenTextures(1)

        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glBindTexture(GL_TEXTURE_2D, self.texid)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        if self.mipmap:
            gluBuild2DMipmaps(GL_TEXTURE_2D,  3,  self.ix,  self.iy,  
                              GL_RGBA,  GL_UNSIGNED_BYTE,  self.pixels);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, 
                            GL_LINEAR_MIPMAP_LINEAR)
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, 3, self.ix, self.iy, 0, 
                         GL_RGBA, GL_UNSIGNED_BYTE, self.pixels)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    def drawSphere(self):
        if not self.listid:
            self.listid = glGenLists(1)
            assert self.listid

            glNewList(self.listid, GL_COMPILE)
            quad = gluNewQuadric()
            gluQuadricNormals(quad, GLU_SMOOTH)
            if self.inside:
                gluQuadricOrientation(quad, GLU_INSIDE)
            else:
                gluQuadricOrientation(quad, GLU_OUTSIDE)
            gluQuadricTexture(quad, GL_TRUE)
            gluSphere(quad, self.radius, 30, 30)
            gluDeleteQuadric(quad)
            glEndList()
        glCallList(self.listid)
        
    def drawSphereTrans(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)
        TexturedSphere.drawSphere(self)
        glCullFace(GL_BACK)
        TexturedSphere.drawSphere(self)
        glDisable(GL_BLEND)

    def display(self):
        if not self.texid:
            self.loadTexture()
        glBindTexture(GL_TEXTURE_2D, self.texid)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glEnable(GL_TEXTURE_2D)

        glPushMatrix()
        glRotate(self.angle, 0, 0, 1 )

        glPushAttrib(GL_CURRENT_BIT)
        glColor(self.color)

        if self.transparent:
            self.drawSphereTrans()
        else:
            self.drawSphere()
        glPopAttrib()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)


class CoordSystemNode(Node):
    def __init__(self, color=[1,1,1,1], *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
        self.color = color
        self.w = 0.001
    def display(self):
        if not self.app.show_coords:
            return
        glDisable(GL_LIGHTING)
        glPushAttrib(GL_CURRENT_BIT)
        glBegin(GL_LINES)
        w = self.w
        glColor(*self.color)
        glVertex(-1, 0, 0, w)
        glVertex( 1, 0, 0, w)
        glVertex( 0,-1, 0, w)
        glVertex( 0, 1, 0, w)
        glVertex( 0, -0.001,-1, w)
        glVertex( 0, 0.001, 1, w)
        glEnd()
        glPopAttrib()
        glEnable(GL_LIGHTING)


class CircleNode(Node):
    def __init__(self, r, N=100, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
        self.r = r
        self.N = N
        self.listid = None
    def render_circle(self):
        from math import sin, cos, pi
        glBegin(GL_LINE_LOOP)
        f = 2 * pi / self.N
        for i in range(self.N):
            glVertex(self.r*cos(i*f), self.r*sin(i*f))
        glEnd()
    def display(self):
        if not self.listid:
            self.listid = glGenLists(1)
            assert self.listid
            glNewList(self.listid, GL_COMPILE)
            self.render_circle()
            glEndList()
        glCallList(self.listid)
        
