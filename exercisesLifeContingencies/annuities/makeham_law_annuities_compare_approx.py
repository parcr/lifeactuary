from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)

t = np.linspace(0, 100, 1000 + 1)
x_s = [0, 20, 50, 80]

'''
Compute Life Table and commutation table
'''
interest_rate = 5
px = np.array([mml.S(x, t=1) for x in range(0, 130 + 0)])
qx = 1 - px
lt = mortality_table.MortalityTable(mt=list(np.append(0, qx)))
lt.df_life_table().to_excel(excel_writer='makeham' + '.xlsx', sheet_name='makeham',
                            index=False, freeze_panes=(1, 1))
ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=list(np.append(0, qx)))
ct.df_commutation_table().to_excel(excel_writer='makeham' + '_comm' + '.xlsx', sheet_name='makeham',
                                   index=False, freeze_panes=(1, 1))

'''
annuities
'''

x_s = range(20, 80 + 20, 20)
rendas_dict = {}
for x in x_s:
    for m in [1, 4]:
        ts = np.arange(0, lt.w - x + 1 / m, 1 / m)
        v = 1 / (1 + interest_rate / 100)
        epv_ai = [mml.S(x=x, t=u) * v ** u for u in ts[1:]]
        epv_aa = epv_ai.copy()
        epv_aa.insert(0, 1)
        name = 'aa_' + str(x) + '_' + str(m)
        rendas_dict[name] = sum(epv_aa) / m
        name = 'ai_' + str(x) + '_' + str(m)
        rendas_dict[name] = sum(epv_ai) / m
        name = 'aC_' + str(x)  # continuous
        rendas_dict[name] = mml.ax(x=x, interest_rate=interest_rate)[0]
        # commutation table
        i = interest_rate / 100
        v = 1 / (1 + i)
        d = i * v
        i_m = (np.power((1 + i), 1 / m) - 1) * m
        d_m = i_m * np.power((1 + i), -1 / m)
        alpha_m = i * d / (i_m * d_m)
        beta_m = (i - i_m) / (i_m * d_m)
        name = 'aa_' + str(x) + '_' + str(m) + '_comm'  # using the usual approximations
        rendas_dict[name] = ct.aax(x=x, m=m)
        name = 'aa_' + str(x) + '_' + str(m) + '_a_b'  # using alpha and beta obtained by the udd
        rendas_dict[name] = ct.aax(x=x, m=1) * alpha_m - beta_m

        name = 'ai_' + str(x) + '_' + str(m) + '_comm'  # using the usual approximations
        rendas_dict[name] = ct.ax(x=x, m=m)
        name = 'ai_' + str(x) + '_' + str(m) + '_a_b'  # using alpha and beta obtained by the udd
        rendas_dict[name] = ct.ax(x=x, m=1) * alpha_m + alpha_m - beta_m - 1 / m

'''
annuities temp
'''
rendas_temp_dict = {}
for x in x_s:
    for m in [1, 4]:
        ts = np.arange(0, 10 + 1 / m, 1 / m)
        v = 1 / (1 + interest_rate / 100)
        epv_ai = [mml.S(x=x, t=u) * v ** u for u in ts[1:]] # [mml.S(x=x, t=u) * v ** u for u in ts[1:]]
        epv_aa = epv_ai.copy()
        epv_aa.insert(0, 1)
        epv_aa.pop()
        name = 'aa_' + str(x) + '_' + str(m)
        rendas_temp_dict[name] = sum(epv_aa) / m
        name = 'ai_' + str(x) + '_' + str(m)
        rendas_temp_dict[name] = sum(epv_ai) / m
        name = 'aC_' + str(x)  # continuous
        rendas_temp_dict[name] = mml.ax(x=x, interest_rate=interest_rate, n=10)[0]

        # commutation table
        i = interest_rate / 100
        v = 1 / (1 + i)
        d = i * v
        i_m = (np.power((1 + i), 1 / m) - 1) * m
        d_m = i_m * np.power((1 + i), -1 / m)
        alpha_m = i * d / (i_m * d_m)
        beta_m = (i - i_m) / (i_m * d_m)
        name = 'aa_' + str(x) + '_' + str(m) + '_comm'  # using the usual approximations
        rendas_temp_dict[name] = ct.naax(x=x, n=10, m=m)
        name = 'aa_' + str(x) + '_' + str(m) + '_a_b'  # using alpha and beta obtained by the udd
        rendas_temp_dict[name] = ct.naax(x=x, n=10, m=1) * alpha_m - beta_m * (1 - ct.nEx(x=x, n=10))

        # a = [ct.naax(x=20, n=10, m=m) for m in range(1, 12)]

        name = 'ai_' + str(x) + '_' + str(m) + '_comm'  # using the usual approximations
        rendas_temp_dict[name] = ct.nax(x=x, n=10, m=m)
        name = 'ai_' + str(x) + '_' + str(m) + '_a_b'  # using alpha and beta obtained by the udd
        rendas_temp_dict[name] = ct.nax(x=x, n=10, m=1) * alpha_m - (-alpha_m + beta_m + 1 / m) * (
                1 - ct.nEx(x=x, n=10))
