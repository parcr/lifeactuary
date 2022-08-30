import numpy as np
import os
import sys
from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst
import matplotlib.pyplot as plt

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../../soa_tables/' + name + '.xml') for name in table_names]
mux_udd = [np.array(t.table_qx[1:]) / (1 - np.array(t.table_qx[1:])) for t in mt_lst]
mux_cfm = [-np.log(1 - np.array(t.table_qx[1:])) for t in mt_lst]

alpha = 0.95
beta = 0.001
qx_changed = [list(1 - (1 - np.array(t.table_qx[1:])) ** alpha * np.exp(-beta)) for idx_t, t in enumerate(mt_lst)]
[qx_changed[idx_t].insert(0, mt_lst[idx_t].table_qx[0]) for idx_t, t in enumerate(mt_lst)]

lt_lst = [mortality_table.MortalityTable(mt=mt) for mt in qx_changed]
ct_lst = [commutation_table.CommutationFunctions(i=4, g=0, mt=mt) for mt in qx_changed]

for idx, lt in enumerate(lt_lst):
    name = parse_table_name(mt_lst[idx].name) + '_riskChange'
    lt.df_life_table().to_excel(excel_writer=name + '.xlsx', sheet_name=name,
                                index=False, freeze_panes=(1, 1))
    ct_lst[idx].df_commutation_table().to_excel(excel_writer=name + '_comm' + '.xlsx', sheet_name=name,
                                                index=False, freeze_panes=(1, 1))

'''
Plot ex
'''
fig, axes = plt.subplots()
for idx, lt in enumerate(lt_lst):
    ages = np.arange(0, lt.w + 1)
    plt.plot(ages, lt.ex, label=table_names[idx])

plt.xlabel(r'$x$')
plt.ylabel(r'${e}_{x}+1/2$')
plt.title('Complete Expectation of Life')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_riskChange' + '.eps', format='eps', dpi=3600)
plt.show()
