#!/usr/bin/env python3
"""Exact dyadic controls and separate numerical checks for the illustrative disk."""
from fractions import Fraction
from math import acos, cos, pi, sin, sqrt, isclose


def dyad(exponent):
    return Fraction(2) ** exponent


def check_exact():
    for ell in range(32):
        for m in (2**ell, 2**(ell+1)-1):
            # Use the worst zero comparison j_m <= D m on the block.
            radius = Fraction(1, 2) / (5 * 2**(ell+1))
            assert radius * 5 * m <= Fraction(1,2)
        for k in range(32):
            # Square the normalized contribution relative to A_k and
            # suppress the fixed comparison constants from the paper.
            prefactor_squared = dyad(ell-k)
            inverse_square_squared = dyad(-4*max(ell-k,0))
            expected = dyad(-(k-ell)) if k >= ell else dyad(-3*(ell-k))
            assert prefactor_squared * inverse_square_squared == expected
    assert Fraction(31,32)**2 > Fraction(1,2)
    print("PASS: 1024 exact squared dyadic weights, 64 endpoint checks, and disk multiplier floor.")


def simpson(f, stop, panels):
    step = stop/panels
    return step/3*(f(0)+f(stop)+sum((4 if k%2 else 2)*f(k*step)
                                    for k in range(1,panels)))


def overlap(relative_radius):
    return 2/pi*(acos(relative_radius)
                 - relative_radius*sqrt(1-relative_radius**2))


def multiplier(argument):
    value = 4/pi*simpson(lambda theta: cos(argument/2*sin(theta))*cos(theta)**2,
                        pi/2, 256)
    return value**2


def series_multiplier(argument):
    """Independent J1 power series for the finite plotted range."""
    z = argument/2
    term = value = 1.
    for k in range(1,64):
        term *= -z*z/(4*k*(k+1))
        value += term
    return value**2


def check_illustration():
    assert isclose(simpson(lambda x: 8*x*overlap(x), 1., 2048),
                   1., abs_tol=2e-8)
    for n in range(97):
        s = n/4
        assert isclose(multiplier(s),series_multiplier(s),abs_tol=2e-11)
        assert 0 <= multiplier(s) <= 1 + 1e-14
        if s <= .5:
            assert multiplier(s) >= (31/32)**2
    print("PASS: numerical unit radial mass and 97 disk-transform agreement checks.")


if __name__ == "__main__":
    check_exact()
    check_illustration()
