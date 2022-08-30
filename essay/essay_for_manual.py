from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst
import pandas as pd

# reads soa table
soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')
table_manual_qx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='qx')
table_manual_lx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='lx')

# creates mortality table from 1x of soa table
tv7377 = mortality_table.MortalityTable(data_type='q', mt=soa.table_qx, perc=100, last_q=1)
grf95 = mortality_table.MortalityTable(data_type='q', mt=list(table_manual_qx['GRF95']), perc=100, last_q=1)
grm95 = mortality_table.MortalityTable(data_type='l', mt=list(table_manual_lx['GRM95']), perc=100, last_q=1)

print('Some Tests')
x = 17.5
print(tv7377.lx_bal(x))
print(tv7377.lx_cfm(x))
print(tv7377.lx_udd(x))

print()
x0 = 17.5
n0 = 62.5
lst_npx = [grf95.npx(x=x0, n=n0, method=m) for m in grf95.methods]
lst_npx_2 = [grf95.npx(x=int(x0), n=int(n0), method=m) for m in grf95.methods]

print(lst_npx)
print(lst_npx_2)

''' Commutation Table '''
tv7377_ct = commutation_table.CommutationFunctions(i=2, g=0, data_type='q', mt=soa.table_qx, perc=100, app_cont=False)
tv7377_ct_ = commutation_table.CommutationFunctions(i=2, g=0, data_type='q', mt=soa.table_qx, perc=100, app_cont=True)
grf95_ct = commutation_table.CommutationFunctions(i=1.5, g=0, data_type='q',
                                                  mt=list(table_manual_qx['GRF95']), perc=100, app_cont=False)
grm95_ct = commutation_table.CommutationFunctions(i=1.5, g=0, data_type='l',
                                                  mt=list(table_manual_lx['GRM95']), perc=100, app_cont=False)

''' Present Value'''
print()
pv = tv7377_ct.present_value(probs=1, age=None,
                             spot_rates=[1.2, 1.4, 1.8, 1.6, 1.9], capital=[100, -25, 120, 300, -50])
print('Present Value:', pv)

pv = tv7377_ct.present_value(probs=None, age=35,
                             spot_rates=[1.2, 1.4, 1.8, 1.6, 1.9], capital=[100, -25, 120, 300, -50])
print('Present Value:', pv)


''' cenas com diferimento'''

print()
a= tv7377_ct.nIArx(50,10,0,1000,50)
print(a)
b= tv7377_ct.nIArx(40,10,10,1000,50)
print(b)



