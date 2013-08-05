# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:39:21 2013

@author: ezander
"""

from sim.odesim import OdeSimulator
from sim.planet import Planet, SolarSystem

solsys = SolarSystem()

solsys.read_json("solarsys.json")

simulator = OdeSimulator()
for body in solsys.get_bodies():
    print body.display_name, ":", body.x
    simulator.add(body)

simulator.integrate(100)
print 
print

for body in solsys.get_bodies():
    print body.display_name, ":", body.x


print "foo"
