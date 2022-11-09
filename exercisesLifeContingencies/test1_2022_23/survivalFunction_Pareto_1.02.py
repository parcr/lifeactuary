import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pareto
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]

rv = pareto(b=1.02, loc=-2, scale=2)
mean, var, skew, kurt = rv.stats(moments='mvsk')
print(f"For this random variable, we've mean={mean}, variance={var}, skewness={skew} and kurtosis={kurt}")
print('min value is:', rv.ppf(0))


def F0(t):
    if t < 0:
        return .0
    return 1-(2/(2+t))**1.02


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
    return 1.02/(x+2)**1.02



'''
\item The probability of $(45)$ dying before complete 65 year old. %1.0
'''
print('\na')
print(round(qxt(45, 65-45), 10))
print(round((rv.sf(45)-rv.sf(65))/rv.sf(45), 10))

'''
\item $\px[40]{25}$. %1.0
'''
print('\nb')
print(round(pxt(25, 40), 10))
print(round(rv.sf(65)/rv.sf(25), 10))

'''
\item $\qx[40|5]{25}$. %1.0
'''
print('\nc')
print(round(pxt(25, 40) * qxt(65, 5), 10))


'''
\item $E(T_{65})$
'''
print('\nd')
probs = [pxt(118, t) for t in range(1, 3)]
print(round(sum(probs), 10))

'''some graphs'''
x_s = np.linspace(0, 120, 1000)

''' Ln force of mortality'''
force_of_mortality_lst = [mu(t) for t in x_s]
fig, axes = plt.subplots()
plt.plot(x_s, np.log(force_of_mortality_lst), label=f'Mortality Force({0}, {120})')
plt.xlabel(r'$x$')
plt.ylabel(r'$\ln{(mu_{x})}$')
plt.title(r'Force of Mortality')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
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
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_Survival_Function' + '.eps', format='eps', dpi=3600)
plt.show()
