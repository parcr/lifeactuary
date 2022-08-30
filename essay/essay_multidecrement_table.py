__author__ = "PedroCR"

from disability_tables import disability_tables as dt
from turnover_tables import turnover_tables as tt
from essential_life import mortality_table as mt, read_soa_table_xml as rst
from essential_life.multidecrement_table import MultiDecrementTable as mdt

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
ekv80 = dt.EVK_80
ekv80_70 = dt.EVK_80_ext_70
pcr1 = tt.pcr_turnover
pcr2 = tt.pcr_turnover_65

mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)
dt_ekv80 = mt.MortalityTable(mt=ekv80, last_q=0)
# dt_ekv80.force_qw_0()
tt_pcr = mt.MortalityTable(mt=pcr1, last_q=0)
# tt_pcr.force_qw_0()

tables_unidecrement = {'mortality': mt_TV7377, 'disability': dt_ekv80, 'turnover': tt_pcr}

tables_multidecrement = mdt(dict_tables=tables_unidecrement)
tables_multidecrement.create_udd_multidecrement_table()
