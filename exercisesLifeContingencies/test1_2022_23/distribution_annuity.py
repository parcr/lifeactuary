import os
import sys

import numpy as np

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst
from annuities_certain import annuities_certain

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95', 'GRM80']
interest_rate = 1.5
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

table_idx = 0
name = table_names[table_idx]
print(f'The Table being used is {name} with a rate of interest equal to {interest_rate}%.')
lt = lt_lst[table_idx]
ct = ct_lst[table_idx]

# Compute Annuity
x = 70
capital = 10000
ann = ct.aax(x=x, m=1)
ann_capital = capital * ann
ann_certain = annuities_certain.Annuities_Certain(interest_rate=interest_rate, m=1)
ann_maximum = ann_certain.aan(terms=ct.w - x + 1)

print(f'The expected value is {ann} so, considering the capital {ann_capital} '
      f'for a maximum of {ann_maximum * capital}')

# Compute the argument of the cdf of K_x
value = 124632.96
v = 1 / (1 + interest_rate / 100)
d = 1 - v
arg = np.log(1 - d * value / capital) / np.log(v) - 1
# Compute the probability
prob = ct.nqx(x=x, n=int(arg))
print(f'The probability of paying less than {int(arg) + 1} is equal to {prob}.')

# Compute the variance
i2 = (1 + interest_rate / 100) ** 2 - 1
interest_rate2 = i2 * 100
v2 = 1 / (1 + interest_rate2 / 100)
d2 = 1 - v2
ct2 = commutation_table.CommutationFunctions(i=interest_rate2, g=0, mt=mt_lst[table_idx].table_qx)

expect_value_Kx = 1 - d * ct.aax(x=x, m=1)
expect_value_Kx2 = 1 - d2 * ct2.aax(x=x, m=1)
var_Kx = expect_value_Kx2 - expect_value_Kx ** 2
var_ann = var_Kx / d ** 2
print(f'Expected Value v^(K_x+1)={expect_value_Kx}')
print(f'Expected Value v^(2(K_x+1))={expect_value_Kx2}')
print(f'Variance v^((K_x+1))={var_Kx}')
print(f'Variance Annuity={var_ann}')
print(f'Variance Annuity with capital={var_ann*capital**2}')
print(f'Standard Deviation Annuity with capital={var_ann**.5*capital}')