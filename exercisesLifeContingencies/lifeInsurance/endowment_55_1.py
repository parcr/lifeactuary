from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 4
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

'''
1000\Ax{\endow{55}{10}}&=1000\Ax{\term{55}{10}}+ 1000\Ax{\pureendow{55}{10}}
'''

x = 55
capital = 1000
term = 10
term_annuity = 10
endow = [ct.nAEx(x=55, n=term) for ct in ct_lst]
endow_ = [ct.nAEx_(x=55, n=term) for ct in ct_lst]
tad = [ct.naax(x=x, n=term_annuity, m=1) for ct in ct_lst]  # temporary annuity due

for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(capital * endow[idx], 5):,}')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(capital * endow[idx] / tad[idx], 5):,}')

print("\nContinous Case")
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(capital * endow_[idx], 5):,}')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(capital * endow_[idx] / tad[idx], 5):,}')

# show the annuities
print('\nannuities')
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(tad[idx], 5):,}')
