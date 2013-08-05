def rescale(d, d0, f):
    return d0 * (d/d0)*f
dp = [1e6, 1.4e5, 1.2e4, 6.6e3, 3.4e3, 1e-1]
[rescale(d, 1e5, 1) for d in dp]
dp
[rescale(d, 1e5, 0) for d in dp]
def rescale(d, d0, f):
    return d0 * (d/d0)**f
[rescale(d, 1e5, 1) for d in dp]
[rescale(d, 1e5, 0) for d in dp]
[rescale(d, 1e5, 0.9) for d in dp]
[rescale(d, 1e5, 0.5) for d in dp]
[rescale(d, 1e5, 0.4) for d in dp]
[rescale(d, 1e5, 0.3) for d in dp]
[rescale(d, 1e5, 0.2) for d in dp]
[rescale(d, 1e5, 0.1) for d in dp]
def pn(a):
    return log((a-0.4)/0.3)/log(2.0)
from math import log
ap = [0.39, 0.72, 1.0, 1.52, 2.77, 5.2, 9.54]
ap
np = [pn(a) for a in ap]
ap = [0.5, 0.72, 1.0, 1.52, 2.77, 5.2, 9.54]
np = [pn(a) for a in ap]
np
def aneu(n, x):
    return (1/(3.0*x)-x/30.0)*(7.0/3*x-1+(1+x)**n)
[aneu(n,1) for n in np]
[aneu(n,0.5) for n in np]
[aneu(n,0.3) for n in np]
[aneu(n,0.1) for n in np]
[aneu(n,0.0) for n in np]
[aneu(n,0.0001) for n in np]
