from soa_tables import read_soa_table_xml as rst
from lifeActuary.commutation_table_frac import CommutationFunctionsFrac
import pandas as pd

######################################################################################################################
#                                         Chapter 7 - Actuarial Tables                                               #
######################################################################################################################

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 7.2 - Class CommutationTableFrac
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# reads soa table TV7377
soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')
table_manual_qx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='qx')
table_manual_lx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='lx')

# creates an actuarial table from qx of SOA table, for ages x+k*0.5, x=0,...,w, k=0,1.
tv7377_ct_f2 = CommutationFunctionsFrac(i=2, g=0, data_type='q', mt=soa.table_qx, perc=100, frac=2, method='udd')

# creates an actuarial table from qx of SOA table, for ages x+k*0.25, x=0,...,w, k=0,1,2,3
tv7377_ct_f4 = CommutationFunctionsFrac(i=2, g=0, data_type='q', mt=soa.table_qx, perc=100, frac=4, method='udd')

# creates an actuarial table from qx of SOA table, for ages x+k*1/6, x=0,...,w, k=0,1,...,5
tv7377_ct_f6 = CommutationFunctionsFrac(i=2, g=0, data_type='q', mt=soa.table_qx, perc=100, frac=6, method='udd')

# creates an actuarial table from qx of SOA table, for ages x+k*1/365, x=0,...,w,              k=0,1,...,364
tv7377_ct_f365 = CommutationFunctionsFrac(i=2, g=0, data_type='q', mt=soa.table_qx, perc=100, frac=365, method='udd')

# creates an actuarial table from qx of SOA table, for ages x+k*0.5, x=0,...,w, k=0,1 with rate of growing of 1%
tv7377_ct_f2_g1 = CommutationFunctionsFrac(i=2, g=1, data_type='q', mt=soa.table_qx, perc=100, frac=2, method='udd')


# Age to Index Function
tv7377_ct_f2.age_to_index(50, 0.5)
tv7377_ct_f4.age_to_index(50, 0.75)
tv7377_ct_f6.age_to_index(50, 5/6)

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 7.3 - CommutationTableFrac Methods
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Example 1
x = 50.5
index_age = tv7377_ct_f2.age_to_index(int(x), x - int(x))
a = tv7377_ct_f2.Dx_frac[index_age]
print(f'For age {x}, with index {index_age}, Dx={a}')


# Several Examples

x=35+1/6
index_age=tv7377_ct_f6.age_to_index(int(x), x-int(x))  # 211
a=tv7377_ct_f6.Nx_frac[index_age]
print(f'For age {x} with index {index_age}, Nx={a}')

## Present value of an unitary whole life annuity due, paid quarterly to an individual aged    x=65.25
x=65.25
index_age=tv7377_ct_f4.age_to_index(int(x), x-int(x))  # 261
a=tv7377_ct_f4.Nx_frac[index_age]/tv7377_ct_f4.Dx_frac[index_age]
print(f'For age {x} with index {index_age}, ax={a}')

## Present value of an unitary whole life annuity due, paid annually to an individual aged    x=65.25
print(f'For age {x}, with index {index_age}, ax(4)={a/4}')

## Present value of an unitary whole life annuity immediate, paid daily to an individual aged    x=66+120/365
x=66+120/365
index_age=tv7377_ct_f365.age_to_index(int(x), x-int(x))  # 24210
a=tv7377_ct_f365.Nx_frac[index_age]/tv7377_ct_f365.Dx_frac[index_age]
print(f'For age {x} with index {index_age}, ax={a}')

## Present value of an unitary whole life annuity immediate, paid annually to an individual aged x=66+120/365
print(f'For age {x}, with index {index_age}, ax(365)={a/365}')

## Some Other Examples

# Present value of an unitary whole life annuity due, paid quarterly to an individual aged     x=65.25
x = 65.25
index_age = tv7377_ct_f4.age_to_index(int(x), x - int(x))  # 261
a = tv7377_ct_f4.Nx_frac[index_age] / tv7377_ct_f4.Dx_frac[index_age]
print(f'For age {x}, with index {index_age}, ax(4)={a}')

## Actuarial present Value of unitary annuity due, paid semiannually with 10 terms for (35.5)
x = 35.5
n=10/2
index_age = tv7377_ct_f2.age_to_index(int(x), x - int(x))
index_age_end = tv7377_ct_f2.age_to_index(int(x+n), x+n - int(x+n))
b = (tv7377_ct_f2.Nx_frac[index_age] - tv7377_ct_f2.Nx_frac[index_age_end])/tv7377_ct_f2.Dx_frac[index_age]
print(f'For age {x}, with index {index_age}, with semiannual payments until age {x+n}, with index {index_age_end}, ax:n={b}')

## Actuarial present value of a whole life insurance for (50.75) with 100.000 m.u. capital.
x=50.75
index_age=tv7377_ct_f4.age_to_index(int(x), x-int(x))  # 203
b=100000*tv7377_ct_f4.Mx_frac[index_age]/tv7377_ct_f4.Dx_frac[index_age]
print(f'For age {x}, with index {index_age}, the risk premium is Ax={b}')

## Actuarial present Value of a whole life annuity paid semiannually to an individual aged x = 35.5.
# Payments have a growth rate of 1%
x = 35.5
index_age = tv7377_ct_f2_g1.age_to_index(int(x), x - int(x))  # 151
a = tv7377_ct_f2_g1.Nx_frac[index_age] / tv7377_ct_f2_g1.Dx_frac[index_age]
print(f'For age {x}, with index {index_age}, Gax(2)={a}')


# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 7.4 - Life Annuities Using Commutation Tables
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
