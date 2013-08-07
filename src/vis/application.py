from OpenGL.GLUT import *
import time

from camera import *

__all__ = ["Application", "Stats", "Timer"]

class Stats(object): 
    def __init__(self):
        self.counter = 0
        self.start = time.time()

    def print_stats(self):
        self.end = time.time()
        print "counter:", self.counter
        print "time:", self.end-self.start
        print "fps:", 1.0*self.counter/(self.end-self.start)


class Timer(object):
    def __init__(self):
        self.start = time.time()
        self.add = 0
        self.speed = 1
        self.paused = False
    def elapsed(self):
        return self.speed * (time.time() - self.start) + self.add
    def reset(self):
        self.add = 0
        self.start = time.time()
    def set_speed(self, speed):
        self.add = self.elapsed()
        self.start = time.time()
        self.speed = speed
        self.paused = False
    def pause(self):
        if self.paused:
            return
        self.old_speed = self.speed
        self.set_speed(0)
        self.paused = True
    def unpause(self):
        if not self.paused:
            return
        self.set_speed(self.old_speed)
        self.paused = False
    def toggle_pause(self):
        if self.paused:
            self.unpause()
        else:
            self.pause()

class Application(object):
    def __init__(self):
        self.window_title = "OpenGL"
        self.fullscreen = None
        self.camera = CameraLookAt()
        self.stats = Stats()
        self.timer = Timer()
        self.update_interval = 10


    def toggle_fullscreen(self):
        if self.fullscreen is None:
            self.fullscreen = [(glutGet(GLUT_WINDOW_X),glutGet(GLUT_WINDOW_Y)),
                   (glutGet(GLUT_WINDOW_WIDTH),glutGet(GLUT_WINDOW_HEIGHT))]
            glutFullScreen()
        else:
            glutPositionWindow(*self.fullscreen[0])
            glutReshapeWindow(*self.fullscreen[1])
            self.fullscreen = None

    def toggle_gamemode(self):
        print "This is instable and often leads to crashes. Exiting..."
        return
        glutGameModeString( "1024x768:32" )
        if not glutGameModeGet(GLUT_GAME_MODE_ACTIVE):
            print glutGameModeGet(GLUT_GAME_MODE_POSSIBLE)
            print "Entering game mode"
            glutEnterGameMode()
            print glutGameModeGet(GLUT_GAME_MODE_ACTIVE)
            print glutGameModeGet(GLUT_GAME_MODE_DISPLAY_CHANGED)
        else:
            print "Leaving game mode"
            glutLeaveGameMode()

    def onInput(self, key, x, y, special):
        return False

    def onInputDef(self, key, x, y, special):
        if key == "\033":
            self.stats.print_stats()
            glutDestroyWindow(self.window)
            self.window = None
        elif key == "f":
            self.toggle_fullscreen()
        elif key == "g":
            self.toggle_gamemode()

    def _onInput(self, key, x, y):
        special = (type(key)==int)
        if not self.onInput(key, x, y, special):
            self.onInputDef(key, x, y, special)

        if self.window:
            glutPostRedisplay()


    def _onResize(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(30, float(w) / h , 0.01, 1000)

    def setupCamera(self):
        self.camera.setup()
    def setupCameraLights(self):
        pass
    def setupSceneLights(self):
        pass
    def renderScene(self):
        pass

    def onUpdate(self):
        pass

    def _update(self, timer_id):
        if self.window:
            glutPostRedisplay()
        glutTimerFunc(self.update_interval, self._update, timer_id)

    def display(self):
        glMatrixMode(GL_MODELVIEW)
        glClearColor(0.0, 0.0, 0.0, 1)
        glColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        try:
            self.setupCameraLights()
            self.camera.setup()
            self.setupSceneLights()
            self.renderScene()
            self.stats.counter += 1
        except:
            glutDestroyWindow(self.window)
            raise

    def onDisplayFadeIn(self):
        # the first display takes longer to set up data structures,
        # display lists etc. Therefore we display once in the
        # background and then reset the timer so that the fade in
        # starts fresh
        if self.stats.counter == 0:
            self.display()
            self.timer.reset()

        T = 2.0
        t = self.timer.elapsed()
        if t >=T:
            self.display()
        else:
            glClear(GL_ACCUM_BUFFER_BIT)
            alpha = 1.0 * t / T
            alpha = alpha**1.5
            self.display()
            glAccum(GL_ACCUM, alpha)
            glAccum(GL_RETURN, 1.0)

    def _onDisplay(self):
        self.display()
        #self.onDisplayFadeIn()
        glutSwapBuffers()


    def main(self):
        # Init glut and create OpenGL window
        glutInit()
        glutInitWindowSize(1000, 700)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE | GLUT_ACCUM)
        self.window = glutCreateWindow(self.window_title)

        # Set the callback functions
        glutKeyboardFunc(self._onInput)
        glutSpecialFunc(self._onInput)
        glutReshapeFunc(self._onResize)
        glutDisplayFunc(self._onDisplay)
        #glutDisplayFunc(onDisplayScissorIn)
        #glutDisplayFunc(onDisplayBlur)
        #glutDisplayFunc(onDisplayFadeIn)

        # Timer functions for updates
        glutTimerFunc(self.update_interval, self._update, 0)

        # Set OpenGL propeties
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_COLOR_MATERIAL)

        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_CULL_FACE)
        glEnable(GL_MULTISAMPLE)

        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        # Start the GLUT main loop
        self.timer.reset()
        #self.print_gl_version()
        glutMainLoop()


    def print_gl_version(self):
        print glGetString(GL_VENDOR)
        print glGetString(GL_RENDERER)
        print glGetString(GL_VERSION)
        for ext in glGetString(GL_EXTENSIONS).split():
            print "  ", ext

        print gluGetString(GLU_VERSION)
        print gluGetString(GLU_EXTENSIONS)


def onDisplayBlur():
    global dist
    glClear(GL_ACCUM_BUFFER_BIT)
    olddist = dist
    N = 3
    alpha = 0.4
    delta = 0.3

    N = 3
    alpha = 0.8
    delta = 0.3
    f = (1.0 - alpha) / (1.0 -  alpha ** (N))
    for i in range(N):
        display()
        glAccum(GL_ACCUM, f)
        dist -= delta
        f *= alpha
    dist = olddist
    glAccum(GL_RETURN, 1.0)
    glutSwapBuffers()



def onDisplayScissorIn():
    N = 50
    global dist
    if dist>N:
        display()
    else:
        glEnable(GL_SCISSOR_TEST)
        x, y, w, h = glGetInteger(GL_VIEWPORT)
        f = 1.0*dist/N
        glScissor(x, y+int(h * 0.5*(1.0 - f)), w, int(h * f))
        display()
        glDisable(GL_SCISSOR_TEST)
    glutSwapBuffers()
