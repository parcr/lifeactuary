import pytest

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=4, g=0, mt=mt.table_qx) for mt in mt_lst]


def test_wlai_1():
    a = ct_lst[0].t_aax(x=55, m=1, defer=10)
    b = ct_lst[0].t_ax(x=55, m=1, defer=9)
    assert 7.774902297975 == pytest.approx(a, rel=1e-12)
    assert 7.774902297975 == pytest.approx(b, rel=1e-12)


def test_wlai_2():
    a = ct_lst[1].t_aax(x=55, m=1, defer=10)
    b = ct_lst[1].t_ax(x=55, m=1, defer=9)
    assert 10.683798089358 == pytest.approx(a, rel=1e-12)
    assert 10.683798089358 == pytest.approx(b, rel=1e-12)


def test_wlai_3():
    a = ct_lst[2].t_aax(x=55, m=1, defer=10)
    b = ct_lst[2].t_ax(x=55, m=1, defer=9)
    assert 8.365856975602 == pytest.approx(a, rel=1e-12)
    assert 8.365856975602 == pytest.approx(b, rel=1e-12)


for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(1000 * ct.t_aax(x=55, m=1, defer=10), 2):,}')
