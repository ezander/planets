# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:40:10 2013

@author: ezander
"""

from sim.odesim import SimObject

class Planet(SimObject):
    def __init__(self):
        self.name = "foo"
        self.display_name = "Foobar planet"
        self.mass = 1
        self.x = [0, 0, 0]
        self.v = [0, 0, 0]
        self.rot_axis = [0, 0, 1]
        self.rot_angle = 0

    @property
    def dim(self):
        return 7
        
    @property
    def state(self):
        return [self.x, self.v, self.rot_angle]
        
    @state.setter
    def state(self, value):
        self.x = value[0:3]
        self.v = value[3:6]
        self.rot_angle = value[6]
    
    def diff(self, t):
        pass
    
class SolarSystem(object):
    def __init__(self):
        self.bodies = {}
        
    def get_bodies(self):
        return self.bodies.values()
        
    def get_body(self, name):
        return self.bodies[name]
        
    def read_json(self, filename):
        import json
        data=json.load(open(filename))
        for key, val in data.iteritems():
            planet = Planet()
            planet.name = key
            planet.display_name = val["name_en"]
            planet.mass = val["mass"]
            planet.x = val["position"]
            planet.y = val["speed"]
            print key
    
    
# vis:  name, refbody, size_scaling_func, radius_scaling_func, texture