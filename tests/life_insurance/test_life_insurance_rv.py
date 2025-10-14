__author__ = "PedroCR and GRG"
import os
import sys
import pytest

from lifeActuary.mortality_insurance_frac import A_x
from lifeActuary.mortality_rv import gen_Axn

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
import numpy as np
from lifeActuary import mortality_table as mt, commutation_table
from soa_tables import read_soa_table_xml as rst

# lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
# lt_grf95 = mortality_table.MortalityTable(mt=GRF95)

soa_TV7377 = rst.SoaTable(os.path.join(project_root, 'soa_tables', 'TV7377.xml'))
soa_GRF95 = rst.SoaTable(os.path.join(project_root, 'soa_tables', 'GRF95.xml'))
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)

def func_test_Ax(x, defer, n, i, g, m, method):
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    m_grf95=cf_grf95.t_nAx(x=x, n=n, defer=defer)
    m_tv7377=cf_tv7377.t_nAx(x=x, n=n, defer=defer)

    m_grf95_frac=A_x(mt_GRF95, x=x, x_first=x+defer+1/m, x_last=x+defer+n, i=i, g=g, m=m, method=method)
    m_tv7377_frac=A_x(mt_TV7377, x=x, x_first=x+defer+1/m, x_last=x+defer+n, i=i, g=g, m=m, method=method)

    # probabilist approach
    n1=defer+1/m
    n2=n+defer #max(mt_GRF95.w - x + 2, mt_TV7377.w - x + 2)
    step=1/m
    v= 1 / (1 + i / 100)
    d = (1-v)
    i2 = ((1 + i / 100) ** 2-1)*100
    v_grow= (1 + g / 100)
    payments_moments=list(np.arange(n1-step, n2+step, step))
    payments_moments=np.linspace(n1-step, n2, int((n2 - n1 + step) / step)+1).tolist()
    if not payments_moments:
        payments_moments=[defer, defer+1/m]
    payments=[v_grow ** i for i in payments_moments[1:]]
    # insert initial payment of 0 at time 0
    payments.insert(0, 0)
    moment=1

    m_grf95_rv=gen_Axn(mort_table=mt_GRF95, interest_rate=i, payments_moments=payments_moments, 
                       payments=payments, x=x, moment=moment, method=method)
    m_tv7377_rv=gen_Axn(mort_table=mt_TV7377, interest_rate=i, payments_moments=payments_moments, 
                       payments=payments, x=x, moment=moment, method=method)

    if m==1:
        assert m_grf95 == pytest.approx(m_grf95_frac, rel=1e-16)
        assert m_tv7377 == pytest.approx(m_tv7377_frac, rel=1e-16)

    assert m_grf95_frac == pytest.approx(m_grf95_rv, rel=1e-6)
    assert m_tv7377_frac == pytest.approx(m_tv7377_rv, rel=1e-6)



def test_Ax_1(x=45, defer=0, n=500, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_2(x=125, defer=0, n=500, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_3(x=160, defer=0, n=500, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)


def test_Ax_4(x=45, defer=0, n=500, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_5(x=125, defer=0, n=500, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_6(x=160, defer=0, n=500, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)


def test_Ax_7(x=45, defer=0, n=500, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_8(x=125, defer=0, n=500, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_9(x=160, defer=0, n=500, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)


# Defered cases
def test_Ax_10(x=45, defer=5, n=500, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_11(x=125, defer=5, n=500, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_12(x=160, defer=5, n=500, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)


def test_Ax_13(x=45, defer=5, n=500, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_14(x=125, defer=5, n=500, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_15(x=160, defer=5, n=500, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)    


def test_Ax_16(x=45, defer=5, n=500, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_17(x=125, defer=5, n=500, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_18(x=160, defer=5, n=500, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)


# Temporary cases
def test_Ax_19(x=45, defer=0, n=10, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_20(x=125, defer=0, n=10, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_21(x=160, defer=0, n=10, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)


def test_Ax_22(x=45, defer=0, n=10, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_23(x=125, defer=0, n=10, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_24(x=160, defer=0, n=10, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)


def test_Ax_25(x=45, defer=0, n=10, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_26(x=125, defer=0, n=10, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_27(x=160, defer=0, n=10, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)



# Deferred Temporary cases
def test_Ax_28(x=45, defer=5, n=10, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_29(x=125, defer=5, n=10, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_30(x=160, defer=5, n=10, i=2, g=0, m=1, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)


def test_Ax_31(x=45, defer=5, n=10, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_32(x=125, defer=5, n=10, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_33(x=160, defer=5, n=10, i=2, g=0, m=3, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)


def test_Ax_34(x=45, defer=5, n=10, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_35(x=125, defer=5, n=10, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)

def test_Ax_36(x=160, defer=5, n=10, i=2, g=0, m=12, method='udd'):
    func_test_Ax(x, defer, n, i, g, m, method)   





def test_Ax():
    i = 2
    g = 0
    m = 3
    x = 45+125*+160*0
    defer=0
    method = 'udd'
    cf_grf95 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_GRF95.table_qx)
    cf_tv7377 = commutation_table.CommutationFunctions(i=i, g=g, mt=soa_TV7377.table_qx)

    m_grf95=cf_grf95.Ax(x=x)
    m_tv7377=cf_tv7377.Ax(x=x)

    m_grf95_frac=A_x(mt_GRF95, x=x, x_first=x+1/m, x_last=500, i=i, g=g, m=m, method=method)
    m_tv7377_frac=A_x(mt_TV7377, x=x, x_first=x+1/m, x_last=500, i=i, g=g, m=m, method=method)

    # probabilist approach
    n1=defer+1/m
    n2=max(mt_GRF95.w - x + 2, mt_TV7377.w - x + 2)
    step=1/m
    v= 1 / (1 + i / 100)
    d = (1-v)
    i2 = ((1 + i / 100) ** 2-1)*100
    v_grow= (1 + g / 100)
    payments_moments=list(np.arange(n1-1/m, n2, step))
    if not payments_moments:
        payments_moments=[0, 1/m]
    payments=[v_grow ** i for i in payments_moments[1:]]
    # insert initial payment of 0 at time 0
    payments.insert(0, 0)
    moment=1

    m_grf95_rv=gen_Axn(mort_table=mt_GRF95, interest_rate=i, payments_moments=payments_moments, 
                       payments=payments, x=x, moment=moment, method=method)
    m_tv7377_rv=gen_Axn(mort_table=mt_TV7377, interest_rate=i, payments_moments=payments_moments, 
                       payments=payments, x=x, moment=moment, method=method)

    if m==1:
        assert m_grf95 == pytest.approx(m_grf95_frac, rel=1e-16)
        assert m_tv7377 == pytest.approx(m_tv7377_frac, rel=1e-16)

    assert m_grf95_frac == pytest.approx(m_grf95_rv, rel=1e-6)
    assert m_tv7377_frac == pytest.approx(m_tv7377_rv, rel=1e-6)

    