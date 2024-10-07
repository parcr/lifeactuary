from soa_tables import read_soa_table_xml as rst
from lifeActuary import mortality_table as mt
from lifeActuary import annuities as la

######################################################################################################################
#                                         Chapter 4 - Life Annuities                                               #
######################################################################################################################

# reads soa table TV7377
soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')

# creates a mortality table
tv7377 = mt.MortalityTable(data_type='q', mt=soa.table_qx, perc=100, last_q=1)

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 4.1 - Whole Life Annuities
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Immediate
la.ax(mt=tv7377, x=50, i=2, g=0, m=1) # 21.554432773700235
la.ax(mt=tv7377, x=50, i=2, g=0, m=4, method='udd') # 21.92701292371532

la.ax(mt=tv7377, x=50.5, i=2, g=0, m=1, method='udd') # 21.31196504242326
la.ax(mt=tv7377, x=50.5, i=2, g=0, m=1, method='cfm') # 21.30528881312939
la.ax(mt=tv7377, x=50.5, i=2, g=0, m=1, method='bal') # 21.29867410830813

# Due
la.aax(mt=tv7377, x=50, i=2, g=0, m=1) # 22.55443277370024
la.aax(mt=tv7377, x=50, i=2, g=0, m=4, method='udd') # 22.17701292371532

la.aax(mt=tv7377, x=50.5, i=2, g=0, m=1, method='udd') # 22.31196504242326
la.aax(mt=tv7377, x=50.5, i=2, g=0, m=1, method='cfm') # 22.30528881312939
la.aax(mt=tv7377, x=50.5, i=2, g=0, m=1, method='bal') # 22.298674108308134

# Deferred Immediate
la.t_ax(mt=tv7377, x=50, i=2, g=0, m=1, defer=5)
la.t_ax(mt=tv7377, x=50, i=2, g=0, m=4, defer=5, method='udd')

la.t_ax(mt=tv7377, x=50.5, i=2, g=0, m=1, defer=5, method='udd') #
la.t_ax(mt=tv7377, x=50.5, i=3, g=0, m=1, defer=5, method='udd') #
la.t_ax(mt=tv7377, x=50.5, i=2, g=1, m=1, defer=5, method='udd') #

# Deferred Due
la.t_aax(mt=tv7377, x=50, i=2, g=0, m=1, defer=5)
la.t_aax(mt=tv7377, x=50, i=2, g=0, m=4, defer=5, method='udd')

la.t_aax(mt=tv7377, x=50.5, i=2, g=0, m=1, defer=5, method='udd') #
la.t_aax(mt=tv7377, x=50.5, i=3, g=0, m=1, defer=5, method='udd') #
la.t_aax(mt=tv7377, x=50.5, i=2, g=1, m=1, defer=5, method='udd') #



# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 4.2 - Temporary Life Annuities
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Immediate
la.nax(mt=tv7377, x=50, n=10, i=2, g=0, m=1) # 8.756215803256637
la.nax(mt=tv7377, x=50, n=10, i=2, g=0, m=2) # 8.811587860311260
la.nax(mt=tv7377, x=50, n=10, i=2, g=0, m=2, method='cfm') # 8.811571464621458

# Due
la.nax(mt=tv7377, x=50, n=10, i=2, g=0, m=1) # 8.756215803256637
la.nax(mt=tv7377, x=50, n=10, i=2, g=0, m=2) # 8.81158786031126
la.nax(mt=tv7377, x=50, n=10, i=2, g=0, m=2, method='cfm') # 8.811571464621458

# Deferred Immediate
la.t_nax(mt=tv7377, x=50, n=10, i=2, g=0, m=1, defer=2)   # 8.316881544013759
la.t_nax(mt=tv7377, x=50, n=10, i=2, g=0, m=2, defer=1.5) # 8.480554177218124
la.t_nax(mt=tv7377, x=50, n=10, i=2, g=0, m=2, defer=1.5, method='cfm') # 8.480533451243083

# Deferred Due
la.t_naax(mt=tv7377, x=50, n=10, i=2, g=0, m=1, defer=2)   # 8.535558101895862
la.t_naax(mt=tv7377, x=50, n=10, i=2, g=0, m=2, defer=1.5) # 8.590388221834296
la.t_naax(mt=tv7377, x=50, n=10, i=2, g=0, m=2, defer=1.5, method='bal') # 8.590351413627872

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 4.3 - Life Annuities with variable terms
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Immediate
la.nIax(mt=tv7377, x=50, n=10, i=2, m=1, first_amount=1, increase_amount=1, method='udd')  # 46.330171698412386
la.nIax(mt=tv7377, x=50, n=10, i=2, m=1, first_amount=1, increase_amount=2, method='udd')  # 83.90412759356813
la.nIax(mt=tv7377, x=50, n=10, i=2, m=1, first_amount=100, increase_amount=-2, method='udd')  # 800.4736685353522
la.nIax(mt=tv7377, x=50, n=10, i=2, m=1, first_amount=1, increase_amount=2, method='udd')  # 83.90412759356813
la.nIax(mt=tv7377, x=50.3, n=10, i=2, m=4, first_amount=1, increase_amount=2, method='cfm')  # 84.66224090334902

# Due
la.nIaax(mt=tv7377, x=50, n=10, i=2, m=1, first_amount=1, increase_amount=1, method='udd')  # 47.53746439543621
la.nIaax(mt=tv7377, x=50, n=10, i=2, m=1, first_amount=1, increase_amount=2, method='udd')  # 86.09588781545513
la.nIaax(mt=tv7377, x=50, n=10, i=2, m=1, first_amount=100, increase_amount=-2, method='udd')  # 820.787250701691
la.nIaax(mt=tv7377, x=50, n=10, i=2, m=1, first_amount=1, increase_amount=2, method='udd')  # 86.09588781545513
la.nIaax(mt=tv7377, x=50.3, n=10, i=2, m=4, first_amount=1, increase_amount=2, method='cfm')  # 85.21250336665355


# Deferred Immediate
la.t_nIax(mt=tv7377, x=50, n=10, i=2, m=1, defer=2, first_amount=1, increase_amount=1, method='udd')  # 45.89083743916951
la.t_nIax(mt=tv7377, x=50, n=10, i=2, m=1, defer=2, first_amount=1, increase_amount=2, method='udd')  # 83.46479333432525
la.t_nIax(mt=tv7377, x=50, n=10, i=2, m=1, defer=10, first_amount=100, increase_amount=-2, method='udd')  # 585.2087875846838
la.t_nIax(mt=tv7377, x=50, n=10, i=2, m=1, defer=1, first_amount=1, increase_amount=2, method='udd')      # 83.68346989220736
la.t_nIax(mt=tv7377, x=50.3, n=10, i=2, m=4, defer=1, first_amount=1, increase_amount=2, method='cfm')  # 84.43983387860666

# Deferred Due
la.t_nIaax(mt=tv7377, x=50, n=10, i=2, m=1, defer=2, first_amount=1, increase_amount=1, method='udd')  # 47.093981521914785
la.t_nIaax(mt=tv7377, x=50, n=10, i=2, m=1, defer=2, first_amount=1, increase_amount=2, method='udd')  # 85.6524049419337
la.t_nIaax(mt=tv7377, x=50, n=10, i=2, m=1, defer=10, first_amount=100, increase_amount=-2, method='udd')  # 606.6457012514408
la.t_nIaax(mt=tv7377, x=50, n=10, i=2, m=1, defer=1, first_amount=1, increase_amount=2, method='udd')      # 604.6767662017144
la.t_nIaax(mt=tv7377, x=50.3, n=10, i=2, m=4, defer=1, first_amount=1, increase_amount=2, method='cfm')  #  84.98956500937922



#********************************************************************************************************************
# Present Value Function
#********************************************************************************************************************

pv1 = la.present_value(mt=None, age=None, spot_rates=[1.2, 1.4, 1.8, 1.6, 1.9], capital=[100, -25, 120, 300, -50], probs=1)
print('Present Value:', pv1)

pv2 = la.present_value(mt=tv7377, age=35, spot_rates=[1.2, 1.4, 1.8, 1.6, 1.9], capital=[100, -25, 120, 300, -50], probs=None)
print('Present Value:', pv2)