# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 11:30:00 2013

@author: ezander
"""

from numpy import array
from numpy.testing import assert_approx_equal, assert_almost_equal

from vis.rescale import rescale_size

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
    

    

    
    
    