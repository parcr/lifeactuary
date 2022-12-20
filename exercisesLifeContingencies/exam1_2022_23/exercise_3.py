import os
import sys

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

"""
\item Consider a \textbf{woman} aged 40 years old that purchases an Endowment with term at 65 years old. 
Considering $2.4\%$/annum as the rate of interest and justifying all calculus, please determine:

\begin{enumerate}
\item For a capital of $150\:000$\euro, the single risk premium if in case of death the capital is paid 
at the moment of death.

\item The monthly leveled premiums paid throughout 10 years.
\end{enumerate}
"""

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 2.4
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

"""
\item For a capital of $150\:000$\euro, the single risk premium if in case of death the capital is paid 
at the moment of death.
"""

x = 40
term = 25
capital = 150000

print('\na')
for idx, lt in enumerate(lt_lst):
    pure_endowment = ct_lst[idx].nEx(x=x, n=term)
    term_life_insurance_ = ct_lst[idx].nAx_(x=x, n=term)
    term_life_insurance = ct_lst[idx].nAx(x=x, n=term)
    endowment = ct_lst[idx].nAEx(x=x, n=term)
    endowment_ = ct_lst[idx].nAEx_(x=x, n=term)

    print(f'Ax: {table_names[idx]}: {term_life_insurance}')
    print(f'Ax_: {table_names[idx]}: {term_life_insurance_}')
    print(f'nEx {table_names[idx]}: {pure_endowment}')
    print(f'Ax+nEx: {table_names[idx]}: {term_life_insurance + pure_endowment}')
    print(f'Ax_+nEx: {table_names[idx]}: {term_life_insurance_ + pure_endowment}')
    print(f'nAEx {table_names[idx]}: {endowment}')
    print(f'nAEx_ {table_names[idx]}: {endowment_}')
    print(f'nAEx capital {table_names[idx]}: {round(endowment * capital, 5)}')
    print(f'nAEx_ capital {table_names[idx]}: {round(endowment_ * capital, 5)}')
    print()

print('\nb')
annuity_term = 10
annuity_fraction = 12

for idx, lt in enumerate(lt_lst):
    tad = ct_lst[idx].naax(x=x, n=annuity_term)
    tad_m = ct_lst[idx].naax(x=x, n=annuity_term, m=annuity_fraction)
    pure_endowment = ct_lst[idx].nEx(x=x, n=annuity_term)
    endowment_ = ct_lst[idx].nAEx_(x=x, n=term)

    print(f'tad: {table_names[idx]}: {tad}')
    print(f'nEx: {table_names[idx]}: {pure_endowment}')
    print(f'tad_m: {table_names[idx]}: {tad- (annuity_fraction-1)/(2*annuity_fraction)*(1-pure_endowment)}')
    print(f'tad_m: {table_names[idx]}: {tad_m}')
    print(f'premium_tad_m: {table_names[idx]}: {round(endowment_ * capital/(tad_m*annuity_fraction), 5)}')

    print()
