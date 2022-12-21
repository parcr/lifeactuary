'''
\item Consider a \textbf{woman} aged 45 years old that purchases an Endowment with the term at 65 years old. Considering
 $3.2\%$/annum as the rate of interest and justifying all calculus, please determine:

\begin{enumerate}
\item {\tiny (3)} For capital of $100\:000$\euro, the single risk premium if in case of death the capital is paid at
the moment of death.

\item {\tiny (2)} For capital of $100\:000$\euro, the single risk premium if in case of death the capital is paid at
the moment of death but considering that the cover is deferred until the age of 55, keeping the same duration.
\end{enumerate}
'''
import os
import sys
import numpy as np
from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
interest_rate = 3.2
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

"""
\item {\tiny (3)} For capital of $100\:000$\euro, the single risk premium if in case of death the capital is paid at
the moment of death.
"""
x = 45
term = 20
capital = 100000

print('\n2a')
for idx, lt in enumerate(lt_lst):
    pure_endowment = ct_lst[idx].nEx(x=x, n=term)
    term_life_insurance = ct_lst[idx].nAx(x=x, n=term)
    term_life_insurance_ = ct_lst[idx].nAx_(x=x, n=term)
    term_life_insurance__ = term_life_insurance * interest_rate / 100 / np.log(1 + interest_rate / 100)
    endowment = ct_lst[idx].nAEx_(x=x, n=term)
    endowment__ = term_life_insurance__ + pure_endowment
    print(f'Term Life Insurance:')
    print(f'{table_names[idx]}: {term_life_insurance}')
    print(f'{table_names[idx]}: {term_life_insurance_}')
    print(f'{table_names[idx]}: {term_life_insurance__}')
    print(f'Pure Endowment:')
    print(f'{table_names[idx]}: {pure_endowment}')
    print(f'Endowment:')
    print(f'test={term_life_insurance_ + pure_endowment - endowment}')
    print(f'{table_names[idx]}: {endowment}')
    print(f'{table_names[idx]}: {round(endowment * capital, 5)}')
    print(f'{table_names[idx]}: {round(endowment__ * capital, 5)}')
    print()

"""
\item {\tiny (2)} For capital of $100\:000$\euro, the single risk premium if in case of death the capital is paid at 
the moment of death but considering that the cover is deferred until the age of 55, keeping the same duration.
"""

print('\n2b')
x = 45
defer = 10
term = 20
capital = 100000

for idx, lt in enumerate(lt_lst):
    deferment_factor = ct_lst[idx].nEx(x=x, n=defer)
    pure_endowment = ct_lst[idx].nEx(x=x + defer, n=term)
    term_life_insurance_ = ct_lst[idx].nAx_(x=x + defer, n=term)
    term_life_insurance = ct_lst[idx].nAx(x=x + defer, n=term)
    endowment = ct_lst[idx].t_nAEx_(x=x, n=term, defer=defer)

    print(f'Deferment Factor for {table_names[idx]}: {deferment_factor}')
    print(f'Term Life Insurance eoy for {table_names[idx]}: {term_life_insurance}')
    print(f'Term Life Insurance mod for {table_names[idx]}: {term_life_insurance_}')
    print(f'Pure Endowment {table_names[idx]}: {pure_endowment}')
    print(f'Endowment {table_names[idx]}: {endowment}')
    print(f'Endowment mod {table_names[idx]}: {round(endowment * capital, 5)}')
    print('test=', deferment_factor * (term_life_insurance_ + pure_endowment) - endowment)
    print()
