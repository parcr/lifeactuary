import numpy as np
import os
import sys
import pandas as pd

from lifeActuary import mortality_table, commutation_table
from soa_tables import read_soa_table_xml as rst
import matplotlib.pyplot as plt

""" interest rate """
interest_rate = 4 #2.5

""" read the tables """
table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../soa_tables/' + name + '.xml') for name in table_names]

lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]


""" reads manually imported mortality table """
table_manual_qx = pd.read_excel ('../soa_tables/' + 'tables_manual.xlsx', sheet_name ='qx')
table_manual_lx = pd.read_excel ('../soa_tables/' + 'tables_manual.xlsx', sheet_name ='lx')

new_table_names = ['S2PMA', 'S2PFA']
new_lt_lst = [mortality_table.MortalityTable(mt=table_manual_lx[n], data_type='l') for n in new_table_names]
new_ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, data_type='l', mt=table_manual_lx[l]) for l in new_table_names]

""" The below format does not work, because we need to pass the first number as the first age """
# new_ct_lst_2= [commutation_table.CommutationFunctions(i=interest_rate, g=0, data_type='l', mt=list(l.lx)) for l in new_lt_lst]
""" The below format does work, because we append the first age  """
new_ct_lst_2= [commutation_table.CommutationFunctions(i=interest_rate, g=0, data_type='l', mt=[l.x0] + list(l.lx)) for l in new_lt_lst]