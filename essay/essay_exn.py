__author__ = "PedroCR"

from essential_life import mortality_table, read_soa_table_xml as rst

mt_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
mt_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
mt_GRM95 = rst.SoaTable('../soa_tables/GRM95.xml')

lt_tv7377 = mortality_table.MortalityTable(mt=mt_TV7377.table_qx)
lt_gRF95 = mortality_table.MortalityTable(mt=mt_GRF95.table_qx)
lt_gRM95 = mortality_table.MortalityTable(mt=mt_GRM95.table_qx)

x = 20.2
n = 10.5
print(f'x={x}, n={n}, hence, from {x} to {x + n}: {lt_tv7377.exn(x, n, "udd")}')

x = 80.2
n = 10.5
print(f'x={x}, n={n}, hence, from {x} to {x + n}: {lt_tv7377.exn(x, n, "udd")}')

x = 80
n = 10
print(f'x={x}, n={n}, hence, from {x} to {x + n}: {lt_tv7377.exn(x, n, "udd")}')

x = 80
n = 10.2
print(f'x={x}, n={n}, hence, from {x} to {x + n}: {lt_tv7377.exn(x, n, "udd")}')

x = 80.8
n = 10.2
print(f'x={x}, n={n}, hence, from {x} to {x + n}: {lt_tv7377.exn(x, n, "udd")}')

x = 80.8
n = 10.8
print(f'x={x}, n={n}, hence, from {x} to {x + n}: {lt_tv7377.exn(x, n, "udd")}')

x = 80.8
n = 10.8
print(f'x={x}, n={n}, hence, from {x} to {x + n}: {lt_tv7377.exn(x, n, "bal")}')


x = 0
n = 200
print(f'x={x}, n={n}, hence, from {x} to {x + n}: {lt_tv7377.exn(x, n, "bal")}')

''' compare with the approximation from truncated '''
x=lt_tv7377.w
print(f'x={x}: {lt_tv7377.get_integral_px_method(x, "udd")}')
print(f'x={x}: {lt_tv7377.get_integral_px_method(x, "cfm")}')
print(f'x={x}: {lt_tv7377.get_integral_px_method(x, "bal")}')

comp_ex = [(x, lt_tv7377.ex[x], lt_tv7377.exn(x, 200), lt_tv7377.exn(x, 200, 'cfm'), lt_tv7377.exn(x, 200, 'bal'))
               for x in range(lt_tv7377.w + 1)]
