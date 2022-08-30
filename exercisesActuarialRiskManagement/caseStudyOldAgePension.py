from essential_life import read_soa_table_xml as rst
import matplotlib.pyplot as plt
import os
import sys

from essential_life import mortality_table, commutation_table

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
path = '../soa_tables/'
interest_rate = 4
mt_lst = [rst.SoaTable(path + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

table_idx = 0
name = table_names[table_idx]
print(f'The Table being used is {name}')
lt = lt_lst[table_idx]
ct = ct_lst[table_idx]


def pvfb_oldAge(y, x, r, table_name, interest_rate, benefit=1):
    mt = rst.SoaTable(path + table_name + '.xml')
    lt = mortality_table.MortalityTable(mt=mt.table_qx)
    ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx)

    if x < y:
        return .0
    prob_surv = lt.npx(x=x, n=r - x)
    i = interest_rate / 100
    v = 1 / (1 + i)
    discount = v ** (max(0, r - x))
    annuity = ct.aax(x=max(x, r), m=1)

    return prob_surv * discount * benefit * annuity


def puc_oldAge(y, x, r, table_name, interest_rate, benefit=1):
    '''
    Calculus for projected unit credit
    :param y:
    :param x:
    :param r:
    :param table_name:
    :param interest_rate:
    :param benefit:
    :return:
    '''
    mt = rst.SoaTable(path + table_name + '.xml')
    lt = mortality_table.MortalityTable(mt=mt.table_qx)
    ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx)

    pvfb = pvfb_oldAge(y, x, r, table_name, interest_rate, benefit)
    tts = max(r - y, 0)
    pts = min(tts, x - y)
    fts = tts - pts
    if x < r:
        nc = pvfb / tts
    else:
        nc = 0
    al = pvfb * pts / tts

    return {'pts': pts, 'fts': fts, 'al': al, 'nc': nc}


def leveled_oldAge(y, x, r, table_name, interest_rate, benefit=1):
    '''
    Calculus for projected unit credit
    :param y:
    :param x:
    :param r:
    :param table_name:
    :param interest_rate:
    :param benefit:
    :return:
    '''
    mt = rst.SoaTable(path + table_name + '.xml')
    lt = mortality_table.MortalityTable(mt=mt.table_qx)
    ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx)

    premium_annuity_y = ct.naax(x=y, n=r - y, m=1)
    pvfb_y = pvfb_oldAge(y, y, r, table_name, interest_rate, benefit)
    premium_leveled = pvfb_y / premium_annuity_y

    pvfb = pvfb_oldAge(y, x, r, table_name, interest_rate, benefit)
    tts = max(r - y, 0)
    pts = min(tts, x - y)
    fts = tts - pts
    if x < r:
        nc = premium_leveled
    else:
        nc = 0
    premium_annuity_x = ct.naax(x=x, n=r - x, m=1)
    al = pvfb - premium_leveled * premium_annuity_x

    return {'pts': pts, 'fts': fts, 'al': al, 'nc': nc}


'''
Solving Case Study
'''
y = 25
r = 65
ages = range(y, r + 11)
pvfb_path = [pvfb_oldAge(y=y, x=age, r=r, table_name=name, interest_rate=interest_rate) for age in ages]
puc_path = [puc_oldAge(y=y, x=age, r=r, table_name=name, interest_rate=interest_rate) for age in ages]
leveled_path = [leveled_oldAge(y=y, x=age, r=r, table_name=name, interest_rate=interest_rate) for age in ages]

puc_path_al = [puc_path[j]['al'] for j in range(0, len(puc_path))]
leveled_path_al = [leveled_path[j]['al'] for j in range(0, len(leveled_path))]

plt.plot(ages, pvfb_path, label='Present Value Future Benefits')
plt.plot(ages, puc_path_al, label='Actuarial Liability PUC')
plt.plot(ages, leveled_path_al, label='Actuarial Liability Leveled')
plt.xlabel(r'$x$')
plt.ylabel('Estimates')
plt.title('Old Age')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_pvfb' + '.eps', format='eps', dpi=3600)
plt.show()

puc_path_nc = [puc_path[j]['nc'] for j in range(0, len(puc_path))]
leveled_path_nc = [leveled_path[j]['nc'] for j in range(0, len(leveled_path))]
plt.plot(ages, puc_path_nc, 'o', label='Normal Contribution PUC')
plt.plot(ages, leveled_path_nc, 'o', label='Normal Contribution Leveled')
plt.xlabel(r'$x$')
plt.ylabel('NC')
plt.title('Old Age NC')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_nc' + '.eps', format='eps', dpi=3600)
plt.show()

