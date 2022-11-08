import os
import sys

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95', 'GRM80']
interest_rate = 2
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

table_idx = 1
name = table_names[table_idx]
print(f'The Table being used is {name}')
lt = lt_lst[table_idx]
ct = ct_lst[table_idx]

lt.df_life_table().to_excel(excel_writer=name + '.xlsx', sheet_name=name,
                            index=False, freeze_panes=(1, 1))
ct.df_commutation_table().to_excel(excel_writer=name + '_comm' + '.xlsx', sheet_name=name,
                                   index=False, freeze_panes=(1, 1))

capital = 4000
x = 60
defer = 5
temp = 20
m = 4

renda_def = ct.naax(x=x + defer, n=temp, m=1)
nEx = ct.nEx(x=x + defer, n=temp)
renda_def_frac = renda_def - (m - 1) / (2 * m) * (1 - nEx)
print(f'renda_def=', renda_def)
print(f'nEx=', nEx)
print(f'renda_def_frac=', renda_def_frac)
print(f'Capital renda_def_frac=', renda_def_frac * capital)
nEx_2 = ct.nEx(x=x, n=defer)
print(f'nEx_2=', nEx_2)
print(f'renda_def_frac_2=', renda_def_frac * nEx_2)
print(f'Capital renda_def_frac_2=', renda_def_frac * capital * nEx_2)

print()
renda_def = ct.t_naax(x=x, n=temp, m=1, defer=defer)
renda_def_frac = ct.t_naax(x=x, n=temp, m=m, defer=defer)

print(f'renda_def=', renda_def)
print(f'renda frac=', renda_def_frac)
print(f'capital frac=', renda_def_frac * capital)
