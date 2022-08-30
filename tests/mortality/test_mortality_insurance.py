__author__ = "PedroCR"

import pytest

from toDelete.mortality_tables_old import TV7377, GRF95
from essential_life import mortality_insurance, mortality_table as mt, mortality_table, commutation_table, \
    read_soa_table_xml as rst

lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
lt_grf95 = mortality_table.MortalityTable(mt=GRF95)

soa_TV7377 = rst.SoaTable('../../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)


def test_Ax():
    i = 2
    g = 0
    x = 45
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.Ax(mt=mt_GRF95, x=x, i=i, g=g, method=method)
    a_tv = mortality_insurance.Ax(mt=mt_TV7377, x=x, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.Ax(x=x)
    a_tv_2 = cf_tv7377.Ax(x=x)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_Ax_():
    i = 2
    g = 0
    x = 45
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.Ax_(mt=mt_GRF95, x=x, i=i, g=g, method=method)
    a_tv = mortality_insurance.Ax_(mt=mt_TV7377, x=x, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.Ax_(x=x)
    cf_tv_2 = cf_tv7377.Ax_(x=x)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_nAx():
    i = 2
    g = 0
    x = 45
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.nAx(mt=mt_GRF95, x=x, n=n, i=i, g=g, method=method)
    a_tv = mortality_insurance.nAx(mt=mt_TV7377, x=x, n=n, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.nAx(x=x, n=n)
    cf_tv_2 = cf_tv7377.nAx(x=x, n=n)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_nAx_():
    i = 2
    g = 0
    x = 45
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.nAx_(mt=mt_GRF95, x=x, n=n, i=i, g=g, method=method)
    a_tv = mortality_insurance.nAx_(mt=mt_TV7377, x=x, n=n, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.nAx_(x=x, n=n)
    cf_tv_2 = cf_tv7377.nAx_(x=x, n=n)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_nAEx():
    i = 2
    g = 0
    x = 45
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.nAEx(mt=mt_GRF95, x=x, n=n, i=i, g=g, method=method)
    a_tv = mortality_insurance.nAEx(mt=mt_TV7377, x=x, n=n, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.nAEx(x=x, n=n)
    cf_tv_2 = cf_tv7377.nAEx(x=x, n=n)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_nAEx_():
    i = 2
    g = 0
    x = 45
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.nAEx_(mt=mt_GRF95, x=x, n=n, i=i, g=g, method=method)
    a_tv = mortality_insurance.nAEx_(mt=mt_TV7377, x=x, n=n, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.nAEx_(x=x, n=n)
    cf_tv_2 = cf_tv7377.nAEx_(x=x, n=n)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_t_Ax():
    i = 2
    g = 0
    x = 45
    defer = 10
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.t_Ax(mt=mt_GRF95, x=x, defer=defer, i=i, g=g, method=method)
    a_tv = mortality_insurance.t_Ax(mt=mt_TV7377, x=x, defer=defer, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.t_Ax(x=x, defer=defer)
    cf_tv_2 = cf_tv7377.t_Ax(x=x, defer=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_t_Ax_():
    i = 2
    g = 0
    x = 45
    defer = 10
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.t_Ax_(mt=mt_GRF95, x=x, defer=defer, i=i, g=g, method=method)
    a_tv = mortality_insurance.t_Ax_(mt=mt_TV7377, x=x, defer=defer, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.t_Ax_(x=x, defer=defer)
    cf_tv_2 = cf_tv7377.t_Ax_(x=x, defer=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_t_nAx():
    i = 2
    g = 0
    x = 45
    defer = 10
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.t_nAx(mt=mt_GRF95, x=x, n=n, defer=defer, i=i, g=g, method=method)
    a_tv = mortality_insurance.t_nAx(mt=mt_TV7377, x=x, n=n, defer=defer, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.t_nAx(x=x, n=n, defer=defer)
    cf_tv_2 = cf_tv7377.t_nAx(x=x, n=n, defer=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_t_nAx_():
    i = 2
    g = 0
    x = 45
    defer = 10
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.t_nAx_(mt=mt_GRF95, x=x, n=n, defer=defer, i=i, g=g, method=method)
    a_tv = mortality_insurance.t_nAx_(mt=mt_TV7377, x=x, n=n, defer=defer, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.t_nAx_(x=x, n=n, defer=defer)
    cf_tv_2 = cf_tv7377.t_nAx_(x=x, n=n, defer=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_t_nAEx():
    i = 2
    g = 0
    x = 45
    defer = 10
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.t_nAEx(mt=mt_GRF95, x=x, n=n, defer=defer, i=i, g=g, method=method)
    a_tv = mortality_insurance.t_nAEx(mt=mt_TV7377, x=x, n=n, defer=defer, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.t_nAEx(x=x, n=n, defer=defer)
    cf_tv_2 = cf_tv7377.t_nAEx(x=x, n=n, defer=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_t_nAEx_():
    i = 2
    g = 0
    x = 45
    defer = 10
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.t_nAEx_(mt=mt_GRF95, x=x, n=n, defer=defer, i=i, g=g, method=method)
    a_tv = mortality_insurance.t_nAEx_(mt=mt_TV7377, x=x, n=n, defer=defer, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.t_nAEx_(x=x, n=n, defer=defer)
    cf_tv_2 = cf_tv7377.t_nAEx_(x=x, n=n, defer=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)
