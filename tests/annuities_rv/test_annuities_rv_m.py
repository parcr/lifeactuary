__author__ = "PedroCR and GRG"
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
import numpy as np
from lifeActuary import mortality_table as mt, commutation_table, annuities, annuities_rv
from soa_tables import read_soa_table_xml as rst

# lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
# lt_grf95 = mortality_table.MortalityTable(mt=GRF95)

soa_TV7377 = rst.SoaTable(os.path.join(project_root, 'soa_tables', 'TV7377.xml'))
soa_GRF95 = rst.SoaTable(os.path.join(project_root, 'soa_tables', 'GRF95.xml'))
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)

def test_ax():
    i = 2
    g = 0
    m = 12
    x = 45*0+125
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.ax(mt=mt_GRF95, x=x, i=i, g=g, m=m, method=method)
    a_tv = annuities.ax(mt=mt_TV7377, x=x, i=i, g=g, m=m, method=method)
    a_grf_2 = cf_grf95.ax(x=x, m=m)
    a_tv_2 = cf_tv7377.ax(x=x, m=m)

    # assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    # assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)

    # probabilist approach
    n1=1/m
    n2=max(mt_GRF95.w - x + 1, mt_TV7377.w - x + 1)
    step=1/m
    v= 1 / (1 + i / 100)
    d = (1-v)
    i2 = ((1 + i / 100) ** 2-1)*100
    v_grow= (1 + g / 100)
    payments_moments=list(np.arange(n1, n2, step))
    payments=[v_grow ** i for i in payments_moments]
    moment=1

    probs_tv=[cf_tv7377.npx(x, m, method) for m in payments_moments]
    probs_grf=[cf_grf95.npx(x, m, method) for m in payments_moments]

    a_grf_prob = annuities_rv.gen_axn(mort_table=mt_GRF95, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_grf_prob*=step
    a_tv_prob = annuities_rv.gen_axn(mort_table=mt_TV7377, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_tv_prob*=step

    # check with probabilistic approach
    assert a_grf == pytest.approx(a_grf_prob, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_prob, rel=1e-16)


def test_t_ax():
    i = 2
    g = 0
    m = 12
    x = 45
    defer = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_ax(mt=mt_GRF95, x=x, i=i, g=g, m=m, defer=defer, method=method)
    a_tv = annuities.t_ax(mt=mt_TV7377, x=x, i=i, g=g, m=m, defer=defer, method=method)

    # assert a_grf == pytest.approx(cf_grf95.t_ax(x=x, m=m, defer=defer), rel=1e-16)
    # assert a_tv == pytest.approx(cf_tv7377.t_ax(x=x, m=m, defer=defer), rel=1e-16)

    # probabilist approach
    n1=defer+1/m
    n2=max(mt_GRF95.w - x + 1, mt_TV7377.w - x + 1)
    step=1/m
    v= 1 / (1 + i / 100)
    d = (1-v)
    i2 = ((1 + i / 100) ** 2-1)*100
    v_grow= (1 + g / 100)
    payments_moments=list(np.arange(n1, n2, step))
    payments=[v_grow ** i for i in payments_moments]
    moment=1

    a_grf_prob = annuities_rv.gen_axn(mort_table=mt_GRF95, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_grf_prob*=step
    a_tv_prob = annuities_rv.gen_axn(mort_table=mt_TV7377, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_tv_prob*=step

    # check with probabilistic approach
    assert a_grf == pytest.approx(a_grf_prob, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_prob, rel=1e-16)



def test_nax():
    i = 2
    g = 0
    m = 12
    x = 45
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.nax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, method=method)
    a_tv = annuities.nax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, method=method)

    # assert a_grf == pytest.approx(cf_grf95.nax(x=x, m=m, n=n), rel=1e-16)
    # assert a_tv == pytest.approx(cf_tv7377.nax(x=x, m=m, n=n), rel=1e-16)

    # probabilist approach
    n1=1/m
    n2=n+1/m
    step=1/m
    v= 1 / (1 + i / 100)
    d = (1-v)
    i2 = ((1 + i / 100) ** 2-1)*100
    v_grow= (1 + g / 100)
    payments_moments=list(np.arange(n1, n2, step))
    payments=[v_grow ** i for i in payments_moments]
    moment=1

    a_grf_prob = annuities_rv.gen_axn(mort_table=mt_GRF95, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_grf_prob*=step
    a_tv_prob = annuities_rv.gen_axn(mort_table=mt_TV7377, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_tv_prob*=step

    # check with probabilistic approach
    assert a_grf == pytest.approx(a_grf_prob, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_prob, rel=1e-16)


def test_t_nax():
    i = 2
    g = 0
    m = 12
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

    # assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    # assert a_tv == pytest.approx(a_tv_2, rel=1e-16)

    # probabilist approach
    n1=defer+1/m
    n2=defer+n+1/m
    step=1/m
    v= 1 / (1 + i / 100)
    d = (1-v)
    i2 = ((1 + i / 100) ** 2-1)*100
    v_grow= (1 + g / 100)
    payments_moments=list(np.arange(n1, n2, step))
    payments=[v_grow ** i for i in payments_moments]
    moment=1

    a_grf_prob = annuities_rv.gen_axn(mort_table=mt_GRF95, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_grf_prob*=step
    a_tv_prob = annuities_rv.gen_axn(mort_table=mt_TV7377, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_tv_prob*=step

    # check with probabilistic approach
    assert a_grf == pytest.approx(a_grf_prob, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_prob, rel=1e-16)


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

    # assert a_grf == pytest.approx(cf_grf95.aax(x=x, m=m), rel=1e-16)
    # assert a_tv == pytest.approx(cf_tv7377.aax(x=x, m=m), rel=1e-16)

    # probabilist approach
    n1=0
    n2=max(mt_GRF95.w - x + 1, mt_TV7377.w - x + 1)
    step=1/m
    v= 1 / (1 + i / 100)
    d = (1-v)
    i2 = ((1 + i / 100) ** 2-1)*100
    v_grow= (1 + g / 100)
    payments_moments=list(np.arange(n1, n2, step))
    payments=[v_grow ** i for i in payments_moments]
    moment=1

    a_grf_prob = annuities_rv.gen_axn(mort_table=mt_GRF95, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_grf_prob*=step
    a_tv_prob = annuities_rv.gen_axn(mort_table=mt_TV7377, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_tv_prob*=step

    # check with probabilistic approach
    assert a_grf == pytest.approx(a_grf_prob, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_prob, rel=1e-16)


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

    # assert a_grf == pytest.approx(cf_grf95.t_aax(x=x, m=m, defer=defer), rel=1e-16)
    # assert a_tv == pytest.approx(cf_tv7377.t_aax(x=x, m=m, defer=defer), rel=1e-16)

    # probabilist approach
    n1=defer
    n2=max(mt_GRF95.w - x + 1, mt_TV7377.w - x + 1)
    step=1/m
    v= 1 / (1 + i / 100)
    d = (1-v)
    i2 = ((1 + i / 100) ** 2-1)*100
    v_grow= (1 + g / 100)
    payments_moments=list(np.arange(n1, n2, step))
    payments=[v_grow ** i for i in payments_moments]
    moment=1

    a_grf_prob = annuities_rv.gen_axn(mort_table=mt_GRF95, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_grf_prob*=step
    a_tv_prob = annuities_rv.gen_axn(mort_table=mt_TV7377, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_tv_prob*=step

    # check with probabilistic approach
    assert a_grf == pytest.approx(a_grf_prob, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_prob, rel=1e-16)




def test_naax():
    i = 2
    g = 0
    m = 1
    # this works with almost all ages and fails with some other, e.g. fails with 116
    x = 55
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.naax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, method=method)
    a_tv = annuities.naax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, method=method)
    a_grf_2 = cf_grf95.naax(x=x, m=m, n=n)
    a_tv_2 = cf_tv7377.naax(x=x, m=m, n=n)

    # assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    # assert a_tv == pytest.approx(a_tv_2, rel=1e-16)

    # probabilist approach
    n1=0
    n2=n
    step=1/m
    v= 1 / (1 + i / 100)
    d = (1-v)
    i2 = ((1 + i / 100) ** 2-1)*100
    v_grow= (1 + g / 100)
    payments_moments=list(np.arange(n1, n2, step))
    payments=[v_grow ** i for i in payments_moments]
    moment=1

    a_grf_prob = annuities_rv.gen_axn(mort_table=mt_GRF95, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_grf_prob*=step
    a_tv_prob = annuities_rv.gen_axn(mort_table=mt_TV7377, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_tv_prob*=step

    # check with probabilistic approach
    assert a_grf == pytest.approx(a_grf_prob, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_prob, rel=1e-16)


def test_t_naax():
    i = 2
    g = 0
    m = 1
    x = 55
    defer = 10
    n = 5
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    a_grf = annuities.t_naax(mt=mt_GRF95, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method)
    a_tv = annuities.t_naax(mt=mt_TV7377, x=x, n=n, i=i, g=g, m=m, defer=defer, method=method)
    a_grf_2 = cf_grf95.t_naax(x=x, n=n, m=m, defer=defer)
    a_tv_2 = cf_tv7377.t_naax(x=x, n=n, m=m, defer=defer)

    # assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    # assert a_tv == pytest.approx(a_tv_2, rel=1e-16)

    # probabilist approach
    n1=defer
    n2=defer+n
    step=1/m
    v= 1 / (1 + i / 100)
    d = (1-v)
    i2 = ((1 + i / 100) ** 2-1)*100
    v_grow= (1 + g / 100)
    payments_moments=list(np.arange(n1, n2, step))
    payments=[v_grow ** i for i in payments_moments]
    moment=1

    a_grf_prob = annuities_rv.gen_axn(mort_table=mt_GRF95, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_grf_prob*=step
    a_tv_prob = annuities_rv.gen_axn(mort_table=mt_TV7377, interest_rate=i, payments_moments=payments_moments, payments=payments, x=x, moment=moment, method=method)
    a_tv_prob*=step

    # check with probabilistic approach
    assert a_grf == pytest.approx(a_grf_prob, rel=1e-16)
    assert a_tv == pytest.approx(a_tv_prob, rel=1e-16)
