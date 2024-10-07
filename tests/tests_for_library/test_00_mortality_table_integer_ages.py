__author__ = "PedroCR and GRGuerreiro"

import pytest
from lifeActuary import mortality_table as mt, commutation_table, annuities
from soa_tables import read_soa_table_xml as rst

# lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
# lt_grf95 = mortality_table.MortalityTable(mt=GRF95)

soa_TV7377 = rst.SoaTable('../../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../../soa_tables/GRF95.xml')
grf95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
tv7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)


def test_lx():

    assert tv7377.lx[0] == pytest.approx(100000, rel=0.000001)
    assert tv7377.lx[30] == pytest.approx(97438.99998, rel=0.000001)
    assert tv7377.lx[106] == pytest.approx(0.999999999146187, rel=0.000001)
    assert tv7377.lx[107] == pytest.approx(0, rel=0.000001)

    assert grf95.lx[0] == pytest.approx(100000, rel=0.000001)
    assert grf95.lx[30] == pytest.approx(99397.38545, rel=0.000001)
    assert grf95.lx[126] == pytest.approx(1.29749453480608, rel=0.000001)
    assert grf95.lx[127] == pytest.approx(0, rel=0.000001)

def test_dx():
    assert tv7377.dx[0] == pytest.approx(1168, rel=0.000001)
    assert tv7377.dx[30] == pytest.approx(72, rel=0.000001)
    assert tv7377.dx[106] == pytest.approx(1, rel=0.000001)

def test_qx():
    assert tv7377.qx[0] == pytest.approx(0.01168, rel=0.000001)
    assert tv7377.qx[30] == pytest.approx(0.000738924, rel=0.000001)
    assert tv7377.qx[106] == pytest.approx(1.000, rel=0.000001)

def test_px():
    assert tv7377.px[0] == pytest.approx(0.98832, rel=0.000001)
    assert tv7377.px[30] == pytest.approx(0.999261076, rel=0.000001)
    assert tv7377.px[106] == pytest.approx(0, rel=0.000001)

def test_ex():
    assert tv7377.ex[0] == pytest.approx(76.50363+0.5, rel=0.000001)
    assert tv7377.ex[30] == pytest.approx(48.28049343+0.5, rel=0.000001)
    assert tv7377.ex[106] == pytest.approx(-1.90781E-09+0.5, rel=0.000001)

def test_w():
    assert tv7377.w == 106

def test_nqx():
    assert tv7377.nqx(0,10) == pytest.approx(0.015530000, rel=0.000001)
    assert tv7377.nqx(30, 10) == pytest.approx(0.010468088, rel=0.000001)
    assert tv7377.nqx(100, 2) == pytest.approx(0.817325800, rel=0.000001)

def test_npx():
    assert tv7377.npx(0,10) == pytest.approx(0.984470000, rel=0.000001)
    assert tv7377.npx(30, 10) == pytest.approx(0.989531912, rel=0.000001)
    assert tv7377.npx(100, 2) == pytest.approx(0.182674200, rel=0.000001)

#def test_exn():