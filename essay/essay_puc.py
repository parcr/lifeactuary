__author__ = "PedroCR"

from disability_tables import disability_tables as dt
from turnover_tables import turnover_tables as tt
from essential_life import mortality_table as mt, age, read_soa_table_xml as rst
from essential_life.multidecrement_table import MultiDecrementTable as mdt
from toDelete import puc_old2
from matplotlib import pyplot as plt

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

dict_dates = {'date_of_birth': '1977-03-12', 'date_of_entry': '1997-05-15'}
date_of_valuation = '2019-12-31'

dates_for_term_cost = age.Age(date1=dict_dates['date_of_birth'], date2=dict_dates['date_of_birth']).date_inc_years(55)
age_term_cost_years = dates_for_term_cost.age_act()
puc_d = puc_old2.PUC(date_of_valuation=date_of_valuation, date_of_birth=dict_dates['date_of_birth'],
                     date_of_entry=dict_dates['date_of_entry'], age_of_term_cost=age_term_cost_years,
                     multi_table=tables_multidecrement, decrement='disability', i=2,
                     age_first_instalment=None, age_last_instalment=None, age_first_payment=None)

puc_d.set_default_waiting_periods()

# compute pvfb
x = 45
print(f"PVTC({puc_d.y}, {puc_d.x}, {puc_d.age_of_term_cost}|{puc_d.y})={puc_d.pvftc(x=puc_d.y)}")
print(f"PVTC({puc_d.y}, {puc_d.x}, {puc_d.age_of_term_cost}|{x})={puc_d.pvftc(x=x)}")
print(f"PVTC({puc_d.y}, {puc_d.x}, {puc_d.age_of_term_cost}|{puc_d.x})={puc_d.pvtc_x()}")
x_1=54
print(f"PVTC({puc_d.y}, {puc_d.x}, {puc_d.age_of_term_cost}|{x_1})={puc_d.pvftc(x=x_1)}")
x_1=55
print(f"PVTC({puc_d.y}, {puc_d.x}, {puc_d.age_of_term_cost}|{x_1})={puc_d.pvftc(x=x_1)}")
x_1=56
print(f"PVTC({puc_d.y}, {puc_d.x}, {puc_d.age_of_term_cost}|{x_1})={puc_d.pvftc(x=x_1)}")
x_1=60
print(f"PVTC({puc_d.y}, {puc_d.x}, {puc_d.age_of_term_cost}|{x_1})={puc_d.pvftc(x=x_1)}")

# test
test = puc_d.test()
print(f"Test NC in disability {test}")

pvfb_all_d = puc_d.vec_pvtc_y_first_payment()
al_all_d = puc_d.al_all_ages()
nc_all_d = puc_d.nc_all_ages()
fig, ax = fig, axs = plt.subplots()
plt.plot(pvfb_all_d[1][:], pvfb_all_d[2][:], 'o-', label='pvfb disability')
plt.plot(al_all_d[1][:], al_all_d[2][:], 'o-', mfc='none', label='al disability')
plt.plot(nc_all_d[1][:], nc_all_d[2][:], 'o--', mfc='none', label='nc disability')
plt.title('Disability')
plt.legend()

# print(pvfb_all_d)
# print(al_all_d)
# print(nc_all_d)


# projection
pvfb_all_d = puc_d.vec_pvtc_y_w_proj()
al_all_d = puc_d.al_y_w_proj()
nc_all_d = puc_d.nc_y_w_proj()
fig, ax = fig, axs = plt.subplots()
plt.plot(pvfb_all_d[1][:], pvfb_all_d[2][:], 'o-', label='pvfb disability projected')
plt.plot(al_all_d[1][:], al_all_d[2][:], 'o-', mfc='none', label='al disability projected')
plt.plot(nc_all_d[1][:], nc_all_d[2][:], 'o--', mfc='none', label='nc disability projected')
plt.title('Disability Projected')
plt.legend()

'''



Retirement
'''
print('\n')
print('Testing for Retirement at 65')
age_retirement_65 = age.Age(date1=dict_dates['date_of_birth'], date2=dict_dates['date_of_birth']).date_inc_years(65)
puc_retirement = puc_old2.PUC(date_of_valuation=date_of_valuation, date_of_birth=dict_dates['date_of_birth'],
                              date_of_entry=dict_dates['date_of_entry'], age_of_term_cost=65,
                              multi_table=tables_multidecrement, decrement=None, i=2,
                              age_first_instalment=None, age_last_instalment=None, age_first_payment=None)

puc_retirement.set_default_waiting_periods()

# compute pvfb
x = 65
print(
    f"PVTC({puc_retirement.y}, {puc_retirement.x}, {puc_retirement.age_of_term_cost}|{x})={puc_retirement.pvftc(x=x)}")
print(
    f"PVTC({puc_retirement.y}, {puc_retirement.x}, {puc_retirement.age_of_term_cost}|{puc_retirement.x})={puc_retirement.pvtc_x()}")

# test
test = puc_retirement.test()
print(f"Test NC in retirement {test}")

pvfb_all_retirement = puc_retirement.vec_pvtc_y_first_payment()
al_all_retirement = puc_retirement.al_all_ages()
nc_all_retirement = puc_retirement.nc_all_ages()
fig, ax = fig, axs = plt.subplots()
plt.plot(pvfb_all_retirement[1], pvfb_all_retirement[2], 'o-', label='pvfb retirement')
plt.plot(al_all_retirement[1], al_all_retirement[2], 'o-', mfc='none', label='al retirement')
plt.plot(nc_all_retirement[1], nc_all_retirement[2], 'o-', mfc='none', label='nc retirement')
plt.title('Retirement')
plt.legend()

# projection
pvfb_all_retirement = puc_retirement.vec_pvtc_y_w_proj()
al_all_retirement = puc_retirement.al_y_w_proj()
nc_all_retirement = puc_retirement.nc_y_w_proj()
fig, ax = fig, axs = plt.subplots()
plt.plot(pvfb_all_retirement[1][:], pvfb_all_retirement[2][:], 'o-', label='pvfb retirement projected')
plt.plot(al_all_retirement[1][:], al_all_retirement[2][:], 'o-', mfc='none', label='al retirement projected')
plt.plot(nc_all_retirement[1][:], nc_all_retirement[2][:], 'o--', mfc='none', label='nc retirement projected')
plt.title('Retirement Projected')
plt.legend()
plt.show()
