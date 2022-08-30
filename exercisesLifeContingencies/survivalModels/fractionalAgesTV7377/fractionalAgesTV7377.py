import os
import sys

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=1.4, g=1, mt=mt.table_qx) for mt in mt_lst]

'''
Exercises
'''
mt = lt_lst[0]
a = mt.nqx(x=52.4, n=0.2, method='udd')
print(a)
b = mt.nqx(x=52.4, n=0.2, method='cfm')
print(b)
c = mt.npx(x=52.4, n=5.7, method='udd')
print(c)
d = mt.npx(x=52.4, n=5.7, method='cfm')
print(d)
e = mt.t_nqx(x=52.4, t=3.2, n=2.5, method='udd')
print(e)
f = mt.t_nqx(x=52.4, t=3.2, n=2.5, method='cfm')
print(f)
