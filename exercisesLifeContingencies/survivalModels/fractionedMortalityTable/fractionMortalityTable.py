from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
import pandas as pd

mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
w = 130
fraction = 4
x_s = np.arange(0, w + 1, 1 / fraction)

'''
Compute Life Table and commutation table
'''
interest_rate = 5
v = 1 / (1 + interest_rate / 100)
v_fraction = v ** (1 / fraction)

l0 = 100000
lx = [mml.S(0, x) for x in x_s]
lx = np.array(lx) * l0
dx = lx[:-1] - lx[1:]
dx = np.append(dx, lx[-1])
qx = dx / lx
px = 1 - qx
# commutation symbols
Dx = [l * v_fraction ** idx_l for idx_l, l in enumerate(lx)]
Nx = [sum(Dx[idx_l:]) for idx_l, l in enumerate(lx)]
Sx = [sum(Nx[idx_l:]) for idx_l, l in enumerate(lx)]
Cx = [dx[idx_l] * v_fraction ** (idx_l + 1) for idx_l, l in enumerate(lx)]
Mx = [sum(Cx[idx_l:]) for idx_l, l in enumerate(lx)]
Rx = [sum(Mx[idx_l:]) for idx_l, l in enumerate(lx)]

comm_table = pd.DataFrame({'x': x_s, 'lx': lx, 'dx': dx, 'qx': qx, 'px': px,
                           'Dx': Dx, 'Nx': Nx, 'Sx': Sx, 'Cx': Cx, 'Mx': Mx, 'Rx': Rx})
comm_table.to_excel(excel_writer='makeham@' + str(interest_rate) + '_' + str(fraction) +
                    '.xlsx', sheet_name='makeham', index=False, freeze_panes=(1, 1))
