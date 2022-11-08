from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
from annuities_certain import annuities_certain
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.00018, b=1.E-6, c=1.12)

interest_rate = 2.5

e0 = mml.moments_Tx()
e70 = mml.moments_Tx(x=70)

'''
Compute Life Table
'''
w = 125 + 5
px = np.array([mml.S(x, t=1) for x in range(0, w)])
qx = 1 - px
lt = mortality_table.MortalityTable(mt=list(np.append(0, qx)))
w = len(px)
ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=list(np.append(0, qx)))

if False:
    lt.df_life_table().to_excel(excel_writer='makeham_' + str(w) + '.xlsx', sheet_name='makeham',
                                index=False, freeze_panes=(1, 1))
    ct.df_commutation_table().to_excel(excel_writer='makeham' + '_comm_' + str(w) + '.xlsx', sheet_name='makeham',
                                       index=False, freeze_panes=(1, 1))

print(f'E(T_0)= {e0}')
print(f'E(T_70)= {e70}')
print(f'E(K_0)= {lt.ex[0] - .5}')
print(f'E(K_70)= {lt.ex[70] - .5}')

'''a'''
capital = 12000
x = 50
t = 15
n = 10
nEx = ct.nEx(x=x, n=t)
Dx = ct.Dx[x]
Nx_t = ct.Nx[x + t]
Nx_t_n = ct.Nx[x + t + n]
Dx_t = ct.Dx[x + t]
ax_t = (Nx_t - Nx_t_n) / Dx_t
renda = nEx * ax_t
renda_cap = capital * renda

renda_ct = ct.t_naax(x=x, n=n, m=1, defer=t)

'''a'''
print('\na')
print(f'N1=', round(Nx_t, 5))
print(f'N2=', round(Nx_t_n, 5))
print(f'D=', round(Dx, 5))
P1 = (Nx_t - Nx_t_n) / Dx
print(f'P1=', round(P1, 5))
print(f'Confirm P1=', round(renda_ct, 5))
P = capital * P1
print(f'P=', round(P, 2))

'''b'''
print('\nb')
level = 15
N_x1 = ct.Nx[x]
N_x2 = ct.Nx[x + level]

print(f'N1=', round(N_x1, 5))
print(f'N2=', round(N_x2, 5))
print('ann_level=', round((N_x1 - N_x2) / Dx, 5))
ann_level_ct = ct.naax(x=x, n=level, m=1)
print('ann_level_ct=', round(ann_level_ct, 5))
print('Pleveled=', round(P / ann_level_ct, 2))

'''c'''
print('\nc')
ac = annuities_certain.Annuities_Certain(interest_rate=interest_rate, m=1)
x = 50
t = 15
term_guarantee = 5
term2 = 5
ann_certain = ac.aan(terms=5) * ac.v ** t
print(f'annuity certain=', round(ann_certain, 5))

N_x1 = ct.Nx[x + t + term_guarantee]
N_x2 = ct.Nx[x + t + term_guarantee + term2]
D_x1 = ct.Dx[x]
ann2 = (N_x1 - N_x2) / D_x1

print(f'N1=', round(N_x1, 5))
print(f'N2=', round(N_x2, 5))
print(f'ann2=', round(ann2, 5))
print(f'Confirm annuity:', ct.t_naax(x=50, n=5, m=1, defer=20))
P1 = ann2 + ann_certain
print(f'P1=', round(P1, 5))
P = capital * P1
print(f'P=', round(P, 2))
