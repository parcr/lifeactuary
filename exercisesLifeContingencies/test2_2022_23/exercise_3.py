import numpy as np
from annuities_certain import annuities_certain
import pandas as pd
import os
import sys

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

"""
\item Consider a \textbf{man} aged 27 years old that purchases insurance for a loan of $350\:000$\euro, that will be 
paid in yearly equal installments with a 40 years term with an agreed $6\%$/annum rate of interest. J
ustifying all calculus, please determine:
    
\begin{enumerate}
\item  {\tiny (3)} The yearly leveled premiums throughout the contract term.
    
\item  {\tiny (2)} The loss for the insurer if the lady dies immediately after paying the $10^{th}$ installment.
\end{enumerate} 
"""

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 6
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]
# ages = np.linspace(start=20, stop=40, num=5, dtype=int)

'''
Prepare the solution for Equal Instalments
'''
ages = np.linspace(start=27, stop=27, num=1, dtype=int)
capital = 350000
terms = 40

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

index_table = 2

premium_leveled = equal_instalments_dict['premium_leveled'][index_table]

print('\na)')

print(f'annuity certain:', equal_instalments_dict['annuity_certain'][index_table])
print(f'annuity:', equal_instalments_dict['annuity'][index_table])
print(f'premium:', equal_instalments_dict['premium'][index_table])
print(f'annuity_level:', equal_instalments_dict['annuity_level'][index_table])
print(f'premium leveled:', premium_leveled)

'''
\item The loss for the insurer the lady dies immediately after paying the $10^{th}$ instalment.
'''
annuity_terms = 20
annuities_certain_m = ac.aan(terms=annuity_terms)
annuities_certain_n_m = ac.aan(terms=terms - annuity_terms + 1)

loan_balance = capital / ac_certain * annuities_certain_n_m
premiums_paid = premium_leveled * annuities_certain_m * (1 + interest_rate / 100) ** annuity_terms

print('\nb)')
print(f'annuity certain {annuity_terms} terms: {annuities_certain_m}')
print(f'annuity certain {terms - annuity_terms + 1} terms: {annuities_certain_n_m}')
print('loan balance=', round(loan_balance, 5))
print('premiums paid=', round(premiums_paid, 5))
print('Loss=', round(loan_balance - premiums_paid, 5))
