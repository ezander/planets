# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 22:33:34 2013

@author: ezander
"""
from numpy.linalg import norm

class Units(object):
    m = 1.0
    km = 1000 * m
    AU=149597870.691 * km

    s = 1.0
    h = 3600 * s
    d = 24 * h
    
    kg = 1

class Constants(Units):
    G = 6.6738480E-11 * Units.m**3 * Units.kg / Units.s**2
    
def gravitational_accel(r, r2, m2):
    dr = r2 - r
    ndr = norm(dr)
    return Constants.G * m2 * dr / ndr**3
