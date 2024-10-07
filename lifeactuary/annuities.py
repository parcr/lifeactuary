__author__ = "PedroCR"

import numpy as np


# life generic annuity 1 head
def annuity_x(mt, x, x_first, x_last, i=None, g=.0, m=1, method='udd'):
    """
    Computes the present value of an annuity that starts paying 1 at age x, increasing by (1+g/100) and stops
    at age x_w, paying (1+g/100)^{x_w-x}
    :param mt: table for life x
    :param x: age x
    :param x_first: age of first payment
    :param x_last: age of final payment
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    """
    if x_first < x: return np.nan
    if x_last < x_first == x: return np.nan
    if int(m) != m: return np.nan
    if x == x_first == x_last: return 1
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))
    number_of_payments = int(np.round((x_last - x_first) * m + 1, 0))
    payments_instants = np.linspace(x_first - x, x_last - x, number_of_payments)
    # payments_instants = np.arange(x_first - x, x_last - x + 1 / m, 1 / m)
    instalments = [mt.npx(x, n=t, method=method) *
                   np.power(d, t) for t in payments_instants]
    instalments = np.array(instalments) / np.power(1 + g, x_first - x) / m
    return np.sum(instalments)


# Life Annuities - 1 head

# Whole Life Annuities

def ax(mt, x, i=None, g=0, m=1, method='udd'):
    """
    Returns the actuarial present value of an immediate whole life annuity of 1 per time period.
    Payments of 1/m are made m times per year at the end of the periods. If g<>0, payments increase by (1+g/100) each period.
    :param mt: mortality table for life x
    :param x: age x
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """
    if x + 1 / m > mt.w: return 0

    return annuity_x(mt=mt, x=x, x_first=x + 1 / m, x_last=mt.w, i=i, g=g, m=m, method=method)


def aax(mt, x, i=None, g=0, m=1, method='udd'):
    """
    Returns the actuarial present value of a whole life annuity due of 1 per time period. The payments of
    1/m are made m times per year at the beginning of the periods. If g<>0, payments increase by
    (1+g/100) each period
    :param mt: mortality table for life x
    :param x: age x
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """
    if x > mt.w: return 1

    return annuity_x(mt=mt, x=x, x_first=x, x_last=mt.w, i=i, g=g, m=m, method=method)


def t_ax(mt, x, i=None, g=0, m=1, defer=0, method='udd'):
    """
    Returns the actuarial present value of an immediate whole life annuity of 1 per time period,
    deferred t periods. The payments of 1/m are made m times per year at the end of the periods.
    If g<>>0, payments increase by (1+g/100) each period.
    :param mt: mortality table for life x
    :param x: age x
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """
    if x + 1 / m + defer > mt.w: return 0

    return annuity_x(mt=mt, x=x, x_first=x + 1 / m + defer, x_last=mt.w, i=i, g=g, m=m, method=method)


def t_aax(mt, x, i=None, g=0, m=1, defer=0, method='udd'):
    """
    Returns the actuarial present value of a due whole life annuity of 1 per time period,
    deferred t periods. The payments of 1/m are made m times per year at the beginning of the periods.
    If g<>>0, payments increase by (1+g/100) each period.
    :param mt: mortality table for life x
    :param x: age x
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """
    if x + defer > mt.w: return 0

    return annuity_x(mt=mt, x=x, x_first=x + defer, x_last=mt.w, i=i, g=g, m=m, method=method)

# Temporary Life Annuities

def nax(mt, x, n, i=None, g=0, m=1, method='udd'):
    """
    Returns the actuarial present value of an immediate n term life annuity of 1 per time period.
    The payments of 1/m are made m times per year at the end of the periods.
    If g<>0, payments increase by (1+g/100) each period.
    :param mt: mortality table for life x
    :param x: age x
    :param n: number of years of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """
    if x + 1 / m > mt.w: return 0

    return annuity_x(mt=mt, x=x, x_first=x + 1 / m, x_last=x + n, i=i, g=g, m=m, method=method)


def naax(mt, x, n, i=None, g=0, m=1, method='udd'):
    """
    Returns the actuarial present value of a due n term life annuity of 1 per time period.
    The payments of 1/m are made m times per year at the beginning of the periods.
    If g<>0, payments increase by (1+g/100) each period.
    :param mt: mortality table for life x
    :param x: age x
    :param n: number of years of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """
    if x > mt.w: return 1

    return annuity_x(mt=mt, x=x, x_first=x, x_last=x + n - 1 / m, i=i, g=g, m=m, method=method)


def t_nax(mt, x, n, i=None, g=0, m=1, defer=0, method='udd'):
    """
    Returns the actuarial present value of a immediate $n$ term life annuity of 1 per time period, deferred t
    periods. The payments of 1/m are made m times per year at the end of the periods.
    If g<>0, payments increase by (1+g/100) each period.
    :param mt: table for life x
    :param x: age x
    :param n: number of years of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """
    if x + 1 / m + defer > mt.w: return 0

    return annuity_x(mt=mt, x=x, x_first=x + 1 / m + defer, x_last=x + n + defer, i=i, g=g, m=m, method=method)


def t_naax(mt, x, n, i=None, g=0, m=1, defer=0, method='udd'):
    """
    Returns the actuarial present value of a due n term life annuity of 1 per time period, deferred t
    periods. The payments of 1/m are made m times per year at the beginning of the periods.
    If g<>0, payments increase by (1+g/100) each period.
    :param mt: table for life x
    :param x: age x
    :param n: number of years of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """
    if x + defer > mt.w: return 0

    return annuity_x(mt=mt, x=x, x_first=x + defer, x_last=x + n + defer - 1 / m, i=i, g=g, m=m, method=method)


# Annuities with terms evolving arithmetically

def nIax(mt, x, n, i=None, m=1, first_amount=1, increase_amount=1, method='udd'):
    """
    Returns the actuarial present value of an immediate n term life annuity with payments evolving in
    arithmetic progression.
    Payments of 1/m are made m times per year at the end of the periods.
    First amount and Increase amount may be different.
    For decreasing life annuities, the increase_amount should be negative.
    :param mt: mortality table
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param i: interest rate, in percentage (e.g. 2 for 2%)
    :param m: frequency of payments per unit of interest rate
    :param first_amount: amount of the first payment
    :param increase_amount: amount of the increase rate
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """

    ann1 = nax(mt=mt, x=x, n=n, i=i, g=0, m=m, method=method)
    lst_ann = [t_nax(mt=mt, x=x, n=n - t, i=i, g=0, m=m, defer=t, method=method) for t in range(1, n)]

    ann = ann1 * first_amount + np.sum(lst_ann) * increase_amount

    return ann


def nIaax(mt, x, n, i=None, m=1, first_amount=1, increase_amount=1, method='udd'):
    """
    Returns the actuarial present value of a due n term life annuity with payments evolving in
    arithmetic progression.
    Payments of 1/m are made m times per year at the beginning of the periods.
    First amount and Increase amount may be different.
    For decreasing life annuities, the increase_amount should be negative.
    :param mt: mortality table
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param i: interest rate, in percentage (e.g. 2 for 2%)
    :param m: frequency of payments per unit of interest rate
    :param first_amount: amount of the first payment
    :param increase_amount: amount of the increase rate
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """

    ann1 = naax(mt=mt, x=x, n=n, i=i, g=0, m=m, method=method)
    lst_ann = [t_naax(mt=mt, x=x, n=n - t, i=i, g=0, m=m, defer=t, method=method) for t in range(1, n)]

    ann = ann1 * first_amount + np.sum(lst_ann) * increase_amount

    return ann


def t_nIax(mt, x, n, i=None, m=1, defer=0, first_amount=1, increase_amount=1, method='udd'):
    """
    Returns the actuarial present value of a deferred immediate n term life annuity with payments evolving in
    arithmetic progression.
    Payments of 1/m are made m times per year at the end of the periods.
    First amount and Increase amount may be different.
    For decreasing life annuities, the increase_amount should be negative.
    :param mt: mortality table
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param i: interest rate, in percentage (e.g. 2 for 2%)
    :param m: frequency of payments per unit of interest rate
    :param defer: number of deferment years
    :param first_amount: amount of the first payment
    :param increase_amount: amount of the increase rate
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """

    ann1 = t_nax(mt=mt, x=x, n=n, i=i, g=0, m=m, defer=defer, method=method)
    lst_ann = [t_nax(mt=mt, x=x, n=n - t, i=i, g=0, m=m, defer=t, method=method) for t in range(1, n)]

    ann = ann1 * first_amount + np.sum(lst_ann) * increase_amount

    return ann


def t_nIaax(mt, x, n, i, m, defer, first_amount, increase_amount, method):
    """
    Returns the actuarial present value of a deferred due n term life annuity with payments evolving in
    arithmetic progression.
    Payments of 1/m are made m times per year at the beginning of the periods.
    First amount and Increase amount may be different.
    For decreasing life annuities, the increase_amount should be negative.
    :param mt: mortality table
    :param x: age at the beginning of the contract
    :param n: number of years of the contract
    :param i: interest rate, in percentage (e.g. 2 for 2%)
    :param m: frequency of payments per unit of interest rate
    :param defer: number of deferment years
    :param first_amount: amount of the first payment
    :param increase_amount: amount of the increase rate
    :param method: the method to approximate the fractional ages (udd, cfm, bal)

    :return: Expected Present Value (EPV) for payments of 1/m
    """

    ann1 = t_naax(mt=mt, x=x, n=n, i=i, g=0, m=m, defer=defer, method=method)
    lst_ann = [t_naax(mt=mt, x=x, n=n - t, i=i, g=0, m=m, defer=t, method=method) for t in range(1, n)]

    ann = ann1 * first_amount + np.sum(lst_ann) * increase_amount

    return ann


def nEx(mt, x, i=None, g=0, n=0, method='udd'):
    """
    Returns the Actuarial Present Value / Pure Endowment / Deferred Capital
    :param mt: mortality table
    :param x: age at the beginning of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param n: number of years of the contract
    :param method: the method to approximate the fractional ages and periods (udd, cfm, bal)

    :return: the present value of a pure endowment of 1 at age x+n
    """

    return t_naax(mt=mt, x=x, n=1, i=i, g=g, m=1, defer=n, method=method)


# Present Value of a series of cash-flows
def present_value(mt, age, spot_rates, capital, probs=None):
    """
    Computes the expected present value of a cash-flows, that can be contingent on some probabilities.
    Payments are considered at the end of the period.

    :param mt: mortality table
    :param age: age at the beginning of the contract
    :param spot_rates: vector of interest rates for the considered time periods
    :param capital: vector of cash-flow amounts
    :param probs: vector of probabilities. For using the instantiated actuarial table, introduce probs=None

    :return: the expected present value of a cash-flow, that can be contingent on some probabilities.
    """
    if len(spot_rates) != len(capital):
        return np.nan
    if probs is None and mt is None:
        return np.nan

    probs_ = None

    if probs is None:
        if age is None:
            return np.nan
        else:
            probs_ = [mt.npx(age, n + 1) for n in range(len(capital))]

    if isinstance(probs, list):
        if len(probs) == len(spot_rates):
            probs_ = probs
        else:
            return np.nan

    if isinstance(probs, (float, int)):
        probs_ = [probs] * len(capital)
    discount = 1 + np.array(spot_rates) / 100.
    discount = np.cumprod(1 / discount)

    return sum([p * capital[idx_p] * discount[idx_p] for idx_p, p in enumerate(probs_)])