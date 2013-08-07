# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 11:30:00 2013

@author: ezander
"""

from numpy import array
from numpy.testing import assert_approx_equal, assert_almost_equal

from vis.rescale import rescale_size, rescale_orbit

def test_rescale_size():
    assert_almost_equal( rescale_size(2.0, 3.0, 1.0), 2)
    assert_almost_equal( rescale_size(2.0, 3.0, 0.0), 3)

    assert_almost_equal( rescale_size(5.0, 3.0, 1.0), 5)
    assert_almost_equal( rescale_size(5.0, 3.0, 0.0), 3)

    assert_almost_equal( rescale_size(2, 3, 1), 2)
    assert_almost_equal( rescale_size(2, 3, 0), 3)
    
def test_rescale_size_realistic():    
    dp = array([1e6, 1.4e5, 1.2e4, 6.6e3, 3.4e3, 1e-1])
    dp1 = array([rescale_size(d, 1e5, 1) for d in dp])
    dp0 = array([rescale_size(d, 1e5, 0) for d in dp])
    assert_almost_equal(dp1, dp)
    assert_almost_equal(dp0, array(len(dp) * [1e5]))
    
def test_rescale_orbit():
    assert_almost_equal( rescale_orbit(2.0, 3.0, 1.5, 1.0, 1.0), 2)
    
    assert_almost_equal( rescale_orbit(2.0, 3.0, 1.5, 1.0, 0.0), 2)
    assert_almost_equal( rescale_orbit(2.0/1.5, 3.0, 1.5, 0.4, 0.0), 2.2)
    assert_almost_equal( rescale_orbit(2.0/1.5, 3.0, 1.5, 0.4, 1.0), 2.0/1.5)
    
    assert_almost_equal( rescale_size(2.0, 3.0, 0.0), 3)

def test_rescale_orbit_realistic():
    rp = array([0.39, 0.72, 1.0, 1.52, 2.77, 5.2, 9.54, 19.2, 30.06])
    assert_almost_equal(array([rescale_orbit(r, 10.0, 1.6, 1, 1.0) for r in rp]), rp)

