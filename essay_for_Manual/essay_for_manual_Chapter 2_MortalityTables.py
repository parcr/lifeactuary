from lifeActuary import mortality_table as mt
from soa_tables import read_soa_table_xml as rst

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

######################################################################################################################
#                                         Chapter 2 - Mortality Tables                                               #
######################################################################################################################

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 2.2 - Importing Mortality Tables
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# reads soa table
soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')

# read table from excel file
table_manual_qx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='qx')
table_manual_lx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='lx')

# creates mortality tables
tv7377 = mt.MortalityTable(data_type='q', mt=soa.table_qx, perc=100, last_q=1)
grf95 = mt.MortalityTable(data_type='q', mt=list(table_manual_qx['GRF95']), perc=80)
grm95 = mt.MortalityTable(data_type='l', mt=list(table_manual_lx['GRM95']), perc=80)

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 2.3 - Demographic Functions
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

tv7377.lx[50]
tv7377.dx[50]
tv7377.qx[50]
tv7377.px[50]
tv7377.ex[50]
tv7377.w

## Other Examples

# Outputs the information necessary to clone the object
tv7377

# Consults the lx of TV7377
tv7377.lx

# Consults the ex of GRF95
grf95.ex

# extracts all methods from an object
grf95.__dict__

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 2.4 - Survival Probability Functions
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# probability that (50) dies before age 52
tv7377.nqx(50,2)

# probability that an aged 50.5 individual dies before age 53
tv7377.nqx(50.5, 2.5,'udd')
tv7377.nqx(50.5, 2.5, 'cfm')
tv7377.nqx(50.5, 2.5, 'bal')

# probability that (80) reaches age 82
tv7377.npx(80, 2)

# probability that an aged 80.5 individual reaches age 85
tv7377.npx(80.5, 4.5, 'udd')
tv7377.npx(80.5, 4.5, 'cfm')
tv7377.npx(80.5, 4.5, 'bal')

# probability that (30) reaches age 40, but dies before age 50.
tv7377.t_nqx(30, 10, 20)

# probability that an aged 80.5 individual reaches age 85 but dies before age 90.5.
tv7377.t_nqx(80.5, 4.5, 10.5, 'udd')
tv7377.t_nqx(80.5, 4.5, 10.5, 'cfm')
tv7377.t_nqx(80.5, 4.5, 10.5, 'bal')

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 2.5 - Life Expectancy Function
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# complete life expectancy for (60) over the next 10 years
tv7377.exn(60, 10)
tv7377.exn(60, 10, 'cfm')
tv7377.exn(60, 10, 'bal')

# complete life expectancy for (60.1) over the next 10.2 years
tv7377.exn(60.1, 10.2)
tv7377.exn(60.1, 10.2, 'cfm')
tv7377.exn(60.1, 10.2, 'bal')

# Final Example of Section 2.6
x = 65
n = np.linspace(0, 40, num=2*40+1)

# 1
sprob = [tv7377.npx(x=x, n=i, method='cfm') for i in n]

plt.stem(n, sprob)
plt.xlabel('n')
plt.ylabel(r'${}_{n}p_{65}$')
plt.title('Survival Probability of (65)')
plt.savefig('example26' + '.pdf', format='pdf', dpi=3600)
plt.show()

# 2

dprob = [tv7377.nqx(x=x+i, n=1, method='cfm') for i in n]
ages=x+n
plt.stem(ages, dprob, bottom=0.5)
plt.xlabel('x')
plt.ylabel(r'$q_{x}$')
plt.title('Mortality Rate')
plt.savefig('example26b' + '.pdf', format='pdf', dpi=3600)
plt.show()


# 3 - Compute the life expectation of (65+t), $t=0, 0.5, 1, 1.5, ..., 19.5, 40$
# and represent it with an adequate plot.

# porque é que isto não funciona? O problema está no x=x+i
ex222 = [tv7377.exn(x=x+i, n=1000, method='cfm') for i in [100]]
# assim funciona....
tv7377.exn(x=x+0.5, n=tv7377.w-(x+0.5), method='cfm')

