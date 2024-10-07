__author__ = "PedroCR"

import pytest
from lifeActuary import mortality_table as mt, commutation_table, commutation_table_frac, annuities, mortality_insurance
from soa_tables import read_soa_table_xml as rst

# lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
# lt_grf95 = mortality_table.MortalityTable(mt=GRF95)

soa_TV7377 = rst.SoaTable('../../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../../soa_tables/GRF95.xml')
grf95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
tv7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)

ct_tv7377 = commutation_table.CommutationFunctions(i=2, g=0, mt=soa_TV7377.table_qx)
ct_tv7377_f10 = commutation_table_frac.CommutationFunctionsFrac(i=2, g=0, data_type='q', mt=soa_TV7377.table_qx, perc=100, frac=10, method='bal')
#tv7377_ct_f6 = commutation_table_frac.CommutationFunctionsFrac(i=2, g=0, data_type='q', mt=soa_TV7377.table_qx, perc=100, frac=6, method='udd')

def test_nEx():
    i = 2
    g = 0
    method = 'udd'
    a = annuities.nEx(mt=tv7377, x=50, i=i, g=g, n=5, method=method)
    b = annuities.nEx(mt=tv7377, x=50, i=i, g=g, n=10, method=method)
    c = annuities.nEx(mt=tv7377, x=80, i=i, g=g, n=10, method=method)

    assert a == pytest.approx(ct_tv7377.nEx(50, 5), rel=1e-16)
    assert b == pytest.approx(ct_tv7377.nEx(50, 10), rel=1e-16)
    assert c == pytest.approx(ct_tv7377.nEx(80, 10), rel=1e-16)

def test_Ax():
    i = 2
    a1 = mortality_insurance.Ax(mt=tv7377, x=50, i=i)
    b1 = mortality_insurance.Ax(mt=tv7377, x=50.7, i=i)
    c1 = mortality_insurance.Ax(mt=tv7377, x=50.7, i=i, method='cfm')

    a2 = mortality_insurance.Ax_(mt=tv7377, x=50, i=i)
    b2 = mortality_insurance.Ax_(mt=tv7377, x=50.7, i=i)
    c2 = mortality_insurance.Ax_(mt=tv7377, x=50.7, i=i, method='cfm')

    assert a1 == pytest.approx(ct_tv7377.Ax(x=50))
    assert a2 == pytest.approx(ct_tv7377.Ax_(x=50))

    # assert b1 ==
    # assert c1 == c2

def test_t_Ax():
    i = 2
    a1 = mortality_insurance.t_Ax(mt=tv7377, x=50, defer=2, i=i)
    a2 = mortality_insurance.t_Ax_(mt=tv7377, x=50, defer=2, i=i)

    assert a1 == ct_tv7377.t_Ax(50 ,2)
    assert a2 == ct_tv7377.t_Ax_(50 ,2)

def test_nAx():
    i = 2
    a1 = mortality_insurance.nAx(mt=tv7377, x=50, n=10, i=i)
    a2 = mortality_insurance.nAx_(mt=tv7377, x=50, n=10, i=i)

    assert a1 == pytest.approx(ct_tv7377.nAx(50 ,10))
    assert a2 == pytest.approx(ct_tv7377.nAx_(50, 10))

def test_t_nAx():
    i=2
    a1 = mortality_insurance.t_nAx(mt=tv7377, x=50, n=10, defer=5, i=2)
    a2 = mortality_insurance.t_nAx_(mt=tv7377, x=50, n=10, defer=5, i=2)

    assert a1 == pytest.approx(ct_tv7377.t_nAx(50, 10, 5))
    assert a2 == pytest.approx(ct_tv7377.t_nAx_(50, 10, 5))

def test_nAEx():
    i=2
    a1 = mortality_insurance.nAEx(mt=tv7377, x=50, n=10, i=i)
    a2 = mortality_insurance.nAEx_(mt=tv7377, x=50, n=10, i=i)

    assert a1 == pytest.approx(ct_tv7377.nAEx(50, 10), rel=1e-16)
    assert a1 == pytest.approx(mortality_insurance.nAx(mt=tv7377, x=50, n=10, i=2) + annuities.nEx(mt=tv7377, x=50, n=10, i=2), rel=1e-16)
    assert a2 == pytest.approx(ct_tv7377.nAEx_(50, 10))

def test_nAEx_2():
    i = 2
    d = mortality_insurance.nAx(mt=tv7377, x=50, n=10, i=i, g=0, method='udd')  # 0.046765545192
    s = annuities.nEx(mt=tv7377, x=50, i=i, g=0, n=10, method='udd')  # 0.777174827839
    p1 = d + s  # 0.823940373031
    d1 = ct_tv7377.nAx(x=50, n=10)  # 0.046765545192
    s2 = ct_tv7377.nEx(x=50, n=10)  # 0.777174827839
    p2 = d1 + s2  # 0.823940373031

    a1 = mortality_insurance.nAEx(mt=tv7377, x=50, n=10, i=i, g=0, method='udd')
    a2 = mortality_insurance.nAEx_(mt=tv7377, x=50, n=10, i=i)

    assert a1 == pytest.approx(ct_tv7377.nAEx(50, 10))
    assert a2 == pytest.approx(ct_tv7377.nAEx_(50, 10))

def test_t_nAEx():
    i=2
    a1 = mortality_insurance.t_nAEx(mt=tv7377, x=50, n=10, defer=2, i=i, g=0, method='udd')
    a2 = mortality_insurance.t_nAEx_(mt=tv7377, x=50, n=10, defer=2, i=i, g=0, method='udd')

    assert a1 == pytest.approx(ct_tv7377.t_nAEx(50, 10, 2))
    assert a2 == pytest.approx(ct_tv7377.t_nAEx_(50, 10, 2))

## Life Insurance with Variable Capitals

def test_IAx():
    i = 2
    a1 = mortality_insurance.IAx(mt=tv7377, x=50, i=i, inc=1)
    a2 = mortality_insurance.IAx_(mt=tv7377, x=50, i=i, inc=1)
    b1 = mortality_insurance.IAx(mt=tv7377, x=50, i=i, inc=10)
    b2 = mortality_insurance.IAx_(mt=tv7377, x=50, i=i, inc=10)

    assert a1 == pytest.approx(ct_tv7377.IAx(50))
    assert a2 == pytest.approx(ct_tv7377.IAx_(50))

    assert b1 == pytest.approx(10*ct_tv7377.IAx(50))
    assert b2 == pytest.approx(10*ct_tv7377.IAx_(50))

def test_t_IAx():
    i = 2
    v = 1/(1+i)
    t = 5
    a1 = mortality_insurance.t_IAx(mt=tv7377, x=50, defer=t, i=i, inc=1)
    a2 = mortality_insurance.t_IAx_(mt=tv7377, x=50, defer=t, i=i, inc=1)
    b1 = mortality_insurance.t_IAx(mt=tv7377, x=50, defer=t, i=i, inc=10)
    b2 = mortality_insurance.t_IAx_(mt=tv7377, x=50, defer=t, i=i, inc=10)

    act = annuities.nEx(mt=tv7377, x=50, i=i, g=0, n=t)

    assert a1 == pytest.approx(act * ct_tv7377.IAx(50+t))
    assert a2 == pytest.approx(act * ct_tv7377.IAx_(50+t))

    assert b1 == pytest.approx(act * 10 * ct_tv7377.IAx(50+t))
    assert b2 == pytest.approx(act * 10 * ct_tv7377.IAx_(50+t))


def test_nIAx():
    i = 2
    a1 = mortality_insurance.nIAx(mt=tv7377, x=50, n=10, i=i, inc=1)
    a2 = mortality_insurance.nIAx_(mt=tv7377, x=50, n=10, i=i, inc=1)

    b1 = mortality_insurance.nIAx(mt=tv7377, x=50, n=10, i=i, inc=10)
    b2 = mortality_insurance.nIAx_(mt=tv7377, x=50, n=10, i=i, inc=10)


    assert a1 == pytest.approx(ct_tv7377.nIAx(50, 10))
    assert a2 == pytest.approx(ct_tv7377.nIAx_(50, 10))

    assert b1 == pytest.approx(10*ct_tv7377.nIAx(50, 10))
    assert b2 == pytest.approx(10*ct_tv7377.nIAx_(50, 10))

def test_t_nIArx():
    t=10
    ex0ct = ct_tv7377.t_nIArx(x=50, n=10, defer=0, first_amount=1, increase_amount=1)
    ex1ct = ct_tv7377.t_nIArx(x=50, n=10, defer=0, first_amount=1000, increase_amount=50)
    ex2ct = ct_tv7377.t_nIArx(x=50, n=10, defer=t, first_amount=1000, increase_amount=50)
    ex3ct = ct_tv7377.t_nIArx(x=50, n=10, defer=0, first_amount=1000, increase_amount=-50)
    ex4ct = ct_tv7377.t_nIArx(x=50, n=10, defer=t, first_amount=1000, increase_amount=-50)

    act = annuities.nEx(mt=tv7377, x=50, i=2, g=0, n=t)

    ex0 = mortality_insurance.t_nIArx(mt=tv7377, x=50, n=10, defer=0, i=2, first_amount=1, inc=1)
    ex01 = mortality_insurance.nIAx(mt=tv7377, x=50, n=10, i=2, inc=1)
    ex1  = mortality_insurance.t_nIArx(mt=tv7377, x=50, n=10, defer=0, i=2, first_amount=1, inc=1)

    #assert ex0ct == pytest.approx(ex0)

    assert ex01 == pytest.approx(ex0ct)
    assert ex01 == pytest.approx(ex0)
    #assert ex0ct == pytest.approx(ex0)

#def test_nIAErx():
#    ex1ct = ct_tv7377.t_nIArx(x=50, n=10, defer=0, first_amount=1, increase_amount=1)
#    ex1 = mortality_insurance.nIAErx(mt=tv7377, x=50, n=10, i=2, first_amount=)