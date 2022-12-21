import numpy as np

from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import scipy.integrate

"""
\item Considering that a life (45) buys Whole Life insurance that pays $100\:000$\euro, immediately on 
here\textbackslash his death of provided she\textbackslash he dies before a life (43). The insurance company selling 
this cover to price this risk uses the technical basis, that is the assumptions, defined in question 1. 
Justifying all calculus, please determine:
\begin{enumerate}
\item  {\tiny (2)} The net single premium that the insurer should charge.

\item  {\tiny (2)} The probability that there is no claim.
\end{enumerate}
"""

mml = makeham_mortality_functions.Makeham(a=0.0025, b=2.5E-6, c=1.07)

e0 = mml.moments_Tx()
print('e0=', e0)

w = 125
interest_rate = 3.5
interest_rate_2 = ((1 + interest_rate / 100) ** 2 - 1) * 100
x = 45
y = 43
capital = 100000
v = 1 / (1 + interest_rate / 100)
v2 = 1 / (1 + interest_rate_2 / 100)


def A_TxTy(x, y, t):
    return mml.S(x, t) * mml.S(y, t) * (mml.mu(x + t) + mml.mu(y + t))


def A_xy(x, y, t):
    def S(t):
        return A_TxTy(x, y, t) * np.power(v, t)

    return scipy.integrate.quad(S, 0, t)[0]


def A_TxTy1(x, y, t):
    return mml.S(x, t) * mml.mu(x + t) * mml.S(y, t)


def A_xy1(x, y, t):
    def S(t):
        return A_TxTy1(x, y, t) * np.power(v, t)

    return scipy.integrate.quad(S, 0, t)[0]


def A_TxTy2(x, y, t):
    return mml.S(x, t) * mml.S(y, t)* mml.mu(y + t)


def A_xy2(x, y, t):
    def S(t):
        return A_TxTy2(x, y, t) * np.power(v, t)

    return scipy.integrate.quad(S, 0, t)[0]


def q_xy1(x, y, t):
    def S(t):
        return A_TxTy1(x, y, t)

    return scipy.integrate.quad(S, 0, t)[0]


"""
\item  {\tiny (2)} The net single premium that the insurer should charge.
"""

tli_xy1 = A_xy1(x, y, 200)
tli_xy2 = A_xy2(x, y, 200)
print('A_xy1:', tli_xy1)
print('A_xy1 capital:', round(tli_xy1 * capital, 5))
print('A_xy2:', tli_xy2)
print('A_xy2 capital:', round(tli_xy2 * capital, 5))

"""
\item  {\tiny (2)} The probability that there is no claim.
"""
prob_xy1 = q_xy1(x, y, 200)
print('q_xy1:', round(prob_xy1 * 100, 5), '%', sep='')
print('q_xy2:', round((1-prob_xy1) * 100, 5), '%', sep='')
