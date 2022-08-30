__author__ = "PedroCR"

import pytest
from essential_life import mortality_table as mt, mortality_table, commutation_table, annuities, \
    read_soa_table_xml as rst
from toDelete.mortality_tables_old import TV7377, GRF95

lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
lt_grf95 = mortality_table.MortalityTable(mt=GRF95)

soa_TV7377 = rst.SoaTable('../../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)


def test_nEx():
    i = 2
    g = 0
    x = 45
    defer = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.nEx(mt=mt_GRF95, x=x, i=i, g=g, defer=defer, method=method)
    a_tv = annuities.nEx(mt=mt_TV7377, x=x, i=i, g=g, defer=defer, method=method)
    a_grf_2 = cf_grf95.nEx(x=x, n=defer)
    cf_tv_2 = cf_tv7377.nEx(x=x, n=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


# note the variable g should have no effect, since is the 1st payment
def test_nEx_g():
    i = 2
    g = 1
    x = 45
    defer = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.nEx(mt=mt_GRF95, x=x, i=i, g=g, defer=defer, method=method)
    a_tv = annuities.nEx(mt=mt_TV7377, x=x, i=i, g=g, defer=defer, method=method)
    a_grf_2 = cf_grf95.nEx(x=x, n=defer)
    cf_tv_2 = cf_tv7377.nEx(x=x, n=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


# note the variable g should have no effect, since is the 1st payment
def test_nEx_g_2():
    i = 2
    g = 1
    x = 45
    defer = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.nEx(mt=mt_GRF95, x=x, i=i, g=g * 0, defer=defer, method=method)
    a_tv = annuities.nEx(mt=mt_TV7377, x=x, i=i, g=g * 0, defer=defer, method=method)
    a_grf_2 = cf_grf95.nEx(x=x, n=defer)
    cf_tv_2 = cf_tv7377.nEx(x=x, n=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)