from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import scipy.integrate
import os
import sys

"""
item Consider the Insurer MMAct that prices its annuities  with the assumptions, defined in question 2.  
Justifying all, please determine
\begin{enumerate}
\item  {\tiny (2)} The net single premium considering that a couple of ages (55) and (52) buy a whole life annuity 
due that pays continuously $10\:000$\euro, per year while both are alive.

\item  {\tiny (2)} The net single premium considering that a life (55) buys a whole life annuity due that pays 
continuously $10\:000$\euro,  to a life (53) in the event of (53) surviving to (55).

\item  {\tiny (1)} The probability that a whole life annuity due, deferred by 10 years, that pays $10\:000$\euro, 
per year, bought by (55) has a present value smaller than $300\:000$\euro.
\end{enumerate}
"""

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.0035, b=1.3E-6, c=1.07)

e0 = mml.moments_Tx()
print('e0=', e0)

w = 125
interest_rate = 2.1
interest_rate_2 = ((1 + interest_rate / 100) ** 2 - 1) * 100
v = 1 / (1 + interest_rate / 100)
v_2 = 1 / (1 + interest_rate_2 / 100)
d = 1 - v

'''
Compute Life Table
'''
px = np.array([mml.S(x, t=1) for x in range(0, w)])
qx = 1 - px
lt = mortality_table.MortalityTable(mt=list(np.append(0, qx)))
lt.df_life_table().to_excel(excel_writer='makeham' + '.xlsx', sheet_name='makeham',
                            index=False, freeze_panes=(1, 1))
ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=list(np.append(0, qx)))
ct.df_commutation_table().to_excel(excel_writer='makeham_comm' + '.xlsx', sheet_name='makeham',
                                   index=False, freeze_panes=(1, 1))
ct_2 = commutation_table.CommutationFunctions(i=interest_rate_2, g=0, mt=list(np.append(0, qx)))

"""
\item  {\tiny (2)} The net single premium considering that a couple of ages (55) and (52) buy a whole life annuity 
due that pays continuously $10\:000$\euro, per year while both are alive.
"""
capital_axy = 10000
x_old = 55
x_new = 52


def a_TxTy(x, y, t):
    return mml.S(x, t) * mml.S(y, t)


def a_xy(x, y, t):
    def S(t):
        return a_TxTy(x, y, t) * np.power(v, t)

    return scipy.integrate.quad(S, 0, t)[0]


print('\n1a')
wlad_xy_ = a_xy(x=x_old, y=x_new, t=np.inf)

print('whole life annuity due =', wlad_xy_)
print('whole life annuity due capital =', round(wlad_xy_ * capital_axy, 5))

"""
\item  {\tiny (2)} The net single premium considering that a life (55) buys a whole life annuity due that pays 
continuously $10\:000$\euro,  to a life (53) in the event of (53) surviving to (55).
"""
print('\n1b')

wlad_y_ = mml.ax(x=x_new, interest_rate=interest_rate, n=np.inf)[0]
print('whole life annuity due_y_ =', wlad_y_)
print('whole life annuity due_x|y_ =', wlad_y_ - wlad_xy_)
print('whole life annuity due_x|y_ capital =', round((wlad_y_ - wlad_xy_) * capital_axy, 5))

"""
\item  {\tiny (1)} The probability that a whole life annuity due, deferred by 10 years, that pays $10\:000$\euro, 
per year, bought by (55) has a present value smaller than $300\:000$\euro.  
"""
print('\n1c')
deferred_x_old = 10
wlad = mml.annuity(x=x_old, interest_rate=interest_rate, age_first_instalment=x_old + deferred_x_old,
                   terms=np.inf, fraction=1, w=130)
wlad_max_value = v ** deferred_x_old / (interest_rate * v / 100)
maximum_period = deferred_x_old - 1 + np.log(1 - 30 * d / v ** deferred_x_old) / np.log(v)
prob = (1-mml.S(x=x_old, t=int(maximum_period) + 1))

print(f'Expected Value of {wlad} in "{"{0}"}" U [{v ** deferred_x_old}, {wlad_max_value}]')
print(f'Expected Value of {wlad * capital_axy} capital in [0, {wlad_max_value * capital_axy}]')
print(f'Maximum period allowed {maximum_period}, hence, a total number of '
      f'{int(maximum_period) - deferred_x_old + 1} installments with probability '
      f'{round(prob*100, 5)}%.')
