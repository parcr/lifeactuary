from soa_tables import read_soa_table_xml as rst
from lifeActuary import commutation_table as ct
import numpy as np

import pandas as pd

######################################################################################################################
#                                         Chapter 7 - Actuarial Tables                                               #
######################################################################################################################

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 7.1 - Class CommutationTable
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# reads soa table TV7377
soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')

# read table from excel file
table_manual_qx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='qx')
table_manual_lx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='lx')

# creates an Actuarial Table from qx of SOA table
tv7377_ct = ct.CommutationFunctions(i=2, g=0, data_type='q', mt=soa.table_qx, perc=100, app_cont=False)

# creates an Actuarial Table from qx of GRF95 available in the Excel file
grf95_ct = ct.CommutationFunctions(i=1.5, g=0, data_type='q', mt=list(table_manual_qx['GRF95']), perc=100,
                                   app_cont=False)

# creates an Actuarial Table from lx of GRM95 available in the Excel file
grm95_ct = ct.CommutationFunctions(i=1.5, g=0, data_type='l', mt=list(table_manual_lx['GRM95']), perc=100,
                                   app_cont=False)

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 7.4 - Life Annuities Using Commutation Tables
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

'''Whole Life Annuities'''
tv7377_ct.ax(x=50, m=1)  # 21.554432773700235
tv7377_ct.ax(x=50, m=4)  # 21.929432773700235

tv7377_ct.aax(x=50, m=1)  # 22.55443277370024
tv7377_ct.aax(x=50, m=4)  # 22.17943277370024

tv7377_ct.t_ax(x=50, m=1, defer=5)  # 16.899196591768252
tv7377_ct.t_ax(x=50, m=14, defer=5)  # 17.231374204075433

tv7377_ct.t_aax(x=50, m=1, defer=5)  # 17.78500355792074
tv7377_ct.t_aax(x=50, m=4, defer=5)  # 17.45282594561355

'''Temporary Life Annuities'''
tv7377_ct.nax(x=50, n=10, m=1)  # 8.756215803256639
tv7377_ct.nax(x=50, n=10, m=4)  # 8.839775242816884

tv7377_ct.naax(x=50, n=10, m=1)  # 8.979040975417291
tv7377_ct.naax(x=50, n=10, m=4)  # 8.895481535857046

tv7377_ct.t_nax(x=50, n=10, m=1, defer=5)  # 7.670292001795834
tv7377_ct.t_nax(x=50, n=10, m=4, defer=5)  # 7.750622055449898

tv7377_ct.t_naax(x=50, n=10, m=1, defer=5)  # 7.8845054782066715
tv7377_ct.t_naax(x=50, n=10, m=4, defer=5)  # 7.804175424552608

'''Life Annuities with Variable Terms'''
tv7377_ct.t_nIax(x=50, n=10, m=1, defer=0, first_amount=1, increase_amount=1)  # 46.33017
tv7377_ct.t_nIax(x=50, n=10, m=1, defer=0, first_amount=1, increase_amount=5)  # 196.62599
tv7377_ct.t_nIax(x=50, n=10, m=1, defer=0, first_amount=100, increase_amount=-5)  # 687.75180

tv7377_ct.t_nIaax(x=50, n=10, m=1, defer=0, first_amount=1, increase_amount=1)  # 47.5374643
tv7377_ct.t_nIaax(x=50, n=10, m=1, defer=0, first_amount=1, increase_amount=5)  # 201.771158
tv7377_ct.t_nIaax(x=50, n=10, m=1, defer=0, first_amount=100, increase_amount=-5)  # 705.111980

'''Geometric Life Annuities'''
from lifeActuary import commutation_table as ct

# reads SOA table
soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')

# creates an actuarial table from qx of SOA table with geometric increase of 5% on payments
tv7377_ctg_inc = ct.CommutationFunctions(i=2, g=5, data_type='q', mt=soa.table_qx, perc=100, app_cont=False)

# creates an actuarial table from qx of SOA table with geometric decrease of 5% on payments
tv7377_ctg_dec = ct.CommutationFunctions(i=2, g=-5, data_type='q', mt=soa.table_qx, perc=100, app_cont=False)

# actuarial present value of a geometrically evolving life annuity for a 50 years old indidivual, for 10 years period
tv7377_ctg_inc.naax(50, 10, 1)  # 11.18091822195998
tv7377_ctg_dec.naax(50, 10, 1)  # 7.281682932595854

'''Present Value Function'''
pv1 = tv7377_ct.present_value(probs=None, age=35,
                              spot_rates=[1.2, 1.4, 1.8, 1.6, 1.9], capital=[100, -25, 120, 300, -50])
print('Present Value:', pv1)
# 424.2408517830521

pv2 = tv7377_ct.present_value(probs=1, age=None,
                              spot_rates=[1.2, 1.4, 1.8, 1.6, 1.9], capital=[100, -25, 120, 300, -50])
print('Present Value:', pv2)
# 425.750701233034

x = 50
survprobs = [1-1.5*tv7377_ct.qx[x], 1-1.55*tv7377_ct.qx[x + 1], 1-1.6*tv7377_ct.qx[x + 2], 1-1.65*tv7377_ct.qx[x + 3],
     1-1.7*tv7377_ct.qx[x + 4]]
pv3 = tv7377_ct.present_value(probs=survprobs, age=None, spot_rates=[1.2, 1.4, 1.8, 1.6, 1.9],
                              capital=[100, -25, 120, 300, -50])
print('SurvProbs:', survprobs)
print('Present Value:', pv3)

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 7.5 - Life Insurance Using Commutation Tables
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# ********************************************************************************************************************
# Payments in the end of the periods
# ********************************************************************************************************************

'''Pure Endowment'''
tv7377_ct.nEx(x=50, n=5)  # 0.8858069661524854
tv7377_ct.nEx(x=50, n=10)  # 0.7771748278393479
tv7377_ct.nEx(x=80, n=10)  # 0.2283081320230277

'''Whole Life Insurance'''
tv7377_ct.Ax(x=50)  # 0.5577562201235239

tv7377_ct.t_Ax(x=50, defer=2)  # 0.550183040772438

'''Temporary Life Insurance'''
tv7377_ct.nAx(x=50, n=10)  # 0.046765545191685375

tv7377_ct.t_nAx(x=50, n=10, defer=5)  # 0.059615329779334834

'''Endowment Insurance'''
tv7377_ct.nAEx(x=50, n=10)  # 0.8239403730310333

tv7377_ct.t_nAEx(x=50, n=10, defer=2)  # 0.7863040688470341

tv7377_ct.t_nAEx(x=50, n=10, defer=10)  # 0.6434898056742981

'''Temporary Life Insurance with variable Capitals'''
tv7377_ct.IAx(x=50)  # 15.807431562003355

tv7377_ct.nIAx(x=50, n=10)  # 0.2751855520152587
tv7377_ct.nIAx(x=50, n=50)  # 15.702602747043013

tv7377_ct.t_nIArx(x=50, n=10, defer=0, first_amount=1000, increase_amount=50)  # 58.18654553286392
tv7377_ct.t_nIArx(x=50, n=10, defer=10, first_amount=1000, increase_amount=50)  # 133.3402470815534
tv7377_ct.t_nIArx(x=50, n=10, defer=0, first_amount=1000, increase_amount=-50)  # 35.344544850506836
tv7377_ct.t_nIArx(x=50, n=10, defer=10, first_amount=1000, increase_amount=-50)  # 28.027981923486493

# ********************************************************************************************************************
# Payments in the middle of the year
# ********************************************************************************************************************

'''Whole Life Insurance'''
tv7377_ct.Ax_(x=50)  # 0.5633061699539695

tv7377_ct.t_Ax_(x=50, defer=2)  # 0.5556576337284301

'''Temporary Life Insurance'''
tv7377_ct.nAx_(x=50, n=10)  # 0.047230885460862126

tv7377_ct.t_nAx_(x=50, n=10, defer=5)  # 0.060208531750847685

'''Endowment Insurance'''
tv7377_ct.nAEx_(x=50, n=10)  # 0.8244057133002101

tv7377_ct.t_nAEx_(x=50, n=10, defer=2)  # 0.7868146552887256

tv7377_ct.t_nAEx_(x=50, n=10, defer=10)  # 0.6442926524583354

'''Temporary Life Insurance with variable Capitals'''
tv7377_ct.IAx_(x=50)  # 15.964723312327344

tv7377_ct.nIAx_(x=50, n=10)  # 0.2779237841543988
tv7377_ct.nIAx_(x=50, n=50)  # 15.858851398889882

tv7377_ct.t_nIArx_(x=50, n=10, defer=0, first_amount=1000, increase_amount=50)  # 58.765530395538875
tv7377_ct.t_nIArx_(x=50, n=10, defer=10, first_amount=1000, increase_amount=50)  # 134.66704838825683
tv7377_ct.t_nIArx_(x=50, n=10, defer=0, first_amount=1000, increase_amount=-50)  # 35.69624052618538
tv7377_ct.t_nIArx_(x=50, n=10, defer=10, first_amount=1000, increase_amount=-50)  # 28.306874184857506
