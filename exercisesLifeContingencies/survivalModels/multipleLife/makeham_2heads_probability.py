from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import scipy.integrate

mml = makeham_mortality_functions.Makeham(a=0.0001, b=0.00030, c=1.075)

'''
$\px[10]{30:40}$
'''

x = 30
y = 40
t = 10
tpx = mml.S(x=x, t=t)
tpy = mml.S(x=y, t=t)
tpxy = tpx * tpy
print(f'a) The probability that ({x}) and ({y}) are both alive after {t} years')
print(f'tpx= {tpx}', f'tpy= {tpy}', f'tpxy= {tpxy}')
print()

'''
'''


# \qx[10]{30:40}[1]
def S_xy_mux(x, y, t):
    return mml.S(x, t) * mml.S(y, t) * mml.mu(x + t)


def q_xy_mux(x, y, t):
    def S(t):
        return S_xy_mux(x, y, t)

    return scipy.integrate.quad(S, 0, t)[0]


tqxy_1 = q_xy_mux(x=x, y=y, t=t)
print(f'b) The probability that ({x}) dies within {t} years and ({y}) is still alive.')
print(f'tqxy_1= {tqxy_1}')
print()

'''
\qx[10]{30:40}[2]
'''
tqx = 1 - mml.S(x=x, t=t)
tqxy_2 = tqx - tqxy_1
print(f'c) The probability that ({x}) dies within {t} years and ({y}) is already death.')
print(f'tqx={tqx}', f'tqxy_2= {tqxy_2}')

def S_xy_muy(x, y, t):
    return mml.S(x, t) * (1 - mml.S(y, t)) * mml.mu(x + t)


def q_xy_muy(x, y, t):
    def S(t):
        return S_xy_muy(x, y, t)

    return scipy.integrate.quad(S, 0, t)[0]


tqxy_2_b = q_xy_muy(x=x, y=y, t=t)
print(f'tqxy_2_b= {tqxy_2_b}')
print('test solution:', tqxy_2-tqxy_2_b)
print()

'''
$\px[10]{\overline{30:40}}$
'''
tqx = 1 - mml.S(x=x, t=t)
tqy = 1 - mml.S(x=y, t=t)

print(f'tqx= {tqx}', f'tqy= {tqy}', f'tqxy= {tqx*tqy}', f'tpxy= {1-tqx*tqy}')