__author__ = "PedroCR"

import numpy as np
import logging
from lifeActuary.mortality_table import MortalityTable


class MortalityTable2Heads:
    """
    Instantiates a mortality table for 2 heads, considering survival independence.
    """

    def __new__(cls, mt_old, mt_young, age_dif, status):
        all_status = {'joint-life', 'last-survivor'}
        bool_mt_old = isinstance(mt_old, MortalityTable)
        bool_mt_young = isinstance(mt_young, MortalityTable)
        bool_status = False
        if status in all_status:
            bool_status = True
        if bool_mt_old and bool_mt_young and bool_status:
            return object.__new__(cls)
        else:
            logging.warning(f'We need two instances of mortality tables and a possible status; {all_status}.')
            return None

    def __init__(self, mt_old, mt_young, age_dif=0, status='joint-life'):
        self.__mt_old = mt_old
        self.__mt_young = mt_young
        self.__age_dif = age_dif
        self.__status = status

        self.__mt_2heads = self.__create_mortality_table_2heads__()

    def __repr__(self):
        return f"{self.__class__.__name__}{self.mt_old, self.mt_young, self.age_dif, self.status}"

    @property
    def mt_old(self):
        return self.__mt_old

    @property
    def mt_young(self):
        return self.__mt_young

    @property
    def age_dif(self):
        return self.__age_dif

    @property
    def status(self):
        return self.__status

    @property
    def mt_2heads(self):
        return self.__mt_2heads

    # create the mortality table for the 2 heads
    def __create_mortality_table_2heads__(self):
        l0 = max(self.mt_old.lx[0], self.mt_young.lx[0])
        if self.status == 'joint-life':
            w = min(self.mt_old.w - self.age_dif, self.mt_young.w)
            qx = [1 - self.mt_old.npx(x=x + self.age_dif, n=1) * self.mt_young.npx(x=x, n=1)
                  for x in range(w + 1)]
        if self.status == 'last-survivor':
            w = max(self.mt_old.w - self.age_dif, self.mt_young.w)
            qx = [self.mt_old.nqx(x=x + self.age_dif, n=1) * self.mt_young.nqx(x=x, n=1)
                  for x in range(w + 1)]
        qx.insert(0, 0)  # appends the minimum age in the table
        return MortalityTable(mt=qx)

    # Probabilities
    def nqxy(self, x_young, x_old, n=1, method='udd'):
        """

        :param x_young:
        :param x_old:
        :param n:
        :param method:
        :return:
        """
        if x_young > x_old:
            return np.nan
        if self.status == 'joint-life':
            return 1 - self.mt_young.npx(x_young, n, method) * self.mt_old.npx(x_old, n, method)
        if self.status == 'last-survivor':
            return self.mt_young.nqx(x_young, n, method) * self.mt_old.nqx(x_old, n, method)

    def npxy(self, x_young, x_old, n=1, method='udd'):
        """

        :param x_young:
        :param x_old:
        :param n:
        :param method:
        :return:
        """
        if x_young > x_old:
            return np.nan
        if self.status == 'joint-life':
            return self.mt_young.npx(x_young, n, method) * self.mt_old.npx(x_old, n, method)
        if self.status == 'last-survivor':
            return 1 - self.mt_young.nqx(x_young, n, method) * self.mt_old.nqx(x_old, n, method)

    def t_nqxy(self, x_young, x_old, t=1, n=1, method='udd'):
        """

        :param x_young:
        :param x_old:
        :param t:
        :param n:
        :param method:
        :return:
        """
        if x_young > x_old:
            return np.nan
        return self.nqxy(x_young, x_old, t + n, method) - self.nqxy(x_young, x_old, t, method)

    # Benefits
    ## Annuities

    def annuity(self, x_young, x_first_payment, x_last_payment, i, g=0, m=1, method='udd'):
        """

        :param x_young:
        :param x_first_payment:
        :param x_last_payment:
        :param i:
        :param g:
        :param m:
        :param method:
        :return:
        """
        if x_young > self.mt_2heads.w or x_young > x_first_payment:
            return .0
        if x_young > self.mt_2heads.w + 1:
            return .0
        if int(m) != m:
            return np.nan
        v = 1 / (1 + i / 100)
        vg = (1 + g / 100) * v
        if x_last_payment > self.mt_2heads.w + 1:
            x_last_payment = self.mt_2heads.w + 1
        number_of_payments = int((x_last_payment - x_first_payment) * m) + 1
        x_lp = x_first_payment + (number_of_payments - 1) / m
        payments_instants = np.linspace(x_first_payment - x_young, x_lp - x_young, number_of_payments)
        terms = [self.npxy(x_young, x_young + self.age_dif, t, method) * vg ** t for t in payments_instants]
        return np.sum(terms) / (1 + g / 100) ** (x_first_payment - x_young) / m


    def naaxy(self, x, y, n, i, g, m):
        pass