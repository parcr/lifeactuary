from lifeActuary import mortality_table as mt
from lifeActuary import mortality_table_2heads as mt2h
from soa_tables import read_soa_table_xml as rst

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)

mt_2heads_jl = mt2h.MortalityTable2Heads(mt_old=mt_GRF95, mt_young=mt_TV7377, age_dif=3, status="joint-life")
mt_2heads_ls = mt2h.MortalityTable2Heads(mt_old=mt_GRF95, mt_young=mt_TV7377, age_dif=3, status="last-survivor")

if False:
    mt_2heads_jl.mt_2heads.df_life_table().to_excel(excel_writer='jointLife' + '.xlsx', sheet_name='jointLife',
                                                    index=False, freeze_panes=(1, 1))
    mt_2heads_ls.mt_2heads.df_life_table().to_excel(excel_writer='lastSurvivor' + '.xlsx', sheet_name='lastSurvivor',
                                                    index=False, freeze_panes=(1, 1))

# Probabilities
probSurv1year_jl = [mt_2heads_jl.npxy(x, x + mt_2heads_jl.age_dif, 1) for x in range(mt_2heads_jl.mt_2heads.w + 1)]
probSurv1year_ls = [mt_2heads_ls.npxy(x, x + mt_2heads_ls.age_dif, 1) for x in range(mt_2heads_ls.mt_2heads.w + 1)]

print(mt_2heads_jl.mt_2heads.lx[25+30]/mt_2heads_jl.mt_2heads.lx[25], ' compares to ',
      mt_2heads_jl.npxy(25, 25+mt_2heads_jl.age_dif, 30))
print(mt_2heads_ls.mt_2heads.lx[25+30]/mt_2heads_ls.mt_2heads.lx[25], ' compares to ',
      mt_2heads_ls.npxy(25, 25+mt_2heads_ls.age_dif, 30))

# Benefits
## Annuities
print('\nAnnuities')
ann_jl = mt_2heads_jl.annuity(x_young=25, x_first_payment=25, x_last_payment=200, i=5, g=0,
                              m=2, method='udd')
print(f'annuity jl: {ann_jl}')
ann_ls = mt_2heads_ls.annuity(x_young=25, x_first_payment=25, x_last_payment=200, i=5, g=0,
                              m=2, method='udd')
print(f'annuity ls: {ann_ls}')

ann_jl = mt_2heads_jl.annuity(x_young=25, x_first_payment=25.5, x_last_payment=200, i=5, g=0,
                              m=2, method='udd')
print(f'annuity jl: {ann_jl}')
ann_ls = mt_2heads_ls.annuity(x_young=25, x_first_payment=25.5, x_last_payment=200, i=5, g=0,
                              m=2, method='udd')
print(f'annuity ls: {ann_ls}')

ann_jl = mt_2heads_jl.annuity(x_young=25, x_first_payment=50, x_last_payment=200, i=5, g=0,
                              m=1, method='udd')
print(f'annuity jl: {ann_jl}')
ann_ls = mt_2heads_ls.annuity(x_young=25, x_first_payment=50, x_last_payment=200, i=5, g=0,
                              m=1, method='udd')
print(f'annuity ls: {ann_ls}')
