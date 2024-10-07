__author__ = "PedroCR"

import pytest
from lifeActuary import mortality_table as mt, mortality_table, commutation_table, annuities
from soa_tables import read_soa_table_xml as rst

soa_TV7377 = rst.SoaTable('../../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)


def test_aax():
    i = 2
    g = 0
    m = 1
    x = 200
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.aax(mt=mt_GRF95, x=x, i=i, g=g, m=m, method=method)
    a_tv = annuities.aax(mt=mt_TV7377, x=x, i=i, g=g, m=m, method=method)
    a_grf_2 = cf_grf95.aax(x=x, m=m)
    a_tv_2 = cf_tv7377.aax(x=x, m=m)

    assert a_grf == pytest.approx(1, rel=1e-16)
    assert a_tv == pytest.approx(1, rel=1e-16)
    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_ax():
    i = 2
    g = 0
    m = 1
    x = 200
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.ax(mt=mt_GRF95, x=x, i=i, g=g, m=m, method=method)
    a_tv = annuities.ax(mt=mt_TV7377, x=x, i=i, g=g, m=m, method=method)
    a_grf_2 = cf_grf95.ax(x=x, m=m)
    a_tv_2 = cf_tv7377.ax(x=x, m=m)

    assert a_grf == pytest.approx(0, rel=1e-16)
    assert a_tv == pytest.approx(0, rel=1e-16)
    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)
