import numpy as np
import os
import sys

from essential_life import mortality_table, read_soa_table_xml as rst
import matplotlib.pyplot as plt

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


dif_age = 3
l0 = 100000

table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]

lt_q_min_xy = []
lt_q_max_xy = []

table_names_min_max = []
for idx_lt, lt in enumerate(lt_lst):
    l = [1 - lt.npx(x=x, n=1) * lt.npx(x=x + dif_age, n=1) for x in range(lt.w - dif_age + 1)]
    l.insert(0, 0)
    lt_q_min_xy.append(l)
    table_names_min_max.append(table_names[idx_lt] + ' joint life xy')
    l = [lt.nqx(x=x, n=1) * lt.nqx(x=x + dif_age, n=1) for x in range(lt.w - dif_age + 1)]
    l.insert(0, 0)
    lt_q_max_xy.append(l)
    table_names_min_max.append(table_names[idx_lt] + ' last survivor xy')

lt_min_lxy_lst = [mortality_table.MortalityTable(mt=mt) for mt in lt_q_min_xy]
lt_max_lxy_lst = [mortality_table.MortalityTable(mt=mt) for mt in lt_q_max_xy]

'''
Plot ex
'''
fig, axes = plt.subplots()
for idx, lt in enumerate(lt_min_lxy_lst):
    ages = np.arange(0, lt.w + 1)
    plt.plot(ages, lt.ex, label=table_names_min_max[idx * 2])

plt.xlabel(r'$x$')
plt.ylabel(r'${e}_{x}+1/2$')
plt.title('Complete Expectation of Life')
plt.grid(b='visible', which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_joint_life' + '.eps', format='eps', dpi=3600)
plt.show()

fig, axes = plt.subplots()
for idx, lt in enumerate(lt_max_lxy_lst):
    ages = np.arange(0, lt.w + 1)
    plt.plot(ages, lt.ex, label=table_names_min_max[idx * 2 + 1])

plt.xlabel(r'$x$')
plt.ylabel(r'${e}_{x}+1/2$')
plt.title('Complete Expectation of Life')
plt.grid(b='visible', which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_last_survivor' + '.eps', format='eps', dpi=3600)
plt.show()

'''
Some results
'''

print(lt_lst[0].ex[0], lt_min_lxy_lst[0].ex[0], lt_max_lxy_lst[0].ex[0])
print(lt_lst[1].ex[0], lt_min_lxy_lst[1].ex[0], lt_max_lxy_lst[1].ex[0])
print(lt_lst[2].ex[0], lt_min_lxy_lst[2].ex[0], lt_max_lxy_lst[2].ex[0])

'''
print the tables
'''

if False:
    for idx, lt in enumerate(lt_lst):
        name = parse_table_name(mt_lst[idx].name)
        lt.df_life_table().to_excel(excel_writer=name + '.xlsx', sheet_name=name,
                                    index=False, freeze_panes=(1, 1))
        lt_min_lxy_lst[idx].df_life_table().to_excel(excel_writer=name + '_min' + '.xlsx', sheet_name=name,
                                                     index=False, freeze_panes=(1, 1))
        lt_max_lxy_lst[idx].df_life_table().to_excel(excel_writer=name + '_max' + '.xlsx', sheet_name=name,
                                                     index=False, freeze_panes=(1, 1))

'''
print for some ages
'''
set_of_ages = [0, 10, 20, 40, 60, 80, 100]
#todo
