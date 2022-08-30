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
Prepare the solution
1. We need all the variables
'''
capital1 = 1000
period1_0 = 0
period1_1 = 10
capital2 = 2000
period2_0 = 10
period2_1 = 20

ages = np.linspace(start=20, stop=80, num=int((80 - 20) / 10 + 1))
cap1 = capital1 * np.power(1 + interest_rate / 100, period1_1)
cap2 = capital2 * np.power(1 + interest_rate / 100, period2_1)

dict_liability = {'table': [], 'x': [], 'tpx': [], 'premium1': [], 'n_tqx': [], 'premium2': [],
                  'premium': [], 'var1': [], 'var2': [], 'cov': [], 'var': []}
for id_ct, ct in enumerate(ct_lst):
    for id_x, x in enumerate(ages):
        prob1 = ct.nqx(x=x, n=period1_1)
        prob2 = ct.t_nqx(x=x, t=period1_1, n=period2_1 - period2_0)
        premium1 = cap1 * prob1
        premium2 = cap2 * prob2
        dict_liability['table'].append(table_names[id_ct])
        dict_liability['x'].append(x)
        dict_liability['tpx'].append(prob1)
        dict_liability['premium1'].append(premium1)
        dict_liability['n_tqx'].append(prob2)
        dict_liability['premium2'].append(premium2)
        dict_liability['premium'].append(premium1 + premium2)
        dict_liability['var1'].append(cap1 ** 2 * prob1 * (1 - prob1))
        dict_liability['var2'].append(cap2 ** 2 * prob2 * (1 - prob2))
        dict_liability['cov'].append(-2 * cap1 * prob1 * cap2 * prob2)
        dict_liability['var'].append(dict_liability['var1'][-1] +
                                     dict_liability['var2'][-1] +
                                     dict_liability['cov'][-1])

df_liability = pd.DataFrame(dict_liability)
df_liability.to_excel(excel_writer='genericLifeInsuranceExample' + '.xlsx',
                      sheet_name='genericLifeInsuranceExample',
                      index=False, freeze_panes=(1, 1))
