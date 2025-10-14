__author__ = "PedroCR"

import numpy as np


def A_x(mt, x, x_first, x_last, i=None, g=.0, m=1, method='udd'):
    """
    Returns the Expected Present Value (EPV) of a Life Insurance that pays 1 at the end of the year of death.
    :param mt: mortality table for life x
    :param x: age at the beginning of the contract
    :param x_first: age of first payment
    :param x_last: age of final payment
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV)
    """
    if x_first < x: return np.nan
    if x_last < x_first == x: return np.nan
    if x == x_first == x_last: return 0
    if x_last>mt.w+1: 
        x_last=max(x_first+1, mt.w+1)

    if int(m) != m: return np.nan
    if m > 356 * 24: return np.nan

    i = i / 100
    g = g / 100
    v = float((1 + g) / (1 + i))

    # the due transformations for multiples of m
    # x_first_ = int(x_first) + int((x_first - int(x_first)) * m) / m
    # x_last_ = int(x_last) + int((x_last - int(x_last)) * m) / m
    # x_ = int(x) + int((x - int(x)) * m) / m
    x_first_ = np.floor(x_first * m) / m
    x_last_ = np.floor(x_last * m) / m
    x_ = np.floor(x * m) / m

    x_first_ = x_first
    x_last_ = x_last
    x_ = x

    # i_m=(1+i)**(1/m)-1
    # g_m=(1+g)**(1/m)-1
    # v_m = float((1 + g_m) / (1 + i_m))

    number_of_payments = int((x_last_ - x_first_) * m + 1)
    if number_of_payments < 1: return .0
    # payments_instants = np.linspace(x_first_ - x_, x_last_ - x, number_of_payments)
    payments_instants = np.arange(x_first_ - x_, x_last_ - x + 1/m, 1/m)
    step=1/m
    payments_instants_step= np.round(payments_instants - step,10)
    probs_surv = [mt.npx(x, n=t, method=method) for t in payments_instants_step]
    probs_death= [mt.nqx(x + t, n=step, method=method) for t in payments_instants_step]

    instalments_=[probs_surv[idx] * probs_death[idx] * np.power(v, t)
        for idx, t in enumerate(payments_instants)]

    instalments = [
        mt.npx(x, n=t - 1 / m, method=method) * mt.nqx(x + t - 1 / m, n=1 / m, method=method) * np.power(v, t)
        for t in payments_instants]
    instalments = np.array(instalments_) / np.power(1 + g, payments_instants[0])
    return np.sum(instalments_)
