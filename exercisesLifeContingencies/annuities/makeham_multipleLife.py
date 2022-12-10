from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions

mml = makeham_mortality_functions.Makeham(a=0.0001, b=0.00030, c=1.075)

'''
$\ax**[]{25:30}$
'''

i = 5
v = 1 / (1 + i / 100)
x = 25
y = 30
w = 130

prob_discount = [mml.S(x=x, t=t) * mml.S(x=y, t=t) * v ** t for t in range(w - max(x, y) + 1)]
print('annuity:', sum(prob_discount))

'''
$\ax**[]{\overline{25:30}}$
'''
prob_discount_2 = [(mml.S(x=x, t=t) + mml.S(x=y, t=t) - mml.S(x=x, t=t) * mml.S(x=y, t=t)) * v ** t for t in
                 range(w - max(x, y) + 1)]
print('annuity:', sum(prob_discount_2))

'''
$\ax**[]{25|30}=\ax**[]{30}-\ax**[]{25:30}$
'''
prob_discount_3 = [mml.S(x=y, t=t) * v ** t for t in range(w - max(x, y) + 1)]
print('annuity:', sum(prob_discount_3)-sum(prob_discount))



