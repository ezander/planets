from numpy import log

from sim.physics import Units

def rescale_size(d, d0, f):
    # 1 realistic, 0 all same
    d0 = float(d0)
    return d0 * (d/d0)**f
    
def rescale_size_factor(d, d0, f):
    return rescale_size(d, d0, f) / d



def rescale_orbit(r, f):
    # 1 realistic, 0 linearly spaced
    r = r / Units.AU
    if r<=0.4:
        return r * Units.AU
    n = log((r-0.4)/0.3)/log(2.0)
    return (1/(3.0*f)-f/30.0)*(7.0/3*f-1+(1+f)**n) * Units.AU


def rescale_orbit_factor(r, f):
    if r == 0:
        return 1
    return rescale_orbit(r, f) / r

#rp = [0.5, 0.72, 1.0, 1.52, 2.77, 5.2, 9.54]
#print rp
#print [rescale_orbit(r,1) for r in rp]
#rint [rescale_orbit(r,0.0001) for r in rp]
