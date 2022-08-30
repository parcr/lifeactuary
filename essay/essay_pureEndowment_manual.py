import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 4
mt_lst = [rst.SoaTable('../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

'''
1000\Ax{\pureendow{55}{10}}
'''

x = 55
capital = 1000
term = 10
term_annuity = 5
pureEndow = [ct.nEx(x=x, n=term) for ct in ct_lst]
tad = [ct.naax(x=x, n=term_annuity, m=1) for ct in ct_lst]  # temporary annuity due

print()
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(capital * pureEndow[idx], 5):,}')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(capital * pureEndow[idx] / tad[idx], 5):,}')

# show the annuities
print('\nannuities')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(tad[idx], 5):,}')

'''Premiums Refund'''
print('\nSingle Net Risk Premium Refund at End of the Year of Death')
termLifeInsurance = [ct.nAx(x=x, n=term) for ct in ct_lst]
pureEndow_refund = [ct.nEx(x=x, n=term) / (1 - ct.nAx(x=x, n=term)) for ct in ct_lst]

print('\nTerm Life Insurance')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(termLifeInsurance[idx], 5):,}')

print('\nSingle Net Premium Refund Cost at End of the Year of Death')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(capital * pureEndow[idx] / (1 - termLifeInsurance[idx]), 5):,}')

print('Refund Cost at End of the Year of Death')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(capital * (pureEndow_refund[idx] - pureEndow[idx]), 5):,}')

print('\nSingle Net Risk Premium Refund at End of the Term')
pureEndow_refund_eot = [ct.nEx(x=x, n=term) / (1 - (1 + interest_rate / 100) ** (-term) + ct.nEx(x=x, n=term))
                        for ct in ct_lst]

for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(capital * pureEndow_refund_eot[idx], 5):,}')

print('Refund Cost at End of the the Term')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(capital * (pureEndow_refund_eot[idx] - pureEndow[idx]), 5):,}')

'''
Refund of Leveled Premiums
'''

print('\nLeveled Net Risk Premium Refund at End of the Year of Death')
tli_increasing = [ct.nIAx(x=x, n=term_annuity) for ct in ct_lst]
tli_deferred = [ct.t_nAx(x=x, n=term - term_annuity, defer=term_annuity) for ct in ct_lst]
pureEndow_leveled_refund = [
    pureEndow[idx_ct] / (tad[idx_ct] - tli_increasing[idx_ct] - term_annuity * tli_deferred[idx_ct])
    for idx_ct, ct in enumerate(ct_lst)]

for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(capital * pureEndow_leveled_refund[idx], 5):,}')

''' 
Test 
'''
term_annuity_b = 1
test_m_equal_1_a = [1 - ct.nAx(x=x, n=term) for ct in ct_lst]
test_m_equal_1_b = [ct.naax(x=x, n=term_annuity_b) -
                    ct.nIAx(x=x, n=term_annuity_b) -
                    term_annuity_b * ct.t_nAx(x=x, n=term - term_annuity_b, defer=term_annuity_b)
                    for ct in ct_lst]
test = np.array(test_m_equal_1_a) - np.array(test_m_equal_1_b)

'''
Net premium reserves path
'''
l0 = 1000
reserves_dict = {'table': [], 'x': [], 'insurer': [], 'insured': [], 'reserve': []}
fund_dict = {'lx': [], 'claim': [], 'premium': [], 'fund': []}
# expected reserves value, that is, considering the survivorship of the group
expected_reserve_dict = {'insurer_exp': [], 'insured_exp': [], 'reserve_exp': []}
ages = range(x, x + term + 1)
print('\n\n Net Premium reserves \n\n')
for idx_clt, clt in enumerate(ct_lst):
    premium_unit = pureEndow[idx_clt]
    premium_capital = capital * premium_unit
    premium_unit_leveled = premium_unit / tad[idx_clt]
    premium_leveled = premium_unit_leveled * capital
    for age in ages:
        # reserves # reserves # reserves # reserves # reserves # reserves
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

        # fund # fund # fund # fund # fund # fund # fund # fund
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
# reserves_df.to_excel(excel_writer=name + '_netReserves' + '.xlsx', sheet_name=name, index=False, freeze_panes=(1, 1))

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
# plt.savefig(this_py + '.eps', format='eps', dpi=3600)
plt.show()