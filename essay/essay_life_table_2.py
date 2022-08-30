__author__ = "PedroCR"

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

mt_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
mt_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
mt_GRM95 = rst.SoaTable('../soa_tables/GRM95.xml')

lt_tv7377 = mortality_table.MortalityTable(mt=mt_TV7377.table_qx)
lt_gRF95 = mortality_table.MortalityTable(mt=mt_GRF95.table_qx)
lt_gRM95 = mortality_table.MortalityTable(mt=mt_GRM95.table_qx)

cf_tv7377 = commutation_table.CommutationFunctions(i=1.4, g=1, mt=mt_TV7377.table_qx)
cf_grf95 = commutation_table.CommutationFunctions(i=1.4, g=1, mt=mt_GRF95.table_qx)
cf_grm95 = commutation_table.CommutationFunctions(i=1.4, g=1, mt=mt_GRM95.table_qx)

print(cf_tv7377.df_commutation_table())
print(cf_tv7377.t_aax(55, m=1, defer=(67-55)))
print(cf_grm95.t_aax(55, m=1, defer=(67-55)))
print(cf_grf95.t_aax(55, m=1, defer=(67-55)))
