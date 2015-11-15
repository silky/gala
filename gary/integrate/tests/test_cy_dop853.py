# coding: utf-8
"""
    Test the integrators.
"""

from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os
import time

# Third-party
import numpy as np
import matplotlib.pyplot as plt

# Project
from ... import potential as gp
from ... import integrate as gi
from ... import dynamics as gd
from ..dopri853 import DOPRI853Integrator
from ...units import galactic
from .._dop853 import dop853_integrate_potential, dop853_lyapunov

def test_derp():
    pot = gp.HernquistPotential(m=1E11, c=0.5, units=galactic)
    w0 = np.array([1.,2.1,0., 0.,0.5,0.])
    t = np.linspace(0., -5., 32)

    t,w = pot.integrate_orbit(w0, dt=t[1]-t[0], nsteps=len(t),
                              Integrator=DOPRI853Integrator,
                              cython_if_possible=False)
    print("Python integration done.")

    t,w = dop853_integrate_potential(pot.c_instance, np.ascontiguousarray(w0[None]),
                                     t, 1E-8, 1E-8, 0)
    print("Cython integration done.")

    print(t[1]-t[0], 0., t.min())
    t,w = pot.integrate_orbit(w0, dt=t[1]-t[0], t1=0., t2=t.min(),
                              Integrator=DOPRI853Integrator,
                              cython_if_possible=True)
    print("Cython integration2 done.")

    return

    from scipy.optimize import leastsq

    def errfunc(p, x, y):
        return y - (p[0]*x + p[1])
    p_opt,ier = leastsq(errfunc, x0=[0.1,0.], args=(norbitses, times))
    print(p_opt)

    plt.plot(norbitses, times)
    plt.plot(norbitses, pytimes)
    derp = np.linspace(norbitses.min(),norbitses.max(),100)
    plt.plot(derp, p_opt[0]*derp + p_opt[1], marker=None)
    plt.show()

    # plt.figure(figsize=(8,8))
    # plt.plot(w[:,0],w[:,1],marker=None)
    # plt.show()

# def test_lyapunov():
#     pot = gp.HernquistPotential(m=1E11, c=0.5, units=galactic)
#     w0 = np.array([5.,0.,0., 0.,0.2,0.])
#     nsteps = 100000

#     # with python
#     # F = lambda t,w: np.hstack((w[...,3:],pot.acceleration(w[...,:3])))
#     # integrator = gi.DOPRI853Integrator(F)
#     # regular_LEs, t, regular_ws = gd.lyapunov_max(w0, integrator, dt=0.1, nsteps=nsteps)
#     # plt.loglog(regular_LEs[:,0], marker=None)

#     print()

#     t,w,l = dop853_lyapunov(pot.c_instance, w0,
#                             0.1, nsteps, 0., 1E-8, 1E-8,
#                             1E-5, 10, 8)

#     # plt.plot(w[:,0], w[:,1], marker=None)
#     plt.loglog(l, marker=None)
#     plt.show()
