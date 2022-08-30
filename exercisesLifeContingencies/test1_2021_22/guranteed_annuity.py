import os
import sys

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst
from annuities_certain import annuities_certain

this_py = os.path.split(sys.argv[0])[-1][:-3]

table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 4
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

table_idx = 1
name = table_names[2]
lt = lt_lst[table_idx]
ct = ct_lst[table_idx]

lt.df_life_table().to_excel(excel_writer=name + '.xlsx', sheet_name=name,
                            index=False, freeze_panes=(1, 1))
ct.df_commutation_table().to_excel(excel_writer=name + '_comm' + '.xlsx', sheet_name=name,
                                   index=False, freeze_panes=(1, 1))

capital = 10000
ac = annuities_certain.Annuities_Certain(interest_rate=interest_rate, m=1)
ac5 = ac.aan(terms=5)
print('renda certa', ac5)
renda_vital = ct.aax(x=70)
print('renda vital', renda_vital)
renda_vital_def = ct.t_aax(x=70, m=1, defer=5)
print('renda vital def', renda_vital_def)
b_guarantee = renda_vital / (ac5 + renda_vital_def)
print('b_guarantee', b_guarantee * capital)

reduction = capital * (1 - renda_vital / (ac5 + renda_vital_def))
print(f'reduction', reduction)
print(f'reduction', capital - b_guarantee*capital)
