from essential_life import read_soa_table_xml as rst
import os
import sys

from essential_life import mortality_table, commutation_table


this_py = os.path.split(sys.argv[0])[-1][:-3]

def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 4
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

table_idx = 2
name = table_names[table_idx]
print(f'The Table being used is {name}')
lt = lt_lst[table_idx]
ct = ct_lst[table_idx]


'''a'''
capital = 10000
x = 55
t = 10
nEx = ct.nEx(x=x, n=t)
Dx = ct.Dx[x]
Nx_t = ct.Nx[x + t]
Dx_t = ct.Dx[x + t]
ax_t = Nx_t / Dx_t
renda = nEx * ax_t
renda_cap = capital * renda

renda_ct = ct.t_aax(x=x, m=1, defer=t)

print()
print(f'N=', round(Nx_t, 5))
print(f'D=', round(Dx, 5))
P1 = Nx_t / Dx
print(f'P1=', round(P1, 5))
P = capital * P1
print(f'P=', round(P, 2))

'''b'''
print()
level = 10
N_x1 = ct.Nx[x]
N_x2 = ct.Nx[x + level]

print(f'N1=', round(N_x1, 5))
print(f'N2=', round(N_x2, 5))
print('ann_level=', round((N_x1 - N_x2) / Dx, 5))
ann_level_ct = ct.naax(x=x, n=level, m=1)
print('ann_level_ct=', round(ann_level_ct, 5))
print('Pleveled=', round(P / ann_level_ct, 2))


'''c'''
print()
x = 55
t = 10
term = 15
nEx = ct.nEx(x=x, n=t)
Dx = ct.Dx[x]
Nx_t = ct.Nx[x + t + 1]
Nx_t2 = ct.Nx[x + t + 1 + term]

print(f'N1=', round(Nx_t, 5))
print(f'N2=', round(Nx_t2, 5))
renda2 = (Nx_t - Nx_t2) / Dx
print('renda2=', round(renda2, 5))
renda2_ct = ct.t_nax(x=x, n=term, m=1, defer=10)
renda2_cap = capital * renda2
print('P=', round(renda2_cap, 2))
