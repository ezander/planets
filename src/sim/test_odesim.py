# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:10:30 2013

@author: ezander
"""

from odesim import OdeSimulator, SimObject

from numpy.testing import assert_equal, assert_almost_equal
from numpy import array

class FallingObject(SimObject):
    def __init__(self, h0, g=9.81, v0=0):
        self.g = g
        self.y = array([h0, v0], dtype=float)

    @property
    def dim(self):
        return len(self.y)
    
    @property
    def state(self):
        return self.y

    @state.setter
    def state(self, value):
        self.y = value
        
    def diff(self, t):
        h, v = self.y
        g = self.g
        #print array([v, -g])
        return array([v, -g])


def test_falling_object():
    obj = FallingObject(1000.0, g=2)
    assert_equal(obj.state, array([1000.0, 0.0]))
    assert_equal(obj.diff(3), array([0.0, -2.0]))

def test_sim_one_object():
    odesim = OdeSimulator()
    obj1 = FallingObject(1000.0, g=2)
    odesim.add(obj1)
    odesim.integrate(1)
    assert_almost_equal(obj1.state, array([999.0, -2.0]))
    odesim.integrate(2)
    assert_almost_equal(obj1.state, array([996.0, -4.0]))
    odesim.integrate(2)
    assert_almost_equal(obj1.state, array([996.0, -4.0]))
    odesim.integrate(3)
    assert_almost_equal(obj1.state, array([991.0, -6.0]))

def test_sim_more_objects():
    odesim = OdeSimulator()
    obj1 = FallingObject(1000.0, g=2)
    odesim.add(obj1)
    obj2 = FallingObject(1000.0, g=20)
    odesim.add(obj2)
    obj3 = FallingObject(100.0, g=20)
    odesim.add(obj3)
    
    odesim.integrate(1)
    odesim.integrate(1.5)
    odesim.integrate(2)
    assert_almost_equal(obj1.state, array([996.0,  -4.0]))
    assert_almost_equal(obj2.state, array([960.0, -40.0]))
    assert_almost_equal(obj3.state, array([ 60.0, -40.0]))


if __name__ == "__main__":
    from numpy.testing import run_module_suite
    run_module_suite()
