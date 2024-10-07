from soa_tables import read_soa_table_xml as rst
from lifeActuary import mortality_table as mt
from lifeActuary import life_2heads as l2h

######################################################################################################################
#                                 Chapter 6 - Multiple Lives Contracts                                               #
######################################################################################################################

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')



# reads soa table TV7377
soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
#soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')

# creates a mortality table
#tv7377 = mt.MortalityTable(data_type='q', mt=soa.table_qx, perc=100, last_q=1)
grf95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
tv7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 6.1 - Survival Probability Functions
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# 6.1.1 - npxy
l2h.npxy(mtx=grf95, mty=tv7377, x=25, y=28, n=10, status='joint-life')    # 0.9849888566208177
l2h.npxy(mtx=grf95, mty=tv7377, x=25, y=28, n=10, status='last-survivor') # 0.9999455887520334

l2h.npxy(mtx=grf95, mty=tv7377, x=20.5, y=50.75, n=10.25, status='joint-life', method='bal')    # 0.9382616738238869
l2h.npxy(mtx=grf95, mty=tv7377, x=20.5, y=50.75, n=10.25, status='last-survivor', method='bal') # 0.9997296719615928


# 6.1.2 - nqxy
l2h.nqxy(mtx=grf95, mty=tv7377, x=25, y=28, n=10, status='joint-life')    # 0.015011143379182301
l2h.nqxy(mtx=grf95, mty=tv7377, x=25, y=28, n=10, status='last-survivor') # 5.44112479665721e-05

l2h.nqxy(mtx=grf95, mty=tv7377, x=25.3, y=28.9, n=10.2, status='joint-life')    # 0.016149189892446625
l2h.nqxy(mtx=grf95, mty=tv7377, x=25.3, y=28.9, n=10.2, status='last-survivor') # 6.235816078524757e-05

# 6.1.3 - t_nqxy
l2h.t_nqxy(mtx=grf95, mty=tv7377, x=25, y=28, n=10, t=5, status='joint-life')    # 0.02113247574184618
l2h.t_nqxy(mtx=grf95, mty=tv7377, x=25, y=28, n=10, t=5, status='last-survivor') # 0.0001707562649220229

## Some other Examples

## Considering two individuals of ages x=35 and y=39:

# probability of at least one of the individuals to die in the folowing 6 years
l2h.nqxy(mtx=grf95, mty=tv7377, x=35, y=39, n=6, status='joint-life')  # 0.0167531655997758

# probability that both individuals are dead in the next 10 years
l2h.nqxy(mtx=grf95, mty=tv7377, x=35, y=39, n=10, status='last-survivor') # 0.00023605857493633854

# probability of both individuals being alive 3 years from now
l2h.npxy(mtx=grf95, mty=tv7377, x=35, y=39, n=3, status='joint-life') # 0.9925748168560576

# probability that, at least one of them is alive 20 years from now
l2h.npxy(mtx=grf95, mty=tv7377, x=35, y=39, n=20, status='last-survivor') # 0.998065729626633

# 6.1.4 - exy
l2h.exy(mtx=grf95, mty=tv7377, x=50, y=45, status='joint-life')    # 30.61022001821019
l2h.exy(mtx=grf95, mty=tv7377, x=50, y=45,status='last-survivor') # 44.732448724147964

# 6.1.5 - Groups of Three Heads

# Example 1 - Three heads
x = 35
y = 40
z = 50

px = grf95.npx(x, 10)
py = tv7377.npx(y, 10)
pz = tv7377.npx(z, 10)
pxy = l2h.npxy(mtx=grf95, mty=tv7377,x=x, y=y, n=10, status='joint-life')
pxz = l2h.npxy(mtx=grf95, mty=tv7377, x=x, y=z, n=10, status='joint-life')
pyz = l2h.npxy(mtx=tv7377, mty=tv7377, x=y, y=z, n=10, status='joint-life')

prob_surv_group = pxy + pxz + pyz - 2 * px * py * pz
print(f'probability: {prob_surv_group}')
# 0.9979281371806732

# Example 2 - Three Heads
x = 35
y = 40
z = 50
px = grf95.npx(x, 10)
py = tv7377.npx(y, 10)
pz = tv7377.npx(z, 10)
pxy = l2h.npxy(mtx=grf95, mty=tv7377, x=x, y=y, n=10, status='joint-life')
pxz = l2h.npxy(mtx=grf95, mty=tv7377, x=x, y=z, n=10, status='joint-life')
pyz = l2h.npxy(mtx=tv7377, mty=tv7377, x=y, y=z, n=10, status='joint-life')

prob_surv_group2 = pxy + pxz + pyz - 3 * px * py * pz
print(f'probability: {prob_surv_group2}')
# 0.0834682538323328


# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 6.2 - Multiple Lives Annuities
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# 6.2.1 - axy

# Whole life unitary, immediate annuity, paid annually
l2h.axy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=1, status='joint-life') # 2.1993512333648
l2h.axy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=1, status='last-survivor') # 6.8225885201728

# Whole life unitary, immediate annuity, paid semi-annually
l2h.axy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=2, status='joint-life') # 2.4380423029643
l2h.axy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=2, status='last-survivor') # 7.0791923426166

# Whole life unitary, immediate annuity, paid annually, with geometric growth of payments
l2h.axy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=1, m=1, status='joint-life') # 2.2390979768651
l2h.axy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=1, m=1, status='last-survivor') # 2.4886702281877

# Whole life unitary, immediate annuity, paid semi-annually, with geometric growth of payments
l2h.axy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=1, m=2, status='joint-life')    # 7.1346827052150
l2h.axy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=1, m=2, status='last-survivor') # 7.4269936907418

# 6.2.2 - aaxy

# Whole life unitary, immediate annuity, paid annually
l2h.aaxy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=1, status='joint-life')     # 3.1993512333648
l2h.aaxy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=1, status='last-survivor')  # 7.8225885201728

# Whole life unitary, immediate annuity, paid semi-annually
l2h.aaxy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=2, status='joint-life')    # 2.9380423029643
l2h.aaxy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=2, status='last-survivor') # 7.5791923426166

# Whole life unitary, immediate annuity, paid annually, with geometric growth of payments
l2h.aaxy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=1, m=1, status='joint-life')     # 3.2614889566337
l2h.aaxy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=1, m=1, status='last-survivor')  # 8.2060295322671

# Whole life unitary, immediate annuity, paid semi-annually, with geometric growth of payments
l2h.aaxy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=1, m=2, status='joint-life')    # 3.0010826255273
l2h.aaxy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=1, m=2, status='last-survivor') # 7.9640362830804

# 6.2.3 - t_axy

# Whole life unitary, annuity, paid annually, with 2 years deferment
l2h.t_axy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=1, defer=2, status='joint-life')   # 0.9670660101740
l2h.t_axy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=1, defer=2, status='last-survivor') # 4.9549321537268

# 6.2.4 - t_aaxy

# Temporary life annuity due, paid annually, with two years deferment
l2h.t_aaxy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=1, defer=2, status='joint-life')    # 1.4765856167554
l2h.t_aaxy(mtx=tv7377, mty=grf95, x=90, y=95, i=2, g=0, m=1, defer=2, status='last-survivor') # 5.8581438045273

# 6.2.5 - naxy

# Temporary immediate life annuity, paid semi-annually with 10 years term
l2h.naxy(mtx=tv7377, mty=grf95, x=90, y=95, n=10, i=2, g=0, m=2, status='joint-life')   # 2.4319176604755
l2h.naxy(mtx=tv7377, mty=grf95, x=90, y=95, n=10, i=2, g=0, m=2, status='last-survivor') # 6.2483535823922

# 6.2.6 - naaxy

# Temporary due life annuity, paid semi-annually with 10 years term
l2h.naaxy(mtx=tv7377, mty=grf95, x=90, y=95, n=10, i=2, g=0, m=2, status='joint-life')
# 2.9278370585219
l2h.naaxy(mtx=tv7377, mty=grf95, x=90, y=95, n=10, i=2, g=0, m=2, status='last-survivor')
# 6.62436464286

# 6.2.7 - t_naxy

# Temporary deferred life annuity, paid semi-annually with 10 years term
l2h.t_naxy(mtx=tv7377, mty=grf95, x=90, y=95, n=10, i=2, g=0, m=2, defer=2, status='joint-life')
# 1.0874293826744
l2h.t_naxy(mtx=tv7377, mty=grf95, x=90, y=95, n=10, i=2, g=0, m=2, defer=2, status='last-survivor')
# 4.7199415824277

# 6.2.8 - t_naaxy

# Temporary deferred life annuity, paid semi-annually with 10 years term paid in the beginning of periods
l2h.t_naaxy(mtx=tv7377, mty=grf95, x=90, y=95, n=10, i=2, g=0, m=2, defer=2, status='joint-life')
# 1.3417110613438
l2h.t_naaxy(mtx=tv7377, mty=grf95,x=90,y=95,n=10, i=2, g=0, m=2, defer=2, status='last-survivor')
# 5.0967616156346

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Section 6.3 - Multiple Lives Insurance
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# 6.3.1 - nExy

l2h.nExy(mtx=grf95,mty=tv7377, x=35, y=40, i=2, n=1, status='joint-life') # 0.9780058667674981
l2h.nExy(mtx=grf95,mty=tv7377, x=35, y=40, i=2, n=1, status='last-survivor') # 0.9803908602913254

l2h.nExy(mtx=grf95,mty=tv7377,x=51.8,y=48.3,i=2,n=10.5, status='joint-life',method='bal') # 0.7501997252543674
l2h.nExy(mtx=grf95,mty=tv7377,x=51.8,y=48.3,i=2,n=10.5,status='last-survivor',method='bal') # 0.81113659782566

# Some Other Examples
# Actuarial Expected Present Value of 50.000 m.u. paid to a group with two lives (x)=40 and     (y)=50, after 15 years

# Joint Life Group
50000*l2h.nExy(mtx=grf95,mty=tv7377, x=40, y=50, i=2, n=15, status='joint-life') # 32809.08 m.u.

# Last Survivor Group
50000*l2h.nExy(mtx=grf95,mty=tv7377, x=40, y=50, i=2, n=15, status='last-survivor') # 37068.79 m.u.

# 6.3.2 - Axy and Axy_

# End of the Year
l2h.Axy(mtx=grf95, mty=tv7377, x=35, y=40, i=2, status='joint-life')         # 0.4883589555345963
l2h.Axy(mtx=grf95, mty=tv7377, x=35, y=40, i=2, status='last-survivor')      # 0.3279490658724815

l2h.Axy(mtx=grf95, mty=tv7377, x=35, y=40, i=2, m=2, status='joint-life')    # 0.4908020439476468
l2h.Axy(mtx=grf95, mty=tv7377, x=35, y=40, i=2, m=2, status='last-survivor') # 0.3295673114271598

l2h.Axy(mtx=grf95, mty=tv7377, x=35, y=40, i=2, g=1, status='joint-life')    # 0.6947836396955362
l2h.Axy(mtx=grf95, mty=tv7377, x=35, y=40, i=2, g=1, status='last-survivor') # 0.5709211125564813

# Moment of Death
l2h.Axy_(mtx=grf95, mty=tv7377, x=35, y=40, i=2, status='joint-life')        # 0.4932183683115002
l2h.Axy_(mtx=grf95, mty=tv7377, x=35, y=40, i=2, status='last-survivor')     # 0.33121232103103576
l2h.Axy_(mtx=grf95, mty=tv7377, x=35.5, y=40.8, i=2, status='joint-life')    # 0.49972941203977206
l2h.Axy_(mtx=grf95, mty=tv7377, x=55.5, y=40.8, i=2, status='last-survivor') # 0.4263873876757644

# 6.3.3 - t_Axy and t_Axy_

# End of the Period
l2h.t_Axy(mtx=grf95, mty=tv7377, x=35.2, y=40.6, i=2, defer=3, status='joint-life', method='udd')
# 0.48509331522128096
l2h.t_Axy(mtx=grf95, mty=tv7377, x=35.2, y=40.6, i=2, defer=3, status='last-survivor', method='udd')
# 0.3292496637625039
l2h.t_Axy(mtx=grf95, mty=tv7377, x=35.2, y=40.6, i=2, g=1, m=4, defer=3, status='joint-life', method='bal')
# 0.6723379046966992
l2h.t_Axy(mtx=grf95, mty=tv7377, x=35.2, y=40.6, i=2, g=1, m=4, defer=3, status='last-survivor', method='bal')
# 0.5573824479627387

# Moment of Death
l2h.t_Axy_(mtx=grf95, mty=tv7377, x=35.2, y=40, i=2, defer=3, status='joint-life', method='udd')
# 0.485844005557544
l2h.t_Axy_(mtx=grf95, mty=tv7377, x=35.2, y=40, i=2, defer=3, status='last-survivor', method='udd')
# 0.33174709690035026
l2h.t_Axy_(mtx=grf95, mty=tv7377, x=35.2, y=40.6, i=2, g=1, defer=3, status='joint-life', method='cfm')
# 0.676502134404232
l2h.t_Axy_(mtx=grf95, mty=tv7377, x=35.2, y=40.6, i=2, g=1, defer=3, status='last-survivor', method='cfm')
# 0.5608068279976409

# 6.3.4 - nAxy and nAxy_

# End of the Period
l2h.nAxy(mtx=grf95, mty=tv7377, x=55.8, y=40, n=10, i=2, status='joint-life', method='bal')
# 0.051536194942196634
l2h.nAxy(mtx=grf95, mty=tv7377, x=55.8, y=40, n=10, i=2, status='last-survivor', method='bal')
# 0.0007237026849450379
l2h.nAxy(mtx=grf95, mty=tv7377, x=35.9, y=40.6, n=15, i=2, g=1, m=4, status='joint-life')
# 0.17823058360706845
l2h.nAxy(mtx=grf95, mty=tv7377, x=35.9, y=40.6, n=15, i=2, g=1, m=4, status='last-survivor')
# 0.12669408363288304


# Moment of Death
l2h.nAxy_(mtx=grf95, mty=tv7377, x=55.8, y=40, n=10, i=2, status='joint-life', method='bal')
# 0.052049005532310566
l2h.nAxy_(mtx=grf95, mty=tv7377, x=55.8, y=40, n=10, i=2, status='last-survivor', method='bal')
# 0.0007309038840508306
l2h.nAxy_(mtx=grf95, mty=tv7377, x=35.9, y=40.6, n=15, i=2, g=1, status='joint-life')
# 0.17372546866918934
l2h.nAxy_(mtx=grf95, mty=tv7377, x=35.9, y=40.6, n=15, i=2, g=1, status='last-survivor')
# 0.1214957914607578

# 6.3.5 - t_nAxy and t_nAxy_

# End of the period
l2h.t_nAxy_(mtx=grf95, mty=tv7377, x=35, y=40, n=20, i=2, defer=3, status='joint-life')
# 0.09156020490195788
l2h.t_nAxy_(mtx=grf95, mty=tv7377, x=35, y=40, n=20, i=2, defer=3, status='last-survivor')
# 0.00212904926970781
l2h.t_nAxy_(mtx=grf95, mty=tv7377, x=35.2, y=40.6, n=20, i=2, g=1, defer=3, status='joint-life', method='cfm')
# 0.22899218321123424
l2h.t_nAxy_(mtx=grf95, mty=tv7377, x=35.2, y=40.6, n=20, i=2, g=1, defer=3, status='last-survivor', method='cfm')
# 0.14319533154878325
# Moment of Death
l2h.t_nAxy_(mtx=grf95, mty=tv7377, x=35, y=40, n=15, i=2, g=1, defer=20, status='joint-life')
# 0.20792147954614337
l2h.t_nAxy_(mtx=grf95, mty=tv7377, x=35, y=40, n=15, i=2, g=1, defer=20, status='last-survivor')
# 0.08858787155153025
l2h.t_nAxy_(mtx=grf95, mty=tv7377, x=55.8, y=40, n=10, i=2, defer=10, status='joint-life', method='bal')
# 0.09201248078665436
l2h.t_nAxy_(mtx=grf95, mty=tv7377, x=55.8, y=40, n=10, i=2, defer=10, status='last-survivor', method='bal')
# 0.0031667131777407304

# 6.3.6 - nAExy and nAExy_

# End of the period
l2h.nAExy(mtx=grf95, mty=tv7377, x=36, y=41, n=15, i=2, g=1, status='joint-life')
# 0.8660767908641055
l2h.nAExy(mtx=grf95, mty=tv7377, x=36, y=41, n=15, i=2, g=1, status='last-survivor')
# 0.8626451905971021
l2h.nAExy(mtx=grf95, mty=tv7377, x=55.8, y=40, n=10, i=2, status='joint-life', method='cfm')
# 0.8242538413270563
l2h.nAExy(mtx=grf95, mty=tv7377, x=55.8, y=40, n=10, i=2, status='last-survivor', method='cfm')
# 0.8203804618128456

# Moment of Death
l2h.nAExy_(mtx=grf95, mty=tv7377, x=36, y=41, n=15, i=2, g=1, status='joint-life')
# 0.8678007454005405
l2h.nAExy_(mtx=grf95, mty=tv7377, x=36, y=41, n=15, i=2, g=1, status='last-survivor')
# 0.8638424731901125
l2h.nAExy_(mtx=grf95, mty=tv7377, x=55.8, y=40, n=10, i=2, status='joint-life', method='cfm')
# 0.8247666396432718
l2h.nAExy_(mtx=grf95, mty=tv7377, x=55.8, y=40, n=10, i=2, status='last-survivor', method='cfm')
# 0.8203876627116821

# 6.3.7 - t_nAExy and t_nAExy_

# End of the period
l2h.t_nAExy(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, g=0, defer=10, status='joint-life')
# 0.5922187614008853
l2h.t_nAExy(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, g=0, defer=10, status='last-survivor')
# 0.6076108022457168

# Moment of Death
l2h.t_nAExy_(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, g=0, defer=10, status='joint-life')
# 0.5933881039489882
l2h.t_nAExy_(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, g=0, defer=10, status='last-survivor')
# 0.6076500583192895

# 6.3.8 - t_nIArxy and t_nIArxy_

# End of the year
l2h.t_nIArxy(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, defer=0, first_payment=1, inc=1, status='joint-life')
# 0.6490737001595632
l2h.t_nIArxy(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, defer=1, first_payment=1, inc=1, status='joint-life')
# 0.6753668707865095
l2h.t_nIArxy(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, defer=0, first_payment=1, inc=1, status='last-survivor')
# 0.6547667655641614
l2h.t_nIArxy(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, defer=1, first_payment=1, inc=1, status='last-survivor')
# 0.6826053359315403

l2h.t_nIArxy(mtx=grf95, mty=tv7377, x=40.5, y=45.25, n=15, i=2, defer=0, first_payment=1, inc=1, status='joint-life', method='cfm')
# 0.6618029051539888

# Moment of Death
l2h.t_nIArxy_(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, defer=0, first_payment=1, inc=1, status='joint-life')
# 0.6555323040122456
l2h.t_nIArxy_(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, defer=1, first_payment=1, inc=1, status='joint-life')
# 0.6820871046714496
l2h.t_nIArxy_(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, defer=0, first_payment=1, inc=1, status='last-survivor')
# 0.6612820182290613
l2h.t_nIArxy_(mtx=grf95, mty=tv7377, x=40, y=45, n=15, i=2, defer=1, first_payment=1, inc=1, status='last-survivor')
# 0.6893975961192896



# Dá erro
#l2h.t_nIArxy(mtx=grf95, mty=tv7377, x=40.5, y=45.3, n=15.5, i=2, defer=1.5, first_payment=1, inc=1, status='joint-life', method='udd')
