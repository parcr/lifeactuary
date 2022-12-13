import numpy as np
import scipy.integrate
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]


class Makeham:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def mu(self, x):
        if x < 0 or self.a < 0 or (self.b <= 0 or self.b >= 1) or self.c <= 1:
            return np.nan
        return self.a + self.b * np.power(self.c, x)

    def S(self, x, t):
        if x < 0 or self.a < 0 or (self.b <= 0 or self.b >= 1) or self.c <= 1:
            return np.nan
        if t < 0:
            return 1
        else:
            return np.exp(-self.b / np.log(self.c) * np.power(self.c, x) *
                          (np.power(self.c, t) - 1)) * np.exp(-self.a * t)

    def pdf(self, x, t):
        if x < 0 or self.a < 0 or (self.b <= 0 or self.b >= 1) or self.c <= 1:
            return np.nan
        if t < 0:
            return 1
        else:
            return (self.a + self.b * np.power(self.c, x + t)) * \
                   np.exp(-self.b / np.log(self.c) * np.power(self.c, x) *
                          (np.power(self.c, t) - 1)) * np.exp(-self.a * t)

    def moments_Tx(self, x=0, k=1):
        if x < 0 or k < 0:
            return np.nan
        if k == 0:
            return 1

        def t_S_x(t):
            return k * np.power(t, k - 1) * \
                   np.exp(-self.b / np.log(self.c) * np.power(self.c, x) * (np.power(self.c, t) - 1)) * \
                   np.exp(-self.a * t)

        ev = scipy.integrate.quad(t_S_x, 0, np.inf)
        return ev

    def expected_value_Tx(self, x=0):
        return self.moments_Tx(x=x, k=1)[0]

    def variance_Tx(self, x=0):
        ev = self.expected_value_Tx(x=x)
        ev_square = self.moments_Tx(x=x, k=2)[0]
        return ev_square - np.power(ev, 2)

    def ax(self, x=0, interest_rate=0, n=np.inf):
        '''
        Computes the continuous form of an annuity
        :param x: age
        :param interest_rate: interest rate
        :param n: periods of payment
        :return: the actuarial present value
        '''
        if x < 0:
            return np.nan

        def a_x(t, interest_rate=interest_rate / 100):
            v = 1 / (1 + interest_rate)
            return np.power(v, t) * \
                   np.exp(-self.b / np.log(self.c) * np.power(self.c, x) * (np.power(self.c, t) - 1)) * \
                   np.exp(-self.a * t)

        ev = scipy.integrate.quad(a_x, 0, n)
        return ev

    def Ax(self, x=0, interest_rate=0, n=np.inf):
        '''
        Computes the expected present value for a life insurance that pays at the moment of death
        :param x:
        :param interest_rate:
        :param n:
        :return:
        '''
        delta = np.log(1 + interest_rate / 100)
        ax = self.ax(x=x, interest_rate=interest_rate, n=n)
        nEx = self.nEx(x=x, interest_rate=interest_rate, defer=n)
        return 1 - delta * ax[0] - nEx

    def Endowment(self, x=0, interest_rate=0, n=np.inf):
        nEx = self.nEx(x=x, interest_rate=interest_rate, defer=n)
        return self.Ax(x=x, interest_rate=interest_rate, n=n) + nEx

    def nEx(self, x=0, interest_rate=0, defer=0):
        v = 1 / (1 + interest_rate / 100)
        return np.power(v, defer) * self.S(x=x, t=defer)

    def annuity(self, x=0, interest_rate=0, age_first_instalment=0, terms=np.inf, fraction=1, w=130):
        # v_m = np.power(1 / (1 + interest_rate / 100), 1 / fraction)
        v = 1 / (1 + interest_rate / 100)
        defer = age_first_instalment - x
        # nEx = np.power(v, defer) * self.S(x=x, t=defer)
        nEx = self.nEx(x=x, interest_rate=interest_rate, defer=defer)
        start = 0
        stop = min(w - age_first_instalment, terms)
        num = min(round((stop - start) * fraction + 1), terms * fraction)

        if terms == np.inf:
            # ts = np.arange(0, w - age_first_instalment + 1 / fraction, 1 / fraction)
            ts = np.linspace(start=start, stop=stop, num=num)
        else:
            # ts = np.arange(0, min(w - age_first_instalment, terms), 1 / fraction)
            ts = np.linspace(start=start, stop=stop - 1 / fraction, num=num)
        epv_ai = [self.S(x=age_first_instalment, t=u) * v ** u for u in ts]
        return sum(epv_ai) * nEx / fraction

    def life_insurance(self, x=0, interest_rate=0, age_first_instalment=0, terms=np.inf, fraction=1, w=130):
        def tqx(x, t):
            if x + t >= w + 1:
                return 1
            return 1 - self.S(x=x, t=t)

        def tpx(x, t):
            return 1 - tqx(x, t)

        v = 1 / (1 + interest_rate / 100)
        defer = age_first_instalment - x
        nEx = self.nEx(x=x, interest_rate=interest_rate, defer=defer)
        start = 0
        stop = min(w - age_first_instalment + 1, terms)
        num = min(round((stop - start) * fraction + 1), terms * fraction)

        if terms == np.inf:
            ts = np.linspace(start=start, stop=stop, num=num)
        else:
            ts = np.linspace(start=start, stop=stop - 1 / fraction, num=num)
        px = [tpx(x=age_first_instalment, t=u) for u in ts]
        qx = [tqx(x=age_first_instalment + u, t=1 / fraction) for u in ts]
        vx = [v ** (u + 1 / fraction) for u in ts]
        epv_li = [px[u] * qx[u] * vx[u] for u in range(len(ts))]

        return sum(epv_li) * nEx
