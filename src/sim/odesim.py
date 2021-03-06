# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:50:27 2013

@author: ezander
"""

from scipy.integrate import ode

from abc import ABCMeta, abstractmethod, abstractproperty
from numpy import array

def floatvec(f):
    return array(f, dtype=float, ndmin=1)

class SimObject(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def dim(self):
        pass
    
    @abstractproperty
    def state(self):
        pass
    
    @abstractmethod
    def diff(self, t):
        pass
    
    def on_add(self, simulator):
        pass

class OdeSimulator(object):
    def __init__(self, integrator='vode', ode_kwargs={}):
        self.objects = []
        self.n1 = []
        self.n2 = []
        self.dim = 0
        
        self.y = floatvec([]);
        self.t = 0
        
        self.myode = ode(self.diff)
        self.myode = self.myode.set_integrator(integrator, **ode_kwargs)

    def add(self, simobj):
        self.objects += [simobj]
        self.n1 += [self.dim]
        self.dim += simobj.dim
        self.n2 += [self.dim]
        self.myode.set_initial_value([], self.t)
        self.y.resize(self.dim)
        self.y[self.n1[-1]:self.n2[-1]] = simobj.state
        simobj.on_add(self)
        self.myode.set_initial_value(self.y, self.t)
        
    def integrate(self, t):
        #self.myode.set_initial_value(self.y, self.t)
        self.myode.integrate(t)
        self.t, self.y = self.myode.t, self.myode.y
        self._copy_state2objects(self.y)

    def _copy_state2objects(self, y):
        for n1, n2, simobj in zip(self.n1, self.n2, self.objects):
            simobj.state = y[n1:n2]
    
    def diff(self, t, y):
        self._copy_state2objects(y)
        
        dydt = y * 0
        for n1, n2, simobj in zip(self.n1, self.n2, self.objects):
            dydt[n1:n2] = simobj.diff(t)

        return dydt

__all__ = [SimObject.__name__,
           OdeSimulator.__name__]
