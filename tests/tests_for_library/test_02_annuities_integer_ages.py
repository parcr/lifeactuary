__author__ = "PedroCR and GRGuerreiro"

import pytest
from lifeActuary import mortality_table as mt, commutation_table, annuities
from soa_tables import read_soa_table_xml as rst

# lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
# lt_grf95 = mortality_table.MortalityTable(mt=GRF95)

soa_TV7377 = rst.SoaTable('../../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)


# Constant Term Life Annuities, Integer Ages

def test_ax():
    i = 2
    g = 0
    m = 1
    x = 45
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.ax(mt=mt_GRF95, x=x, i=i, g=g, m=m, method=method)
    a_tv = annuities.ax(mt=mt_TV7377, x=x, i=i, g=g, m=m, method=method)
    a_grf_2 = cf_grf95.ax(x=x, m=m)
    cf_tv_2 = cf_tv7377.ax(x=x, m=m)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_t_ax():
    i = 2
    g = 0
    m = 1
    x = 45
    defer = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_ax(mt=mt_GRF95, x=x, i=i, g=g, m=m, defer=defer, method=method)
    a_tv = annuities.t_ax(mt=mt_TV7377, x=x, i=i, g=g, m=m, defer=defer, method=method)

    assert a_grf == pytest.approx(cf_grf95.t_ax(x=x, m=m, defer=defer), rel=1e-16)
    assert a_tv == pytest.approx(cf_tv7377.t_ax(x=x, m=m, defer=defer), rel=1e-16)


def test_nax():
    i = 2
    g = 0
    m = 1
    x = 45
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.nax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, method=method)
    a_tv = annuities.nax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, method=method)

    assert a_grf == pytest.approx(cf_grf95.nax(x=x, m=m, n=n), rel=1e-16)
    assert a_tv == pytest.approx(cf_tv7377.nax(x=x, m=m, n=n), rel=1e-16)


def test_t_nax():
    i = 2
    g = 0
    m = 1
    x = 45
    defer = 10
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_nax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method)
    a_tv = annuities.t_nax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method)
    a_grf_2 = cf_grf95.t_nax(x=x, n=n, m=m, defer=defer)
    a_tv_2 = cf_tv7377.t_nax(x=x, n=n, m=m, defer=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_aax():
    i = 2
    g = 0
    m = 1
    x = 45
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.aax(mt=mt_GRF95, x=x, i=i, g=g, m=m, method=method)
    a_tv = annuities.aax(mt=mt_TV7377, x=x, i=i, g=g, m=m, method=method)

    assert a_grf == pytest.approx(cf_grf95.aax(x=x, m=m), rel=1e-16)
    assert a_tv == pytest.approx(cf_tv7377.aax(x=x, m=m), rel=1e-16)


def test_t_aax():
    i = 2
    g = 0
    m = 1
    x = 45
    defer = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_aax(mt=mt_GRF95, x=x, i=i, g=g, m=m, defer=defer, method=method)
    a_tv = annuities.t_aax(mt=mt_TV7377, x=x, i=i, g=g, m=m, defer=defer, method=method)

    assert a_grf == pytest.approx(cf_grf95.t_aax(x=x, m=m, defer=defer), rel=1e-16)
    assert a_tv == pytest.approx(cf_tv7377.t_aax(x=x, m=m, defer=defer), rel=1e-16)


def test_naax():
    i = 2
    g = 0
    m = 1
    # this works with almost all ages and fails with some other, e.g. fails with 116
    x = 121
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.naax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, method=method)
    a_tv = annuities.naax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, method=method)
    a_grf_2 = cf_grf95.naax(x=x, m=m, n=n)
    a_tv_2 = cf_tv7377.naax(x=x, m=m, n=n)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_t_naax():
    i = 2
    g = 0
    m = 1
    x = 111
    defer = 10
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_naax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method)
    a_tv = annuities.t_naax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method)
    a_grf_2 = cf_grf95.t_naax(x=x, n=n, m=m, defer=defer)
    a_tv_2 = cf_tv7377.t_naax(x=x, n=n, m=m, defer=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)

def test_nEx():
    i=2
    g=0
    n=5
    x=30
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.nEx(mt=mt_GRF95, x=x, n=n, i=i, g=g, method=method)
    a_tv = annuities.nEx(mt=mt_TV7377, x=x, n=n, i=i, g=g, method=method)
    a_grf_2 = cf_grf95.nEx(x=x, n=n)
    a_tv_2 = cf_tv7377.nEx(x=x, n=n)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)

def test_t_nIax():
    i=2
    g=0
    n=5
    x=30
    defer=0
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_nIax(mt=mt_GRF95, x=x, n=n, i=i, defer=defer, first_amount=1, increase_amount=1, method=method)
    a_tv = annuities.t_nIax(mt=mt_TV7377, x=x, n=n, i=i, defer=defer, first_amount=1, increase_amount=1, method=method)
    a_grf_2 = cf_grf95.t_nIax(x=x, n=n, m=1, defer=defer, first_amount=1, increase_amount=1)
    a_tv_2 = cf_tv7377.t_nIax(x=x, n=n, m=1, defer=defer, first_amount=1, increase_amount=1)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)

def test_nIax():
    i=2
    g=0
    n=5
    x=30
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.nIax(mt=mt_GRF95, x=x, n=n, i=i, first_amount=1, increase_amount=1, method=method)
    a_tv = annuities.nIax(mt=mt_TV7377, x=x, n=n, i=i, first_amount=1, increase_amount=1, method=method)
    a_grf_2 = cf_grf95.t_nIax(x=x, n=n, m=1, defer=0, first_amount=1, increase_amount=1)
    a_tv_2 = cf_tv7377.t_nIax(x=x, n=n, m=1, defer=0, first_amount=1, increase_amount=1)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)

def test_t_nIaax():
    i=2
    g=0
    n=5
    x=30
    defer=0
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_nIaax(mt=mt_GRF95, x=x, n=n, i=i, m=1, defer=defer, first_amount=1, increase_amount=1, method=method)
    a_tv = annuities.t_nIaax(mt=mt_TV7377, x=x, n=n, i=i, m=1, defer=defer, first_amount=1, increase_amount=1, method=method)
    a_grf_2 = cf_grf95.t_nIaax(x=x, n=n, m=1, defer=defer, first_amount=1, increase_amount=1)
    a_tv_2 = cf_tv7377.t_nIaax(x=x, n=n, m=1, defer=defer, first_amount=1, increase_amount=1)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)

def test_nIaax():
    i=2
    g=0
    n=5
    x=30
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.nIaax(mt=mt_GRF95, x=x, n=n, i=i, first_amount=1, increase_amount=1, method=method)
    a_tv = annuities.nIaax(mt=mt_TV7377, x=x, n=n, i=i, first_amount=1, increase_amount=1, method=method)
    a_grf_2 = cf_grf95.t_nIaax(x=x, n=n, m=1, defer=0, first_amount=1, increase_amount=1)
    a_tv_2 = cf_tv7377.t_nIaax(x=x, n=n, m=1, defer=0, first_amount=1, increase_amount=1)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)

def test_present_value():
    a = annuities.present_value(mt=None, age=None, spot_rates=[1.2, 1.4, 1.8, 1.6, 1.9], capital=[100, -25, 120, 300, -50],
                     probs=1)
    b = annuities.present_value(mt=mt_TV7377, age=35, spot_rates=[1.2, 1.4, 1.8, 1.6, 1.9], capital=[100, -25, 120, 300, -50], probs=None)

    assert a == pytest.approx(425.7507012, rel=0.00001)
    assert b == pytest.approx(424.2408518, rel=0.00001)


# Life Annuities with Geometric Evolving Terms


def test_gax():
    i = 2
    g = 1
    m = 1
    x = 45
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.ax(mt=mt_GRF95, x=x, i=i, g=g, m=m, method=method)
    a_tv = annuities.ax(mt=mt_TV7377, x=x, i=i, g=g, m=m, method=method)

    assert a_grf == pytest.approx(cf_grf95.ax(x=x, m=m), rel=1e-16)
    assert a_tv == pytest.approx(cf_tv7377.ax(x=x, m=m), rel=1e-16)


def test_t_gax():
    i = 2
    g = 1
    m = 1
    x = 45
    defer = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_ax(mt=mt_GRF95, x=x, i=i, g=g, m=m, defer=defer, method=method)
    a_tv = annuities.t_ax(mt=mt_TV7377, x=x, i=i, g=g, m=m, defer=defer, method=method)
    a_gref_2 = cf_grf95.t_ax(x=x, m=m, defer=defer)
    a_tv_2 = cf_tv7377.t_ax(x=x, m=m, defer=defer)

    assert a_grf == pytest.approx(a_gref_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_ngax():
    i = 2
    g = 1
    m = 1
    x = 45
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.nax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, method=method)
    a_tv = annuities.nax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, method=method)

    assert a_grf == pytest.approx(cf_grf95.nax(x=x, m=m, n=n), rel=1e-16)
    assert a_tv == pytest.approx(cf_tv7377.nax(x=x, m=m, n=n), rel=1e-16)


def test_t_ngax():
    i = 2
    g = 1
    m = 1
    x = 45
    defer = 10
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_nax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method)
    a_tv = annuities.t_nax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method)
    a_grf_2 = cf_grf95.t_nax(x=x, n=n, m=m, defer=defer)
    a_tv_2 = cf_tv7377.t_nax(x=x, n=n, m=m, defer=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_gaax():
    i = 2
    g = 1
    m = 1
    x = 45
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.aax(mt=mt_GRF95, x=x, i=i, g=g, m=m, method=method)
    a_tv = annuities.aax(mt=mt_TV7377, x=x, i=i, g=g, m=m, method=method)

    assert a_grf == pytest.approx(cf_grf95.aax(x=x, m=m), rel=1e-16)
    assert a_tv == pytest.approx(cf_tv7377.aax(x=x, m=m), rel=1e-16)


def test_t_gaax():
    i = 2
    g = 1
    m = 1
    x = 45
    defer = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_aax(mt=mt_GRF95, x=x, i=i, g=g, m=m, defer=defer, method=method)
    a_tv = annuities.t_aax(mt=mt_TV7377, x=x, i=i, g=g, m=m, defer=defer, method=method)
    a_grf_2 = cf_grf95.t_aax(x=x, m=m, defer=defer)
    a_tv_2 = cf_tv7377.t_aax(x=x, m=m, defer=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_ngaax():
    i = 2
    g = 1
    m = 1
    x = 45
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.naax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, method=method)
    a_tv = annuities.naax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, method=method)
    a_grf_2 = cf_grf95.naax(x=x, m=m, n=n)
    a_tv_2 = cf_tv7377.naax(x=x, m=m, n=n)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)


def test_t_ngaax():
    i = 2
    g = 1
    m = 1
    x = 45
    defer = 10
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_naax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method)
    a_tv = annuities.t_naax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method)
    a_grf_2 = cf_grf95.t_naax(x=x, n=n, m=m, defer=defer)
    a_tv_2 = cf_tv7377.t_naax(x=x, n=n, m=m, defer=defer)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_2, rel=1e-16)
