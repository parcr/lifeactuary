from soa_tables import read_soa_table_xml as rst
from lifeActuary import mortality_table as mt
from lifeActuary import annuities as la
from lifeActuary import mortality_insurance as lins

######################################################################################################################
#                                         Chapter 5 - Life Insurance                                               #
######################################################################################################################

# reads soa table TV7377
soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')

# creates a mortality table
tv7377 = mt.MortalityTable(data_type='q', mt=soa.table_qx, perc=100, last_q=1)

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 5.1 - Pure Endowment
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

la.nEx(mt=tv7377, x=50, i=2, g=0, n=5)  # 0.8858069661524853
la.nEx(mt=tv7377, x=50, i=2, g=0, n=10) # 0.7771748278393478
la.nEx(mt=tv7377, x=80, i=2, g=0, n=10) # 0.2283081320230278
la.nEx(mt=tv7377, x=50.4, i=2, g=0, n=10.5, method='bal') # 0.7653132063796898


# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 5.2 - Whole Life Insurance
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

## Payments in the end of the year

# Immediate
lins.Ax(mt=tv7377, x=50, i=2)    # 0.5577562201235239
lins.Ax(mt=tv7377, x=50.7, i=2)  # 0.5613776896906858
lins.Ax(mt=tv7377, x=50.7, i=2, method='cfm') # 0.5615358294624957

# Deferred
lins.t_Ax(mt=tv7377, x=50, defer=2, i=2) # 0.550183040772438

## Payments in the middle of the year

# Immediate, payments in the middle of the year
lins.Ax_(mt=tv7377, x=50, i=2)    # 0.5633061699539693
lins.Ax_(mt=tv7377, x=50.7, i=2)  # 0.5669636749317376
lins.Ax_(mt=tv7377, x=50.7, i=2, method='cfm')  # 0.5671233882723721

# Deferred
lins.t_Ax_(mt=tv7377, x=50, defer=2, i=2) # 0.5556576337284301


# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 5.3 - Term Life Insurance
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

## Payment in the end of the year

# Immediate
lins.nAx(mt=tv7377, x=50, n=10, i=2, g=0) # 0.04676554519168518
lins.nAx(mt=tv7377, x=50, n=10, i=2, g=3) # 0.054219259550225045

# Deferred
lins.t_nAx(mt=tv7377, x=50, n=10, defer=5, i=2, g=0) # 0.059615329779335056
lins.t_nAx(mt=tv7377, x=50, n=10, defer=5, i=2, g=10) # 0.09883714561436167

## Payment in the middle of the year

# Immediate
lins.nAx_(mt=tv7377, x=50, n=10, i=2)      # 0.04723088546086194
lins.nAx_(mt=tv7377, x=50, n=10, i=2, g=3) # 0.05475876795818331

# Deferred
lins.t_nAx_(mt=tv7377, x=50, n=10, defer=5, i=2, g=0) # 0.060208531750847824
lins.t_nAx_(mt=tv7377, x=50, n=10, defer=5, i=2, g=10) # 0.09982062402258575


# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 5.4 - Endowment Insurance
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

## Payment in the end of the year

# Immediate
lins.nAEx(mt=tv7377, x=50, n=10, i=2)       # 0.823940373031033
lins.nAEx(mt=tv7377, x=50, n=10, i=2, g=12) # 0.8627337141815358

# Deferred
lins.t_nAEx(mt=tv7377, x=50, n=10, defer=2, i=2)        # 0.786304068847034
lins.t_nAEx(mt=tv7377, x=50, n=10, defer=10, i=2, g=12) # 0.7133653742582529

## Payment in the Middle of the year

# Immediate
lins.nAEx_(mt=tv7377, x=50, n=10, i=2)       # 0.8244057133002097
lins.nAEx_(mt=tv7377, x=50, n=10, i=2, g=12) # 0.8635850673527166
lins.nAEx_(mt=tv7377, x=50.25, n=10.75, i=2, g=12, method='udd') # 0.8552846772135826
lins.nAEx_(mt=tv7377, x=50.25, n=10.75, i=2, g=12, method='cfm') # 0.8552909163204725
lins.nAEx_(mt=tv7377, x=50.25, n=10.75, i=2, g=12, method='bal') # 0.8552971473777993

# Deferred
lins.t_nAEx_(mt=tv7377, x=50, n=10, defer=2, i=2)        # 0.7868146552887255
lins.t_nAEx_(mt=tv7377, x=50, n=10, defer=10, i=2, g=12) # 0.7148635174567862


# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 5.5 - Life Insurance with Capitals evolving in arithmetic progression
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

## First Capital = Rate of Progression

# Whole Life Increasing LIfe Insurance

lins.IAx(mt=tv7377, x=50, i=2, inc=1)   # 15.807431562003352
lins.IAx_(mt=tv7377, x=50, i=2, inc=1)   # 15.964723312327344

lins.IAx(mt=tv7377, x=50, i=2, inc=10)  # 158.0743156200335
lins.IAx(mt=tv7377, x=50, i=2, inc=100) # 1580.7431562003353

lins.IAx(mt=tv7377, x=50, i=2, inc=0)

# Deferred Increasing Capital Whole Life Insurance
lins.t_IAx(mt=tv7377, x=50, defer=5, i=2, inc=1)  # 13.057686275247685
lins.t_IAx_(mt=tv7377, x=50, defer=5, i=2, inc=1) # 13.187616702044672
lins.t_IAx(mt=tv7377, x=50, defer=5, i=2, inc=10) # 130.57686275247684


# Increasing Capital Term LIfe Insurance

lins.nIAx(mt=tv7377, x=50, n=10, i=2, inc=1)    # 0.2751855520152558
lins.nIAx_(mt=tv7377, x=50, n=10, i=2, inc=1)   # 0.27792378415439706

lins.nIAx(mt=tv7377, x=50, n=10, i=2, inc=10)  # 2.7518555201525583


# Deferred Increasing Capital  Term Life Insurance
lins.t_nIAx(mt=tv7377, x=50, n=10, defer=5, i=2, inc=1)  # 0.3529086516825162
lins.t_nIAx_(mt=tv7377, x=50, n=10, defer=5, i=2, inc=1) # 0.35642026704582747
lins.t_nIAx(mt=tv7377, x=50, n=10, defer=5, i=2, inc=10) # 3.5290865168251617


## First Capital <> Rate of Progression
lins.t_nIArx(mt=tv7377, x=50, n=10, defer=0, i=2, first_amount=1, inc=1) # 0.2751855520152558
lins.t_nIArx(mt=tv7377, x=50, n=10, defer=0, i=2, first_amount=1000, inc=50) # 58.18654553286372
lins.t_nIArx(mt=tv7377, x=50, n=10, defer=10, i=2, first_amount=1000, inc=50) # 101.10261167944806
lins.t_nIArx(mt=tv7377, x=50, n=10, defer=0, i=2, first_amount=1000, inc=-50) # 35.34454485050665
lins.t_nIArx(mt=tv7377, x=50, n=10, defer=10, i=2, first_amount=1000, inc=-50) # 60.26561732559179

lins.t_nIArx_(mt=tv7377, x=50, n=10, defer=0, i=2, first_amount=1, inc=1) # 0.27792378415439706
lins.t_nIArx_(mt=tv7377, x=50, n=10, defer=0, i=2, first_amount=1000, inc=50) # 58.765530395538704
lins.t_nIArx_(mt=tv7377, x=50, n=10, defer=10, i=2, first_amount=1000, inc=50) # 102.10863259378893
lins.t_nIArx_(mt=tv7377, x=50, n=10, defer=0, i=2, first_amount=1000, inc=-50) # 35.696240526185186
lins.t_nIArx_(mt=tv7377, x=50, n=10, defer=10, i=2, first_amount=1000, inc=-50) # 60.865289979325354

## Endowment Insurance, Increasing/Deacreasing Capital
lins.t_nIAErx(mt=tv7377, x=50, n=10, defer=0, i=2, first_amount=1, inc=1) # 8.046933830408733
lins.t_nIAErx(mt=tv7377, x=50, n=10, defer=0, i=2, first_amount=1000, inc=50) # 1185.0900458999179
lins.t_nIAErx(mt=tv7377, x=50, n=10, defer=0, i=2, first_amount=1000, inc=-50) # 462.7907001621479

lins.t_nIAErx_(mt=tv7377, x=50, n=10, defer=5, i=2, first_amount=1, inc=1) # 7.072355164462292
lins.t_nIAErx_(mt=tv7377, x=50, n=10, defer=5, i=2, first_amount=1000, inc=50) # 1048.8296786409842
lins.t_nIAErx_(mt=tv7377, x=50, n=10, defer=5, i=2, first_amount=1000, inc=-50) # 414.7743643440044