'''
\item Consider a \textbf{woman} aged 30 years old that purchases an Endowment with term at 65 years old. Considering $2\%$/annum as rate of interest and justifying all calculus, please determine:

\begin{enumerate}
\item For a capital of $500\:000$\euro, the monthly leveled risk premiums paid 25 years if in case of death the capital is paid at the moment of death.

\item For a capital of $100\:000$\euro, where in case of death the capital is paid at the end of the year of death, the probability that the present value of this (risk) liability is larger than its expected present value.

\item For a capital of $500\:000$\euro, the single risk premium if in case of death the capital is paid at the end of the year but considering that the cover is deferred until the age of 40, keeping the term age at 65.
\end{enumerate}
'''

import numpy as np
from plotCDF.discrete import plot
import os
import sys

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 2
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]
# ages = np.linspace(start=20, stop=40, num=5, dtype=int)

table_index = 1  # woman
'''
\item For a capital of $100\:000$\euro, where in case of death the capital is paid at the end of the year of death, 
the probability that the present value of this (risk) liability is larger than its expected present value. 

'''

x = 30
term = 35
annuity_terms = 25
annuity_fraction = 12
capital = 500000

tad_1 = ct_lst[table_index].naax(x=x, n=annuity_terms, m=1)
tad_12 = ct_lst[table_index].naax(x=x, n=annuity_terms, m=annuity_fraction)
endowment_ = ct_lst[table_index].nAEx_(x=x, n=term)
pure_endowment = ct_lst[table_index].nEx(x=x, n=term)
tli_ = ct_lst[table_index].nAx_(x=x, n=term)
single_premium_capital = endowment_ * capital
leveled_premium_capital = single_premium_capital / tad_12 / annuity_fraction

print('\n q1')
print('term life insurance_:', round(tli_, 10))
print('pure_endowment:', round(pure_endowment, 10))
print('single_premium_unit:', round(endowment_, 10))
print('test:', (tli_ + pure_endowment) - endowment_)
print('single_premium_capital:', round(single_premium_capital, 5))
print('tad_12:', round(tad_12, 10))
print('leveled_premium_capital:', round(leveled_premium_capital, 5))

'''
\item For a capital of $500\:000$\euro, the single risk premium if in case of death the capital is paid at the 
end of the year but considering that the cover is deferred until the age of 40, keeping the term age at 65.
'''
print('\n q2')
endow = ct_lst[table_index].nAEx(x=x, n=term)
v = 1 / (1 + interest_rate / 100)
support = [v ** j for j in range(1, term + 1)]
support.reverse()
pmf = [ct_lst[table_index].t_nqx(x=x, t=j - 1, n=1) for j in range(1, term)]
pmf.append(ct_lst[table_index].npx(x=x, n=term - 1))
pmf.reverse()
cdf = np.cumsum(pmf)

print('endowment:', round(endow, 10))
print('support', support)
print('pmf:', pmf)
print('cdf', cdf)
epv_lst = [pmf[j] * support[j] for j in range(0, term)]
print('expected present value:', sum(epv_lst))
print('test:', sum(epv_lst) - endow)
cut_year = np.log(endow) / np.log(v)
print('cut_year:', cut_year)
print('cut_probability:', round(ct_lst[table_index].npx(x=x, n=term - 1), 10))
print('answer:', round(1 - ct_lst[table_index].npx(x=x, n=term - 1), 10) * 100, '%', sep='')

# another way
probs_bool = [pmf[idx_v] for idx_v, v in enumerate(support) if v > endow]
print('answer:', round(sum(probs_bool), 10) * 100, '%', sep='')

# some graphics
discrete_rv = plot.RV(support=support, prob=pmf, complete_left=True, complete_right=True, max_tol=1e-12)
discrete_rv.plot_pmf(rv_name='Z')
discrete_rv.plot_cdf(rv_name='Z')
discrete_rv.plot_sf(rv_name='Z')
discrete_rv.plot_quantile(rv_name='Z')

'''
\item For a capital of $500\:000$\euro, the single risk premium if in case of death the capital is paid at the 
end of the year but considering that the cover is deferred until the age of 40, keeping the term age at 65.
'''

print('\n q3')
defer = 10
term = term - defer
deferment_factor = ct_lst[table_index].nEx(x=x, n=defer)
pure_endowment = ct_lst[table_index].nEx(x=x + defer, n=term)
term_life_insurance_ = ct_lst[table_index].nAx_(x=x + defer, n=term)
term_life_insurance = ct_lst[table_index].nAx(x=x + defer, n=term)
endowment = ct_lst[table_index].t_nAEx(x=x, n=term, defer=defer)

print(f'{table_names[table_index]} deferment_factor: {deferment_factor}')
print(f'{table_names[table_index]} term_life_insurance: {term_life_insurance}')
print(f'{table_names[table_index]} term_life_insurance_: {term_life_insurance_}')
print(f'{table_names[table_index]} pure_endowment: {pure_endowment}')
print(f'{table_names[table_index]} endowment: {endowment}')
print(f'{table_names[table_index]}: {endowment * capital}')
print('test=', deferment_factor * (term_life_insurance + pure_endowment) - endowment)
print()
