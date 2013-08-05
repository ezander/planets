# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:50:27 2013

@author: ezander
"""

from numpy import array
from odesim import SimObject

def floatvec(f):
    return array(f, dtype=float, ndmin=1)

class Stage(SimObject):
    def __init__(self, v_g, m_e, m_t, dmdt):
        self.v_g = v_g
        self.m_e = m_e
        self.m_t = floatvec(m_t)
        self.dmdt = dmdt
        self.active = False

    @property
    def dim(self):
        return 1
    
    @property
    def state(self):
        return self.m_t

    @state.setter
    def state(self, value):
        self.m_t = max(value, 0.0)
        
    def diff(self, t):
        if self.active and self.m_t>0:
            dydt = floatvec(-self.dmdt)
        else:
            dydt = floatvec(0.0)
            
        return dydt

class Rocket(SimObject):
    def __init__(self, v_0=0):
        self.stage = None
        self.v = floatvec(v_0)
        self.payload = 0
    
    def set_stage(self, stage, payload=None):
        self.stage = stage
        if payload is None:
            self.payload = stage.m_e
        else:
            self.payload = payload

    @property
    def dim(self):
        return len(self.v)
    
    @property
    def state(self):
        return self.v

    @state.setter
    def state(self, value):
        self.v = value
        
    def diff(self, t):
        from numpy.linalg import norm
        m_t = self.stage.m_t
        m = self.payload + m_t
        dmdt = self.stage.dmdt

        v = self.v
        if norm(v)==0:
            v = v + 1 # TODO: mean hack here if initial velocity is zero, should have an initial direction additionally
        vs = v / norm(v)
        v_g = self.stage.v_g
            
        if self.stage.active and self.stage.m_t>0:
            return floatvec(vs * v_g * dmdt / m)
        else:
            return floatvec(0.0 * vs)

class SimpleRocket(Rocket):
    def __init__(self, v_g, m_e, m_t, dmdt, v_0=0):
        Rocket.__init__(self, v_0)
        self.set_stage(Stage(v_g, m_e, m_t, dmdt))
        self.stage.active = True

    def on_add(self, simulator):
        simulator.add(self.stage)
        
class MultistageRocket(Rocket):
    def __init__(self, v_0=0):
        Rocket.__init__(self, v_0)
        self.stages = []

    def add(self, stage):
        self.stages = self.stages + [stage]
        self._init_stages()
        
    def add_stage(self, v_g, m_e, m_t, dmdt):
        self.add(Stage(v_g, m_e, m_t, dmdt))
        
    def on_add(self, simulator):
        for stage in self.stages:
            simulator.add(stage)
        
    def _init_stages(self):
        payload = sum(stage.m_e for stage in self.stages)
        payload += sum(stage.m_t for stage in self.stages[1:])
        self.set_stage(self.stages[0], payload)
        for stage in self.stages:
            stage.active = False
        self.stage.active = True


    def diff(self, t):
        dydt = Rocket.diff(self, t)
        if self.stage.m_t<=0 and len(self.stages)>1:
            self.stage.active = False
            self.stages = self.stages[1:]
            self._init_stages()
        return dydt


__all__ = [SimpleRocket.__name__, MultistageRocket.__name__]
