__author__ = "PedroCR"

import pytest
from lifeActuary import mortality_table as mt
from lifeActuary import commutation_table as ct
from lifeActuary import life_2heads as a2h
from soa_tables import read_soa_table_xml as rst

# lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
# lt_grf95 = mortality_table.MortalityTable(mt=GRF95)

soa_TV7377 = rst.SoaTable('../../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)
ct_grf95 = ct.CommutationFunctions(i=2, g=0, mt=soa_GRF95.table_qx)
ct_tv7377 = ct.CommutationFunctions(i=2, g=0, mt=soa_TV7377.table_qx)

def test_npxy():
    x = 25
    y = 26
    n=3
    mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)
    mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
    a = mt_TV7377.npx(x, n)
    b = mt_GRF95.npx(y, n)

    prob_joint=a2h.npxy(mtx=mt_TV7377, mty=mt_GRF95, x=x, y=y, n=n, status='joint-life')
    prob_last=a2h.npxy(mtx=mt_TV7377, mty=mt_GRF95, x=x, y=y, n=n, status='last-survivor')

    assert a*b == pytest.approx(prob_joint, rel=1e-16)
    assert a+b-a*b == pytest.approx(prob_last,rel=1e-16)
# joint: 0.9966184964690245
# last: 0.9999971588031015

def test_nqxy():
    x = 25
    y = 26
    n = 15
    mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)
    mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
    a = mt_TV7377.npx(x, n)
    b = mt_GRF95.npx(y, n)

    prob_joint = a2h.nqxy(mtx=mt_TV7377, mty=mt_GRF95, x=x, y=y, n=n, status='joint-life')
    prob_last = a2h.nqxy(mtx=mt_TV7377, mty=mt_GRF95, x=x, y=y, n=n, status='last-survivor')

    assert 1 - a * b == pytest.approx(prob_joint, rel=1e-16)
    assert (1-a) * (1-b) == pytest.approx(prob_last, rel=1e-16)
# joint: 0.024709743755887303
# last: 0.00015301284981504725

def test_t_nqxy():
    x = 25
    y = 23
    t = 10
    n = 50
    mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)
    mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
    a1 = mt_TV7377.npx(x, t)
    b1 = mt_GRF95.npx(y, t)
    a2 = mt_TV7377.npx(x, t+n)
    b2 = mt_GRF95.npx(y, t+n)


    prob_joint = a2h.t_nqxy(mtx=mt_TV7377, mty=mt_GRF95, x=x, y=y, n=n, t=t, status='joint-life')
    prob_last = a2h.t_nqxy(mtx=mt_TV7377, mty=mt_GRF95, x=x, y=y, n=n, t=t, status='last-survivor')

    assert (a1 * b1) - (a2 * b2) == pytest.approx(prob_joint, rel=1e-16)
    assert (1-a2*b2)-(1-a1*b1) == pytest.approx(prob_joint, rel=1e-16)
    assert (1 - a2) * (1 - b2) - (1 - a1) * (1 - b1) == pytest.approx(prob_last, rel=1e-16)

# joint: 0.0021955045167378895
# last: 4.581960277931107e-06

def test_annuity_xy():
    x = 90
    y = 95
    n = 10
    m=2
    g=1
    mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)
    mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)

    axyn_joint = a2h.annuity_xy(mt_TV7377,mt_GRF95,x=x, y=y, i=2, x_first_payment=x+1, x_last_payment=x+n,g=0, m=1,
                                status='joint-life')
    axyn_last = a2h.annuity_xy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, x_first_payment=x + 1, x_last_payment=x + n, g=0, m=1,
                                status='last-survivor')

    axynm_joint = a2h.annuity_xy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, x_first_payment=x + 1/m, x_last_payment=x + n, g=0, m=2,
                                status='joint-life')
    axynm_last = a2h.annuity_xy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, x_first_payment=x + 1/m, x_last_payment=x + n, g=0, m=2,
                                status='last-survivor')
    axyn_joint_g1 = a2h.annuity_xy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, x_first_payment=x + 1, x_last_payment=x + n, g=g,
                                m=1, status='joint-life')
    axyn_last_g1 = a2h.annuity_xy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, x_first_payment=x + 1, x_last_payment=x + n, g=g,
                               m=1, status='last-survivor')
    axynm_joint_g1 = a2h.annuity_xy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, x_first_payment=x + 1 / m, x_last_payment=x + n,
                                 g=g, m=2, status='joint-life')
    axynm_last_g1 = a2h.annuity_xy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, x_first_payment=x + 1 / m, x_last_payment=x + n,
                                g=g, m=2,
                                status='last-survivor')
    # Inteiras
    assert 2.1950854315834 == pytest.approx(axyn_joint, rel=1e-16)
    assert 6.0533137490162 == pytest.approx(axyn_last, rel=1e-16)
    # Fraccionadas
    assert 2.4319176604755 == pytest.approx(axynm_joint, rel=1e-16)
    assert 6.2483535823922 == pytest.approx(axynm_last, rel=1e-16)
    # Inteira g=1
    assert 2.2343657889640 == pytest.approx(axyn_joint_g1, rel=1e-16)
    assert 6.2622557930949 == pytest.approx(axyn_last_g1, rel=1e-16)
    # Fraccionada g=1
    assert 2.4818622493186 == pytest.approx(axynm_joint_g1, rel=1e-16)
    assert 6.4822250174071 == pytest.approx(axynm_last_g1, rel=1e-16)


# Annuities Two Heads ###############################################################################################

def test_axy():
    x = 90
    y = 95
    n = 10
    m = 2
    g = 1
    # Joint Life
    axy = a2h.axy(mt_TV7377,mt_GRF95,x=x,y=y,i=2,g=0,m=1,status='joint-life')
    a2xy = a2h.axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=2, status='joint-life')
    Gaxy = a2h.axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=1, status='joint-life')
    Ga2xy = a2h.axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=2, status='joint-life')
    assert 2.1993512333648 == pytest.approx(axy, rel=1e-16)
    assert 2.4380423029643 == pytest.approx(a2xy, rel=1e-6)
    assert 2.2390979768651 == pytest.approx(Gaxy, rel=1e-16)
    assert 2.4886702281877 == pytest.approx(Ga2xy, rel=1e-6)
    # Last Survivor
    axylast = a2h.axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=1, status='last-survivor')
    a2xylast = a2h.axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=2, status='last-survivor')
    Gaxylast = a2h.axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=1, status='last-survivor')
    Ga2xylast = a2h.axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=2, status='last-survivor')
    assert 6.8225885201728 == pytest.approx(axylast, rel=1e-16)
    assert 7.0791923426166 == pytest.approx(a2xylast, rel=1e-6)
    assert 7.1346827052150 == pytest.approx(Gaxylast, rel=1e-16)
    assert 7.4269936907418 == pytest.approx(Ga2xylast, rel=1e-6)

def test_aaxy():
    x = 90
    y = 95
    n = 10
    m = 2
    g = 1
    # Joint Life
    aaxy = a2h.aaxy(mt_TV7377,mt_GRF95,x=x,y=y,i=2,g=0,m=1,status='joint-life')
    aa2xy = a2h.aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=2, status='joint-life')
    Gaaxy = a2h.aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=1, status='joint-life')
    Gaa2xy = a2h.aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=2, status='joint-life')
    assert 3.1993512333648 == pytest.approx(aaxy, rel=1e-16)
    assert 2.9380423029643 == pytest.approx(aa2xy, rel=1e-16)
    assert 3.2614889566337 == pytest.approx(Gaaxy, rel=1e-16)
    assert 3.0010826255273 == pytest.approx(Gaa2xy, rel=1e-6)
    # Last Survivor
    aaxylast = a2h.aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=1, status='last-survivor')
    aa2xylast = a2h.aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=2, status='last-survivor')
    Gaaxylast = a2h.aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=1, status='last-survivor')
    Gaa2xylast = a2h.aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=2, status='last-survivor')
    assert 7.8225885201728 == pytest.approx(aaxylast, rel=1e-16)
    assert 7.5791923426166 == pytest.approx(aa2xylast, rel=1e-6)
    assert 8.2060295322671 == pytest.approx(Gaaxylast, rel=1e-16)
    assert 7.9640362830804 == pytest.approx(Gaa2xylast, rel=1e-6)

def test_t_axy():
    x = 90
    y = 95
    defer = 2
    # Joint Life
    taxy = a2h.t_axy(mt_TV7377,mt_GRF95,x=x,y=y,i=2,g=0,m=1,defer=2,status='joint-life')
    ta2xy = a2h.t_axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=2,defer=2,status='joint-life')
    tGaxy = a2h.t_axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=1, defer=2,status='joint-life')
    tGa2xy = a2h.t_axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=2, defer=2,status='joint-life')
    assert 0.9670660101740 == pytest.approx(taxy, rel=1e-16)
    assert 1.0880138791504 == pytest.approx(ta2xy, rel=1e-16)
    assert 0.9819797643451 == pytest.approx(tGaxy, rel=1e-16)
    assert 1.1076852487976 == pytest.approx(tGa2xy, rel=1e-16)
    # Last Survivor
    taxylast = a2h.t_axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=1, defer=2, status='last-survivor')
    ta2xylast = a2h.t_axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=2, defer=2, status='last-survivor')
    tGaxylast = a2h.t_axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=1, defer=2, status='last-survivor')
    tGa2xylast = a2h.t_axy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=2, defer=2, status='last-survivor')
    assert 4.9549321537268 == pytest.approx(taxylast, rel=1e-16)
    assert 5.1838325240527 == pytest.approx(ta2xylast, rel=1e-16)
    assert 5.1543909638868 == pytest.approx(tGaxylast, rel=1e-16)
    assert 5.4090315189107 == pytest.approx(tGa2xylast, rel=1e-16)

def test_t_aaxy():
    x = 90
    y = 95
    defer = 2
    # Joint Life
    taaxy = a2h.t_aaxy(mt_TV7377,mt_GRF95,x=x,y=y,i=2,g=0,m=1,defer=2,status='joint-life')
    taa2xy = a2h.t_aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=2,defer=2,status='joint-life')
    tGaaxy = a2h.t_aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=1, defer=2,status='joint-life')
    tGaa2xy = a2h.t_aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=2, defer=2,status='joint-life')
    assert 1.4765856167554 == pytest.approx(taaxy, rel=1e-16)
    assert 1.3427736824411 == pytest.approx(taa2xy, rel=1e-16)
    assert 1.5013191685700 == pytest.approx(tGaaxy, rel=1e-16)
    assert 1.3679697010673 == pytest.approx(tGaa2xy, rel=1e-16)
    # Last Survivor
    taaxylast = a2h.t_aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=1, defer=2, status='last-survivor')
    taa2xylast = a2h.t_aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=0, m=2, defer=2, status='last-survivor')
    tGaaxylast = a2h.t_aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=1, defer=2, status='last-survivor')
    tGaa2xylast = a2h.t_aaxy(mt_TV7377, mt_GRF95, x=x, y=y, i=2, g=1, m=2, defer=2, status='last-survivor')
    assert 5.8581438045273 == pytest.approx(taaxylast, rel=1e-16)
    assert 5.6354383494529 == pytest.approx(taa2xylast, rel=1e-16)
    assert 6.1091465243262 == pytest.approx(tGaaxylast, rel=1e-16)
    assert 5.8876152249777 == pytest.approx(tGaa2xylast, rel=1e-16)


def test_naxy():
    x = 90
    y = 95
    n=10
    # Joint Life
    naxy = a2h.naxy(mt_TV7377,mt_GRF95,x=x,y=y,n=10,i=2,g=0,m=1,status='joint-life')
    na2xy = a2h.naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=2, status='joint-life')
    nGaxy = a2h.naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=1,status='joint-life')
    nGa2xy = a2h.naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=2, status='joint-life')
    assert 2.1950854315834 == pytest.approx(naxy, rel=1e-16)
    assert 2.4319176604755 == pytest.approx(na2xy, rel=1e-16)
    assert 2.2343657889640 == pytest.approx(nGaxy, rel=1e-16)
    assert 2.4818622493186 == pytest.approx(nGa2xy, rel=1e-16)
    # Last Survivor
    naxylast = a2h.naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=1, status='last-survivor')
    na2xylast = a2h.naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=2, status='last-survivor')
    nGaxylast = a2h.naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=1, status='last-survivor')
    nGa2xylast = a2h.naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=2, status='last-survivor')
    assert 6.0533137490162 == pytest.approx(naxylast, rel=1e-16)
    assert 6.2483535823922 == pytest.approx(na2xylast, rel=1e-16)
    assert 6.2622557930949 == pytest.approx(nGaxylast, rel=1e-16)
    assert 6.4822250174071 == pytest.approx(nGa2xylast, rel=1e-16)

def test_naaxy():
    x = 90
    y = 95
    n=10
    # Joint Life
    naaxy = a2h.naaxy(mt_TV7377,mt_GRF95,x=x,y=y,n=10,i=2,g=0,m=1,status='joint-life')
    naa2xy = a2h.naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=2, status='joint-life')
    nGaaxy = a2h.naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=1,status='joint-life')
    nGaa2xy = a2h.naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=2, status='joint-life')
    assert 3.1869242276762 == pytest.approx(naaxy, rel=1e-16)
    assert 2.9278370585219 == pytest.approx(naa2xy, rel=1e-16)
    assert 3.2476944004477 == pytest.approx(nGaaxy, rel=1e-16)
    assert 2.9897331682378 == pytest.approx(nGaa2xy, rel=1e-16)
    # Last Survivor
    naaxylast = a2h.naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=1, status='last-survivor')
    naa2xylast = a2h.naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=2, status='last-survivor')
    nGaaxylast = a2h.naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=1, status='last-survivor')
    nGaa2xylast = a2h.naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=2, status='last-survivor')
    assert 6.8053358699690 == pytest.approx(naaxylast, rel=1e-16)
    assert 6.6243646428686 == pytest.approx(naa2xylast, rel=1e-16)
    assert 7.0509564992178 == pytest.approx(nGaaxylast, rel=1e-16)
    assert 6.8775945914019 == pytest.approx(nGaa2xylast, rel=1e-16)

def test_t_naxy():
    x = 90
    y = 95
    n=10
    t=2
    # Joint Life
    tnaxy = a2h.t_naxy(mt_TV7377,mt_GRF95,x=x,y=y,n=10,i=2,g=0,m=1,defer=2, status='joint-life')
    tna2xy = a2h.t_naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=2, defer=2, status='joint-life')
    tnGaxy = a2h.t_naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=1,defer=2, status='joint-life')
    tnGa2xy = a2h.t_naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=2, defer=2, status='joint-life')
    assert 0.9666963329541 == pytest.approx(tnaxy, rel=1e-16)
    assert 1.0874293826744 == pytest.approx(tna2xy, rel=1e-16)
    assert 0.9815701186571 == pytest.approx(tnGaxy, rel=1e-16)
    assert 1.1070363765526 == pytest.approx(tnGa2xy, rel=1e-16)
    # Last Survivor
    tnaxylast = a2h.t_naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=1, defer=2, status='last-survivor')
    tna2xylast = a2h.t_naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=2, defer=2, status='last-survivor')
    tnGaxylast = a2h.t_naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=1, defer=2, status='last-survivor')
    tnGa2xylast = a2h.t_naxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=2, defer=2, status='last-survivor')
    assert 4.5280980544243 == pytest.approx(tnaxylast, rel=1e-16)
    assert 4.7199415824277 == pytest.approx(tna2xylast, rel=1e-16)
    assert 4.6715881322676 == pytest.approx(tnGaxylast, rel=1e-16)
    assert 4.8828953792874 == pytest.approx(tnGa2xylast, rel=1e-16)

def test_t_naaxy():
    x = 90
    y = 95
    n=10
    t=2
    # Joint Life
    tnaaxy = a2h.t_naaxy(mt_TV7377,mt_GRF95,x=x,y=y,n=10,i=2,g=0,m=1,defer=2, status='joint-life')
    tnaa2xy = a2h.t_naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=2, defer=2, status='joint-life')
    tnGaaxy = a2h.t_naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=1,defer=2, status='joint-life')
    tnGaa2xy = a2h.t_naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=2, defer=2, status='joint-life')
    assert 1.4752596902929 == pytest.approx(tnaaxy, rel=1e-16)
    assert 1.3417110613438 == pytest.approx(tnaa2xy, rel=1e-16)
    assert 1.4998491323542 == pytest.approx(tnGaaxy, rel=1e-16)
    assert 1.3667894454963 == pytest.approx(tnGaa2xy, rel=1e-16)
    # Last Survivor
    tnaaxylast = a2h.t_naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=1, defer=2, status='last-survivor')
    tnaa2xylast = a2h.t_naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=0, m=2, defer=2, status='last-survivor')
    tnGaaxylast = a2h.t_naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=1, defer=2, status='last-survivor')
    tnGaa2xylast = a2h.t_naaxy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, i=2, g=1, m=2, defer=2, status='last-survivor')
    assert 5.2817381208381 == pytest.approx(tnaaxylast, rel=1e-16)
    assert 5.0967616156346 == pytest.approx(tnaa2xylast, rel=1e-16)
    assert 5.4562955829444 == pytest.approx(tnGaaxylast, rel=1e-16)
    assert 5.2762449079555 == pytest.approx(tnGaa2xylast, rel=1e-16)




# Mortality Two Heads ###############################################################################################

def test_A_xy():
    x = 90
    y = 95
    n = 10
    defer=0
    m=2
    g=1
    mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)
    mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
    ct_grf95 = ct.CommutationFunctions(i=2, g=0, mt=soa_GRF95.table_qx)
    ct_tv7377 = ct.CommutationFunctions(i=2, g=0, mt=soa_TV7377.table_qx)
    Axyn_joint = a2h.A_xy(mt_TV7377, mt_GRF95, x=x, y=y, n=10, defer=0,  i=2, g=0, m=1, status='joint-life', method='udd')
    Axn=ct_tv7377.nAx(x=90,n=10)
    Ayn=ct_grf95.nAx(x=95,n=10)
    Axyn_last = a2h.A_xy(mt_TV7377, mt_GRF95, x=x, n=10, defer=0, y=y, i=2, g=0, m=1, status='last-survivor', method='udd')
    assert 0.9293500857462 == pytest.approx(Axyn_joint, rel=1e-16)
    assert Axn+Ayn-0.9293500857462 == pytest.approx(Axyn_last, rel=1e-16)


