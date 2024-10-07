from soa_tables import read_soa_table_xml as rst
from lifeActuary import mortality_table as mtable, commutation_table as ct, annuities as la, \
    mortality_insurance as lins, life_2heads as a2h

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

######################################################################################################################
#                                 Chapter 9 - Examples                                               #
######################################################################################################################

# Reading the Mortality Tables
mt = rst.SoaTable('../soa_tables/TV7377' + '.xml')
lt = mtable.MortalityTable(mt=mt.table_qx)


# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 9.1 - Example 1
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# QUESTION 1
x = 55
n = np.linspace(0, 10, 10*12)
sprobs = [lt.npx(x=x, n=i, method='udd') for i in n]
dprobs = [lt.nqx(x=x, n=i, method='udd') for i in n]
ages = x + n
df = pd.DataFrame.from_dict({'n': n, 'x': ages, 'npx': sprobs, 'nqx': dprobs})

# QUESTION 2
df.to_excel(excel_writer='example1.xlsx', sheet_name='example1', index=False, freeze_panes=(1, 1))


# QUESTION 3
# Probability of Survival
plt.scatter(n, sprobs, s=.5, color='blue')

plt.xlabel(r'$n$')
plt.ylabel(r'${}_{n}p_{55}$')
plt.title('Probability of Survival')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.savefig('example1s' + '.eps', format='eps', dpi=3600)
plt.show()

# Probability of Dying
plt.scatter(n, dprobs, s=.5, color='red')

plt.xlabel(r'$n$')
plt.ylabel(r'${}_{n}q_{55}$')
plt.title('Probability of Dying')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.savefig('example1d' + '.eps', format='eps', dpi=3600)
plt.show()



# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 9.2 - Example 2
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

this_py = os.path.split(sys.argv[0])[-1][:-3]

def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')

# QUESTION 1
table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mtable.MortalityTable(mt=mt.table_qx) for mt in mt_lst]


# QUESTION 2 - DÁ ERRO
interest_rate = 4
ct_lst = [ct.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

for idx, lt in enumerate(lt_lst):
    name = parse_table_name(mt_lst[idx].name)
    lt.df_life_table().to_excel(excel_writer=name + '.xlsx', sheet_name=name, index=False, freeze_panes=(1, 1))
    ct_lst[idx].df_commutation_table().to_excel(excel_writer=name + '_comm' + '.xlsx', sheet_name=name, index=False, freeze_panes=(1, 1))

# QUESTION 3
'''
Plot lx
'''
fig, axes = plt.subplots()
for idx, lt in enumerate(lt_lst):
    ages = np.arange(0, lt.w + 2)
    plt.plot(ages, lt.lx, label=table_names[idx])
plt.xlabel(r'$x$')
plt.ylabel(r'$l_x$')
plt.title('Expected Number of Individuals Alive')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + 'lx' + '.eps', format='eps', dpi=3600)
plt.show()

'''
Plot dx
'''
fig, axes = plt.subplots()
for idx, lt in enumerate(lt_lst):
    ages = np.arange(0, lt.w + 1)
    plt.plot(ages, lt.dx, label=table_names[idx])
plt.xlabel(r'$x$')
plt.ylabel(r'$d_x$')
plt.title('Expected Number of Deaths')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + 'dx' +'.eps', format='eps', dpi=3600)
plt.show()

'''
Plot qx
'''
fig, axes = plt.subplots()
for idx, lt in enumerate(lt_lst):
    ages = np.arange(0, lt.w + 1)
    plt.plot(ages, lt.qx, label=table_names[idx])
plt.xlabel(r'$x$')
plt.ylabel(r'$q_x$')
plt.title('Mortality Rate')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + 'qx' +'.eps', format='eps', dpi=3600)
plt.show()

'''
Plot px
'''
fig, axes = plt.subplots()
for idx, lt in enumerate(lt_lst):
    ages = np.arange(0, lt.w + 1)
    plt.plot(ages, lt.px, label=table_names[idx])
plt.xlabel(r'$x$')
plt.ylabel(r'$p_x$')
plt.title('Probability of Survival')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + 'px' +'.eps', format='eps', dpi=3600)
plt.show()

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
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + 'ex' + '.eps', format='eps', dpi=3600)
plt.show()

'''
Plot ln(Dx)
'''
fig, axes = plt.subplots()
for idx, lt in enumerate(ct_lst):
    ages = np.arange(0, lt.w + 1)
    plt.plot(ages, np.log(lt.Dx), label=table_names[idx])
plt.xlabel(r'$x$')
plt.ylabel(r'$ln(D_x)$')
plt.title(r'ln(D_x)')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py +'lnDx' + '.eps', format='eps', dpi=3600)
plt.show()

# QUESTION 4
for idx, ct_ in enumerate(ct_lst):
    print(table_names[idx] + ": " + f'{round(1000 * ct_.ax(x=55, m=1), 2):,}')
print()

# QUESTION 5
for idx, ct_ in enumerate(ct_lst):
    print(table_names[idx]+":"+f'{round(1000 * ct_.ax(x=55, m=1) / ct_.naax(x=55, n=5, m=1), 2):,}')

# Consult the values used each computation (Nx, Dx)
for idx, ct_ in enumerate(ct_lst):
    print(ct_.msn)
    print()

# Consult the values used in the computation, only for TV7377
ct_lst[0].msn



# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 9.3 - Example 3
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 4
mt_lst = [rst.SoaTable('../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mtable.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [ct.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

# General Information
x = 55
capital = 1000
term = 10
term_annuity = 5
# pure endowment
pureEndow = [ct.nEx(x=x, n=term) for ct in ct_lst]
# temporary annuity due
tad = [ct.naax(x=x, n=term_annuity, m=1) for ct in ct_lst]

### QUESTION 1
print('\nnet single premium')
for idx, ct in enumerate(ct_lst):
    print(table_names[idx] + ": " + f'{round(capital * pureEndow[idx], 5):,}')

### QUESTION 2
print('\nlevel premium')
for idx, ct in enumerate(ct_lst):
    print(table_names[idx] + ":" + f'{round(capital * pureEndow[idx] / tad[idx], 5):,}')

# show the annuities
print('\nannuities')
for idx, ct in enumerate(ct_lst):
    print(table_names[idx] + ":" + f'{round(tad[idx], 5):,}')

### QUESTION 3

## Refund of Net Single Premium
print('\nSingle Net Risk Premium Refund at End of the Year of Death')
termLifeInsurance = [ct.nAx(x=x, n=term) for ct in ct_lst]
pureEndow_refund = [ct.nEx(x=x, n=term) / (1 - ct.nAx(x=x, n=term)) for ct in ct_lst]

print('\nTerm Life Insurance')
for idx, ct in enumerate(ct_lst):
    print(table_names[idx] + ":" + f'{round(termLifeInsurance[idx], 5):,}')

print('\nSingle Net Premium Refund Cost at End of the Year of Death')
for idx, ct in enumerate(ct_lst):
    print(table_names[idx] + ":" + f'{round(capital * pureEndow[idx] / (1 - termLifeInsurance[idx]), 5):,}')

print('Refund Cost at End of the Year of Death')
for idx, ct in enumerate(ct_lst):
    print(table_names[idx] + ":" + f'{round(capital * (pureEndow_refund[idx] - pureEndow[idx]), 5):,}')

print('\nSingle Net Risk Premium Refund at End of the Term')
pureEndow_refund_eot = [ct.nEx(x=x, n=term) / (1 - (1 + interest_rate / 100) ** (-term) + ct.nEx(x=x, n=term))
                        for ct in ct_lst]

for idx, ct in enumerate(ct_lst):
    print(table_names[idx] + ":" + f'{round(capital * pureEndow_refund_eot[idx], 5):,}')

print('Refund Cost at End of the the Term')
for idx, ct in enumerate(ct_lst):
    print(table_names[idx] + ":" + f'{round(capital * (pureEndow_refund_eot[idx] - pureEndow[idx]), 5):,}')

## Refund of Net Level Premiums

print('\nLeveled Net Risk Premium Refund at End of the Year of Death')
tli_increasing = [ct.nIAx(x=x, n=term_annuity) for ct in ct_lst]
tli_deferred = [ct.t_nAx(x=x, n=term - term_annuity, defer=term_annuity) for ct in ct_lst]
pureEndow_leveled_refund = [
    pureEndow[idx_ct] / (tad[idx_ct] - tli_increasing[idx_ct] - term_annuity * tli_deferred[idx_ct])
    for idx_ct, ct in enumerate(ct_lst)]

for idx, ct in enumerate(ct_lst):
    print(table_names[idx] + ":" + f'{round(capital * pureEndow_leveled_refund[idx], 5):,}')



# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 9.3 - Example 4
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

## Net premium reserves path

l0 = 1000
reserves_dict = {'table': [], 'x': [], 'insurer': [], 'insured': [], 'reserve': []}
fund_dict = {'lx': [], 'claim': [], 'premium': [], 'fund': []}

# Expected reserves value, that is, considering the survivorship of the group
expected_reserve_dict = {'insurer_exp': [], 'insured_exp': [], 'reserve_exp': []}
ages = range(x, x + term + 1)
print('\n\n Net Premium reserves \n\n')
for idx_clt, clt in enumerate(ct_lst):
    premium_unit = pureEndow[idx_clt]
    premium_capital = capital * premium_unit
    premium_unit_leveled = premium_unit / tad[idx_clt]
    premium_leveled = premium_unit_leveled * capital
    for age in ages:
        # reserves
        reserves_dict['table'].append(table_names[idx_clt])
        reserves_dict['x'].append(age)
        insurer_liability = clt.nEx(x=age, n=term - (age - x)) * \
                            capital
        reserves_dict['insurer'].append(insurer_liability)
        tad2 = clt.naax(x=age, n=term_annuity - (age - x))
        insured_liability = premium_leveled * tad2
        reserves_dict['insured'].append(insured_liability)
        reserve = insurer_liability - insured_liability
        reserves_dict['reserve'].append(reserve)

        prob_survival = clt.npx(x=x, n=age - x)
        lx = l0 * prob_survival
        expected_reserve_dict['insurer_exp'].append(insurer_liability*lx)
        expected_reserve_dict['insured_exp'].append(insured_liability*lx)
        expected_reserve_dict['reserve_exp'].append(reserve*prob_survival*lx)

        # fund
        fund_dict['lx'].append(lx)
        qx_1 = clt.nqx(x=age, n=1)
        claim = 0
        if age == x + term:
            claim = capital * lx
        fund_dict['claim'].append(claim)
        premium = 0
        if tad2 > 0:
            premium = premium_leveled*lx
        fund_dict['premium'].append(premium)
        if age == x:
            fund = lx * premium_leveled
        else:
            fund = fund_dict['fund'][-1] * (1 + interest_rate / 100) - claim + premium
        fund_dict['fund'].append(fund)

reserves_df = pd.DataFrame(reserves_dict)
expected_reserve_df = pd.DataFrame(expected_reserve_dict)
fund_df = pd.DataFrame(fund_dict)
name = 'pureEndowment_55_1'
reserves_df.to_excel(excel_writer=name + '_netReserves' + '.xlsx', sheet_name=name, index=False, freeze_panes=(1, 1))

'''
plot the reserves
'''
for idx_clt, clt in enumerate(ct_lst):
    plt.plot(ages, reserves_df.loc[reserves_df['table'] == table_names[idx_clt]]['reserve'],
             label=table_names[idx_clt])

plt.xlabel(r'$x$')
plt.ylabel('Reserves')
plt.title('Net Premium Reserves Pure Endowment')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.show()

# save the graph
plt.savefig(this_py + '.eps', format='eps', dpi=3600)



# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 9.4 - Example 5
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# reads soa table TV7377
soaTV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soaGRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
#soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')

# creates a mortality table
#tv7377 = mt.MortalityTable(data_type='q', mt=soa.table_qx, perc=100, last_q=1)
grf95 = mtable.MortalityTable(mt=soaGRF95.table_qx)
tv7377 = mtable.MortalityTable(mt=soaTV7377.table_qx)

## Silvia
age = 66
premium = 200000
a4_66 = la.ax(mt=grf95, x=age, i=1, g=0, m=4)
a2_66 = la.ax(mt=grf95, x=age, i=1, g=0, m=2)
T = premium/(4 * a4_66 + 2 * a2_66)
print(T)

## Robert
age = 66
premium = 200000
termIa=grf95.w
Ia_66 = la.nIax(mt=tv7377, x=age, n=termIa, i=1, m=1, first_amount=1, increase_amount=1)
E466 = la.nEx(mt=tv7377, x=age, i=1, g=0, n=4)
ad66 = la.aax(mt=tv7377, x=age, i=1, g=0, m=1)
A66_10 = lins.nAx_(mt=tv7377, x=age, n=10, i=1, g=0)

T = (premium -50 * Ia_66 - 800 * E466)/(ad66 + E466 + A66_10)
print(T)


# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 9.4 - Example 6
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# Reading the Mortality Tables
mt = rst.SoaTable('../soa_tables/TV7377' + '.xml')
lt = mtable.MortalityTable(mt=mt.table_qx)

path_liabilities = {'t': [], 'age': [], 'px': [], 'qx': [], 'premium': [], 'al': []}
path_fund = {'t': [], 'lx': [], 'in': [], 'out': [], 'fund': []}

# Data
x = 40
r = 65
n_premiums = 15
i = 2
g=0
capital = 100000
l0 = 1000

# QUESTION 1
risk_premium_1 = lins.nAEx(mt=lt, x=x, n=r - x, i=i, g=g)
risk_premium = risk_premium_1 * capital
print(f'risk_premium: {risk_premium}')

# QUESTION 2
aax_r = la.naax(mt=lt, x=x, n=n_premiums, i=i, g=g, m=1)
premium_leveled = risk_premium / aax_r
print(f'premium_leveled: {premium_leveled: ,.2f}')

# QUESTION 3
# lx, Premiums, Claims and Actuarial Liabilities
for idx_ages, ages in enumerate(range(x, r + 1)):
    path_liabilities['t'].append(idx_ages)
    path_liabilities['age'].append(ages)
    npx = lt.npx(x=x, n=idx_ages)
    nqx = lt.nqx(x=x + idx_ages, n=1)
    path_liabilities['px'].append(npx)
    path_liabilities['qx'].append(nqx)
    if idx_ages <= n_premiums - 1:
        path_liabilities['premium'].append(premium_leveled)
        path_liabilities['al'].append(lins.nAEx(mt=lt, x=x + idx_ages, n=r - x - idx_ages, i=i, g=g) * capital -
                                      premium_leveled *
                                      la.naax(mt=lt, x=x + idx_ages, n=n_premiums - idx_ages, i=i, g=g, m=1))
    else:
        path_liabilities['premium'].append(0)
        path_liabilities['al'].append(lins.nAEx(mt=lt, x=x + idx_ages, n=r - x - idx_ages, i=i, g=g) * capital)

    # EVOLUTION OF THE FUND
    path_fund['t'].append(idx_ages)
    path_fund['lx'].append(l0 * npx)
    path_fund['in'].append(l0 * npx * path_liabilities['premium'][idx_ages])
    if idx_ages == 0:
        path_fund['fund'].append(l0 * path_liabilities['premium'][idx_ages])
        path_fund['out'].append(0)
    else:
        if ages < r:
            path_fund['out'].append(l0 * path_liabilities['px'][idx_ages-1] *
                                    path_liabilities['qx'][idx_ages-1] * capital)
        else:
            path_fund['out'].append(l0 * path_liabilities['px'][idx_ages - 1] *
                                    path_liabilities['qx'][idx_ages - 1] * capital+
                                    l0*path_liabilities['px'][idx_ages]*capital)
        path_fund['fund'].append(path_fund['fund'][-1] * (1 + i / 100) + path_fund['in'][-1] - path_fund['out'][-1])


# QUESTION 4
(pd.DataFrame(path_liabilities)).to_excel(excel_writer='liabilities' + '.xlsx', sheet_name='liabilities',
                                          index=False, freeze_panes=(1, 1))

(pd.DataFrame(path_fund)).to_excel(excel_writer='fund' + '.xlsx', sheet_name='fund',
                                   index=False, freeze_panes=(1, 1))

# QUESTION 5
df_liabilities = pd.DataFrame(path_liabilities)
df_fund = pd.DataFrame(path_fund)


# QUESTION 6
# lx
fig, axes = plt.subplots()
barWidth = .1
br1 = np.arange(len(df_fund['lx']))
plt.bar(br1, df_fund['lx'], edgecolor='gray', color='goldenrod')
plt.title('Expected Insured Population')
#plt.savefig('example6lx' + '.eps', format='eps', dpi=3600)
plt.show()

# Premiums
fig, axes = plt.subplots()
barWidth = .1
br1 = np.arange(len(df_fund['in']))
plt.bar(br1, df_fund['in'], edgecolor='gray', color='yellowgreen')
plt.title('Expected Collected Premiums')
#plt.savefig('example6premiums' + '.eps', format='eps', dpi=3600)
plt.show()

# Claims
fig, axes = plt.subplots()
barWidth = .1
br1 = np.arange(len(df_fund['out']))
plt.bar(br1, df_fund['out'], edgecolor='gray', color='teal')
plt.title('Expected Claims')
#plt.savefig('example6claims' + '.eps', format='eps', dpi=3600)
plt.show()

# Fund
fig, axes = plt.subplots()
barWidth = .1
br1 = np.arange(len(df_fund['fund']))
plt.bar(br1, df_fund['fund'], edgecolor='gray', color='silver')
plt.title('Expected Fund')
#plt.savefig('example6fund' + '.eps', format='eps', dpi=3600)
plt.show()

# QUESTION 7
fig, axes = plt.subplots()
barWidth = .1
br1 = np.arange(len(df_fund['in']))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
plt.bar(br3, df_fund['fund'], label='Fund', edgecolor='gray', color='silver')
plt.bar(br2, df_fund['out'], label='Claims', edgecolor='gray', color='teal') #lightblue
plt.bar(br1, df_fund['in'], label='Premium', edgecolor='gray', color='yellowgreen')
plt.legend()
plt.savefig('example6all' + '.eps', format='eps', dpi=3600)
plt.show()




# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 9.5 - Example 7
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#from soa_tables import read_soa_table_xml as rst
#from lifeActuary import mortality_table as mtable, commutation_table as ct, annuities as la, \
#    mortality_insurance as lins, annuities_2head as a2h

#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt



# reads soa table TV7377
soaTV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
tv7377 = mtable.MortalityTable(mt=soaTV7377.table_qx)

this_py = os.path.split(sys.argv[0])[-1][:-3]

x=50
y=50
n=20
i=2

# QUESTION 1
a12xy = a2h.naxy(mtx=tv7377, mty=tv7377, x=x, y=y, n=n, i=i, g=2, m=12, status='last-survivor')
Axy = a2h.nAxy_(mtx=tv7377, mty=tv7377, x=x, y=y, n=n, i=i, g=0, status='last-survivor')
aa2xy = a2h.naaxy(mtx=tv7377, mty=tv7377, x=x, y=y, n=n, i=i, g=0, m=2, status='joint-life')

premium_leveled = (500 * 12 * a12xy + 1000000 * Axy) / (2 * aa2xy)

print(f'a12xy:{a12xy}')
print(f'Axy:{Axy}')
print(f'aa2xy:{aa2xy}')
print(f'Leveled Premium:{premium_leveled}')

# QUESTION 2
# Risk Premium
g=2
premium_annual = [a2h.naxy(mtx=tv7377, mty=tv7377, x=x + a, y=y + a, n=1, i=i, g=0, m=12, status='last-survivor', method='udd') * 500 * 12 * (1+g/100) ** a+
                  a2h.nAxy_(mtx=tv7377, mty=tv7377, x=x + a, y=y + a, n=1, i=i, g=0, status='last-survivor', method='udd') * 1000000
                  for a in range(n)]

# Plot
fig, axes = plt.subplots()
ages = range(x, x + n)
plt.xticks(ages)
plt.plot(ages, premium_annual, 'ro', label='Risk Premium')
plt.axhline(y=premium_leveled*2, color='b', linestyle='dotted', label='Leveled', alpha=.5)

plt.xlabel('ages')
plt.ylabel('premium')
plt.title('Annual Risk Premium')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + 'arp' + '.eps', format='eps', dpi=3600)
plt.show()

