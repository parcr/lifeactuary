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

'''
note that the 1st capital is 1 and the second 1+inc, so we can not multiply everything by the increment!
def test_capital():
    i = 2
    x = 45
    inc = 1
    inc_2 = 100
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.IAx(mt=mt_GRF95, x=x, i=i, inc=inc, method=method)
    a_tv = mortality_insurance.IAx(mt=mt_TV7377, x=x, i=i, inc=inc, method=method)
    a_grf_cap = mortality_insurance.IAx(mt=mt_GRF95, x=x, i=i, inc=inc_2, method=method)
    a_tv_cap = mortality_insurance.IAx(mt=mt_TV7377, x=x, i=i, inc=inc_2, method=method)
    a_grf_2 = cf_grf95.IAx(x=x)
    cf_tv_2 = cf_tv7377.IAx(x=x)

    assert a_grf * inc_2 == pytest.approx(a_grf_cap, rel=1e-16)
    assert a_tv * inc_2 == pytest.approx(a_tv_cap, rel=1e-16)
'''

def test_IAx():
    i = 2
    x = 45
    inc = 1
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.IAx(mt=mt_GRF95, x=x, i=i, inc=inc, method=method)
    a_tv = mortality_insurance.IAx(mt=mt_TV7377, x=x, i=i, inc=inc, method=method)
    a_grf_2 = cf_grf95.IAx(x=x)
    cf_tv_2 = cf_tv7377.IAx(x=x)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_IAx_2():
    i = 2
    x = 45
    inc = 1
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.IAx(mt=mt_GRF95, x=x, i=i, inc=inc, method=method) - \
            mortality_insurance.Ax(mt=mt_GRF95, x=x, i=i, g=0, method=method)
    a_tv = mortality_insurance.IAx(mt=mt_TV7377, x=x, i=i, inc=inc, method=method) - \
           mortality_insurance.Ax(mt=mt_TV7377, x=x, i=i, g=0, method=method)
    a_grf_2 = cf_grf95.IAx(x=x) - cf_grf95.Ax(x=x)
    cf_tv_2 = cf_tv7377.IAx(x=x) - cf_tv7377.Ax(x=x)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_IAx_3():
    i = 2
    x = 45
    inc = 2
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_TV7377.table_qx)

    a_grf = mortality_insurance.IAx(mt=mt_GRF95, x=x, i=i, inc=inc, method=method)
    a_tv = mortality_insurance.IAx(mt=mt_TV7377, x=x, i=i, inc=inc, method=method)
    a_grf_2 = inc * cf_grf95.IAx(x=x) - (inc - 1) * cf_grf95.Ax(x=x)
    cf_tv_2 = inc * cf_tv7377.IAx(x=x) - (inc - 1) * cf_tv7377.Ax(x=x)

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)


def test_IAx_4():
    capital = 1000
    i = 2
    x = 45
    inc = capital * 2 / 100.
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=0, mt=soa_TV7377.table_qx)

    a_grf_cost_inc = (mortality_insurance.IAx(mt=mt_GRF95, x=x, i=i, inc=1, method=method) - \
                      mortality_insurance.Ax(mt=mt_GRF95, x=x, i=i, g=0, method=method)) * inc
    a_grf_cost_capital = mortality_insurance.Ax(mt=mt_GRF95, x=x, i=i, g=0, method=method) * capital
    a_grf = a_grf_cost_capital + a_grf_cost_inc
    a_tv_cost_inc = (mortality_insurance.IAx(mt=mt_TV7377, x=x, i=i, inc=1, method=method) - \
                     mortality_insurance.Ax(mt=mt_TV7377, x=x, i=i, g=0, method=method)) * inc
    a_tv_cost_capital = mortality_insurance.Ax(mt=mt_TV7377, x=x, i=i, g=0, method=method) * capital
    a_tv = a_tv_cost_capital + a_tv_cost_inc
    a_grf_2_cost_capital = capital * cf_grf95.Ax(x=x)
    a_grf_2_cost_inc = (cf_grf95.IAx(x=x) - cf_grf95.Ax(x=x)) * inc
    a_grf_2 = a_grf_2_cost_capital + a_grf_2_cost_inc

    cf_tv_2 = capital * cf_tv7377.Ax(x=x) + (cf_tv7377.IAx(x=x) - cf_tv7377.Ax(x=x)) * inc

    assert a_grf == pytest.approx(a_grf_2, rel=1e-16)
    assert a_tv == pytest.approx(cf_tv_2, rel=1e-16)
