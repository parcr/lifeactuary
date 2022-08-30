'''
\item Consider a \textbf{man} aged 25 years old that purchases an Endowment with term at 65 years old. Considering $3\%$/annum as rate of interest and justifying all calculus, please determine:

\begin{enumerate}
\item For a capital of $1\:000\:000$\euro, the single risk premium if in case of death the capital is paid at the moment of death.

\item For a capital of $1\:000\:000$\euro, the single risk premium if in case of death the capital is paid at the moment of death but considering that the cover is deferred until the age of 30, keeping the same term.
\end{enumerate}
'''
import os
import sys

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
interest_rate = 3
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

'''
\item For a capital of $1\:000\:000$\euro, the single risk premium 
if in case of death the capital is paid at the moment of death.
'''

x = 25
term = 40
capital = 1000000

for idx, lt in enumerate(lt_lst):
    pure_endowment = ct_lst[idx].nEx(x=x, n=term)
    term_life_insurance_ = ct_lst[idx].nAx_(x=x, n=term)
    term_life_insurance = ct_lst[idx].nAx(x=x, n=term)
    endowment = ct_lst[idx].nAEx_(x=x, n=term)

    print(f'{table_names[idx]}: {term_life_insurance}')
    print(f'{table_names[idx]}: {term_life_insurance_}')
    print(f'{table_names[idx]}: {pure_endowment}')
    print(f'{table_names[idx]}: {endowment * 1000000}')
    print()

'''
\item For a capital of $1\:000\:000$\euro, the single risk premium if in case of death the capital 
is paid at the moment of death but considering that the cover is deferred until the age of 30, keeping the same term.
'''
print('_________________')
x = 25
defer = 5
term = 40 - defer
capital = 1000000

for idx, lt in enumerate(lt_lst):
    deferment_factor = ct_lst[idx].nEx(x=x, n=defer)
    pure_endowment = ct_lst[idx].nEx(x=x + defer, n=term)
    term_life_insurance_ = ct_lst[idx].nAx_(x=x+defer, n=term)
    term_life_insurance = ct_lst[idx].nAx(x=x+defer, n=term)
    endowment = ct_lst[idx].t_nAEx_(x=x, n=term, defer=defer)

    print(f'{table_names[idx]}: {deferment_factor}')
    print(f'{table_names[idx]}: {term_life_insurance}')
    print(f'{table_names[idx]}: {term_life_insurance_}')
    print(f'{table_names[idx]}: {pure_endowment}')
    print(f'{table_names[idx]}: {endowment * 1000000}')
    print('test=', deferment_factor * (term_life_insurance_ + pure_endowment) - endowment)
    print()
