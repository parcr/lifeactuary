__author__ = "PedroCR"

from toDelete.mortality_tables_old import TV7377, GRF95
from essential_life import mortality_insurance, mortality_table as mt, mortality_table, commutation_table, \
    read_soa_table_xml as rst

lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
lt_grf95 = mortality_table.MortalityTable(mt=GRF95)

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)

i = 2
x = 45
inc = 1
method = 'udd'
cf_grf95 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_GRF95.table_qx)
cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_TV7377.table_qx)

a_grf = mortality_insurance.IA_x(mt=mt_GRF95, x=x, x_first=46, x_last=50, i=i, inc=inc, method=method)
a_grf = mortality_insurance.IA_x(mt=mt_TV7377, x=x, x_first=46, x_last=50, i=i, inc=inc, method=method)
a_grf_2 = cf_grf95.IAx(x=x)
cf_tv_2 = cf_tv7377.IAx(x=x)
