__author__ = "PedroCR"

from disability_tables import disability_tables as dt
from turnover_tables import turnover_tables as tt
from essential_life import mortality_table as mt, read_soa_table_xml as rst
from essential_life.multidecrement_table import MultiDecrementTable as mdt
import numpy as np
import matplotlib.pyplot as plt

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
ekv80 = dt.EVK_80
ekv80_70 = dt.EVK_80_ext_70
pcr1 = tt.pcr_turnover
pcr2 = tt.pcr_turnover_65

mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)
dt_ekv80 = mt.MortalityTable(mt=ekv80, last_q=0)
tt_pcr = mt.MortalityTable(mt=pcr1, last_q=0)

tables_unidecrement = {'mortality': mt_TV7377, 'disability': dt_ekv80, 'turnover': tt_pcr}

tables_multidecrement = mdt(dict_tables=tables_unidecrement)
tables_multidecrement.create_udd_multidecrement_table()

# create a transition matrix
transition_info = [[(tables_multidecrement.net_table, 'p'),
                    (tables_multidecrement.multidecrement_tables['disability'], 'q'),
                    (tables_multidecrement.multidecrement_tables['turnover'], 'q'),
                    (tables_multidecrement.multidecrement_tables['mortality'], 'q')]]
transition_info.append([0,
                        (tables_multidecrement.unidecrement_tables['mortality'], 'p'),
                        0,
                        (tables_multidecrement.unidecrement_tables['mortality'], 'q')])
transition_info.append([0,
                        0,
                        (tables_multidecrement.unidecrement_tables['mortality'], 'p'),
                        (tables_multidecrement.unidecrement_tables['mortality'], 'q')])
transition_info.append([0,
                        0,
                        0,
                        1])


def transition_matrix_1(transition_info, x):
    c = len(transition_info)
    r = len(transition_info[0])
    mat = np.zeros((r, c))
    control = np.zeros((r))
    for r_i, r in enumerate(transition_info):
        for c_i, c in enumerate(r):
            if type(transition_info[r_i][c_i]) == tuple:
                if transition_info[r_i][c_i][1] == 'p':
                    mat[r_i][c_i] = transition_info[r_i][c_i][0].npx(x=x, n=1, method='udd')
                else:
                    mat[r_i][c_i] = transition_info[r_i][c_i][0].nqx(x=x, n=1, method='udd')
            else:
                mat[r_i][c_i] = transition_info[r_i][c_i]
        control[r_i] = sum(mat[r_i])  # todo: pass control to log when sum of rows are different of 1
    return mat


def transition_matrix_n(transition_info, x1, x2, init_state=None):
    if x2 <= x1: return None
    c = len(transition_info)
    r = len(transition_info[0])
    mat = np.identity(c)
    if init_state is None:
        init_state = np.zeros((r, 1))
        init_state[0][0] = 1

    control = []
    state_path = [init_state]
    for x in range(x1, x2):
        mat_1 = transition_matrix_1(transition_info, x)
        mat = np.dot(mat, mat_1)
        control.append(mat.sum(axis=1))
        final_state = np.dot(mat.transpose(), init_state)
        state_path.append(final_state.flatten().tolist())
    return mat, state_path


mat = transition_matrix_1(transition_info, x=45)
mat_n = transition_matrix_n(transition_info, 45, 106, np.array([1000, 100, 200, 50]))
init_pop = np.array((1000, 0, 0, 0))
final_pop = np.dot(mat_n[0].transpose(), init_pop)

# if we want to create a dictionary
keys = ['active', 'disable', 'withdraw', 'death']
final_pop_dict = dict()
state_path_to_plot = np.array(mat_n[1]).transpose().tolist()
for k_i, k in enumerate(keys):
    final_pop_dict[k] = state_path_to_plot[k_i]

# plot a bar chart
ages = list(range(len(mat_n[1])))
bottom = np.zeros(len(mat_n[1]))
for k, v in final_pop_dict.items():
    plt.bar(ages, v, bottom=bottom)
    bottom += v
plt.legend(final_pop_dict.keys(), loc=2)
plt.xlabel('Year')
plt.ylabel('Population Path')
