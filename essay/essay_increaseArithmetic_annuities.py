__author__ = "PedroCR"

from essential_life import mortality_table as mt, commutation_table, read_soa_table_xml as rst

# lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
# lt_grf95 = mortality_table.MortalityTable(mt=GRF95)

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)


cf_tv7377 = commutation_table.CommutationFunctions(i=2, g=0, mt=soa_TV7377.table_qx)
print(cf_tv7377.df_commutation_table())

aan = cf_tv7377.naax(x=50, n=15, m=1)

ann_ai = cf_tv7377.t_nIaax(x=50, n=15, m=1, defer=0, first_amount=1, increase_amount=1)
print(ann_ai)