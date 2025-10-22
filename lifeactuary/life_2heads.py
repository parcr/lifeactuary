"""
Two-Life Actuarial Functions Module

This module provides comprehensive actuarial calculations for two-life insurance and annuity products.
It includes functions for computing probabilities, life expectancies, annuities, and life insurance
benefits for groups of two lives under different status configurations.

Key Features:
    - Joint-life and last-survivor probability calculations
    - Life expectancy computations for two lives
    - Annuity valuations (immediate, due, deferred, temporary)
    - Life insurance valuations (whole life, term, endowment)
    - Support for various approximation methods (UDD, CFM, BAL)
    - Geometric growth patterns for benefits

Status Types:
    - joint-life: Benefits depend on both lives being alive
    - last-survivor: Benefits continue until both lives have died

Author: PedroCR
"""

__author__ = "PedroCR"

from typing import Union, Optional, Literal
import numpy as np
import logging
from lifeActuary import mortality_table as mt
from lifeActuary import mortality_table_2heads as mt2h
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
def npxy(mtx: mt.MortalityTable, 
         mty: mt.MortalityTable, 
         x: Union[int, float], 
         y: Union[int, float], 
         n: Union[int, float] = 1, 
         status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
         method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the probability that a group of two lives survives at least n years.

    This function computes the survival probability for two lives based on their 
    individual mortality tables and the specified status type.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    y : Union[int, float]
        Current age of life y.
    n : Union[int, float], default=1
        Number of years for the survival period.
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Type of survival condition:
        - 'joint-life': Both lives must survive
        - 'last-survivor': At least one life must survive
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Probability that the group survives at least n years.

    Examples
    --------
    >>> npxy(mt_male, mt_female, 30, 28, 10, 'joint-life')
    0.95
    >>> npxy(mt_male, mt_female, 65, 62, 5, 'last-survivor')
    0.88
    """
    if status == 'joint-life':
        return mtx.npx(x, n, method) * mty.npx(y, n, method)
    if status == 'last-survivor':
        return 1 - mtx.nqx(x, n, method) * mty.nqx(y, n, method)

@check_status
@check_mortality_tables
def nqxy(mtx: mt.MortalityTable, 
         mty: mt.MortalityTable, 
         x: Union[int, float], 
         y: Union[int, float], 
         n: Union[int, float] = 1, 
         status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
         method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the probability that a group of two lives dies within n years.

    This function computes the probability that the group status condition fails
    within the specified time period.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    y : Union[int, float]
        Current age of life y.
    n : Union[int, float], default=1
        Number of years for the mortality period.
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Type of mortality condition:
        - 'joint-life': At least one life must die
        - 'last-survivor': Both lives must die
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Probability that the group dies within n years according to status.

    Examples
    --------
    >>> nqxy(mt_male, mt_female, 30, 28, 10, 'joint-life')
    0.05
    >>> nqxy(mt_male, mt_female, 65, 62, 5, 'last-survivor')
    0.12
    """
    if status == 'joint-life':
        return 1 - mtx.npx(x, n, method) * mty.npx(y, n, method)
    if status == 'last-survivor':
        return mtx.nqx(x, n, method) * mty.nqx(y, n, method)


@check_status
@check_mortality_tables
def t_nqxy(mtx: mt.MortalityTable, 
           mty: mt.MortalityTable, 
           x: Union[int, float], 
           y: Union[int, float], 
           n: Union[int, float] = 1, 
           t: Union[int, float] = 1, 
           status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
           method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the deferred probability of death for a group of two lives.

    This function computes the probability that a group survives t years and 
    then dies within the next n years.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    y : Union[int, float]
        Current age of life y.
    n : Union[int, float], default=1
        Number of years for the mortality period after deferment.
    t : Union[int, float], default=1
        Deferment period (years to survive before mortality period).
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Type of group condition:
        - 'joint-life': Both lives affect the condition
        - 'last-survivor': At least one life must survive initially
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Probability of surviving t years and then dying within n years.

    Examples
    --------
    >>> t_nqxy(mt_male, mt_female, 30, 28, 5, 10, 'joint-life')
    0.03
    """
    return npxy(mtx, mty, x, y, t, status, method) - npxy(mtx, mty, x, y, n + t, status, method)

# Life Expectancy
@check_status
@check_mortality_tables
def exy(mtx: mt.MortalityTable, 
        mty: mt.MortalityTable, 
        x: Union[int, float], 
        y: Union[int, float], 
        status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
        method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the complete expectation of life for a group of two lives.

    This function computes the expected number of years until the group condition
    fails based on the specified status type.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    y : Union[int, float]
        Current age of life y.
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Type of group condition:
        - 'joint-life': Expected years until first death
        - 'last-survivor': Expected years until last death
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Complete expectation of life for the group in years.

    Examples
    --------
    >>> exy(mt_male, mt_female, 30, 28, 'joint-life')
    45.2
    >>> exy(mt_male, mt_female, 65, 62, 'last-survivor')
    28.7
    """
    if status == 'joint-life':
        ages = np.arange(1, min(mtx.w - x, mty.w - y) + 1, 1)
    if status == 'last-survivor':
        ages = np.arange(1, max(mtx.w - x, mty.w - y) + 1, 1)
    pxy = [npxy(mtx, mty, x, y, n=age, status=status, method=method) for age in ages]
    return sum(pxy) + .5


@check_status
@check_mortality_tables
def exyn(mtx: mt.MortalityTable, 
         mty: mt.MortalityTable, 
         x_young: Union[int, float], 
         y_old: Union[int, float], 
         n: Union[int, float], 
         status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
         method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the temporary expectation of life for two lives with different ages.

    This function creates a temporary mortality table for the younger life adjusted
    for the age difference and computes the n-year expectation of life.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for the younger life.
    mty : mt.MortalityTable
        Mortality table for the older life.
    x_young : Union[int, float]
        Current age of the younger life.
    y_old : Union[int, float]
        Current age of the older life.
    n : Union[int, float]
        Number of years for the temporary expectation.
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Type of group condition:
        - 'joint-life': Expected years until first death
        - 'last-survivor': Expected years until last death
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Temporary expectation of life in years, or NaN if x_young > y_old.

    Examples
    --------
    >>> exyn(mt_male, mt_female, 25, 30, 10, 'joint-life')
    8.5
    """
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
def annuity_xy(mtx: mt.MortalityTable, 
               mty: mt.MortalityTable, 
               x: Union[int, float], 
               x_first_payment: Union[int, float], 
               x_last_payment: Union[int, float], 
               y: Union[int, float], 
               i: Optional[Union[int, float]] = None, 
               g: Union[int, float] = 0.0, 
               m: int = 1, 
               status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
               method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the present value of a generic two-life annuity.

    This function computes the actuarial present value of an annuity that pays
    periodic amounts to a group of two lives based on their survival status.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    x_first_payment : Union[int, float]
        Age of life x at the first payment.
    x_last_payment : Union[int, float]
        Age of life x at the final payment.
    y : Union[int, float]
        Current age of life y.
    i : Optional[Union[int, float]], default=None
        Technical interest rate as a percentage (e.g., 2 for 2%).
    g : Union[int, float], default=0.0
        Growth rate as a percentage (e.g., 2 for 2% annual increase).
    m : int, default=1
        Frequency of payments per year.
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Payment condition:
        - 'joint-life': Payments while both lives are alive
        - 'last-survivor': Payments while at least one life is alive
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Actuarial present value of the annuity.

    Notes
    -----
    - For constant annuities (g=0), each payment is 1 per time period
    - For fractional annuities, payments of 1/m are made m times per year
    - For geometric growth annuities, payments increase by (1+g/100) each period

    Examples
    --------
    >>> annuity_xy(mt_male, mt_female, 30, 30.5, 65, 28, i=3, g=2, m=12)
    12.5
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

def axy(mtx: mt.MortalityTable, 
        mty: mt.MortalityTable, 
        x: Union[int, float], 
        y: Union[int, float], 
        i: Optional[Union[int, float]] = None, 
        g: Union[int, float] = 0, 
        m: int = 1, 
        status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
        method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the actuarial present value of an immediate whole life annuity for two lives.

    This function computes the present value of an annuity that pays at the end
    of each period while the group condition is satisfied.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    y : Union[int, float]
        Current age of life y.
    i : Optional[Union[int, float]], default=None
        Technical interest rate as a percentage (e.g., 2 for 2%).
    g : Union[int, float], default=0
        Growth rate as a percentage (e.g., 2 for 2% annual increase).
    m : int, default=1
        Frequency of payments per year.
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Payment condition:
        - 'joint-life': Payments while both lives are alive
        - 'last-survivor': Payments while at least one life is alive
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Actuarial present value of the immediate whole life annuity.

    Notes
    -----
    - For constant annuities (g=0), each payment is 1 per time period
    - For fractional annuities, payments of 1/m are made m times per year
    - For geometric growth annuities, payments increase by g% each period
    - Payments are made at the end of each period

    Examples
    --------
    >>> axy(mt_male, mt_female, 30, 28, i=3, status='joint-life')
    18.5
    >>> axy(mt_male, mt_female, 65, 62, i=3, status='last-survivor')
    25.2
    """

    if x + 1 / m > max(mtx.w, mty.w): return 0

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first_payment=x + 1 / m, x_last_payment=max(mtx.w, mty.w) + 1,
                      y=y, i=i, g=g, m=m, status=status, method=method)

def aaxy(mtx: mt.MortalityTable, 
         mty: mt.MortalityTable, 
         x: Union[int, float], 
         y: Union[int, float], 
         i: Optional[Union[int, float]] = None, 
         g: Union[int, float] = 0, 
         m: int = 1, 
         status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
         method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the actuarial present value of a due whole life annuity for two lives.

    This function computes the present value of an annuity that pays at the beginning
    of each period while the group condition is satisfied.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    y : Union[int, float]
        Current age of life y.
    i : Optional[Union[int, float]], default=None
        Technical interest rate as a percentage (e.g., 2 for 2%).
    g : Union[int, float], default=0
        Growth rate as a percentage (e.g., 2 for 2% annual increase).
    m : int, default=1
        Frequency of payments per year.
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Payment condition:
        - 'joint-life': Payments while both lives are alive
        - 'last-survivor': Payments while at least one life is alive
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Actuarial present value of the due whole life annuity.

    Notes
    -----
    - For constant annuities (g=0), each payment is 1 per time period
    - For fractional annuities, payments of 1/m are made m times per year
    - For geometric growth annuities, payments increase by g% each period
    - Payments are made at the beginning of each period

    Examples
    --------
    >>> aaxy(mt_male, mt_female, 30, 28, i=3, status='joint-life')
    19.5
    """
    if x > max(mtx.w, mty.w): return 1

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first_payment=x, x_last_payment=max(mtx.w, mty.w) + 1,
                      y=y, i=i, g=g, m=m, status=status, method=method)

def t_axy(mtx: mt.MortalityTable, 
          mty: mt.MortalityTable, 
          x: Union[int, float], 
          y: Union[int, float], 
          i: Optional[Union[int, float]] = None, 
          g: Union[int, float] = 0, 
          m: int = 1, 
          defer: Union[int, float] = 0, 
          status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
          method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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

def t_aaxy(mtx: mt.MortalityTable, 
           mty: mt.MortalityTable, 
           x: Union[int, float], 
           y: Union[int, float], 
           i: Optional[Union[int, float]] = None, 
           g: Union[int, float] = 0, 
           m: int = 1, 
           defer: Union[int, float] = 0, 
           status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
           method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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

def naxy(mtx: mt.MortalityTable, 
         mty: mt.MortalityTable, 
         x: Union[int, float], 
         y: Union[int, float], 
         n: Union[int, float], 
         i: Optional[Union[int, float]] = None, 
         g: Union[int, float] = 0, 
         m: int = 1, 
         status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
         method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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

def naaxy(mtx: mt.MortalityTable, 
          mty: mt.MortalityTable, 
          x: Union[int, float], 
          y: Union[int, float], 
          n: Union[int, float], 
          i: Optional[Union[int, float]] = None, 
          g: Union[int, float] = 0, 
          m: int = 1, 
          status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
          method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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


def t_naxy(mtx: mt.MortalityTable, 
           mty: mt.MortalityTable, 
           x: Union[int, float], 
           y: Union[int, float], 
           n: Union[int, float], 
           i: Optional[Union[int, float]] = None, 
           g: Union[int, float] = 0, 
           m: int = 1, 
           defer: Union[int, float] = 0, 
           status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
           method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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


def t_naaxy(mtx: mt.MortalityTable, 
            mty: mt.MortalityTable, 
            x: Union[int, float], 
            y: Union[int, float], 
            n: Union[int, float], 
            i: Optional[Union[int, float]] = None, 
            g: Union[int, float] = 0, 
            m: int = 1, 
            defer: Union[int, float] = 0, 
            status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
            method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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
def nExy(mtx: mt.MortalityTable, 
         mty: mt.MortalityTable, 
         x: Union[int, float], 
         y: Union[int, float], 
         i: Optional[Union[int, float]] = None, 
         n: Union[int, float] = 1, 
         status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
         method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the actuarial present value of a pure endowment for two lives.

    This function computes the expected present value of a unit capital paid
    after n years if the group condition is satisfied at that time.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    y : Union[int, float]
        Current age of life y.
    i : Optional[Union[int, float]], default=None
        Technical interest rate as a percentage (e.g., 2 for 2%).
    n : Union[int, float], default=1
        Number of years until the endowment payment.
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Survival condition:
        - 'joint-life': Both lives must survive
        - 'last-survivor': At least one life must survive
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Actuarial expected present value of the pure endowment.

    Notes
    -----
    A pure endowment pays a benefit only if the specified survival condition
    is met at the end of the term. No benefit is paid if the condition fails.

    Examples
    --------
    >>> nExy(mt_male, mt_female, 30, 28, i=3, n=10, status='joint-life')
    0.65
    >>> nExy(mt_male, mt_female, 65, 62, i=3, n=5, status='last-survivor')
    0.78
    """

    if status == 'joint-life':
        return mtx.npx(x=x, n=n, method=method) * mty.npx(x=y, n=n, method=method) / \
            (1 + i / 100) ** n
    if status == 'last-survivor':
        return (1 - mtx.nqx(x=x, n=n, method=method) * mty.nqx(x=y, n=n, method=method)) / \
            (1 + i / 100) ** n


# Life Benefits - 2 heads

## Generic Term Life Insurance 2 head
def A_xy(mtx: mt.MortalityTable, 
         mty: mt.MortalityTable, 
         x: Union[int, float], 
         y: Union[int, float], 
         n: Union[int, float], 
         i: Optional[Union[int, float]] = None, 
         g: Union[int, float] = 0, 
         m: int = 1, 
         defer: Union[int, float] = 0, 
         status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
         method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the expected present value of a generic term life insurance for two lives.

    This is the core function for computing term life insurance values with
    various options for deferment, growth, and payment frequency.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    y : Union[int, float]
        Current age of life y.
    n : Union[int, float]
        Number of periods for the insurance term.
    i : Optional[Union[int, float]], default=None
        Technical interest rate as a percentage (e.g., 2 for 2%).
    g : Union[int, float], default=0
        Growth rate as a percentage for benefit increases.
    m : int, default=1
        Number of payment periods per year for benefit calculation.
    defer : Union[int, float], default=0
        Deferment period before insurance coverage begins.
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Insurance trigger condition:
        - 'joint-life': Benefit paid upon first death
        - 'last-survivor': Benefit paid upon last death
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Expected present value of the term life insurance.

    Notes
    -----
    This function uses an annuity-based calculation approach, computing the
    insurance value as the difference between a pure endowment and the
    present value of an annuity.

    Examples
    --------
    >>> A_xy(mt_male, mt_female, 30, 28, 20, i=3, status='joint-life')
    0.08
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


def Axy(mtx: mt.MortalityTable, 
        mty: mt.MortalityTable, 
        x: Union[int, float], 
        y: Union[int, float], 
        i: Optional[Union[int, float]] = None, 
        g: Union[int, float] = 0, 
        m: int = 1, 
        status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
        method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the expected present value of a whole life insurance for two lives.

    This function computes the net single premium for a life insurance that pays
    a benefit upon the occurrence of the insured event based on the group status.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    y : Union[int, float]
        Current age of life y.
    i : Optional[Union[int, float]], default=None
        Technical interest rate as a percentage (e.g., 2 for 2%).
    g : Union[int, float], default=0
        Growth rate as a percentage for benefit increases.
    m : int, default=1
        Number of payment periods per year for benefit calculation.
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Insurance trigger condition:
        - 'joint-life': Benefit paid upon first death
        - 'last-survivor': Benefit paid upon last death
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Expected present value (net single premium) of the whole life insurance.

    Notes
    -----
    - The benefit is paid at the end of the period of death
    - For contracts with geometric growth, the benefit increases by g% each period
    - For joint-life status, benefit is paid when the first life dies
    - For last-survivor status, benefit is paid when the second life dies

    Examples
    --------
    >>> Axy(mt_male, mt_female, 30, 28, i=3, status='joint-life')
    0.15
    >>> Axy(mt_male, mt_female, 65, 62, i=3, status='last-survivor')
    0.45
    """
    n = max(mtx.w, mty.w)
    return A_xy(mtx, mty, x, y, n, i, g, m, defer=0, status=status, method=method)


def Axy_(mtx: mt.MortalityTable, 
         mty: mt.MortalityTable, 
         x: Union[int, float], 
         y: Union[int, float], 
         i: Optional[Union[int, float]] = None, 
         g: Union[int, float] = 0, 
         status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
         method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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


def t_Axy(mtx: mt.MortalityTable, 
          mty: mt.MortalityTable, 
          x: Union[int, float], 
          y: Union[int, float], 
          i: Optional[Union[int, float]] = None, 
          g: Union[int, float] = 0, 
          m: int = 1, 
          defer: Union[int, float] = 0, 
          status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
          method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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


def t_Axy_(mtx: mt.MortalityTable, 
           mty: mt.MortalityTable, 
           x: Union[int, float], 
           y: Union[int, float], 
           i: Optional[Union[int, float]] = None, 
           g: Union[int, float] = 0, 
           defer: Union[int, float] = 0, 
           status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
           method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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

def nAxy(mtx: mt.MortalityTable, 
         mty: mt.MortalityTable, 
         x: Union[int, float], 
         y: Union[int, float], 
         n: Union[int, float], 
         i: Optional[Union[int, float]] = None, 
         g: Union[int, float] = 0, 
         m: int = 1, 
         status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
         method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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


def nAxy_(mtx: mt.MortalityTable, 
          mty: mt.MortalityTable, 
          x: Union[int, float], 
          y: Union[int, float], 
          n: Union[int, float], 
          i: Optional[Union[int, float]] = None, 
          g: Union[int, float] = 0, 
          status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
          method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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


def t_nAxy(mtx: mt.MortalityTable, 
           mty: mt.MortalityTable, 
           x: Union[int, float], 
           y: Union[int, float], 
           n: Union[int, float], 
           i: Optional[Union[int, float]] = None, 
           g: Union[int, float] = 0, 
           m: int = 1, 
           defer: Union[int, float] = 0, 
           status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
           method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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


def t_nAxy_(mtx: mt.MortalityTable, 
            mty: mt.MortalityTable, 
            x: Union[int, float], 
            y: Union[int, float], 
            n: Union[int, float], 
            i: Optional[Union[int, float]] = None, 
            g: Union[int, float] = 0, 
            defer: Union[int, float] = 0, 
            status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
            method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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
def nAExy(mtx: mt.MortalityTable, 
          mty: mt.MortalityTable, 
          x: Union[int, float], 
          y: Union[int, float], 
          n: Union[int, float], 
          i: Optional[Union[int, float]] = None, 
          g: Union[int, float] = 0, 
          m: int = 1, 
          status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
          method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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


def nAExy_(mtx: mt.MortalityTable, 
           mty: mt.MortalityTable, 
           x: Union[int, float], 
           y: Union[int, float], 
           n: Union[int, float], 
           i: Optional[Union[int, float]] = None, 
           g: Union[int, float] = 0, 
           status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
           method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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


def t_nAExy(mtx: mt.MortalityTable, 
            mty: mt.MortalityTable, 
            x: Union[int, float], 
            y: Union[int, float], 
            n: Union[int, float], 
            i: Optional[Union[int, float]] = None, 
            g: Union[int, float] = .0, 
            m: int = 1, 
            defer: Union[int, float] = 1, 
            status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
            method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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


def t_nAExy_(mtx: mt.MortalityTable, 
             mty: mt.MortalityTable, 
             x: Union[int, float], 
             y: Union[int, float], 
             n: Union[int, float], 
             i: Optional[Union[int, float]] = None, 
             g: Union[int, float] = .0, 
             defer: Union[int, float] = 1, 
             status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
             method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
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
def t_nIArxy(mtx: mt.MortalityTable, 
             mty: mt.MortalityTable, 
             x: Union[int, float], 
             y: Union[int, float], 
             n: Union[int, float], 
             i: Optional[Union[int, float]] = None, 
             defer: Union[int, float] = 0, 
             first_payment: Union[int, float] = 1, 
             inc: Union[int, float] = 1,
             status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
             method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the expected present value of a deferred increasing term life insurance.

    This function computes the present value of a term life insurance where
    the benefit amount increases each year by a fixed increment.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    y : Union[int, float]
        Current age of life y.
    n : Union[int, float]
        Number of periods for the insurance term.
    i : Optional[Union[int, float]], default=None
        Technical interest rate as a percentage (e.g., 2 for 2%).
    defer : Union[int, float], default=0
        Deferment period before insurance coverage begins.
    first_payment : Union[int, float], default=1
        Amount of benefit in the first year of coverage.
    inc : Union[int, float], default=1
        Annual increment to the benefit amount (in monetary units).
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Insurance trigger condition:
        - 'joint-life': Benefit paid upon first death
        - 'last-survivor': Benefit paid upon last death
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Expected present value of the increasing term life insurance.

    Notes
    -----
    The benefit paid in year k is: first_payment + (k-1) * inc
    where k is the year of death within the coverage period.

    Examples
    --------
    >>> t_nIArxy(mt_male, mt_female, 30, 28, 20, i=3, first_payment=1000, inc=50)
    850.5
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
def t_nIArxy_(mtx: mt.MortalityTable, 
              mty: mt.MortalityTable, 
              x: Union[int, float], 
              y: Union[int, float], 
              n: Union[int, float], 
              i: Optional[Union[int, float]] = None, 
              defer: Union[int, float] = 0, 
              first_payment: Union[int, float] = 1, 
              inc: Union[int, float] = 1,
              status: Literal['joint-life', 'last-survivor'] = 'joint-life', 
              method: Literal['udd', 'cfm', 'bal'] = 'udd') -> float:
    """
    Calculate the EPV of a deferred increasing term life insurance (moment of death).

    This function is similar to t_nIArxy but assumes benefits are paid at the
    moment of death rather than at the end of the year of death.

    Parameters
    ----------
    mtx : mt.MortalityTable
        Mortality table for life x.
    mty : mt.MortalityTable
        Mortality table for life y.
    x : Union[int, float]
        Current age of life x.
    y : Union[int, float]
        Current age of life y.
    n : Union[int, float]
        Number of periods for the insurance term.
    i : Optional[Union[int, float]], default=None
        Technical interest rate as a percentage (e.g., 2 for 2%).
    defer : Union[int, float], default=0
        Deferment period before insurance coverage begins.
    first_payment : Union[int, float], default=1
        Amount of benefit in the first year of coverage.
    inc : Union[int, float], default=1
        Annual increment to the benefit amount (in monetary units).
    status : {'joint-life', 'last-survivor'}, default='joint-life'
        Insurance trigger condition:
        - 'joint-life': Benefit paid upon first death
        - 'last-survivor': Benefit paid upon last death
    method : {'udd', 'cfm', 'bal'}, default='udd'
        Method for approximating fractional periods:
        - 'udd': Uniform distribution of deaths
        - 'cfm': Constant force of mortality
        - 'bal': Balducci assumption

    Returns
    -------
    float
        Expected present value of the increasing term life insurance
        with benefits paid at the moment of death.

    Notes
    -----
    This version accounts for the timing difference between payment at
    the moment of death versus at the end of the year of death.

    Examples
    --------
    >>> t_nIArxy_(mt_male, mt_female, 30, 28, 20, i=3, first_payment=1000, inc=50)
    865.2
    """

    return t_nIArxy(mtx, mty, x, y, n, i, defer, first_payment, inc, status, method) * (1 + i / 100) ** .5