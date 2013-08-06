# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:39:21 2013

@author: ezander
"""

from sim.odesim import OdeSimulator
from sim.planet import SolarSystem, Units

solsys = SolarSystem()

solsys.read_base_json("solarsys_data.json")
solsys.read_dyn_json("solarsys_dyndata.json")
solsys.read_vis_json("solarsys_vis.json")

simulator = OdeSimulator()
for body in solsys.get_bodies():
    print body.display_name, ":", body.x
    simulator.add(body)

from numpy.linalg import norm
earth = solsys.get_body("earth")
for i in range(5):
    simulator.integrate(i * 365.25 * Units.d / 4)
    #simulator.integrate(1 * Units.d)
    #print earth.x/Units.AU, earth.v/(Units.AU/Units.d)
    #print norm(earth.x/Units.AU), norm(earth.v/(Units.AU/Units.d))
    #print 2*3.14159 * norm(earth.x/Units.AU)/norm(earth.v/(Units.AU/Units.d))
    print earth.x[0:2]/Units.AU
    print simulator.t / Units.d

if False:
    simulator.integrate(100)
    print 
    print
    
    for body in solsys.get_bodies():
        print body.display_name, ":", body.x
    
    
    print "foo"
