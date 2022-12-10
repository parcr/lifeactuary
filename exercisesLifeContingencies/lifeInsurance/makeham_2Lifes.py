import numpy as np

from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import scipy.integrate

mml = makeham_mortality_functions.Makeham(a=0.0001, b=0.00030, c=1.075)

'''
\item $\Ax*[]{25:30}$
'''

x = 25
y = 30
i = 5
v = 1 / (1 + i / 100)


def A_TxTy(x, y, t):
    return mml.S(x, t) * mml.S(y, t) * (mml.mu(x + t) + mml.mu(y + t))


def A_xy(x, y, t):
    def S(t):
        return A_TxTy(x, y, t) * np.power(v, t)

    return scipy.integrate.quad(S, 0, t)[0]


wli_xy = A_xy(x, y, 1000)
print('A_xy:', wli_xy)

'''
\item $\Ax*[]{25:30:\angl{10}}[1]$
'''


def A_TxTy1(x, y, t):
    return mml.S(x, t) * mml.mu(x + t) * mml.S(y, t)


def A_xy1(x, y, t):
    def S(t):
        return A_TxTy1(x, y, t) * np.power(v, t)

    return scipy.integrate.quad(S, 0, t)[0]


tli_xy1 = A_xy1(x, y, 10)
print('A_xy1:', tli_xy1)

'''
\item $\Ax*[]{xy}[2]$
'''


def A_TxTy2(x, y, t):
    return mml.S(x, t) * mml.mu(x + t) * (1-mml.S(y, t))


def A_xy2(x, y, t):
    def S(t):
        return A_TxTy2(x, y, t) * np.power(v, t)

    return scipy.integrate.quad(S, 0, t)[0]


wli_xy2 = A_xy2(x, y, 1000)
print('A_xy2:', wli_xy2)


def A_Tx(x,t):
    return mml.S(x, t) * mml.mu(x + t)


def A_x(x, t):
    def S(t):
        return A_Tx(x, t) * np.power(v, t)

    return scipy.integrate.quad(S, 0, t)[0]


wli_x = A_x(x, 1000)
print('A_x:', wli_x)

print('test:', A_xy1(x, y, 1000)+A_xy2(x, y, 1000)-wli_x)