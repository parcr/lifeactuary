__author__ = "PedroCR"

import pytest

from lifeActuary import mortality_table as mt, mortality_table, commutation_table, annuities
from soa_tables import read_soa_table_xml as rst


soa_TV7377 = rst.SoaTable('../../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)


def test_ax():
    i = 2
    g = 1
    m = 1
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)
    ages = range(0, max(mt_TV7377.w, mt_GRF95.w) + 10)

    a_grf = [annuities.ax(mt=mt_GRF95, x=x, i=i, g=g, m=m, method=method) for x in ages]
    a_tv = [annuities.ax(mt=mt_TV7377, x=x, i=i, g=g, m=m, method=method) for x in ages]
    a_grf_2 = [cf_grf95.ax(x=x, m=m) for x in ages]
    a_tv_2 = [cf_tv7377.ax(x=x, m=m) for x in ages]

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_t_ax():
    i = 2
    g = 1
    m = 1
    defer = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)
    ages = range(0, max(mt_TV7377.w, mt_GRF95.w) + 10)

    a_grf = [annuities.t_ax(mt=mt_GRF95, x=x, i=i, g=g, m=m, defer=defer, method=method) for x in ages]
    a_tv = [annuities.t_ax(mt=mt_TV7377, x=x, i=i, g=g, m=m, defer=defer, method=method) for x in ages]
    a_grf_2 = [cf_grf95.t_ax(x=x, m=m, defer=defer) for x in ages]
    a_tv_2 = [cf_tv7377.t_ax(x=x, m=m, defer=defer) for x in ages]

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_nax():
    i = 2
    g = 1
    m = 1
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)
    ages = range(0, max(mt_TV7377.w, mt_GRF95.w) + 10)

    a_grf = [annuities.nax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, method=method) for x in ages]
    a_tv = [annuities.nax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, method=method) for x in ages]
    a_grf_2 = [cf_grf95.nax(x=x, n=n, m=m) for x in ages]
    a_tv_2 = [cf_tv7377.nax(x=x, n=n, m=m) for x in ages]

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_t_nax():
    i = 2
    g = 1
    m = 1
    defer = 10
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)
    ages = range(0, max(mt_TV7377.w, mt_GRF95.w) + 10)

    a_grf = [annuities.t_nax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method) for x in ages]
    a_tv = [annuities.t_nax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method) for x in ages]
    a_grf_2 = [cf_grf95.t_nax(x=x, n=n, m=m, defer=defer) for x in ages]
    a_tv_2 = [cf_tv7377.t_nax(x=x, n=n, m=m, defer=defer) for x in ages]

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_aax():
    i = 2
    g = 1
    m = 1
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)
    ages = range(0, max(mt_TV7377.w, mt_GRF95.w) + 10)

    a_grf = [annuities.aax(mt=mt_GRF95, x=x, i=i, g=g, m=m, method=method) for x in ages]
    a_tv = [annuities.aax(mt=mt_TV7377, x=x, i=i, g=g, m=m, method=method) for x in ages]
    a_grf_2 = [cf_grf95.aax(x=x, m=m) for x in ages]
    a_tv_2 = [cf_tv7377.aax(x=x, m=m) for x in ages]

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_t_aax():
    i = 2
    g = 1
    m = 1
    defer = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)
    ages = range(0, max(mt_TV7377.w, mt_GRF95.w) + 10)

    a_grf = [annuities.t_aax(mt=mt_GRF95, x=x, i=i, g=g, m=m, defer=defer, method=method) for x in ages]
    a_tv = [annuities.t_aax(mt=mt_TV7377, x=x, i=i, g=g, m=m, defer=defer, method=method) for x in ages]
    a_grf_2 = [cf_grf95.t_aax(x=x, m=m, defer=defer) for x in ages]
    a_tv_2 = [cf_tv7377.t_aax(x=x, m=m, defer=defer) for x in ages]

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)



def test_naax():
    i = 2
    g = 1
    m = 1
    x = 45
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)
    ages = range(0, max(mt_TV7377.w, mt_GRF95.w) + 10)

    a_grf = [annuities.naax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, method=method) for x in ages]
    a_tv = [annuities.naax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, method=method) for x in ages]
    a_grf_2 = [cf_grf95.naax(x=x, n=n, m=m) for x in ages]
    a_tv_2 = [cf_tv7377.naax(x=x, n=n, m=m) for x in ages]

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_t_naax():
    i = 2
    g = 1
    m = 1
    defer = 10
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)
    ages = range(0, max(mt_TV7377.w, mt_GRF95.w) + 10)

    a_grf = [annuities.t_naax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method) for x in ages]
    a_tv = [annuities.t_naax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method) for x in ages]
    a_grf_2 = [cf_grf95.t_naax(x=x, n=n, m=m, defer=defer) for x in ages]
    a_tv_2 = [cf_tv7377.t_naax(x=x, n=n, m=m, defer=defer) for x in ages]

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)
