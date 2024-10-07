from lifeActuary import mortality_table as mt
from lifeActuary import life_2heads as a2h
from soa_tables import read_soa_table_xml as rst

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)

# Probabilities
p1 = a2h.nqxy(mtx=mt_GRF95, mty=mt_TV7377, x=25, y=28, n=10, status='joint-life', method='udd')
print(f'probability: {p1}')
p1 = a2h.nqxy(mt_GRF95, mt_TV7377, 25, 28, 10, 'joint-life', 'udd')
print(f'probability: {p1}')

p1 = a2h.npxy(mtx=mt_GRF95, mty=mt_TV7377, x=25, y=28, n=10, status='joint-life', method='udd')
print(f'probability: {p1}')
p1 = a2h.npxy(mt_GRF95, mt_TV7377, 25, 28, 10, 'joint-life', 'udd')
print(f'probability: {p1}')

p1 = a2h.npxy(mtx=mt_GRF95, mty=mt_TV7377, x=25, y=28, n=10, status='last-survivor', method='udd')
print(f'probability: {p1}')
p1 = a2h.npxy(mt_GRF95, mt_TV7377, 25, 28, 10, 'last-survivor', 'udd')
print(f'probability: {p1}')

## Manual
a2h.npxy(mtx=mt_GRF95, mty=mt_TV7377, x=25, y=28, n=10, status='joint-life', method='udd')
a2h.npxy(mtx=mt_GRF95, mty=mt_TV7377, x=25, y=28, n=10, status='last-survivor')
a2h.npxy(mt_GRF95, mt_TV7377, 20.5, 50.75, 10.25, 'joint-life', 'bal')
a2h.npxy(mt_GRF95, mt_TV7377, 20.5, 50.75, 10.25, 'last-survivor', 'bal')

a2h.nqxy(mtx=mt_GRF95, mty=mt_TV7377, x=25, y=28, n=10, status='joint-life')
a2h.nqxy(mtx=mt_GRF95, mty=mt_TV7377, x=25, y=28, n=10, status='last-survivor')
a2h.nqxy(mtx=mt_GRF95, mty=mt_TV7377, x=25.3, y=28.9, n=10.2, status='joint-life')
a2h.nqxy(mtx=mt_GRF95, mty=mt_TV7377, x=25.3, y=28.9, n=10.2, status='last-survivor')

a2h.t_nqxy(mtx=mt_GRF95, mty=mt_TV7377, x=25, y=28, n=10, t=5,  status='joint-life')
a2h.t_nqxy(mtx=mt_GRF95, mty=mt_TV7377, x=25, y=28, n=10, t=5, status='last-survivor')

a2h.nqxy(mt_GRF95, mt_TV7377, 35, 39, 6, 'joint-life')
a2h.nqxy(mt_GRF95, mt_TV7377, 35, 39, 10, 'last-survivor')
a2h.npxy(mt_GRF95, mt_TV7377, 35, 39, 3, 'joint-life')
a2h.npxy(mt_GRF95, mt_TV7377, 35, 39, 20, 'last-survivor')

## 3 heads

# Group extinguishes at second death
x = 35
y = 40
z = 50
px = mt_GRF95.npx(x, 10)
py = mt_TV7377.npx(y, 10)
pz = mt_TV7377.npx(z, 10)
pxy = a2h.npxy(mt_GRF95,mt_TV7377,x=x, y=y, n=10, status='joint-life')
pxz = a2h.npxy(mt_GRF95,mt_TV7377,x=x, y=z, n=10, status='joint-life')
pyz = a2h.npxy(mt_TV7377,mt_TV7377,x=y, y=z, n=10, status='joint-life')

prob_surv_group = pxy + pxz + pyz - 2 * px * py * pz
print(f'probability: {prob_surv_group}')

# Group exists only while exactly two individuals are alive
x = 35
y = 40
z = 50
px = mt_GRF95.npx(x, 10)
py = mt_TV7377.npx(y, 10)
pz = mt_TV7377.npx(z, 10)
pxy = a2h.npxy(mt_GRF95,mt_TV7377,x=x, y=y, n=10, status='joint-life')
pxz = a2h.npxy(mt_GRF95,mt_TV7377,x=x, y=z, n=10, status='joint-life')
pyz = a2h.npxy(mt_TV7377,mt_TV7377,x=y, y=z, n=10, status='joint-life')

prob_surv_group2 = pxy + pxz + pyz - 3 * px * py * pz
print(f'probability: {prob_surv_group2}')

# Life Annuities


# Actuarial Expected Present Value
a2h.nExy(mt_GRF95,mt_TV7377, x=35, y=40, i=2, n=1, status='joint-life', method='udd')
a2h.nExy(mt_GRF95,mt_TV7377, x=35, y=40, i=2, n=1, status='last-survivor', method='udd')

a2h.nExy(mt_GRF95,mt_TV7377, x=51.8, y=48.3, i=2, n=10.5, status='joint-life', method='bal')
a2h.nExy(mt_GRF95,mt_TV7377, x=51.8, y=48.3, i=2, n=10.5, status='last-survivor', method='bal')

a2h.nExy(mt_GRF95,mt_TV7377, x=40, y=50, i=2, n=15, status='joint-life', method='udd')*50000
a2h.nExy(mt_GRF95,mt_TV7377, x=35, y=40, i=2, n=15, status='last-survivor', method='udd')*50000


# Life Insurance
a2h.Axy(mt_GRF95,mt_TV7377, x=35, y=40, i=2, status='joint-life')
a2h.Axy(mt_GRF95,mt_TV7377, x=35, y=40, i=2, status='last-survivor')
a2h.Axy(mt_GRF95,mt_TV7377, x=35, y=40, i=2, m=2, status='joint-life')
a2h.Axy(mt_GRF95,mt_TV7377, x=35, y=40, i=2, m=2, status='last-survivor')
a2h.Axy(mt_GRF95,mt_TV7377, x=35, y=40, i=2, g=1, status='joint-life')
a2h.Axy(mt_GRF95,mt_TV7377, x=35, y=40, i=2, g=1, status='last-survivor')

a2h.Axy_(mt_GRF95, mt_TV7377, x=35, y=40, i=2, status='joint-life')
a2h.Axy_(mt_GRF95, mt_TV7377, x=35, y=40, i=2, status='last-survivor')
a2h.Axy_(mt_GRF95, mt_TV7377, x=35.5, y=40.8, i=2, status='joint-life')
a2h.Axy_(mt_GRF95, mt_TV7377, x=35.5, y=40.8, i=2, status='last-survivor')

a2h.t_Axy(mt_GRF95,mt_TV7377, x=35.2, y=40.6, i=2, defer=3, status='joint-life', method='udd')
a2h.t_Axy(mt_GRF95,mt_TV7377, x=35.2, y=40.6, i=2, defer=3, status='last-survivor', method='udd')
a2h.t_Axy(mt_GRF95,mt_TV7377, x=35.2, y=40.6, i=2, g=1, m=4, defer=3, status='joint-life', method='bal')
a2h.t_Axy(mt_GRF95,mt_TV7377, x=35.2, y=40.6, i=2, g=1, m=4, defer=3, status='last-survivor', method='bal')

a2h.t_Axy_(mt_GRF95, mt_TV7377, x=35.2, y=40.6, i=2, defer=3, status='joint-life', method='udd')
a2h.t_Axy_(mt_GRF95, mt_TV7377, x=35.2, y=40.6, i=2, defer=3, status='last-survivor', method='udd')
a2h.t_Axy_(mt_GRF95, mt_TV7377, x=35.2, y=40.6, i=2, g=1, defer=3, status='joint-life', method='cfm')
a2h.t_Axy_(mt_GRF95, mt_TV7377, x=35.2, y=40.6, i=2, g=1, defer=3, status='last-survivor', method='cfm')

a2h.nAxy(mt_GRF95,mt_TV7377, x=55.8, y=40, n=10, i=2, status='joint-life', method='bal')
a2h.nAxy(mt_GRF95,mt_TV7377, x=55.8, y=40, n=10, i=2, status='last-survivor', method='bal')
a2h.nAxy(mt_GRF95,mt_TV7377, x=35.9, y=40.6, n=15, i=2, g=1, m=4, status='joint-life')
a2h.nAxy(mt_GRF95,mt_TV7377, x=35.9, y=40.6, n=15, i=2, g=1, m=4, status='last-survivor')
a2h.nAxy(mt_GRF95,mt_TV7377, x=36, y=41, n=15, i=2, g=1, m=4, status='joint-life')
a2h.nAxy(mt_GRF95,mt_TV7377, x=36, y=41, n=15, i=2, g=1, m=4, status='last-survivor')

a2h.nAxy_(mt_GRF95, mt_TV7377, x=55.8, y=40, n=10, i=2, status='joint-life', method='bal')
a2h.nAxy_(mt_GRF95, mt_TV7377, x=55.8, y=40, n=10, i=2, status='last-survivor', method='bal')
a2h.nAxy_(mt_GRF95, mt_TV7377, x=35.9, y=40.6, n=15, i=2, g=1, status='joint-life')
a2h.nAxy_(mt_GRF95, mt_TV7377, x=35.9, y=40.6, n=15, i=2, g=1, status='last-survivor')

a2h.t_nAxy_(mt_GRF95, mt_TV7377, x=35, y=40, n=20, i=2, defer=3, status='joint-life')
a2h.t_nAxy_(mt_GRF95, mt_TV7377, x=35, y=40, n=20, i=2, defer=3, status='last-survivor')
a2h.t_nAxy_(mt_GRF95, mt_TV7377, x=35.2, y=40.6, n=20, i=2, g=1, defer=3, status='joint-life', method='cfm')
a2h.t_nAxy_(mt_GRF95, mt_TV7377, x=35.2, y=40.6, n=20, i=2, g=1, defer=3, status='last-survivor', method='cfm')

a2h.t_nAxy_(mt_GRF95, mt_TV7377, x=35, y=40, n=15, i=2, g=1, defer=20, status='joint-life')
a2h.t_nAxy_(mt_GRF95, mt_TV7377, x=35, y=40, n=15, i=2, g=1, defer=20, status='last-survivor')
a2h.t_nAxy_(mt_GRF95, mt_TV7377, x=55.8, y=40, n=10, i=2, defer=10, status='joint-life', method='bal')
a2h.t_nAxy_(mt_GRF95, mt_TV7377, x=55.8, y=40, n=10, i=2, defer=10, status='last-survivor', method='bal')

a2h.nAExy(mt_GRF95,mt_TV7377, x=36, y=41, n=15, i=2, g=1, status='joint-life')
a2h.nAExy(mt_GRF95,mt_TV7377, x=36, y=41, n=15, i=2, g=1, status='last-survivor')
a2h.nAExy(mt_GRF95,mt_TV7377, x=55.8, y=40, n=10, i=2, status='joint-life', method='cfm')
a2h.nAExy(mt_GRF95,mt_TV7377, x=55.8, y=40, n=10, i=2, status='last-survivor', method='cfm')

a2h.nAExy_(mt_GRF95, mt_TV7377, x=36, y=41, n=15, i=2, g=1, status='joint-life')
a2h.nAExy_(mt_GRF95, mt_TV7377, x=36, y=41, n=15, i=2, g=1, status='last-survivor')
a2h.nAExy_(mt_GRF95, mt_TV7377, x=55.8, y=40, n=10, i=2, status='joint-life', method='cfm')
a2h.nAExy_(mt_GRF95, mt_TV7377, x=55.8, y=40, n=10, i=2, status='last-survivor', method='cfm')

a2h.t_nAExy(mt_GRF95,mt_TV7377, x=40, y=45, n=15, i=2, g=0, defer=10, status='joint-life')
a2h.t_nAExy(mt_GRF95,mt_TV7377, x=40, y=45, n=15, i=2, g=0, defer=10, status='last-survivor')

a2h.t_nAExy_(mt_GRF95, mt_TV7377, x=40, y=45, n=15, i=2, g=0, defer=10, status='joint-life')
a2h.t_nAExy_(mt_GRF95, mt_TV7377, x=40, y=45, n=15, i=2, g=0, defer=10, status='last-survivor')




# Life Expectancy
a2h.exy(mt_GRF95,mt_TV7377, x=50, y=45,status='joint-life')
a2h.exy(mt_GRF95,mt_TV7377, x=50, y=45,status='last-survivor')









# Annuities
gener_ann = a2h.annuity_xy(mtx=mt_TV7377, mty=mt_GRF95, x=25, x_first_payment=25, x_last_payment=200, y=28,
                           i=5, g=0, m=1, status='last-survivor', method='udd')
print(f'gener_ann: {gener_ann}')
gener_ann = a2h.annuity_xy(mtx=mt_TV7377, mty=mt_GRF95, x=25, x_first_payment=25, x_last_payment=200, y=28,
                           i=5, g=0, m=2, status='last-survivor', method='udd')
print(f'gener_ann: {gener_ann}')

# Life Insurance
#gener_li = a2h.A_xy(mtx=mt_TV7377, mty=mt_GRF95, x=25, x_first_payment=25, x_last_payment=200, y=28,
#                    i=5, g=0, m=1, status='last-survivor', method='udd')
#print(f'gener_li: {gener_li}')

##########################################  MANUAL  #########################################################

p = a2h.t_nIArxy(mt_GRF95, mt_TV7377, x=35, y=40, n=10, i=2, defer=1, first_payment=1, inc=1,
                 status='joint-life', method='udd')
print(p)

p = a2h.t_nIArxy(mt_GRF95, mt_TV7377, x=35, y=40, n=10, i=2, defer=1, first_payment=1, inc=1,
                 status='last-survivor', method='udd')
print(p)

