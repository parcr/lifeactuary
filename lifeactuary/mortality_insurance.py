__author__ = "PedroCR"

import numpy as np
from lifeActuary import annuities


def A_x(mt, x, x_first, x_last, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value (EPV) of a Life Insurance that pays 1 at the end of the year of death.
    :param mt: mortality table for life x
    :param x: age at the beginning of the contract
    :param x_first: age of first payment
    :param x_last: age of final payment
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV)
    """
    if x_first < x: return np.nan
    if x_last < x_first == x: return np.nan
    if x == x_first == x_last: return 0
    i = i / 100
    g = g / 100
    v = float((1 + g) / (1 + i))
    number_of_payments = int((x_last - x_first) + 1)
    if number_of_payments < 1: return .0  # according to the mortality table x is going to die before x+1
    payments_instants = np.linspace(x_first - x, x_last - x, number_of_payments)
    instalments = [mt.npx(x, n=t - 1, method=method) * mt.nqx(x + t - 1, n=1, method=method) * np.power(v, t)
                   for t in payments_instants]
    instalments = np.array(instalments) / np.power(1 + g, payments_instants[0])
    return np.sum(instalments)


def Ax(mt, x, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value (EPV) of a Whole Life Insurance that pays 1 at the end of the year of death.
    :param mt: mortality table for life x
    :param x: age at the beginning of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Whole Life Insurance (end of the year of death)
    """

    if x > mt.w:
        return np.power(1 + i / 100, -1)  # it will die before year's end, because already attained age>w
    return A_x(mt=mt, x=x, x_first=x + 1, x_last=mt.w + 1, i=i, g=g, method=method)


def Ax_(mt, x, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value (EPV) of a Whole Life Insurance that pays 1 at the moment of death.
    :param mt: mortality table for life x
    :param x: age at the beginning of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Whole Life Insurance (moment of death)
    """
    if x > mt.w:
        return np.power(1 + i / 100, -.5)
    return Ax(mt=mt, x=x, i=i, g=g, method=method) * np.sqrt(1 + i / 100)


def t_Ax(mt, x, defer=0, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value of a deferred whole life insurance, that pays 1 at the end of year of death.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Deferred Whole Life Insurance (end of year of death)
    """

    return A_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=mt.w + 1, i=i, g=g, method=method)


def t_Ax_(mt, x, defer=0, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value of a deferred whole life insurance, that pays 1 at the moment of death.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Deferred Whole Life Insurance (moment of death)
    """
    return t_Ax(mt=mt, x=x, defer=defer, i=i, g=g, method=method) * np.sqrt(1 + i / 100)


# Term Life Insurance

def nAx(mt, x, n, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value of a term life insurance, that pays 1, at the end of the year of death.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional ages and periods (udd, cfm, bal)

    :return: Term life insurance (end of year of death)
    """
    if x > mt.w:
        return np.power(1 + i / 100, -1)
    return A_x(mt=mt, x=x, x_first=x + 1, x_last=x + n, i=i, g=g, method=method)


def nAx_(mt, x, n, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value of a term life insurance, that pays 1, at the end of the year of death.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional ages and periods (udd, cfm, bal)

    :return: Term life insurance (moment of death)
    """
    if x > mt.w:
        return np.power(1 + i / 100, -.5)
    return nAx(mt=mt, x=x, n=n, i=i, g=g, method=method) * np.sqrt(1 + i / 100)


def t_nAx(mt, x, n, defer=0, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value of a deferred term life insurance, that pays 1, at the end of the year of death.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods

    :return: Deferred Term Life Insurance (end of year of death).
    """
    return A_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, g=g, method=method)


def t_nAx_(mt, x, n, defer=0, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value of a deferred term life insurance, that pays 1, at the moment of death.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods

    :return: Deferred Term Life Insurance (moment of death).
    """
    return t_nAx(mt=mt, x=x, n=n, defer=defer, i=i, g=g, method=method) * np.sqrt(1 + i / 100)


# Endowment Insurance

def nAEx(mt, x, n, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value of an Endowment life insurance, that pays 1, at the end of year of death
    or 1 if (x) survives to age x+n.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional ages and periods (udd, cfm, bal)

    :return: Endowment insurance (end of year of death)
    """
    return nAx(mt=mt, x=x, n=n, i=i, g=g, method=method) + annuities.nEx(mt=mt, x=x, i=i, g=g, n=n, method=method)


def nAEx_(mt, x, n, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value of an Endowment life insurance, that pays 1, at the moment of death
    or 1 if (x) survives to age x+n.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional ages and periods (udd, cfm, bal)

    :return: Endowment insurance (moment of death)
    """
    return nAx_(mt=mt, x=x, n=n, i=i, g=g, method=method) + annuities.nEx(mt=mt, x=x, i=i, g=g, n=n, method=method)


def t_nAEx(mt, x, n, defer=0, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value of a deferred Endowment life insurance that pays 1
    at the end of year of death or 1 if (x) survives to age x+t+n.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional ages and periods (udd, cfm, bal)

    :return: Deferred Endowment insurance (end of the year of death)
    """
    return A_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, g=g, method=method) + \
        annuities.nEx(mt=mt, x=x, i=i, g=g, n=n + defer, method=method)


def t_nAEx_(mt, x, n, defer=0, i=None, g=.0, method='udd'):
    """
    Returns the Expected Present Value of a deferred Endowment life insurance that pays 1
    at the moment of death or 1 if (x) survives to age x+t+n.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional ages and periods (udd, cfm, bal)

    :return: Deferred Endowment insurance (moment of death)
    """
    return A_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, g=g, method=method) * np.sqrt(
        1 + i / 100) + \
        annuities.nEx(mt=mt, x=x, i=i, g=g, n=n + defer, method=method)


# Life Insurance with linear increment


def IA_x(mt, x, x_first, x_last, i=None, first=1., inc=1., method='udd'):
    """
    Returns the Expected Present Value of a Term Life Insurance , that pays 1+k, at the end of year, if
    death occurs between ages x+k and x+k+1, for k=0, 1, ...
    The capital of the first year equals the rate of the progression.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param x_first: age of first payment
    :param x_last: age of final payment
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param first: amount of the first payment
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)
    :return: Life Insurance with Linear Increment
    """
    if x_first < x: return np.nan
    if x_last < x_first == x: return np.nan
    if x == x_first == x_last: return 0
    if first + (x_last - x_first) * inc < 0: return np.nan
    i = i / 100
    i = float(1 / (1 + i))
    number_of_payments = int((x_last - x_first) + 1)
    if number_of_payments < 1: return 1.  # according to the mortality table x is going to die before x+1
    payments_instants = np.linspace(x_first - x, x_last - x, number_of_payments)
    pppp=[((t - (x_first - x)) * inc + first) for t in payments_instants]


    instalments = [mt.npx(x, n=t - 1, method=method) * mt.nqx(x + t - 1, n=1, method=method) * np.power(i, t) *
                   ((t - (x_first - x)) * inc + first) for t in payments_instants]
    instalments = np.array(instalments)
    return np.sum(instalments)

# Whole LIfe

def IAx(mt, x, i=None, inc=1., method='udd'):
    """
    Returns the Expected Present Value of a Whole Life Insurance , that pays 1+k, at the end of year of death, if
    death occurs between ages x+k and x+k+1, for k=0, 1,...
    The capital of the first year equals the rate of the progression.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Whole Life Insurance with Linear Increment (end of year of death)
    """

    return IA_x(mt=mt, x=x, x_first=x + 1, x_last=mt.w + 1, i=i, first=inc, inc=inc, method=method)


def IAx_(mt, x, i=None, inc=1., method='udd'):
    """
    Returns the Expected Present Value of a Whole Life Insurance , that pays 1+k, at the moment of death, if
    death occurs between ages x+k and x+k+1, for k=0, 1,...
    The capital of the first year equals the rate of the progression.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Whole Life Insurance with Linear Increment (moment of death)
    """

    return IAx(mt=mt, x=x, i=i, inc=inc, method=method) * np.sqrt(1 + i / 100)


def t_IAx(mt, x, defer=0, i=None, inc=1., method='udd'):
    """
    Returns the Expected Present Value of a Whole Life Insurance , that pays 1+k, at the end of year of death, if
    death occurs between ages x+k and x+k+1, for k=0, 1,...
    The capital of the first year equals the rate of the progression.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages and periods (udd, cfm, bal)

    :return: Deferred Whole Life Insurance with Linear Increment (end of year of death)
    """

    return IA_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=mt.w + 1, i=i, first=inc, inc=inc, method=method)


def t_IAx_(mt, x, defer=0, i=None, inc=1., method='udd'):
    """
    Returns the Expected Present Value of a Whole Life Insurance , that pays 1+k, at the moment of death, if
    death occurs between ages x+k and x+k+1, for k=0, 1,...
    The capital of the first year equals the rate of the progression.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages and periods (udd, cfm, bal)

    :return: Deferred Whole Life Insurance with Linear Increment (moment of death)
    """

    return t_IAx(mt=mt, x=x, defer=defer, i=i, inc=inc, method=method) * np.sqrt(1 + i / 100)

# Term Life

def nIAx(mt, x, n, i=None, inc=1., method='udd'):
    """
    Returns the Expected Present Value of a Term Life Insurance , that pays 1+k, at the end of year of death, if
    death occurs between ages x+k and x+k+1, for k=0, 1,..., n-1
    The capital of the first year equals the rate of the progression.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Term Life Insurance with Linear Increment (end of year of death)
    """

    return IA_x(mt=mt, x=x, x_first=x + 1, x_last=x + n, i=i, first=inc, inc=inc, method=method)


def nIAx_(mt, x, n, i=None, inc=1., method='udd'):
    """
    Returns the Expected Present Value of a Term Life Insurance , that pays 1+k, at the moment of death, if
    death occurs between ages x+k and x+k+1, for k=0, 1,..., n-1
    The capital of the first year equals the rate of the progression.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Term Life Insurance with Linear Increment (moment of death)
    """

    return nIAx(mt=mt, x=x, n=n, i=i, inc=inc, method=method) * np.sqrt(1 + i / 100)



def t_nIAx(mt, x, n, defer=0, i=None, inc=1., method='udd'):
    """
    Returns the Expected Present Value of a Term Life Insurance , that pays 1+k, at the end of the year of death, if
    death occurs between ages x+k and x+k+1, for k=0, 1,..., n-1
    The capital of the first year equals the rate of the progression.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param defer: deferment periods
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Deferred Term Life Insurance with Linear Increment (end of the year of death)
    """
    return IA_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, first=inc, inc=inc, method=method)


def t_nIAx_(mt, x, n, defer=0, i=None, inc=1., method='udd'):
    """
    Returns the Expected Present Value of a Term Life Insurance , that pays 1+k, at the moment of death, if
    death occurs between ages x+k and x+k+1, for k=0, 1,..., n-1
    The capital of the first year equals the rate of the progression.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param defer: deferment periods
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Deferred Term Life Insurance with Linear Increment (moment of death)
    """
    return t_nIAx(mt=mt, x=x, n=n, defer=defer, i=i, inc=inc, method=method) * np.sqrt(1 + i / 100)



# First Capital different from Increase Rate
def t_nIArx(mt, x, n, defer=0, i=None, first_amount=1, inc=1, method='udd'):
    """
    Returns the Expected Present Value term life insurance that pays first_amount + k * increase_amount,
    at the end of the year of death, if death occurs between ages x+defer+k and x+k+defer+1,
    for k=0,..., n-1.
    Allows the computation for decreasing capitals.
    The first capital may differ from the increasing/decreasing amount.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param defer: deferment periods
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param first_amount: insured amount in the first year of the contract
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Term Life Insurance with Linear Increment (emd of the year of death)
    """
    return IA_x(mt, x=x, x_first=x + 1 + defer, x_last=x + defer + n, i=i, first=first_amount, inc=inc, method=method)


def t_nIArx_(mt, x, n, defer=0, i=None, first_amount=1, inc=1, method='udd'):
    """
    Returns the Expected Present Value term life insurance that pays first_amount + k * increase_amount,
    at the moment of the year of death, if death occurs between ages x+defer+k and x+k+defer+1,
    for k=0,..., n-1.
    Allows the computation for decreasing capitals.
    The first capital may differ from the increasing/decreasing amount.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param defer: deferment periods
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param first_amount: insured amount in the first year of the contract
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Term Life Insurance with Linear Increment (moment of death)
    """
    return IA_x(mt, x, x_first=x + 1 + defer, x_last=x + defer + n, i=i, first=first_amount, inc=inc, method=method) * \
        np.sqrt(1 + i / 100)


# Endowment Life Insurance with linear increment

def nIAErx(mt, x, n, i=None, first_amount=1, inc=1, method='udd'):
    """
    Returns the Expected Present Value of an Endowment Life Insurance that pays
    (first_amount + k*increase_amount), at the end of the year of death,
    if death happens between ages x+k and x+k+1, for k=0,..., n-1 and a capital of
    first_amount + (n-1)*increase_amount in case of life at the end of the contract.
    Allows the computation for decreasing capitals.
    The first capital may differ from the increasing/decreasing amount.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param first_amount: insured amount in the first year of the contract
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Endowment Life Insurance with Linear Increment (emd of the year of death)
    """
    return t_nIArx(mt=mt, x=x, n=n, defer=0, i=i, first_amount=first_amount, inc=inc, method=method) + \
        annuities.nEx(mt=mt, x=x, i=i, g=0, n=n, method=method)*(first_amount+inc*(n-1))


def nIAErx_(mt, x, n, i=None, first_amount=1, inc=1, method='udd'):
    """
    Returns the Expected Present Value of an Endowment Life Insurance that pays
    (first_amount + k*increase_amount), at the moment of death,
    if death happens between ages x+k and x+k+1, for k=0,..., n-1 and a capital of
    first_amount + (n-1)*increase_amount in case of life at the end of the contract.
    Allows the computation for decreasing capitals.
    The first capital may differ from the increasing/decreasing amount.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param first_amount: insured amount in the first year of the contract
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Endowment Life Insurance with Linear Increment (moment of death)
    """
    return t_nIArx(mt=mt, x=x, n=n, defer=0, i=i, first_amount=first_amount, inc=inc, method=method)\
        * np.sqrt(1 + i / 100) + \
        annuities.nEx(mt=mt, x=x, i=i, g=0, n=n, method=method)*(first_amount+inc*(n-1))


def t_nIAErx(mt, x, n, defer=0, i=None, first_amount=1, inc=1., method='udd'):
    """
    Returns the Expected Present Value of an Endowment Life Insurance that pays
    (first_amount + k*increase_amount), at the end of the year of death,
    if death happens between ages x+k and x+k+1, for k=0,..., n-1 and a capital of
    first_amount + (n-1)*increase_amount in case of life at the end of the contract.
    Allows the computation for decreasing capitals.
    The first capital may differ from the increasing/decreasing amount.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param defer: deferment periods
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param first_amount: insured amount in the first year of the contract
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Deferred Endowment Life Insurance with Linear Increment (emd of the year of death)
    """
    return IA_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, first=first_amount, inc=inc, method=method) + \
        annuities.nEx(mt=mt, x=x, i=i, g=0, n=n + defer, method=method)*(first_amount+(n-1)*inc)


def t_nIAErx_(mt, x, n, defer=0, i=None, first_amount=1, inc=1., method='udd'):
    """
    Returns the Expected Present Value of an Endowment Life Insurance that pays
    (first_amount + k*increase_amount), at the moment of death,
    if death happens between ages x+k and x+k+1, for k=0,..., n-1 and a capital of
    first_amount + (n-1)*increase_amount in case of life at the end of the contract.
    Allows the computation for decreasing capitals.
    The first capital may differ from the increasing/decreasing amount.
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param defer: deferment periods
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param first_amount: insured amount in the first year of the contract
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Endowment Life Insurance with Linear Increment (moment year of death)
    """
    return IA_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, first=first_amount, inc=inc, method=method) * \
        np.sqrt(1 + i / 100) + annuities.nEx(mt=mt, x=x, i=i, g=0, n=n + defer, method=method)*(first_amount+(n-1)*inc)

