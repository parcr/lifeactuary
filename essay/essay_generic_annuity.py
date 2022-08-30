__author__ = "PedroCR"

from essential_life import mortality_table as mt, annuities, read_soa_table_xml as rst

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)

a1 = annuities.annuity_x(mt=mt_TV7377, x=50, x_first=51, x_last=55, i=2, g=.0, m=10, method='udd')
print(a1)


a2 = annuities.aax(mt=mt_GRF95, x=45, i=2, g=0, m=10)
print(a2)
a3 = annuities.ax(mt=mt_GRF95, x=45, i=2, g=0, m=10)
print(a3)
