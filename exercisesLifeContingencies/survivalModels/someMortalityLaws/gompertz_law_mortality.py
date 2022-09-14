import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import scipy.integrate


def mu(b, c, x):
    if x < 0 or (b <= 0 or b >= 1) or c <= 1:
        return np.nan
    return b * np.power(c, x)


def S(b, c, x, t):
    if x < 0 or (b <= 0 or b >= 1) or c <= 1:
        return np.nan
    if t < 0:
        return 1
    else:
        return np.exp(-b / np.log(c) * np.power(c, x) * (np.power(c, t) - 1))


def pdf(b, c, x, t):
    if x < 0 or (b <= 0 or b >= 1) or c <= 1:
        return np.nan
    if t < 0:
        return 1
    else:
        return b * np.power(c, x + t) * np.exp(-b / np.log(c) * np.power(c, x) * (np.power(c, t) - 1))


def moments_Tx(b, c, x=0, k=1):
    if x < 0 or k < 0:
        return np.nan
    if k == 0:
        return 1
    elif k > 0:
        def t_pxt(t):
            return k * np.power(t, k - 1) * np.exp(-b / np.log(c) * np.power(c, x) * (np.power(c, t) - 1))

        ev = scipy.integrate.quad(t_pxt, 0, np.inf)
        return ev


def expected_value_Tx(b, c, x=0):
    return moments_Tx(b=b, c=c, x=x, k=1)[0]


def variance_Tx(b, c, x=0):
    ev = expected_value_Tx(b=b, c=c, x=x)
    ev_square = moments_Tx(b=b, c=c, x=x, k=2)[0]
    return ev_square - np.power(ev, 2)


def moments_Kx(b, c, x=0, k=1, truncated=120):
    if x < 0 or k < 0:
        return np.nan
    if k == 0:
        return 1
    elif k == 1:
        probs = [S(b=b, c=c, x=x, t=n) for n in range(1, int(truncated - x + 1))]
        ev = np.sum(probs)
        return ev
    elif k == 2:
        probs = [S(b=b, c=c, x=x, t=n) for n in range(1, int(truncated - x + 1))]
        ev = np.sum(probs)
        probs = [n * S(b=b, c=c, x=x, t=n) for n in range(1, int(truncated - x + 1))]
        ev = k * np.sum(probs) - ev
        return ev


def expected_value_Kx(b, c, x=0, truncated=120):
    return moments_Kx(b=b, c=c, x=x, k=1, truncated=truncated)


def variance_Kx(b, c, x=0, truncated=120):
    ev = expected_value_Kx(b=b, c=c, x=x, truncated=truncated)
    ev_square = moments_Kx(b=b, c=c, x=x, k=2, truncated=truncated)
    return ev_square - np.power(ev, 2)


t = np.linspace(0, 100, 1000 + 1)
b = 0.0003
c = 1.07
x_s = [0, 20, 50, 80]

S_vec = np.vectorize(S)
fig, ax = plt.subplots()
for x in x_s:
    y = S_vec(b=b, c=c, x=x, t=t)
    plt.plot(t, y, label=f'x={x}')

plt.title(f'Gompertz Law Survival Function (B={b}, c={c})')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('t')
plt.ylabel(f'$S_x(t)$')
this_py = os.path.split(sys.argv[0])[-1][:-3]
plt.savefig(this_py + '_sf' + '.eps', format='eps', dpi=3600)
plt.show()

pdf_vec = np.vectorize(pdf)
fig, ax = plt.subplots()
for x in x_s:
    y = pdf_vec(b=b, c=c, x=x, t=t)
    plt.plot(t, y, label=f'x={x}')

plt.title(f'Gompertz Law Probability Density Function (B={b}, c={c})')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('t')
plt.ylabel(f'$f_x(t)$')
plt.savefig(this_py + '_pdf' + '.eps', format='eps', dpi=3600)
plt.show()

'''
Compare q_x with \mu_{x+.5}
'''

mu_vec = np.vectorize(mu)
ages = np.linspace(0, 120, 121)
mu_s = mu_vec(b=b, c=c, x=ages + .5)
qx = 1 - S_vec(b=b, c=c, x=ages, t=1)
error_qx = qx - mu_s
relat_error_qx = np.abs(error_qx / qx)

fig, ax = plt.subplots()
plt.plot(ages, qx, label=f'$q_x$')
plt.plot(ages, mu_s, label=f'$\mu_s$')
plt.title(f'Gompertz Law $q_x$ versus $\mu_x$ (B={b}, c={c})')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('t')
plt.ylabel(f'$q_x$ and $\mu_x$')
plt.savefig(this_py + '_qx_mu' + '.eps', format='eps', dpi=3600)
plt.show()

#
for a in [20, 50, 110]:
    print(f"$q_{{{a}}}$={qx[a]} versus $\mu_{{{a}+.5}}$={mu_s[a]}")

'''
Calculation of the Moments for T_x and K_x
'''

ev_s = [expected_value_Tx(b=b, c=c, x=age) for age in ages]
ev_K_s = [expected_value_Kx(b=b, c=c, x=age, truncated=ages[-1] + 1) for age in ages]
fig, ax = plt.subplots()
plt.plot(ages, ev_s, label=f'$E(T_x)$')
plt.plot(ages, ev_K_s, label=f'$E(K_x)$')
plt.title(f'Complete Expectation of Life')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('x')
plt.ylabel(r'$E(T_x)$ and $E(K_x)$')
plt.savefig(this_py + '_ev_Tx' + '.eps', format='eps', dpi=3600)
plt.show()

ev_s = [np.sqrt(variance_Tx(b=b, c=c, x=age)) for age in ages]
ev_K_s = [np.sqrt(variance_Kx(b=b, c=c, x=age, truncated=ages[-1] + 1)) for age in ages]
fig, ax = plt.subplots()
plt.plot(ages, ev_s, label=r'$\sqrt{V(T_x)}$')
plt.plot(ages, ev_K_s, label=r'$\sqrt{V(K_x)}$')
plt.title(f'Standard Deviation for Future Lifetime')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('x')
plt.ylabel(r'$\sqrt{V(T_x)}$ and $\sqrt{V(K_x)}$')
plt.savefig(this_py + '_var_Tx' + '.eps', format='eps', dpi=3600)
plt.show()

for a in [0, 20, 30, 50, 80, 110]:
    print(
        f"$E(T_{{{a}}})$={expected_value_Tx(b=b, c=c, x=a)}" + ' and ' + f"$V(T_{{{a}}})$={variance_Tx(b=b, c=c, x=a)}")
    print(
        f"$E(K_{{{a}}})$={expected_value_Kx(b=b, c=c, x=a)}" + ' and ' + f"$V(K_{{{a}}})$={variance_Kx(b=b, c=c, x=a)}")


