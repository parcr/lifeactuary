from soa_tables import read_soa_table_xml as rst

import pandas as pd
import numpy as np

from lifeActuary.commutation_table_frac import CommutationFunctionsFrac

# reads soa table
#soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')
soa = rst.SoaTable('../soa_tables/' + 'GRF95' + '.xml')
table_manual_qx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='qx')
table_manual_lx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='lx')

# creates mortality table from 1x of soa table
''' Commutation Table '''
tv7377_ct_frac = CommutationFunctionsFrac(i=2, g=0, data_type='q', mt=soa.table_qx, perc=100,
                                          frac=2, method='udd')

grf95_ct_frac = CommutationFunctionsFrac(i=2, g=0, data_type='q', mt=soa.table_qx, perc=100,
                                          frac=2, method='udd')

name = (soa.name.replace(' ', '')).replace('/', '')


grf95_ct_frac.df_commutation_table_frac().to_excel(excel_writer=name + '_comm' + '.xlsx', sheet_name=name,
                                                    index=False, freeze_panes=(1, 1))


# Compare Whole Life Annuitie Due
wlad = tv7377_ct_frac.Nx_frac[:-1] / tv7377_ct_frac.Dx_frac[:-1]
wlad_test = []
for x in tv7377_ct_frac.ages:
    time_to_to = int((tv7377_ct_frac.w + 1 - x) * tv7377_ct_frac.frac)
    p = [tv7377_ct_frac.npx(x=x, n=h / tv7377_ct_frac.frac, method='udd') *
         tv7377_ct_frac.v ** (h / tv7377_ct_frac.frac)
         for h in range(time_to_to)]
    wlad_test.append(sum(p))
wlad_test = np.array(wlad_test)
dif_wlad_test = np.sum(np.abs(wlad - wlad_test[:-1]))

# Compare Whole Life Insurance
wli = tv7377_ct_frac.Mx_frac[:-1] / tv7377_ct_frac.Dx_frac[:-1]
wli_test = []
for x in tv7377_ct_frac.ages:
    time_to_to = int((tv7377_ct_frac.w + 1 - x) * tv7377_ct_frac.frac)
    p = [tv7377_ct_frac.npx(x=x, n=h / tv7377_ct_frac.frac, method='udd') *
         tv7377_ct_frac.nqx(x=x + h / tv7377_ct_frac.frac, n=1 / tv7377_ct_frac.frac, method='udd') *
         tv7377_ct_frac.v ** (h / tv7377_ct_frac.frac + 1 / tv7377_ct_frac.frac)
         for h in range(time_to_to)]
    wli_test.append(sum(p))
wli_test = np.array(wli_test)
dif_wli_test = np.sum(np.abs(wli - wli_test[:-1]))
