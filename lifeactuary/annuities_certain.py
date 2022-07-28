import numpy as np


class Annuities_Certain:
    '''

    '''

    def __new__(cls, interest_rate, m):
        if interest_rate < 0 or m < 0 or int(m) != m:
            print(f"We need a rate of interest non negative and a positive integer frequency")
            return None
        return object.__new__(cls)

    def __init__(self, interest_rate, m=1):
        '''

        :param interest_rate:
        :param m:
        '''

        self.interest_rate = interest_rate / 100.
        self.frequency = m

        self.v = 1 / (1 + self.interest_rate)
        self.im = self.frequency * (np.power(1 + self.interest_rate, 1 / self.frequency) - 1)
        self.vm = np.power((1 + self.im / self.frequency), -1)
        self.dm = self.im * self.vm

    def check_terms(func):
        def func_wrapper(self, terms, *args, **kwargs):
            if not terms:
                terms = 0
            if terms < 0 or int(terms) != terms:
                return np.nan
            res = func(self, terms, *args, **kwargs)
            return res

        return func_wrapper

    def check_grow(func):
        def func_wrapper(self, terms, payment, grow):
            if grow / 100 <= -1 or terms < 0 or int(terms) != terms:
                return np.nan
            res = func(self, terms, payment, grow)
            return res

        return func_wrapper

    @check_terms
    def aan(self, terms):
        '''

        :param terms:
        :return:
        '''
        if not terms:
            return 1 / self.dm
        return (1 - np.power(self.vm, terms * self.frequency)) / self.dm

    @check_terms
    def an(self, terms):
        '''

        :param terms:
        :return:
        '''
        if not terms:
            return 1 / self.im
        return (1 - np.power(self.vm, terms * self.frequency)) / self.im

    @check_terms
    def Imaan(self, terms, payment=1, increase=1):
        '''

        :param terms:
        :param payment:
        :param increase:
        :return:
        '''
        return self.Iman(terms, payment, increase) / self.vm

    @check_terms
    def Iman(self, terms, payment=1, increase=1):
        '''

        :param terms:
        :param payment:
        :param increase:
        :return:
        '''
        if payment + increase * terms < 0:
            return np.nan

        return (payment - increase) * self.an(terms) \
               + increase * self.v \
               * (self.v ** terms * ((terms * self.frequency) * (self.vm - 1) - 1) + 1) \
               / (self.frequency * self.v ** ((self.frequency - 1) / self.frequency) * (self.vm - 1) ** 2)

    @check_terms
    def Iaan(self, terms, payment=1, increase=1):
        '''

        :param terms:
        :param payment:
        :param increase:
        :return:
        '''
        return self.Ian(terms, payment, increase) / self.vm

    @check_terms
    def Ian(self, terms, payment=1, increase=1):
        '''

        :param terms:
        :param payment:
        :param increase:
        :return:
        '''
        if payment + increase * terms < 0:
            return np.nan
        # (payment - increase) * self.an(terms) + increase * (self.aan(terms) - terms * self.v ** terms) / self.im
        return payment * self.an(terms) + increase / self.im * (
                (1 - self.v ** terms) / self.interest_rate - terms * self.v ** terms)

    @check_grow
    def Gaan(self, terms, payment=1, grow=0):
        '''

        :param terms:
        :param payment:
        :param grow:
        :return:
        '''
        v = (1 + grow / 100) * self.v
        return self.Gan(terms, payment, grow) / v ** (1 / self.frequency)

    @check_grow
    def Gan(self, terms, payment=1, grow=0):
        '''

        :param terms:
        :param payment:
        :param grow:
        :return:
        '''
        v = (1 + grow / 100) * self.v
        if self.interest_rate == grow / 100:
            return payment * terms * self.frequency * self.vm / self.frequency
        return payment / (1 + grow / 100) ** (1 / self.frequency) * (1 - v ** terms) / \
               (1 - v ** (1 / self.frequency)) * v ** (1 / self.frequency) / self.frequency

    @check_grow
    def Gmaan(self, terms, payment=1, grow=0):
        '''

        :param terms:
        :param payment:
        :param grow:
        :return:
        '''
        v = (1 + grow / 100) * self.v
        return self.Gman(terms, payment, grow) / v ** (1 / self.frequency)

    @check_grow
    def Gman(self, terms, payment=1, grow=0):
        '''

        :param terms:
        :param payment:
        :param grow:
        :return:
        '''
        a1 = (1 - self.v) / self.im
        if self.interest_rate == grow / 100:
            return a1 * terms
        ig = (self.interest_rate - grow / 100) / (1 + grow / 100)
        vg = 1 / (1 + ig)
        a2 = (1 - vg ** terms) / (1 - vg)
        return payment * a1 * a2
