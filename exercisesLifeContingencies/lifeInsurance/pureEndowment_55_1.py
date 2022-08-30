import numpy as np

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 4
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
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
