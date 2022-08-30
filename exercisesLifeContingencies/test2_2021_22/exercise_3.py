'''\item Consider a \textbf{woman} aged 35 years old that purchases an insurance for a loan of  $200\:000$\euro, that will be paid in yearly equal instalments with a 20 years term and an agreed $4\%$/annum rate of interest. Justifying all calculus, please determine:

\begin{enumerate}
\item The yearly leveled premiums throughout the contract term.

\item The loss for the insurer the lady dies immediately after paying the $10^{th}$ instalment.
\end{enumerate}
'''

import numpy as np
from annuities_certain import annuities_certain
import pandas as pd
import os
import sys

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 4
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]
# ages = np.linspace(start=20, stop=40, num=5, dtype=int)

'''
Prepare the solution for Equal Instalments
'''
ages = np.linspace(start=35, stop=35, num=1, dtype=int)
capital = 200000
terms = 20

ac = annuities_certain.Annuities_Certain(interest_rate=interest_rate, m=1)
ac_certain = ac.an(terms=terms)
equal_instalments_dict = {'table': [], 'x': [], 'annuity_certain': [], 'annuity': [], 'premium': [],
                          'annuity_level': [], 'premium_leveled': []}

for id_ct, ct in enumerate(ct_lst):
    for id_x, x in enumerate(ages):
        equal_instalments_dict['table'].append(table_names[id_ct])
        equal_instalments_dict['x'].append(x)
        equal_instalments_dict['annuity_certain'].append(ac_certain)
        annuity = ct.nax(x=x, n=terms, m=1)
        equal_instalments_dict['annuity'].append(annuity)
        premium = capital - capital * annuity / ac_certain
        equal_instalments_dict['premium'].append(premium)
        annuity_level = ct.naax(x=x, n=terms, m=1)
        equal_instalments_dict['annuity_level'].append(annuity_level)
        equal_instalments_dict['premium_leveled'].append(premium / annuity_level)

equal_instalments_df = pd.DataFrame(equal_instalments_dict)
equal_instalments_df.to_excel(excel_writer='equal_instalments' + '.xlsx',
                              sheet_name='equal_instalments',
                              index=False, freeze_panes=(1, 1))

'''
Prepare the solution for Equal Amortizations
'''

equal_amortizations_dict = {'table': [], 'x': [], 'life_ins': [], 'life_ins_inc': [], 'premium': [],
                            'annuity_level': [], 'premium_leveled': []}

for id_ct, ct in enumerate(ct_lst):
    for id_x, x in enumerate(ages):
        equal_amortizations_dict['table'].append(table_names[id_ct])
        equal_amortizations_dict['x'].append(x)
        life_ins = ct.nAx(x=x, n=terms)
        equal_amortizations_dict['life_ins'].append(life_ins)
        life_ins_inc = ct.nIAx(x=x, n=terms)
        equal_amortizations_dict['life_ins_inc'].append(life_ins_inc)
        premium = capital * (1 + interest_rate / 100) / terms * ((terms + 1) * life_ins - life_ins_inc)
        equal_amortizations_dict['premium'].append(premium)
        annuity_level = ct.naax(x=x, n=terms, m=1)
        equal_amortizations_dict['annuity_level'].append(annuity_level)
        equal_amortizations_dict['premium_leveled'].append(premium / annuity_level)

equal_amortizations_df = pd.DataFrame(equal_amortizations_dict)
equal_amortizations_df.to_excel(excel_writer='equal_amortizations' + '.xlsx',
                                sheet_name='equal_amortizations',
                                index=False, freeze_panes=(1, 1))

'''
\item The loss for the insurer the lady dies immediately after paying the $10^{th}$ instalment.
'''
annuity_terms = 10
annuities_certain_m = ac.an(terms=annuity_terms)
annuities_certain_n_m = ac.an(terms=terms - annuity_terms)

loan_balance = capital / ac_certain * annuities_certain_n_m
premiums_paid = equal_instalments_dict['premium_leveled'][1] * annuities_certain_m * (
            1 + interest_rate / 100) ** annuity_terms
print('loan balance=', loan_balance)
print('premiums paid=', premiums_paid)
print('Loss=', loan_balance - premiums_paid)
