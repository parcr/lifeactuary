from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 4
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

'''
1000\frac{M_{55}-M_{65}}{D_{55}}
'''

x = 55
capital = 1000
term = 10
term_annuity = 10
tli = [ct.nAx(x=55, n=term) for ct in ct_lst]
tli_ = [ct.nAx_(x=55, n=term) for ct in ct_lst]
tad = [ct.naax(x=x, n=term_annuity, m=1) for ct in ct_lst]  # temporary annuity due

print()
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(capital * tli[idx], 5):,}')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(capital * tli[idx] / tad[idx], 5):,}')

print("\nContinous Case")
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(capital * tli_[idx], 5):,}')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(capital * tli_[idx] / tad[idx], 5):,}')

# show the annuities
print('\nannuities')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(tad[idx], 5):,}')

'''Premiums Refund'''
print('\nSingle Net Risk Premium Refund at End of the Year of Death')
pureEndow = [ct.nEx(x=55, n=term) for ct in ct_lst]
tli_refund = [ct.nAx(x=55, n=term) / (1 - ct.nEx(x=55, n=term)) for ct in ct_lst]
tli_refund_ = [ct.nAx_(x=55, n=term) / (1 - ct.nEx(x=55, n=term)) for ct in ct_lst]

print('\nPure Endowment')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(pureEndow[idx], 5):,}')

print('\nSingle Net Risk Premium Refund at End of the Term for Discrete Case')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(capital * tli_refund[idx], 5):,}')

print('Refund Cost at End of the the Term for Discrete Case')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(capital * (tli_refund[idx] - tli[idx]), 5):,}')

print('\nSingle Net Risk Premium Refund at End of the Term for Approximation to Continuous Case')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(capital * tli_refund_[idx], 5):,}')

print('Refund Cost at End of the the Term for Approximation to Continuous Case')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(capital * (tli_refund_[idx] - tli_[idx]), 5):,}')

'''
Refund of Leveled Premiums
'''

print('\nLeveled Net Risk Premium Refund at End of the Term for Discrete Case')
tli_leveled_refund = [tli[idx_ct] / (tad[idx_ct] - term_annuity * pureEndow[idx_ct]) for idx_ct, ct in
                      enumerate(ct_lst)]

for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(capital * tli_leveled_refund[idx], 5):,}')
