import pytest

from essential_life import mortality_table, commutation_table, read_soa_table_xml as rst

table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=4, g=0, mt=mt.table_qx) for mt in mt_lst]


def test_wlai_1():
    a = ct_lst[0].nax(x=55, n=10, m=1)
    assert 7.828734291528 == pytest.approx(a, rel=1e-12)
    renda = ct_lst[0].naax(x=55, n=5, m=1)
    assert 1.710228528423 == pytest.approx(a / renda, rel=1e-12)


def test_wlai_2():
    a = ct_lst[1].nax(x=55, n=10, m=1)
    assert 7.989832533058 == pytest.approx(a, rel=1e-12)
    renda = ct_lst[1].naax(x=55, n=5, m=1)
    assert 1.734037382978 == pytest.approx(a / renda, rel=1e-12)


def test_wlai_3():
    a = ct_lst[2].nax(x=55, n=10, m=1)
    assert 7.781079676134 == pytest.approx(a, rel=1e-12)
    renda = ct_lst[2].naax(x=55, n=5, m=1)
    assert 1.702707246502 == pytest.approx(a / renda, rel=1e-12)


for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " + f'{round(1000 * ct.nax(x=55, n=10, m=1), 2):,}')

print()
for idx, ct in enumerate(ct_lst):
    print("\\textbf{" + table_names[idx] + ":} " +
          f'{round(1000 * ct.nax(x=55, n=10, m=1) / ct.naax(x=55, n=5, m=1), 2):,}')
