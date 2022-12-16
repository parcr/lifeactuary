import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pareto
import os
import sys

"""
\item
Consider $T_{0}$ a continuous random variable that represents the future lifetime of a newborn, with 
\begin{align*}
f_{T_0}(x)=79.5\left(x+53\right)^{-2.5} \quad \text { for } x \in \mathbb{R}^+_0
\end{align*}

Determine:
\begin{enumerate}
\item {\tiny (1)} The probability of $(45)$ dying before attaining 65 years old. %1.0
\item {\tiny (1)} $\px[10]{35}$. %1.0
\item {\tiny (1)} $\qx[10|20]{35}$. %1.0
\item {\tiny (1)} $E(T_{65})$. %1.0
\item {\tiny (1)} $\mu_x$. %1
\end{enumerate}
"""

this_py = os.path.split(sys.argv[0])[-1][:-3]

# X\sim P(1, 1.5) and Y=aX+b, with a=e0(1.5-1) and b=-a
e0 = 106
shape = 1.5
scale = e0 * (shape - 1)
loc = -scale

rv = pareto(b=shape, loc=loc, scale=scale)
mean, var, skew, kurt = rv.stats(moments='mvsk')
print(f"For sub-portfolio A, we've mean={mean}, variance={var}, skewness={skew} and kurtosis={kurt}")
print('min value is:', rv.ppf(0))


def F0(t):
    if t < 0:
        return .0
    return 1 - np.power(scale / (t - loc), shape)


def f0(t):
    if t < 0:
        return .0
    return e0 * shape * (shape - 1) * np.power(t - loc, -shape - 1)


def S0(t):
    return 1 - F0(t)


def pxt(x, t):
    if t <= 0:
        return 1
    try:
        return S0(x + t) / S0(x)
    except ZeroDivisionError:
        return .0


def qxt(x, t):
    return 1 - pxt(x, t)


def mu(x):
    if x < 0:
        return .0
    else:
        return f0(x) / pxt(0, x)


"""
\item {\tiny (1)} The probability of $(45)$ dying before attaining 65 years old. %1.0
"""
print('\na)', round(qxt(45, 20), 10))
print('a)', round(1 - rv.sf(45 + 20) / rv.sf(45), 10))

"""
\item {\tiny (1)} $\px[10]{35}$. %1.0
"""
print('\nb)', round(pxt(35, 10), 10))
print('b)', round(rv.sf(35 + 10) / rv.sf(35), 10))

"""
\item {\tiny (1)} $\qx[10|20]{35}$. %1.0
"""
print('\nc)', round(pxt(35, 10), 10), 'x', round(qxt(45, 20), 10), '=',
      round(pxt(35, 10) * qxt(45, 20), 10))

'''some graphs'''
x_s = np.linspace(0, 120, 1000)

''' Ln force of mortality'''
force_of_mortality_lst = [mu(t) for t in x_s]
fig, axes = plt.subplots()
plt.plot(x_s, np.log(force_of_mortality_lst), label=f' ln Mortality Force({0}, {120})')
plt.xlabel(r'$x$')
plt.ylabel(r'$\mu_{x}$')
plt.title(r'ln Force of Mortality')
plt.grid(b='visible', which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_force_of_mortality' + '.eps', format='eps', dpi=3600)
plt.show()

''' Survival Function '''
prob_survival_lst = [S0(t) for t in x_s]
fig, axes = plt.subplots()
plt.plot(x_s, prob_survival_lst, label=f'Survival Function({0}, {120})')
plt.xlabel(r'$x$')
plt.ylabel(r'$S_{0}(x)$')
plt.title(r'Survival Function')
plt.grid(b='visible', which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_Survival_Function' + '.eps', format='eps', dpi=3600)
plt.show()

'''
Note this is not a good survival function because the probabilities of surviving one year are increasing
'''
lst_1px = [(x, pxt(x, 1)) for x in range(0, 120 + 1)]
