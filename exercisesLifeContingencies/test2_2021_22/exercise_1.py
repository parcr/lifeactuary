'''
\item
\label{exer.Makehams_lifeInsurance1_compare}
Considering \textbf{Makehams law of mortality} with $A=0.00018,B=1.9E-6$ and $c=1.124$, with $w=115$ and a rate of
interest of $2.5\%$/annum, determine:

\begin{enumerate}
\item The single risk premium for a Pure Endowment purchased by a life aged 45, if $250\:000$\euro\ are payable
on reaching 60 years old.

\item The 10 years leveled risk premiums for a Whole Life Insurance purchased by a life aged 50,
paying $250\:000$\euro\ at the moment of death.

\item The 10 years monthly leveled risk premiums for an Endowment Insurance purchased by a life
aged 50 if the payment in the event of death happens at the final of semester of the death with capital underwritten
$100\:000$\euro.
\end{enumerate}
'''

import pandas as pd
from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.0003, b=1.0E-6, c=1.09)

e0 = mml.moments_Tx()
print('e0=', e0)

w = 125
interest_rate = 2.5
interest_rate_2 = ((1 + interest_rate / 100) ** 2 - 1) * 100
capital = 100000

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
\item The single risk premium for a Pure Endowment purchased by a life aged 45, 
if $250\:000$\euro\ are payable on reaching 60 years old.
'''
capital_pure_endowment = 250000
x = 45
term = 15

pure_endowment = ct.nEx(x=x, n=term) * capital_pure_endowment
print()
print(f'D_{x}={ct.Dx[x]}')
print(f'D_{x + term}={ct.Dx[x + term]}')
print('pure_endowment=', round(pure_endowment, 5))

'''
\item The 10 years leveled risk premiums for a Whole Life Insurance purchased by a life aged 50, 
paying $250\:000$\euro\ at the moment of death.
'''
capital_whole_life_insurance = 250000
x = 50
annuity_terms = 10
annuity_fraction = 12

wli_1__ = mml.Ax(x=x, interest_rate=interest_rate)
wli_1_w = mml.Ax(x=x, interest_rate=interest_rate, n=w)
wli_1_eoy = ct.Ax(x=x)

print()
print('wli_1__=', wli_1__)
print('wli_1_w=', wli_1_w)
print('wli_1_eoy=', wli_1_eoy)

pure_whole_life_insurance = wli_1__ * capital_whole_life_insurance
print('pure_whole_life_insurance=', round(pure_whole_life_insurance, 5))

tad_12 = mml.annuity(x=x, interest_rate=interest_rate, age_first_instalment=x,
                      terms=annuity_terms, fraction=annuity_fraction, w=w * 2)
tad_1 = mml.annuity(x=x, interest_rate=interest_rate, age_first_instalment=x, terms=annuity_terms, fraction=1, w=w * 2)
tad_1_ = mml.ax(x=x, interest_rate=interest_rate, n=annuity_terms)

print('tad_12=', tad_12)
print('tad_1=', tad_1)
print('tad_1_=', tad_1_)

print('wli_1__leveled=', pure_whole_life_insurance / tad_1)
print(411.10086350538955 * annuity_terms * annuity_fraction)

'''
\item The 10 years monthly leveled risk premiums for an Endowment Insurance purchased by a life aged 50 
if the payment in the event of death happens at the final of semester of the death with 
capital underwritten $100\:000$\euro.
\end{enumerate}
'''
capital_endowment_insurance = 100000
x = 50
term_2 = 10
life_insurance_fraction = 2
annuity_terms = 10
annuity_fraction = 12

pure_endowment_2 = ct.nEx(x=x, n=term_2)
pure_endowment_3 = mml.nEx(x=x, interest_rate=interest_rate, defer=term_2)
term_life_insurance = mml.Ax(x=x, interest_rate=interest_rate, n=term_2)
endowment = mml.Endowment(x=x, interest_rate=interest_rate, n=term_2)

term_life_insurance_frac = mml.life_insurance(x=x, interest_rate=interest_rate, age_first_instalment=x,
                                              terms=term_2, fraction=life_insurance_fraction)

tad_12 = mml.annuity(x=x, interest_rate=interest_rate, age_first_instalment=x,
                      terms=annuity_terms, fraction=annuity_fraction, w=w * 2)
print()
print('term_life_insurance=', term_life_insurance)
print('pure_endowment_2=', pure_endowment_2)
endowment_capital = endowment * capital_endowment_insurance
print('endowment_capital=', endowment_capital)
premium_leveled = endowment_capital / tad_12 / annuity_fraction
print('premium_leveled=', premium_leveled)
print('compare Premium vs Leveled Premium:', premium_leveled * annuity_terms * annuity_fraction - endowment_capital)

print()
print('term_life_insurance_frac=', term_life_insurance_frac)
endowment_frac = term_life_insurance_frac + pure_endowment_2
print('endowment_frac=', endowment_frac)
endowment_frac_capital = endowment_frac * capital_endowment_insurance
print('endowment_frac_capital=', round(endowment_frac_capital, 5))
premium_leveled_frac = endowment_frac_capital / tad_12 / annuity_fraction
print('premium_leveled_frac=', premium_leveled_frac)
print('compare Premium vs Leveled Premium:', premium_leveled_frac * annuity_terms * annuity_fraction -
      endowment_capital)