# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:40:10 2013

@author: ezander
"""

import json
from numpy import concatenate

from sim.odesim import SimObject, floatvec
from sim.physics import Units, gravitational_accel

class Planet(SimObject):
    def __init__(self, solarsys):
        self.name = "planet"
        self.display_name = "Planet"
        self.mass = 1
        self.radius = 1
        self.x = floatvec([0, 0, 0])
        self.v = floatvec([0, 0, 0])
        self.rot_axis = [0, 0, 1]
        self.rot_speed = [0]
        self.rot_angle = [0]
        self.solarsys = solarsys
        self.material = None
        self.light = None

    @property
    def dim(self):
        return 7
        
    @property
    def state(self):
        return concatenate((self.x, self.v, self.rot_angle))
        
    @state.setter
    def state(self, value):
        self.x = value[0:3]
        self.v = value[3:6]
        self.rot_angle = value[6]
    
    def diff(self, t):
        a = 0 * self.x
        for body in self.solarsys.get_bodies():
            if body.name == self.name:
                continue
            a += gravitational_accel(self.x, body.x, body.mass)
        return concatenate((self.v, a, self.rot_speed))
    
class SolarSystem(object):
    def __init__(self):
        self.bodies = {}
        
    def get_bodies(self):
        return self.bodies.values()
        
    def get_body(self, name):
        if name in self.bodies:
            return self.bodies[name]
        else:
            body = Planet(self)
            body.name = name
            self.bodies[name] = body
            return body
        
    def read_base_json(self, filename):
        data=json.load(open(filename))
        for key, val in data.iteritems():
            planet = self.get_body(key)
            planet.display_name = val["name_en"]
            planet.mass = val["mass"] * Units.kg
            planet.radius = val["radius"] * Units.km

    def read_dyn_json(self, filename):
        data=json.load(open(filename))
        for key, val in data.iteritems():
            planet = self.get_body(key)
            planet.x = floatvec(val["position"]) * Units.AU
            planet.v = floatvec(val["velocity"]) * Units.AU / Units.d

    def read_vis_json(self, filename):
        data=json.load(open(filename))
        for key, val in data.iteritems():
            planet = self.get_body(key)
            planet.texture = val["texture"]
            planet.material = val.get("material", None)
            planet.lightsource = val.get("lightsource", None)
            # vis:  name, refbody, size_scaling_func, radius_scaling_func, texture
