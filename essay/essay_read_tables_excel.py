from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst
import pandas as pd

# reads soa table
soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')
table_manual_qx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='qx')
table_manual_lx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='lx')

table_names = ['TV7377', 'GRF95', 'GRM95', 'S2PFA', 'S2PMA']
mt_lst = [mortality_table.MortalityTable(data_type='q', mt=list(table_manual_qx[name]), perc=100, last_q=1)
          for name in table_names]
ct_lst = [commutation_table.CommutationFunctions(i=4., g=0., data_type='q',
                                                 mt=list(table_manual_qx[name]), perc=100, app_cont=False)
          for name in table_names]
