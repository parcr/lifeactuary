import pandas as pd
from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt
import os
import sys

"""
Considering \textbf{Makehams law of mortality} with $A=0.0025,B=2.5E-6$ and $c=1.07$ with a rate of interest of 
$3.5\%$/annum, determine: 
"""

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.0025, b=2.5E-6, c=1.07)

e0 = mml.moments_Tx()
print('e0=', e0)

w = 125
interest_rate = 3.5
interest_rate_2 = ((1 + interest_rate / 100) ** 2 - 1) * 100
x = 45
v = 1 / (1 + interest_rate / 100)
v2 = 1 / (1 + interest_rate_2 / 100)

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

'''
\item {\tiny (2)} The single risk premium for a Whole Life Insurance purchased by a life aged 55, with capital 
$100\:000$\euro\ payable at the moment of death.
'''
capital_wli = 100000
x_wli = 55

wli_eoy = ct.Ax(x_wli)  # payment at the end of year
wli_eoy_capital = wli_eoy * capital_wli
wli = ct.Ax_(x_wli)  # approximation to payment at the moment of death
wli_capital = ct.Ax_(x_wli) * capital_wli  # approximation to payment at the moment of death
wli_ = mml.Ax(x=x_wli, interest_rate=interest_rate, n=np.inf)
wli_capital_ = wli_ * capital_wli

print('\n1a')
print(f'D_{x_wli}={ct.Dx[x_wli]}')
print(f'M_{x_wli}={ct.Mx[x_wli]}')
print('whole life insurance (end of the year)=', round(ct.Mx[x_wli] / ct.Dx[x_wli] * capital_wli, 5))
print('whole life insurance (end of the year)=', round(wli_eoy_capital, 5))
print('whole life insurance (approximation moment of death)=', round(wli, 10))
print('whole life insurance (approximation moment of death)=', round(wli_capital, 5))
print('whole life insurance (moment of death)=', round(wli_, 10))
print('whole life insurance (approximation moment of death)=', round(wli_capital_, 5))

"""
\item {\tiny (2)} The risk premiums for an Endowment purchased by a life aged 50 with a term of 15 years and capital 
of $250\:000$\euro\ that, in case of death, pays at the end of the quarter in which the death occurred.
"""

print('\n1b')
capital_endow = 250000
x_endow = 50
term_endow = 15
m_endow = 4

# tli_ = ct.nAx_(x=x_endow, n=term_endow)
tli_ = mml.Ax(x=x_endow, interest_rate=interest_rate, n=term_endow)
pure_endow = ct.nEx(x=x_endow, n=term_endow)
endow_mod = tli_ + pure_endow
endow_mod_capital = endow_mod*capital_endow
endow_mod2 = ct.nAEx_(x=x_endow, n=term_endow)
endow_mod2_capital = endow_mod * capital_endow
print(f'{tli_}+{pure_endow}={endow_mod}')
print(f'endow_mod2_capital: {round(endow_mod_capital, 5)}')

# when the claim in case of death happens at the end of the quarter
tli_quarter = mml.life_insurance(x=x_endow, interest_rate=interest_rate, age_first_instalment=x_endow,
                                 terms=term_endow, fraction=m_endow)
endow_eoq = tli_quarter + pure_endow
endow_eoq_capital = endow_eoq * capital_endow

print(f'Term Life Insurance + Pure Endowment={tli_quarter}+{pure_endow}={endow_eoq}')
print(f'Endowment Capital={round(endow_eoq_capital, 5)}')

"""
\item {\tiny (2)} The 10-year monthly leveled risk premiums for the previous liability. 
\textcolor{blue}{\textbf{Note:}} if you didn't solve the previous questions, please use a single risk premium of $100\:000$\euro.
"""

print('\n1c')
term_annuity = 10
fraction_annuity = 12
tad = mml.annuity(x=x_endow, interest_rate=interest_rate, age_first_instalment=x_endow,
                  terms=term_annuity, fraction=fraction_annuity)
print(f'Term Annuity Due={tad}')
print(f'Term Annuity Duex{fraction_annuity}={tad*fraction_annuity}')
print(f'Leveled Premium={round(endow_eoq_capital / tad / fraction_annuity, 5)}')
