import pandas as pd
from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt
from annuities_certain import annuities_certain
import os
import sys

"""
\item
Considering \textbf{Makehams law of mortality} with $A=0.0035,B=1.3E-6$ and $c=1.07$ with a rate of interest of 
$2.1\%$/annum, determine:

\begin{enumerate}
\item {\tiny (2)} The single risk premium for a Whole Life Insurance purchased by a life aged 40, with a capital of 
$100\:000$\euro\, payable at the moment of death.

\item {\tiny (2)} The risk premiums for an Endowment, purchased by a life aged 45, with a term of 20 years and a 
capital of $320\:000$\euro\ that, in case of death, pays at the end of the month in which the death occurred.

\item {\tiny (2)} The net single premium for an annuity due for a (55) years old today, deferred 10 years, 
that pays $1\:000$\euro, monthly.  
\end{enumerate}
"""

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.0035, b=1.3E-6, c=1.07)

e0 = mml.moments_Tx()
print('e0=', e0)

w = 125
interest_rate = 2.1
interest_rate_2 = ((1 + interest_rate / 100) ** 2 - 1) * 100

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
\item {\tiny (2)} The single risk premium for a Whole Life Insurance purchased by a life aged 40, with a capital 
of $100\:000$\euro\, payable at the moment of death.
"""
capital_wli = 100000
x_wli = 40

wli_eoy = ct.Ax(x_wli)  # payment at the end of year
wli_eoy_capital = wli_eoy * capital_wli
wli = ct.Ax_(x_wli)  # payment at the moment of death
wli_capital = ct.Ax_(x_wli) * capital_wli  # payment at the moment of death

print('\n1a')
print(f'D_{x_wli}={ct.Dx[x_wli]}')
print(f'M_{x_wli}={ct.Mx[x_wli]}')
print('whole life insurance (end of the year)=', round(ct.Mx[x_wli] / ct.Dx[x_wli] * capital_wli, 5))
print('whole life insurance (end of the year)=', round(wli_eoy_capital, 5))
print('whole life insurance (moment of death)=', round(wli, 10))
print('whole life insurance (moment of death)=', round(wli_capital, 5))

"""
\item {\tiny (2)} The risk premiums for an Endowment, purchased by a life aged 45, with a term of 20 years and a 
capital of $320\:000$\euro\ that, in case of death, pays at the end of the month in which the death occurred.
"""
print('\n1b')
capital_endow = 320000
x_endow = 45
term_endow = 20
m_endow = 12

tli_ = ct.nAx_(x=x_endow, n=term_endow)
pure_endow = ct.nEx(x=x_endow, n=term_endow)
endow_mod = tli_ + pure_endow
endow_mod2 = ct.nAEx_(x=x_endow, n=term_endow)
endow_mod2_capital = endow_mod2 * capital_endow
print(f'{tli_}+{pure_endow}={endow_mod}={endow_mod2}')
print(f'endow_mod2_capital: {round(endow_mod2_capital, 5)}')

# when the claim in case of death happens at the end of the month
tli_month = mml.life_insurance(x=x_endow, interest_rate=interest_rate, age_first_instalment=x_endow,
                               terms=term_endow, fraction=m_endow)
endow_eoq = tli_month + pure_endow
endow_eoq_capital = endow_eoq * capital_endow

print(f'Term Life Insurance + Pure Endowment={tli_month}+{pure_endow}={endow_eoq}')
print(f'Endowment Capital={round(endow_eoq_capital, 5)}')

"""
\item {\tiny (2)} The net single premium for an annuity due for a (55) years old today, deferred 10 years, 
that pays $1\:000$\euro, monthly.
"""
x_annuity = 55
annuity_defer = 10
fraction_annuity = 12
capital_annuity_monthly = 1000
term_annuity = np.inf
annuity_w = 125+75
tad = mml.annuity(x=x_annuity, interest_rate=interest_rate, age_first_instalment=x_annuity + annuity_defer,
                  terms=term_annuity, fraction=fraction_annuity, w=annuity_w)

print('\n1c')

print(f'Term Annuity Due (closing table at {annuity_w}): {tad}')
print(f'Leveled Premium={round(tad * capital_annuity_monthly*fraction_annuity, 5)}')
