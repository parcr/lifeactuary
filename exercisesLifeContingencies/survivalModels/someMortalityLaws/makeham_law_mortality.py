from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.0001, b=0.0003, c=1.07) # E(T_0)= 71.66316
# mml = makeham_mortality_functions.Makeham(a=2E-6, b=6E-6, c=1.07) #E(T_0)= 129.36947076690612
#mml = makeham_mortality_functions.Makeham(a=0.0001, b=0.00035, c=1.075)
# mml = makeham_mortality_functions.Makeham(a=0.00015, b=0.0004, c=1.1)

e0 = mml.moments_Tx()
e70 = mml.moments_Tx(x=70)

t = np.linspace(0, 100, 1000 + 1)
x_s = [0, 20, 50, 80]

S_vec = np.vectorize(mml.S)
fig, ax = plt.subplots()
for x in x_s:
    y = S_vec(x=x, t=t)
    plt.plot(t, y, label=f'x={x}')

plt.title(f'Makeham Law Survival Function (A={mml.a}, B={mml.b}, c={mml.c})')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('t')
plt.ylabel(f'$S_x(t)$')
this_py = os.path.split(sys.argv[0])[-1][:-3]
plt.savefig(this_py + '_sf' + '.eps', format='eps', dpi=3600)
plt.show()

pdf_vec = np.vectorize(mml.pdf)
fig, ax = plt.subplots()
for x in x_s:
    y = pdf_vec(x=x, t=t)
    plt.plot(t, y, label=f'x={x}')

plt.title(f'Makeham Law Probability Density Function (A={mml.a}, B={mml.b}, c={mml.c})')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('t')
plt.ylabel(f'$f_x(t)$')
plt.savefig(this_py + '_pdf' + '.eps', format='eps', dpi=3600)
plt.show()

'''
Compute Life Table
'''
interest_rate = 3.546
px = np.array([mml.S(x, t=1) for x in range(0, 125+1)])
qx = 1 - px
lt = mortality_table.MortalityTable(mt=list(np.append(0, qx)))
w = len(px)
lt.df_life_table().to_excel(excel_writer='makeham_' + str(w) + '.xlsx', sheet_name='makeham',
                            index=False, freeze_panes=(1, 1))
ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=list(np.append(0, qx)))
ct.df_commutation_table().to_excel(excel_writer='makeham' + '_comm_' + str(w) + '.xlsx', sheet_name='makeham',
                                   index=False, freeze_panes=(1, 1))

print('px')
print(lt.px)

print(f'E(T_0)= {e0}')
print(f'E(T_70)= {e70}')
print(f'E(K_0)= {lt.ex[0]-.5}')
print(f'E(K_70)= {lt.ex[70]-.5}')

'''
Plot ex
'''
fig, axes = plt.subplots()
plt.plot(range(lt.x0, lt.w + 1), lt.ex, label=f'Makeham({mml.a}, {mml.b}, {mml.c})')

plt.xlabel(r'$x$')
plt.ylabel(r'${e}_{x}+1/2$')
plt.title('Complete Expectation of Life')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_ex' + '.eps', format='eps', dpi=3600)
plt.show()

'''
Plot t|q_70
'''

t_s = np.array(range(0, lt.w - 70))
t_1q70 = [mml.S(x=70, t=t) - mml.S(x=70, t=t + 1) for t in t_s]
max_at = t_1q70.index(max(t_1q70))
print(f'The maximum is {max(t_1q70)} at t={max_at}')
print(np.round(np.array(t_1q70)[0:max_at + 3], 7))

fig, axes = plt.subplots()
plt.plot(t_s + 70, t_1q70, label=f'Makeham({mml.a}, {mml.b}, {mml.c})')

plt.xlabel(r'$t+70$')
plt.ylabel(r'$_{t|}q_{70}$')
plt.title(r'$_{t|}q_{70}$')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + 'pk70' + '.eps', format='eps', dpi=3600)
plt.show()
