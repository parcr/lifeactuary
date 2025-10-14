__author__ = "PedroCR"
import os
import sys

# Add project root to path so we can import modules
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
from lifeActuary import mortality_insurance as mi
from lifeActuary import mortality_insurance_frac as mif

from lifeActuary import mortality_table, commutation_table
from soa_tables import read_soa_table_xml as rst

""" interest rate """
interest_rate = 4  # 2.5

""" read the tables """
table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable(os.path.join(project_root, 'soa_tables', name + '.xml')) for name in table_names]

lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

""" reads manually imported mortality table """
table_manual_qx = pd.read_excel(os.path.join(project_root, 'soa_tables', 'tables_manual.xlsx'), sheet_name='qx')
table_manual_lx = pd.read_excel(os.path.join(project_root, 'soa_tables', 'tables_manual.xlsx'), sheet_name='lx')

new_table_names = ['S2PMA', 'S2PFA']
new_lt_lst = [mortality_table.MortalityTable(mt=table_manual_lx[n], data_type='l') for n in new_table_names]
new_ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, data_type='l', mt=table_manual_lx[l]) for l
              in new_table_names]

""" The below format does not work, because we need to pass the first number as the first age """
# new_ct_lst_2= [commutation_table.CommutationFunctions(i=interest_rate, g=0, data_type='l', mt=list(l.lx)) for l in new_lt_lst]
""" The below format does work, because we append the first age  """
new_ct_lst_2 = [commutation_table.CommutationFunctions(i=interest_rate, g=0, data_type='l', mt=[l.x0] + list(l.lx)) for
                l in new_lt_lst]

lt_lst += new_lt_lst
ct_lst += new_ct_lst

ct = ct_lst[0]

# Expected Value for t_nAx_mom
a = mi.t_nAx_mom(mt=ct, x=45, n=10, defer=20, i=4, g=0, method='udd', mom=0)
b = ct.t_nqx(x=45, t=20, n=10, method='udd')
print(a, ' and ', b)

# Expected Value for t_nAx_mom but frac
a1 = mi.A_x(mt=ct, x=45, x_first=45 + 21, x_last=45 + 20 + 10, i=4, g=.0, method='udd')
a1_c = mi.t_nAx(mt=ct, x=45, n=10, defer=20, i=4, g=0, method='udd')
a1_ = mi.A_x(mt=ct, x=45, x_first=45 + 21, x_last=45 + 20 + 10, i=4, g=.0, method='udd') * (
            1 + interest_rate / 100) ** .5

a2 = mif.A_x(mt=ct, x=45, x_first=45 + 21, x_last=45 + 20 + 10, i=4, g=.0, m=1, method='udd')
b2 = mi.t_nAx_mom(mt=ct, x=45, n=10, defer=20, i=4, g=0, method='udd', mom=1)
print(a1, ' and ', a1_c, ' and ', a2, ' and ', b2, ' and', a1_)


m = 12
a_frac2 = mif.A_x(mt=ct, x=45, x_first=45 + 20 + 1 / m, x_last=45 + 20 + 10, i=4, g=.0,
                  m=m, method='udd')
print(a_frac2)
