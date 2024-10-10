__author__ = "PedroCR"

import numpy as np
import logging
from lifeActuary import mortality_table as mt
from lifeActuary import mortality_table_2heads as mt2h
from lifeActuary import commutation_table as ct
from lifeActuary import mortality_insurance as mi

all_status = {'joint-life', 'last-survivor'}
log_message_mt = 'We need mtx and mty to be an instance of the class MortalityTable.'
log_message_status = f'Please, check the status. Status available are {all_status}'


def check_mortality_tables(func):
    def wrapper(*args, **kwargs):
        mt_in_args = [isinstance(m, mt.MortalityTable) for m in args[0:2]]
        mt_in_kwargs = [isinstance(m, mt.MortalityTable) for m in kwargs.values()]
        if sum(mt_in_args) + sum(mt_in_kwargs) != 2:  # len(mortality_instance):
            return logging.warning(log_message_mt)
        return func(*args, **kwargs)

    return wrapper


def check_status(func):
    def wrapper(*args, **kwargs):
        test_args = [s in args for s in all_status]
        test_kwargs = [s in kwargs.values() for s in all_status]
        if sum(test_args) + sum(test_kwargs) != 1:
            logging.warning(log_message_status)
            return
        return func(*args, **kwargs)

    return wrapper


# Probabilities

@check_status
@check_mortality_tables
def npxy(mtx, mty, x, y, n=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of years
        status: probabilities for 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods, ages or terms (udd, cfm, bal)
    Returns: probability of a group of two lives to survive at least n years
    """
    if status == 'joint-life':
        return mtx.npx(x, n, method) * mty.npx(y, n, method)
    if status == 'last-survivor':
        return 1 - mtx.nqx(x, n, method) * mty.nqx(y, n, method)

@check_status
@check_mortality_tables
def nqxy(mtx, mty, x, y, n=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of years
        status: probabilities for 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods, ages or terms
    Returns: probability of a group of two lives to extinguish before n years (udd, cfm, bal)
    """
    if status == 'joint-life':
        return 1 - mtx.npx(x, n, method) * mty.npx(y, n, method)
    if status == 'last-survivor':
        return mtx.nqx(x, n, method) * mty.nqx(y, n, method)


@check_status
@check_mortality_tables
def t_nqxy(mtx, mty, x, y, n=1, t=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of years
        status: probabilities for 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods, ages or terms
    Returns: probability of a group of two lives to survive at least n years and extinguishes
    before n+t years
    """
    return npxy(mtx, mty, x, y, t, status, method) - npxy(mtx, mty, x, y, n + t, status, method)

# Life Expectancy
@check_status
@check_mortality_tables
def exy(mtx, mty, x, y, status='joint-life', method='udd'):
    if status == 'joint-life':
        ages = np.arange(1, min(mtx.w - x, mty.w - y) + 1, 1)
    if status == 'last-survivor':
        ages = np.arange(1, max(mtx.w - x, mty.w - y) + 1, 1)
    pxy = [npxy(mtx, mty, x, y, n=age, status=status, method=method) for age in ages]
    return sum(pxy) + .5


@check_status
@check_mortality_tables
def exyn(mtx, mty, x_young, y_old, n, status='joint-life', method='udd'):
    if x_young > y_old:
        return np.nan
    dif_age = y_old - x_young

    if status == 'joint-life':
        last_age = min(mtx.w, mty.w) + 1
        ages_jl = np.linspace(0, last_age, last_age + 1)
        px = [npxy(mtx, mty, x, x + dif_age, n=1, status='joint-life', method=method) for x in ages_jl]
    if status == 'last-survivor':
        last_age = max(mtx.w, mty.w) + 1
        ages_ls = np.linspace(0, last_age, last_age + 1)
        px = [npxy(mtx, mty, x, x + dif_age + dif_age, n=1, status='last-survivor', method=method) for x in ages_ls]

    px = [p for p in px if p != 0]
    px.insert(0, 0)
    mt_xy = mt.MortalityTable(data_type='p', mt=px, perc=100, last_q=1)

    return mt_xy.exn(x=x_young, n=n, method=method)


# Multiple Life Annuities

## Life Generic Annuity 2 head
@check_status
@check_mortality_tables
def annuity_xy(mtx, mty, x, x_first_payment, x_last_payment, y, i=None, g=.0, m=1, status='joint-life', method='udd'):
    """
    Computes the present value of an annuity that starts paying 1 at age x, increasing by (1+g/100) and stops
    at age x_w, paying (1+g)^{t-1}
    :param mtx: mortality table for life x
    :param mty: mortality table for life y
    :param x: age of life x
    :param y: age of life y
    :param x_first_payment: age of x at the first payment
    :param x_last_payment: age of x at the final payment
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param status: joint-life or last-survivor
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    """

    if x_first_payment < x: return np.nan
    if x_last_payment < x_first_payment == x: return np.nan
    if int(m) != m or m <= 0: return np.nan
    if x == x_first_payment == x_last_payment: return 1
    if x < 0 or y < 0: return np.nan
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))

    y_first_payment = y + (x_first_payment - x)
    y_last_payment = min(y + (x_last_payment - x), mty.w + 1)
    x_first_payment = min(x_first_payment, mtx.w + 1)
    if x_first_payment > mtx.w and y_first_payment > mty.w:
        if x_first_payment == x:
            return 1.
        return .0

    number_of_payments = int(np.round((x_last_payment - x_first_payment) * m + 1, 0))
    number_of_payments_y = int(np.round((y_last_payment - y_first_payment) * m + 1, 0))
    payments_instants = np.linspace(x_first_payment - x, x_last_payment - x, number_of_payments)
    payments_instants_y = np.linspace(y_first_payment - y, y_last_payment - y, number_of_payments_y)

    py = payments_instants
    if len(payments_instants_y) < len(payments_instants):
        py = payments_instants_y

    instalments_jl = [mtx.npx(x, n=t, method=method) * mty.npx(y, n=t, method=method) * np.power(d, t)
                      for t in py]
    sum_instalments = sum(instalments_jl)

    if status == 'last-survivor':
        instalments_x = [mtx.npx(x, n=t, method=method) * np.power(d, t) for t in payments_instants]
        instalments_y = [mty.npx(y, n=t, method=method) * np.power(d, t) for t in payments_instants_y]
        sum_instalments = sum(instalments_x) + sum(instalments_y) - sum_instalments

    return sum_instalments / np.power(1 + g, x_first_payment - x) / m


# Whole Life Annuities - 2 heads

def axy(mtx, mty, x, y, i=None, g=0, m=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: frequency of payments per unit of interest rate quoted
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods or ages (udd, cfm, bal)

    Returns: Returns the actuarial present value of an immediate whole life annuity paid for a group of two lives.
    Payments are made in the end of the periods.
    For constant annuities, pays 1 per time period.
    For fractional annuities, payments of 1/m are made m times per year at the end of the periods.
    For annuities with geometric growth, the rate is g for each payment period.
    """

    if x + 1 / m > max(mtx.w, mty.w): return 0

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first_payment=x + 1 / m, x_last_payment=max(mtx.w, mty.w) + 1,
                      y=y, i=i, g=g, m=m, status=status, method=method)

def aaxy(mtx, mty, x, y, i=None, g=0, m=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: frequency of payments per unit of interest rate quoted
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods or ages (udd, cfm, bal)

    Returns: actuarial present value of a due whole life annuity paid for a group of two lives.
    Payments are made in the beginning of the periods.
    For constant annuities, pays 1 per time period.
    For fractional annuities, payments of 1/m are made m times per year at the beginning of periods.
    For annuities with geometric growth, the rate is g for each payment period.

    """
    if x > max(mtx.w, mty.w): return 1

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first_payment=x, x_last_payment=max(mtx.w, mty.w) + 1,
                      y=y, i=i, g=g, m=m, status=status, method=method)

def t_axy(mtx, mty, x, y, i=None, g=0, m=1, defer=0, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: frequency of payments per unit of interest rate quoted
        defer: deferment period
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: Returns the actuarial present value of a deferred whole life annuity paid for a group of two lives.
    Payments are made in the end of the periods.
    For constant annuities, pays 1 per time period.
    For fractional annuities, payments of 1/m are made m times per year at the end of the periods.
    For annuities with geometric growth, the rate is g for each payment period.
    """

    if x + 1 / m + defer > max(mtx.w, mty.w): return 0

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first_payment=x + 1 / m + defer, x_last_payment=max(mtx.w, mty.w) + 1,
                      y=y, i=i, g=g, m=m, status=status, method=method)

def t_aaxy(mtx, mty, x, y, i=None, g=0, m=1, defer=0, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: frequency of payments per unit of interest rate quoted
        defer: deferment period
        status: probabilities for 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: Returns the actuarial present value of a deferred whole life annuity paid for a group of two lives.
    Payments are made in the beginning of periods.
    For constant annuities, pays 1 per time period.
    For fractional annuities, payments of 1/m are made m times per year at the beginning of the periods.
    For annuities with geometric growth, the rate is g for each payment period.
    """

    if x + defer > max(mtx.w, mty.w): return 1

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first_payment=x + defer, x_last_payment=max(mtx.w, mty.w) + 1,
                      y=y, i=i, g=g, m=m, status=status, method=method)


# Temporary Life Annuites - 2 heads

def naxy(mtx, mty, x, y, n, i=None, g=0, m=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: frequency of payments per unit of interest rate quoted
        status: probabilities for 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: Returns the actuarial present value of an immediate temporary life annuity paid for a group of two lives.
    Payments are made in the end of the periods.
    For constant annuities, pays 1 per time period.
    For fractional annuities, payments of 1/m are made m times per year at the end of the periods.
    For annuities with geometric growth, the rate is g for each payment period.
    """

    if x + 1 / m > max(mtx.w, mty.w): return 0

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first_payment=x + 1 / m, x_last_payment=x + n, y=y, i=i, g=g, m=m,
                      status=status, method=method)

def naaxy(mtx, mty, x, y, n, i=None, g=0, m=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortaity table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: frequency of payments per unit of interest rate quoted
        status: probabilities for 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: Returns the actuarial present value of a temporary life annuity due paid for a group of two lives.
    Payments are made in the beginning of periods.
    For constant annuities, pays 1 per time period.
    For fractional annuities, payments of 1/m are made m times per year at the end of the periods.
    For annuities with geometric growth, the rate is g for each payment period.
    """

    if x > max(mtx.w, mty.w): return 1

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first_payment=x, x_last_payment=x + n - 1 / m, y=y, i=i, g=g, m=m,
                      status=status, method=method)


def t_naxy(mtx, mty, x, y, n, i=None, g=0, m=1, defer=0, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: frequency of payments per unit of interest rate quoted
        defer: deferment period
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: Returns the actuarial present value of a deferred temporary life annuity paid for a group of two lives.
    Payments are made at the end of the periods.
    For constant annuities, pays 1 per time period.
    For fractional annuities, payments of 1/m are made m times per year at the end of the periods.
    For annuities with geometric growth, the rate is g for each payment period.
    """

    if x + 1 / m + defer > max(mtx.w, mty.w): return 0

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first_payment=x + 1 / m + defer, x_last_payment=x + n + defer, y=y,
                      i=i, g=g, m=m, status=status, method=method)


def t_naaxy(mtx, mty, x, y, n, i=None, g=0, m=1, defer=0, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: frequency of payments per unit of interest rate quoted
        defer: deferment period
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: Returns the actuarial present value of a deferred temporary life annuity paid for a group of two lives.
    Payments are made in the beginning of the periods.
    For constant annuities, pays 1 per time period.
    For fractional annuities, payments of 1/m are made m times per year at the end of the periods.
    For annuities with geometric growth, the rate is g for each payment period.
    """

    if x + defer > max(mtx.w, mty.w): return 1

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first_payment=x + defer, x_last_payment=x + n + defer - 1 / m, y=y,
                      i=i, g=g, m=m, status=status, method=method)

# Actuarial Present Value / Endowment Insurance - 2 heads
@check_status
@check_mortality_tables
def nExy(mtx, mty, x, y, i=None, n=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        n: number of years until term
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate due to fractional ages (udd, cfm, bal) 

    Returns: Returns the actuarial expected present value of an unitary capital paid in n years 
    term (Pure Endowment) paid upon the survival of a group of two lives.
    """

    if status == 'joint-life':
        return mtx.npx(x=x, n=n, method=method) * mty.npx(x=y, n=n, method=method) / \
            (1 + i / 100) ** n
    if status == 'last-survivor':
        return (1 - mtx.nqx(x=x, n=n, method=method) * mty.nqx(x=y, n=n, method=method)) / \
            (1 + i / 100) ** n


# Life Benefits - 2 heads

## Generic Term Life Insurance 2 head
def A_xy(mtx, mty, x, y, n, i=None, g=0, m=1, defer=0, status='joint-life', method='udd'):
    """

    Args:
        mtx: mortality table for x
        mty: mortality table for y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: frequency of payments per unit of interest rate quoted
        defer: deferment period
        status: probabilities for 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods, ages or terms

    Returns: Returns the actuarial expected present value
    """
    if defer < 0:
        return np.nan
    v = (1 + g / 100) / (1 + i / 100)
    d_m = (1 - v ** (1 / m)) * m
    ann = annuity_xy(mtx=mtx, mty=mty, x=x + defer, x_first_payment=x + defer,
                     x_last_payment=x + defer + n - 1, y=y + defer, i=i, g=g, m=m, status=status, method=method)
    pure_endow_1 = nExy(mtx, mty, x, y, i, defer, status, method)
    pure_endow_2 = nExy(mtx, mty, x + defer, y + defer, i, n, status, method)
    endow = (1 - d_m * ann)
    return pure_endow_1 * (endow - pure_endow_2)


def Axy(mtx, mty, x, y, i=None, g=0, m=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: number of periods per year at the end of which the capital is payable in case of insured event
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: returns the expected present value of a whole life insurance (i.e. net single premium),
    that pays 1 at the end of the period of death of a group of two lives.
    For contracts with geometric growth, the rate is g for each payment period.
    """
    n = max(mtx.w, mty.w)
    return A_xy(mtx, mty, x, y, n, i, g, m, defer=0, status=status, method=method)


def Axy_(mtx, mty, x, y, i=None, g=0, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: returns the expected present value of a whole life insurance (i.e. net single premium), that pays 1 at the
    middle of the year of the death of a group of two lives.
    For contracts with geometric growth, the rate is g for each payment period.
    """
    return Axy(mtx, mty, x, y, i=i, g=g, m=1, status=status, method=method) * (1 + i / 100) ** .5


def t_Axy(mtx, mty, x, y, i=None, g=0, m=1, defer=0, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: number of periods per year at the end of which the capital is payable in case of insured event
        defer: deferment period
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: returns the expected present value of a deferred whole life insurance (i.e. net single premium),
    that pays 1 at the end of the period of death of a group of two lives.
    For contracts with geometric growth, the rate is g for each payment period.
    """
    n = max(mtx.w, mty.w)
    return A_xy(mtx, mty, x, y, n, i=i, g=g, m=m, defer=defer, status=status, method=method)


def t_Axy_(mtx, mty, x, y, i=None, g=0, defer=0, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        defer: deferment period
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: returns the expected present value of a deferred whole life insurance
    (i.e. net single premium), that pays 1 at the middle of the year of the death of a group of two lives.
    For contracts with geometric growth, the rate is g for each payment period.
    """
    return t_Axy(mtx, mty, x, y, i=i, g=g, m=1, defer=defer, status=status, method=method) * (1 + i / 100) ** .5

# Term Life Insurance - 2 heads

def nAxy(mtx, mty, x, y, n, i=None, g=0, m=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: number of periods per year at the end of which the capital is payable in case of insured event
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: returns the expected present value of a temporary life insurance (i.e. net single premium),
    that pays 1 at the end of the period of death of a group of two lives.
    For contracts with geometric growth, the rate is g for each payment period.
    """
    return A_xy(mtx, mty, x, y, n, i, g=g, m=m, defer=0, status=status, method=method)


def nAxy_(mtx, mty, x, y, n, i=None, g=0, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        status: probabilities for 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: returns the expected present value of a temporary life insurance (i.e. net single premium),
    that pays 1 at the middle of the year of the death of a group of two lives.
    For contracts with geometric growth, the rate is g for each payment period.
    """
    return A_xy(mtx, mty, x, y, n, i, g, m=1, defer=0, status=status, method=method) * (1 + i / 100) ** .5


def t_nAxy(mtx, mty, x, y, n, i=None, g=0, m=1, defer=0, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: number of periods per year at the end of which the capital is payable in case of insured event
        defer: deferment period
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods, ages or terms

    Returns: returns the expected present value of a deferred temporary life insurance (i.e. net single premium),
    that pays 1 at the end of the period of death of a group of two lives.
    For contracts with geometric growth, the rate is g for each payment period.
    """
    return A_xy(mtx, mty, x, y, n, i, g, m, defer=defer, status=status, method=method)


def t_nAxy_(mtx, mty, x, y, n, i=None, g=0, defer=0, status='joint-life', method='udd'):
    """
        Args:
            mtx: mortality table for life x
            mty: mortality table for life y
            x: age of life x
            y: age of life y
            n: number of periods
            i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
            g: growth rate (flat rate) in percentage, e.g., 2 for 2%
            defer: deferment period
            status: 'joint-life' or 'last-survivor' status
            method: the method to approximate the fractional periods and ages

        Returns: returns the expected present value of a deferred temporary life insurance (i.e. net single premium),
        that pays 1 in the middle of the year of death of a group of two lives.
        For contracts with geometric growth, the rate is g for each payment period.
        """
    return A_xy(mtx, mty, x, y, n, i, g, m=1, defer=defer, status=status, method=method) * (1 + i / 100) ** .5

# Endowment Life Insurance - 2 heads
def nAExy(mtx, mty, x, y, n, i=None, g=0, m=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: number of periods per year at the end of which the capital is payable in case of insured event
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods, ages or terms

    Returns: returns the expected present value of an endowment life insurance (i.e. net single premium),
    that pays 1 at the end of the period of death of a group of two lives or pays 1 if the group is alive at the end
    of the contract.
    For contracts with geometric growth, the rate is g for each payment period.
    """
    return nAxy(mtx, mty, x, y, n, i, g=g, m=m, status=status, method=method) + \
        nExy(mtx, mty, x, y, i, n=n, status=status, method=method)


def nAExy_(mtx, mty, x, y, n, i=None, g=0, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: returns the expected present value of an endowment life insurance (i.e. net single premium),
    that pays 1 in the middle of the period of death of a group of two lives or pays 1 if the group is alive at the end
    of the contract.
    For contracts with geometric growth, the rate is g for each payment period.
    """
    return nAxy_(mtx, mty, x, y, n, i, g=g, status=status, method=method) + \
        nExy(mtx, mty, x, y, i, n=n, status=status, method=method)


def t_nAExy(mtx, mty, x, y, n, i=None, g=.0, m=1, defer=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        m: number of periods per year at the end of which the capital is payable in case of insured event
        defer: deferment period
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: returns the expected present value of a deferred endowment life insurance (i.e. net single premium),
    that pays 1 at the end of the period of death of a group of two lives or pays 1 if the group is alive at the end
    of the contract.
    For contracts with geometric growth, the rate is g for each payment period.
    """
    return t_nAxy(mtx, mty, x, y, n, i, g=g, m=m, defer=defer, status=status, method=method) + \
        nExy(mtx, mty, x, y, i, n=defer + n, status=status, method=method)


def t_nAExy_(mtx, mty, x, y, n, i=None, g=.0, defer=1, status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        g: growth rate (flat rate) in percentage, e.g., 2 for 2%
        defer: deferment period
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: returns the expected present value of a deferred endowment life insurance (i.e. net single premium),
    that pays 1 at the moment of death of a group of two lives or pays 1 if the group is alive at the end
    of the contract.
    For contracts with geometric growth, the rate is g for each payment period.
    """
    return t_nAxy_(mtx, mty, x, y, n, i, g=g, defer=defer, status=status, method=method) + \
        nExy(mtx, mty, x, y, i, n=defer + n, status=status, method=method)




#################################################
@check_status
@check_mortality_tables
def _create_joint_mortality_table(mt_old, mt_young, age_dif=0, status='joint-life'):
    return mt2h.MortalityTable2Heads(mt_old=mt_old, mt_young=mt_young, age_dif=age_dif, status=status)


@check_status
@check_mortality_tables
def t_nIArxy(mtx, mty, x, y, n, i=None, defer=0, first_payment=1, inc=1,
             status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        defer: deferment period
        first_payment: amount of capital in the first year
        inc: rate of the progression (in monetary units)
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: Returns the Expected Present Value of a deferred Term Life Insurance that pays
    1+k, at the end of year of death of a group of two individuals, if death occurs between ages
    x+t+k and x+t+k+1, for k=0, 1,..., n-1.
    The capital of the first year may differ from the rate of the progression.
    """
    if n < 0 or defer < 0 or x < 0 or y < 0: return np.nan
    if first_payment + n * inc < 0: return np.nan

    payment1 = t_nAxy(mtx, mty, x, y, n, i, g=.0, m=1, defer=defer, status=status, method=method)
    payment1 *= first_payment

    payment2 = [t_nAxy(mtx, mty, x, y, n - j, i, g=.0, m=1, defer=defer + j, status=status, method=method)
                for j in range(1, min(max(mtx.w - x, mty.w - y), n))]
    payment2 = sum(payment2)
    payment2 *= inc
    payment_jl = payment1 + payment2

    if status == 'joint-life':
        return payment_jl

    payment_x = mi.t_nIArx(mtx, x, n, defer, i, first_payment, inc, method)
    payment_y = mi.t_nIArx(mty, y, n, defer, i, first_payment, inc, method)

    return payment_x+payment_y-payment_jl

@check_status
@check_mortality_tables
def t_nIArxy_(mtx, mty, x, y, n, i=None, defer=0, first_payment=1, inc=1,
             status='joint-life', method='udd'):
    """
    Args:
        mtx: mortality table for life x
        mty: mortality table for life y
        x: age of life x
        y: age of life y
        n: number of periods
        i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
        defer: deferment period
        first_payment: amount of capital in the first year
        inc: rate of the progression (in monetary units)
        status: 'joint-life' or 'last-survivor' status
        method: the method to approximate the fractional periods and ages (udd, cfm, bal)

    Returns: Returns the Expected Present Value of a deferred Term Life Insurance that pays
    1+k, at the moment of death of a group of two individuals, if death occurs between ages
    x+t+k and x+t+k+1, for k=0, 1,..., n-1.
    The capital of the first year may differ from the rate of the progression.
    """

    return t_nIArxy(mtx, mty, x, y, n, i, defer, first_payment, inc, status, method) * (1 + i / 100) ** .5