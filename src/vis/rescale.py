from numpy import log

def rescale_size(d, d0, f):
    # 1 realistic, 0 all same
    d0 = float(d0)
    return d0 * (d/d0)**f
    
def rescale_size_factor(d, d0, f):
    return rescale_size(d, d0, f) / d



def rescale_orbit(r, r0, sr, dr, f):
    #a=dr/log(sr)
    #b=r0-a*log(r0)
    #rn = a*log(r) + b
    if r==0:
        return 0
    rn = dr*log(r/r0)/log(sr) + r0
    if r<r0:
        rn = max(r, rn)
    return r**(f) * rn**(1-f)

def rescale_orbit_factor(r, f):
    if r == 0:
        return 1
    return rescale_orbit(r, f) / r
