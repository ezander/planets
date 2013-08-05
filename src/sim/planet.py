# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:40:10 2013

@author: ezander
"""

from sim.odesim import SimObject, floatvec
from numpy import concatenate as cat

class Units:
    m = 1.0
    km = 1000 * m
    AU=149597870.691 * km

    s = 1.0
    h = 3600 * s
    d = 24 * hr

    G = 6.6738480E-11 m**3 * kg / s**2

print Units.d

class Planet(SimObject):
    def __init__(self):
        self.name = "foo"
        self.display_name = "Foobar planet"
        self.mass = 1
        self.x = floatvec([0, 0, 0])
        self.v = floatvec([0, 0, 0])
        self.rot_axis = [0, 0, 1]
        self.rot_speed = [0]
        self.rot_angle = [0]

    @property
    def dim(self):
        return 7
        
    @property
    def state(self):
        return cat((self.x, self.v, self.rot_angle))
        
    @state.setter
    def state(self, value):
        self.x = value[0:3]
        self.v = value[3:6]
        self.rot_angle = value[6]
    
    def diff(self, t):
        a = 0 * self.x
        return cat((self.v, a, self.rot_speed))
    
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
            planet.x = floatvec(val["position"])
            planet.v = floatvec(val["speed"])
            self.bodies[key] = planet
            print key
    
    
# vis:  name, refbody, size_scaling_func, radius_scaling_func, texture
