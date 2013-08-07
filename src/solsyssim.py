import json

from numpy.linalg import norm

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from vis.scenegraph import *
from vis.camera import *
from vis.application import *
from vis.rescale import rescale_size_factor, rescale_orbit_factor

from sim.physics import Units
from sim.odesim import OdeSimulator
from sim.planet import SolarSystem

class StarField(TexturedSphere):
    def __init__(self, *args, **kwargs):
        TexturedSphere.__init__(self, *args, **kwargs)
        self.inside = True
        self.mipmap = False

class CelestialBody(TexturedSphere):
    def __init__(self, body, app, *args, **kwargs):
        TexturedSphere.__init__(self, 
                                body.texture, 
                                body.radius / Units.AU, 
                                *args, **kwargs)
        self.body = body
        self.app = app

    def display(self):
        glPushMatrix()
        
        scale_factor = rescale_orbit_factor(norm(self.body.x), 
                                            10 * Units.AU,
                                            1.6,
                                            1 * Units.AU,
                                            self.app.rescale_orbit)
        if scale_factor>1:
            scale_factor = 1
        #print self.body.name, scale_factor, norm(self.body.x)/Units.AU
        glTranslate(*(scale_factor * self.body.x / Units.AU))

        glPushAttrib(GL_LIGHTING_BIT)
        if self.body.material is not None:
            glMaterial(GL_FRONT, GL_EMISSION, [1, 1, 0.3, 1])

        scale_factor = rescale_size_factor(self.body.radius, 
                                           self.app.rescale_size_ref,
                                           self.app.rescale_size)
        glScale(scale_factor, scale_factor, scale_factor)
        TexturedSphere.display(self)
        glPopAttrib()
        
        if self.body.light:
            pass
        
        glPopMatrix()

class PlanetsApplication(Application):
    def __init__(self):
        Application.__init__(self)

        config = self.load_config()

        self.window_title = config.get("window_title", "Planets")
        self.show_coords = config.get("show_coords", False)
        self.ambient = config.get("ambient", 0.3)
        if not isinstance(self.ambient, list):
            self.ambient = 3 * [self.ambient]
        if len(self.ambient)<3:
            self.ambient = self.ambient + [1]

        self.rescale_orbit = config.get("rescale_orbit", 0.5)
        self.rescale_size = config.get("rescale_size", 0.5)
        self.rescale_size_ref = config.get("rescale_size_ref", 1e6) * Units.km


        solsys = SolarSystem()
        solsys.read_base_json("solarsys_data.json")
        solsys.read_dyn_json("solarsys_dyndata.json")
        solsys.read_vis_json("solarsys_vis.json")

        self.root_node = Node()
        self.root_node.add_child(CoordSystemNode(color=[0.3, 0.3, 0, 1], app=self))
        
        integrator = config.get("integrator", "vode")
        ode_kwargs = config.get("ode_kwargs", {})
        self.simulator = OdeSimulator(integrator, ode_kwargs)
        
        for body in solsys.get_bodies():
            sphere = CelestialBody(body, app=self)
            self.root_node.add_child(sphere)
            self.simulator.add(body)
            print body.name, body.x/Units.AU


        self.camera = CameraOnSphere()
        self.camera.pan_out(config.get("pan_out", 5))
        self.camera.pan_right(config.get("pan_right", 30))
        self.camera.pan_up(config.get("pan_up", 30))

        

    def setupSceneLights(self):
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient)
        
        light = GL_LIGHT0 # + 1
        glEnable(light)
        glLight(light, GL_POSITION, (0, 0, 0, 1))
        glLight(light, GL_DIFFUSE, (1, 1, 0.9, 1))
        glLight(light, GL_SPECULAR, (1, 1, 0.9, 1))
    
    def renderScene(self):
        t=self.timer.elapsed()
        self.simulator.integrate(t * Units.d * 10)
        self.root_node.render()
        
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
        elif key == GLUT_KEY_INSERT:
            self.rescale_size = max(0.0, self.rescale_size - f/50.0)
        elif key == chr(127):
            self.rescale_size = min(1.0, self.rescale_size + f/50.0)
        elif key == GLUT_KEY_HOME:
            self.rescale_orbit = max(0.0001, self.rescale_orbit - f/50.0)
        elif key == GLUT_KEY_END:
            self.rescale_orbit = min(1.0, self.rescale_orbit + f/50.0)
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
            print "Key pressed", key, x, y
            return False
        return True

    def load_config(self):
        config = json.load(open("config.json"))
        if config.get("dump", False):
            print json.JSONEncoder(indent=2).encode(data)
        return config


if __name__ == "__main__":
    app = PlanetsApplication()
    app.main()

