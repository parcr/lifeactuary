'''
\item Consider a life aged 45 and an interest rate of $1.25\%$/year.


\begin{enumerate}
\item The 10 years leveled premiums if the life buys a 20 years Pure Endowment Insurance with premiums refund and capital $100\:000$\euro.

\item The 5 years leveled premiums if the life buys insurance for a $300\:000$\euro \: loan, that will be paid in yearly equal amortizations with a 25 years term.
\end{enumerate}
'''

import numpy as np
import pandas as pd
from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst
from annuities_certain import annuities_certain

table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 1.25
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

table_index = 0  # unisex

x = 45
term = 20
term_annuity = 10
capital = 100000

print('\nq1')
print('Leveled Net Risk Premium Refund at End of the Year of Death')
pureEndow = ct_lst[table_index].nEx(x=x, n=term)
tad = ct_lst[table_index].naax(x=x, n=term_annuity, m=1)
tli_increasing = ct_lst[table_index].nIAx(x=x, n=term_annuity)
tli_deferred = ct_lst[table_index].t_nAx(x=x, n=term - term_annuity, defer=term_annuity)
pureEndow_leveled_refund = pureEndow / (tad - tli_increasing - term_annuity * tli_deferred)

print('pureEndow:', round(pureEndow, 10))
print('tad:', round(tad, 10))
print('tli_increasing:', round(tli_increasing, 10))
print('tli_deferred:', round(tli_deferred, 10))
print('pureEndow_leveled_refund:', round(pureEndow_leveled_refund, 10))
print('pureEndow_leveled_refund_capital:', round(capital * pureEndow_leveled_refund, 5))

'''
\item The 5 years leveled premiums if the life buys insurance for a $300\:000$\euro \: loan, 
that will be paid in yearly equal amortizations with a 25 years term.
'''

'''
Prepare the solution for Equal Instalments
'''
ages = np.linspace(start=x, stop=x, num=1, dtype=int)
capital = 300000
terms = 25
terms_annuity_leveled = 5

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
        annuity_level = ct.naax(x=x, n=terms_annuity_leveled, m=1)
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
        annuity_level = ct.naax(x=x, n=terms_annuity_leveled, m=1)
        equal_amortizations_dict['annuity_level'].append(annuity_level)
        equal_amortizations_dict['premium_leveled'].append(premium / annuity_level)

equal_amortizations_df = pd.DataFrame(equal_amortizations_dict)
equal_amortizations_df.to_excel(excel_writer='equal_amortizations' + '.xlsx',
                                sheet_name='equal_amortizations',
                                index=False, freeze_panes=(1, 1))
