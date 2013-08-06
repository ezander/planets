from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from vis.scenegraph import *
from vis.camera import *
from vis.application import *


class StarField(TexturedSphere):
    def __init__(self, *args, **kwargs):
        TexturedSphere.__init__(self, *args, **kwargs)
        self.inside = True
        self.mipmap = False

class CelestialBody(TexturedSphere):
    def __init__(self, *args, **kwargs):
        TexturedSphere.__init__(self, *args, **kwargs)
        self.orbital_radius = 0
        self.orbital_speed = 0
        self.orbital_angle0 = 0
        self.rotational_speed = 0
        self.rotation_angle0 = 0
        self.rotation_axis = [1, 0, 0];
        self.rotation_axis_angle = 0;
        self.sys_node = Node()

    def prerender(self):
        glPushMatrix()

        vec = [0, 0, 1];
        time = self.app.timer.elapsed()
        angle = self.orbital_angle0 + time * self.orbital_speed
        glRotate(angle, *vec)
        glTranslate(self.orbital_radius, 0, 0)
        glRotate(-angle, *vec)
        
    def postrender(self):
        glPopMatrix()

    def display(self):
        glPushMatrix()
        glRotate(self.rotation_axis_angle, *self.rotation_axis)

        time = self.app.timer.elapsed()
        angle = self.rotation_angle0 + time * self.rotational_speed
        vec = [0, 0, 1];
        glRotate(angle, *vec)
        self.sys_node.render()
        TexturedSphere.display(self)
        glPopMatrix()

class SunSphere(CelestialBody):
    def display(self):
        glPushAttrib(GL_LIGHTING_BIT)
        glMaterial(GL_FRONT, GL_EMISSION, [1, 1, 0.3, 1])
        CelestialBody.display(self)
        glPopAttrib()

class PlanetSphere(CelestialBody):
    def __init__(self, *args, **kwargs):
        CelestialBody.__init__(self, *args, **kwargs)

class PlanetsApplication(Application):
    def __init__(self):
        Application.__init__(self)
        self.window_title = "Planets"
        self.camera = CameraOnSphere()
        self.show_coords = False
        self.ambient = 0.3

        solar_system = Node()
        solar_system.add_child(CoordSystemNode(color=[0.3, 0.3, 0, 1], app=self))

        #starfield = StarField("starfield/1024x512.png", 500, app=self)
        #starfield = StarField("starfield/8192x4096.png", 500, app=self)
        #starfield = StarField("starfield/4096x2048.png", 500, app=self)
        #starfield = StarField("starfield/2048x1024.png", 500, app=self)

        #solar_system.add_child(starfield)


        sun = SunSphere("sunmap.jpg", 7, app=self)
        sun.rotational_speed = 10
        solar_system.add_child(sun)

        mars = PlanetSphere("mars_1k_color.jpg", 1, app=self)
        mars.orbital_radius = 10
        mars.orbital_speed = 31.2
        mars.rotational_speed = 40
        solar_system.add_child(mars)
        solar_system.add_child(CircleNode(mars.orbital_radius))

        jupiter = PlanetSphere("jupitermap.jpg", 3, app=self)
        #jupiter = PlanetSphere("arne.jpg", 3, app=self)
        jupiter.orbital_radius = 30
        jupiter.orbital_speed = 15
        jupiter.rotational_speed = 50
        solar_system.add_child(jupiter)
        solar_system.add_child(CircleNode(jupiter.orbital_radius))

        earth = PlanetSphere("earthmap1k.jpg", 2, app=self)
        earth.orbital_radius = 20
        earth.orbital_speed = 10
        earth.orbital_angle0 = -30
        earth.rotational_speed = 150
        earth.rotation_axis = [1, 0, 0];
        earth.rotation_axis_angle = 23.5;
        #earth.transparent = True
        #earth.color = [3, 0, 1, 0.6]
        
        solar_system.add_child(earth)
        solar_system.add_child(CircleNode(earth.orbital_radius))

        moon = PlanetSphere("moonmap.jpg", 0.8, app=self)
        moon.orbital_radius = 5
        moon.orbital_speed = 50
        moon.rotational_speed = 50
        earth.add_child(moon)
        earth.add_child(CircleNode(moon.orbital_radius))
        earth.sys_node.add_child(CoordSystemNode(color=[0.3, 0.3, 0.6, 1], app=self))

        neptune = PlanetSphere("neptunemap.jpg", 2, app=self)
        neptune.orbital_radius = 50
        neptune.orbital_speed = 7
        neptune.orbital_angle0 = 150
        solar_system.add_child(neptune)
        solar_system.add_child(CircleNode(neptune.orbital_radius))

        self.solar_system = solar_system
        self.camera.pan_out(40)
        self.camera.pan_right(30)
        self.camera.pan_up(30)

        # all this info should really come from a json file
        self.load_json_stuff()
        

    def setupSceneLights(self):
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, 3 * [self.ambient] +[1])

        light = GL_LIGHT0 # + 1
        glEnable(light)
        glLight(light, GL_POSITION, (0, 0, 0, 1))
        glLight(light, GL_DIFFUSE, (1, 1, 0.9, 1))
        glLight(light, GL_SPECULAR, (1, 1, 0.9, 1))
    
    def renderScene(self):
        self.solar_system.render()
        
    def onInput(self, key, x, y, special):
        mods = glutGetModifiers()
        if special and (mods & GLUT_ACTIVE_SHIFT):
            f = 5
        else:
            f = 1

        camera = self.camera
        if key == GLUT_KEY_LEFT:
            camera.pan_left(f)
        elif key == GLUT_KEY_RIGHT:
            camera.pan_right(f)
        elif key == GLUT_KEY_PAGE_UP:
            camera.pan_in(f)
        elif key == GLUT_KEY_PAGE_DOWN:
            camera.pan_out(f)
        elif key == GLUT_KEY_UP:
            camera.pan_up(f)
        elif key == GLUT_KEY_DOWN:
            camera.pan_down(f)
        elif key == "c":
            self.show_coords = not self.show_coords
        elif "1" <= key <= "9":
            s = 2.0 ** (int(key)-1)
            self.timer.set_speed(s)
        elif key == "0":
            self.timer.set_speed(0)
        elif key == " ":
            self.timer.toggle_pause()
        elif key == "a":
            self.ambient = 0.3 - self.ambient
        else:
            #print "Key pressed", key, x, y
            return False
        return True

    def load_json_stuff(self):
        import json
        import pprint
        data = json.load(open("config.json"))
        pprint.pprint(data)
        print json.dumps(data)
        print json.JSONEncoder(indent=2).encode(data)


if __name__ == "__main__":
    app = PlanetsApplication()
    app.main()

