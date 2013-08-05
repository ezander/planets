# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:10:30 2013

@author: ezander
"""

from rocket import SimpleRocket, MultistageRocket
from odesim import OdeSimulator

from numpy.testing import assert_almost_equal, assert_array_almost_equal
from numpy import array, log

def test_simple_rocket():
    odesim = OdeSimulator()
    rocket = SimpleRocket(1000.0, 10.0, 90.0, 1)
    odesim.add(rocket)
    odesim.integrate(1)
    assert_almost_equal(rocket.state, array([1000.0 * log(100.0/99.0)]))
    assert_almost_equal(rocket.stage.state, array([89.0]))
    assert_almost_equal(rocket.stage.active, True)
    odesim.integrate(12)
    assert_almost_equal(rocket.state, array([1000.0 * log(100.0/88.0)]))
    assert_almost_equal(rocket.stage.state, array([78.0]))
    assert_almost_equal(rocket.stage.active, True)
    odesim.integrate(89)
    assert_almost_equal(rocket.state, array([1000.0 * log(100.0/11.0)]), decimal=4)
    assert_almost_equal(rocket.stage.state, array([1.0]))
    assert_almost_equal(rocket.stage.active, True)
    odesim.integrate(90)
    assert_almost_equal(rocket.state, array([1000.0 * log(100.0/10.0)]), decimal=4)
    assert_almost_equal(rocket.stage.state+1, array([1.0]))
    odesim.integrate(99.1)
    assert_almost_equal(rocket.stage.active, True)
    assert_almost_equal(rocket.stage.state, array([0.0]))
    assert_almost_equal(rocket.state, array([1000.0 * log(100.0/10.0)]), decimal=4)

def test_multi_rocket1():
    odesim = OdeSimulator()
    rocket = MultistageRocket()
    rocket.add_stage(1000.0, 10.0, 90.0, 1)
    odesim.add(rocket)

    odesim.integrate(1)
    assert_almost_equal(rocket.state, array([1000.0 * log(100.0/99.0)]))
    assert_almost_equal(rocket.stage.state, array([89.0]))
    assert_almost_equal(rocket.stage.active, True)
    odesim.integrate(12)
    assert_almost_equal(rocket.state, array([1000.0 * log(100.0/88.0)]))
    assert_almost_equal(rocket.stage.state, array([78.0]))
    assert_almost_equal(rocket.stage.active, True)
    odesim.integrate(89)
    assert_almost_equal(rocket.state, array([1000.0 * log(100.0/11.0)]), decimal=4)
    assert_almost_equal(rocket.stage.state, array([1.0]))
    assert_almost_equal(rocket.stage.active, True)
    odesim.integrate(90)
    assert_almost_equal(rocket.state, array([1000.0 * log(100.0/10.0)]), decimal=4)
    assert_almost_equal(rocket.stage.state+1, array([1.0]))
    odesim.integrate(99.1)
    assert_almost_equal(rocket.stage.active, True)
    assert_almost_equal(rocket.stage.state, array([0.0]))
    assert_almost_equal(rocket.state, array([1000.0 * log(100.0/10.0)]), decimal=4)

def test_multi_rocket2():
    odesim = OdeSimulator()
    rocket = MultistageRocket()
    rocket.add_stage(1000.0, 10.0, 90.0, 1)
    rocket.add_stage(1000.0,  2.0, 18.0, 1)
    odesim.add(rocket)

    assert_almost_equal(rocket.stages[0].state, array([90.0]))
    assert_almost_equal(rocket.stages[1].state, array([18.0]))
    
    odesim.integrate(1)
    assert_almost_equal(rocket.stages[0].state, array([89.0]))
    assert_almost_equal(rocket.stages[1].state, array([18.0]))
    assert_almost_equal(rocket.state, array([1000.0 * log(120.0/119.0)]))

    odesim.integrate(90)
    assert_array_almost_equal(rocket.state, 1000.0 * log(120.0/30.0), decimal=3)
    odesim.integrate(95)
    assert_almost_equal(rocket.stage.state, array([13.0]))
    assert_array_almost_equal(rocket.state, 1000.0 * (log(120.0/30.0) + log(20.0/15.0)), decimal=3)
    odesim.integrate(125)
    assert_almost_equal(rocket.stage.state, array([0.0]))
    assert_array_almost_equal(rocket.state, 1000.0 * (log(120.0/30.0) + log(20.0/2.0)), decimal=3)

if __name__ == "__main__":
    from numpy.testing import run_module_suite
    run_module_suite()
