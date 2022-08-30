import numpy as np
import pandas as pd
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

'''
for idx, lt in enumerate(lt_lst):
    name = parse_table_name(mt_lst[idx].name)
    lt.df_life_table().to_excel(excel_writer=name + '.xlsx', sheet_name=name,
                                index=False, freeze_panes=(1, 1))
    ct_lst[idx].df_commutation_table().to_excel(excel_writer=name + '_comm' + '.xlsx', sheet_name=name,
                                                index=False, freeze_panes=(1, 1))
'''

'''
Prepare the solution for (IA)x
'''
capital = 10000
capital_inc = 1000

ages = np.linspace(start=20, stop=80, num=int((80 - 20) / 10 + 1), dtype=int)

dict_liability = {'table': [], 'x': [], 'premium1_unit': [], 'premium2_unit': [],
                  'premium1': [], 'premium2': [], 'premium': []}
for id_ct, ct in enumerate(ct_lst):
    for id_x, x in enumerate(ages):
        premium1_unit = ct.Ax(x=x)
        premium2_unit = ct.IAx(x=x)
        premium1 = premium1_unit * (capital - capital_inc)
        premium2 = premium2_unit * capital_inc
        premium = premium1 + premium2
        dict_liability['table'].append(table_names[id_ct])
        dict_liability['x'].append(x)
        dict_liability['premium1_unit'].append(premium1_unit)
        dict_liability['premium2_unit'].append(premium2_unit)
        dict_liability['premium1'].append(premium1)
        dict_liability['premium2'].append(premium2)
        dict_liability['premium'].append(premium)

df_liability = pd.DataFrame(dict_liability)
df_liability.to_excel(excel_writer='IAx_lifeTables3' + '.xlsx',
                      sheet_name='IAx_lifeTables3',
                      index=False, freeze_panes=(1, 1))

'''
Prepare the solution for (IA)x:n
'''
term = 10

dict_liability_term = {'table': [], 'x': [], 'premium1_unit': [], 'premium2_unit': [],
                  'premium1': [], 'premium2': [], 'premium': []}
for id_ct, ct in enumerate(ct_lst):
    for id_x, x in enumerate(ages):
        premium1_unit = ct.nAx(x=x, n=term)
        premium2_unit = ct.nIAx(x=x, n=term)
        premium1 = premium1_unit * (capital - capital_inc)
        premium2 = premium2_unit * capital_inc
        premium = premium1 + premium2
        dict_liability_term['table'].append(table_names[id_ct])
        dict_liability_term['x'].append(x)
        dict_liability_term['premium1_unit'].append(premium1_unit)
        dict_liability_term['premium2_unit'].append(premium2_unit)
        dict_liability_term['premium1'].append(premium1)
        dict_liability_term['premium2'].append(premium2)
        dict_liability_term['premium'].append(premium)

df_liability_term = pd.DataFrame(dict_liability_term)
df_liability_term.to_excel(excel_writer='nIAx_lifeTables3' + '.xlsx',
                      sheet_name='nIAx_lifeTables3',
                      index=False, freeze_panes=(1, 1))
