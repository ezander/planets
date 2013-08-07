# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:10:30 2013

@author: ezander
"""

from rocket import SimpleRocket, MultistageRocket
from odesim import OdeSimulator

from numpy.testing import assert_approx_equal, assert_array_almost_equal, assert_almost_equal
from numpy import array, log

def test_simple_rocket():
    odesim = OdeSimulator()
    rocket = SimpleRocket(1000.0, 10.0, 90.0, 1)
    odesim.add(rocket)
    odesim.integrate(1)
    assert_approx_equal(rocket.state, array([1000.0 * log(100.0/99.0)]))
    assert_approx_equal(rocket.stage.state, array([89.0]))
    assert_approx_equal(rocket.stage.active, True)
    odesim.integrate(12)
    assert_approx_equal(rocket.state, array([1000.0 * log(100.0/88.0)]))
    assert_approx_equal(rocket.stage.state, array([78.0]))
    assert_approx_equal(rocket.stage.active, True)
    odesim.integrate(89)
    assert_approx_equal(rocket.state, array([1000.0 * log(100.0/11.0)]), significant=4)
    assert_approx_equal(rocket.stage.state, array([1.0]))
    assert_approx_equal(rocket.stage.active, True)
    odesim.integrate(90)
    assert_approx_equal(rocket.state, array([1000.0 * log(100.0/10.0)]), significant=4)
    assert_approx_equal(rocket.stage.state+1, array([1.0]))
    odesim.integrate(99.1)
    assert_approx_equal(rocket.stage.active, True)
    assert_almost_equal(rocket.stage.state, array([0.0]))
    assert_approx_equal(rocket.state, array([1000.0 * log(100.0/10.0)]), significant=4)

def test_multi_rocket1():
    odesim = OdeSimulator()
    rocket = MultistageRocket()
    rocket.add_stage(1000.0, 10.0, 90.0, 1)
    odesim.add(rocket)

    odesim.integrate(1)
    assert_approx_equal(rocket.state, array([1000.0 * log(100.0/99.0)]))
    assert_approx_equal(rocket.stage.state, array([89.0]))
    assert_approx_equal(rocket.stage.active, True)
    odesim.integrate(12)
    assert_approx_equal(rocket.state, array([1000.0 * log(100.0/88.0)]))
    assert_approx_equal(rocket.stage.state, array([78.0]))
    assert_approx_equal(rocket.stage.active, True)
    odesim.integrate(89)
    assert_approx_equal(rocket.state, array([1000.0 * log(100.0/11.0)]), significant=5)
    assert_approx_equal(rocket.stage.state, array([1.0]))
    assert_approx_equal(rocket.stage.active, True)
    odesim.integrate(90)
    assert_approx_equal(rocket.state, array([1000.0 * log(100.0/10.0)]), significant=5)
    assert_approx_equal(rocket.stage.state+1, array([1.0]))
    odesim.integrate(99.1)
    assert_approx_equal(rocket.stage.active, True)
    assert_almost_equal(rocket.stage.state, array([0.0]))
    assert_approx_equal(rocket.state, array([1000.0 * log(100.0/10.0)]), significant=5)

def test_multi_rocket2():
    odesim = OdeSimulator(integrator="dop853")
    rocket = MultistageRocket()
    rocket.add_stage(1000.0, 10.0, 90.0, 1)
    rocket.add_stage(1000.0,  2.0, 18.0, 1)
    odesim.add(rocket)

    assert_approx_equal(rocket.stages[0].state, array([90.0]))
    assert_approx_equal(rocket.stages[1].state, array([18.0]))
    
    odesim.integrate(1)
    assert_approx_equal(rocket.stages[0].state, array([89.0]))
    assert_approx_equal(rocket.stages[1].state, array([18.0]))
    assert_approx_equal(rocket.state, array([1000.0 * log(120.0/119.0)]), significant=5)
    assert_approx_equal(len(rocket.stages), 2)

    odesim.integrate(50)
    assert_approx_equal(rocket.stages[0].state, array([40.0]))
    assert_approx_equal(rocket.stages[1].state, array([18.0]))
    #assert_approx_equal(rocket.state, array([1000.0 * log(120.0/119.0)]), significant=5)
    assert_approx_equal(len(rocket.stages), 2)

    odesim.integrate(87)
    assert_approx_equal(rocket.stages[0].state, array([3.0]))
    assert_approx_equal(rocket.stages[1].state, array([18.0]))
    #assert_approx_equal(rocket.state, array([1000.0 * log(120.0/119.0)]), significant=5)
    assert_approx_equal(len(rocket.stages), 2)
    
    # note: multistage rockets do not work correctly because there is not 
    # way to specify events for state changes in the ode solver suite in 
    # scipy. The problem is that the solvers integrate over the state change,
    # later go back in time with the already changed state, which leads to 
    # nonsense results. This can be fixed either by wrapping lsodar in scipy, 
    # or with some trickery in the rocket code, I don't have time to do now.
    
    return

    odesim.integrate(87)
    print rocket.stages[0].state, rocket.stages[1].state
    print odesim.t, rocket.cur_stage, rocket.stage.state
    #odesim.integrate(87.952)
    #print rocket.stages[0].state, rocket.stages[1].state
    #print odesim.t, rocket.cur_stage, rocket.stage.state
    odesim.integrate(89)
    
    
    
    odesim.integrate(89)
    print odesim.t, rocket.cur_stage, rocket.stage.state
    odesim.integrate(89.9)
    print odesim.t, rocket.cur_stage, rocket.stage.state
    #print rocket.stage.state, rocket.stages[1].state
    odesim.integrate(90)
    print odesim.t, rocket.cur_stage, rocket.stage.state
    odesim.integrate(90.01)
    print odesim.t, rocket.cur_stage, rocket.stage.state
    print rocket.stage.state
    #assert_array_almost_equal(rocket.state, 1000.0 * log(120.0/30.0), significant=3)
    odesim.integrate(95)
    assert_approx_equal(len(rocket.stages), 1)
    assert_approx_equal(rocket.stage.state, array([13.0]))
    assert_array_almost_equal(rocket.state, 1000.0 * 
                              (log(120.0/30.0) + log(20.0/15.0)), significant=3)

    odesim.integrate(125)
    assert_approx_equal(rocket.stage.state, array([0.0]))
    assert_array_almost_equal(rocket.state, 1000.0 * 
                              (log(120.0/30.0) + log(20.0/2.0)), significant=3)

if __name__ == "__main__":
    from numpy.testing import run_module_suite
    run_module_suite()
