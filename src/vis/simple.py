from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

dist = 0
def update(val):
    global dist
    dist -= 1
    if dist < -360:
        dist = 0.0
    glutPostRedisplay()
    glutTimerFunc(25, update, val)

class Node(object):
    def __init__(self):
        self.children = []
    def addChild(self, child):
        self.children.append(child)
        return child
    def prerender(self):
        pass
    def postrender(self):
        pass
    def display(self):
        pass
    def render():
        self.prerender()
        self.display()
        for child in self.children:
            self.render()
        self.postrender()

class Rotation(Node):
    def __init__(self, angle, vec):
        Node.__init__(self)
        self.angle = angle
        self.vec = vec
    def prerender(self):
        glPushMatrix()
        glRotate(angle, *vec)
    def postrender(self):
        glPopMatrix()

class Scaling(Node):
    def __init__(self, vec):
        Node.__init__(self)
        self.vec = vec
    def prerender(self):
        glPushMatrix()
        glScale(*vec)
    def postrender(self):
        glPopMatrix()

class Translation(Node):
    def __init__(self, vec):
        Node.__init__(self)
        self.vec = vec
    def prerender(self):
        glPushMatrix()
        glScale(*vec)
    def postrender(self):
        glPopMatrix()


def loadTextures():
    #global texture
    import Image as im
    image = im.open("jupitermap.jpg")
    print image
	
    ix = image.size[0]
    iy = image.size[1]
    image = image.tostring("raw", "RGBX", 0, -1)
	
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)


window = 0
def onKeyPress(key, x, y):
    if ord(key) == 27:
        glutDestroyWindow(window)
    print "Key pressed", ord(key), x, y

def onResize(w, h):
    print "Resized:", w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, float(w) / h , 0.01, 1000)



def setupCameraLights():
    pass

def setupCamera():
    glLoadIdentity()
    gluLookAt( 40,20,40, 0,0,0, 0,1,0)

def setupSceneLights():
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.1, 0, 0.0, 1))

    glEnable(GL_LIGHT0)
    glLight(GL_LIGHT0, GL_POSITION, (0, 5, 3))
    glLight(GL_LIGHT0, GL_DIFFUSE, (1, 1, 0.2, 1))

def renderScene():
    glColor(1,1,1,1)
    glPushMatrix()
    glBegin(GL_LINES)
    w = 0.01
    glVertex(-1, 0, 0, w)
    glVertex( 1, 0, 0, w)
    glVertex( 0,-1, 0, w)
    glVertex( 0, 1, 0, w)
    glVertex( 0, 0,-1, w)
    glVertex( 0, 0, 1, w)
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glRotate(90, 0, 1, 0 )
    glutSolidTeapot(5)
    
    glTranslate(10, 7, 0)
    sphere = gluNewQuadric()
    gluQuadricNormals(sphere, GLU_SMOOTH)
    gluQuadricOrientation(sphere, GLU_OUTSIDE)
    glEnable(GL_TEXTURE_2D)
    gluQuadricTexture(sphere, GL_TRUE)
    glPushMatrix()
    glRotate(90, 1, 0, 0 )
    glRotate(dist, 0, 0, 1 )
    gluSphere(sphere, 3, 30, 30)
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)
    gluDeleteQuadric(sphere)
    

    glColor(1,1,1,1)
    glTranslate(0, 0, 10)
    glutSolidSphere(3, 40, 40)
    #glScale(2,2,2)
    #glutSolidDodecahedron()
    glPopMatrix()
    

def onDisplay():
    print "Display"
    glMatrixMode(GL_MODELVIEW)
    glClearColor(0.0, 0.0, 0.0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setupCameraLights()
    setupCamera()
    setupSceneLights()
    renderScene()
    glutSwapBuffers()
    

def main():
    global window
    glutInit()
    glutInitWindowSize(1000, 700)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    window = glutCreateWindow("Planets")
    glutKeyboardFunc(onKeyPress)
    glutReshapeFunc(onResize)
    glutDisplayFunc(onDisplay)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)

    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    loadTextures()
    

    glutTimerFunc(25, update, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()




