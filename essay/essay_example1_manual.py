import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from essential_life import mortality_table, read_soa_table_xml as rst

mt = rst.SoaTable('../soa_tables/TV7377' + '.xml')
lt = mortality_table.MortalityTable(mt=mt.table_qx)

'''answer'''
x = 55
n = np.linspace(0, 5, 5*12)
probs = [lt.npx(x=x, n=i, method='udd') for i in n]
ages = x + n
df = pd.DataFrame.from_dict({'x': ages, 'npx': probs})
df.to_excel(excel_writer='example1.xlsx', sheet_name='example1', index=False, freeze_panes=(1, 1))


''' plot '''
plt.scatter(ages, probs, s=.5, color='red')

plt.xlabel(r'$x$')
plt.ylabel(r'${}_{n}p_{55}$')
plt.title('Probability of Survival')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig('example1' + '.eps', format='eps', dpi=3600)
plt.show()

