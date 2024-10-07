__author__ = "PedroCR and GRGuerreiro"

import pytest
from lifeActuary import mortality_table as mt, commutation_table as ct, annuities, mortality_insurance
from soa_tables import read_soa_table_xml as rst

soa_TV7377 = rst.SoaTable('../../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../../soa_tables/GRF95.xml')
grf95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
tv7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)

ct_tv7377 = ct.CommutationFunctions(i=2, g=0, mt=soa_TV7377.table_qx)

def test_ax():
    a1 = ct_tv7377.ax(x=0,m=1)
    a2 = ct_tv7377.ax(x=50, m=1)
    a3 = ct_tv7377.ax(x=100, m=1)

    m1 = ct_tv7377.ax(x=0, m=12)
    m2 = ct_tv7377.ax(x=50, m=12)
    m3 = ct_tv7377.ax(x=100, m=12)


    assert a1 == pytest.approx(38.22554446, rel=0.000001)
    assert a2 == pytest.approx(21.55443277, rel=0.000001)
    assert a3 == pytest.approx(0.706416114, rel=0.000001)

    assert m1 == pytest.approx(38.68387779, rel=0.000001)
    assert m2 == pytest.approx(22.01276611, rel=0.000001)
    assert m3 == pytest.approx(1.164749448, rel=0.000001)


def test_aax():
    a1 = ct_tv7377.aax(x=0,m=1)
    a2 = ct_tv7377.aax(x=50, m=1)
    a3 = ct_tv7377.aax(x=100, m=1)

    m1 = ct_tv7377.aax(x=0, m=12)
    m2 = ct_tv7377.aax(x=50, m=12)
    m3 = ct_tv7377.aax(x=100, m=12)


    assert a1 == pytest.approx(39.22554446, rel=0.000001)
    assert a2 == pytest.approx(22.55443277, rel=0.000001)
    assert a3 == pytest.approx(1.706416114, rel=0.000001)

    assert m1 == pytest.approx(38.76721113, rel=0.000001)
    assert m2 == pytest.approx(22.09609944, rel=0.000001)
    assert m3 == pytest.approx(1.248082781, rel=0.000001)


def test_t_ax():
    a1 = ct_tv7377.t_ax(x=0, m=1, defer=5)
    a2 = ct_tv7377.t_ax(x=50, m=1, defer=5)
    a3 = ct_tv7377.t_ax(x=100, m=1, defer=5)

    nEx1 = ct_tv7377.nEx(x=0, n=5)

    assert a1 == pytest.approx(ct_tv7377.ax(x=5, m=1) * nEx1, rel=0.000001)

