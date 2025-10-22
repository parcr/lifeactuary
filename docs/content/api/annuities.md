# Life Annuities

The annuities module provides comprehensive functions for calculating the present value of various types of life annuities, including immediate, deferred, temporary, and growing annuities.

::: lifeActuary.annuities

## Key Functions

### Immediate Whole Life Annuities

#### `ax(mt, x, i=None, g=0, m=1, method='udd')`
Returns the actuarial present value of an immediate whole life annuity.

**Parameters:**
- `mt`: Mortality table for life x
- `x`: Age at the beginning of the annuity
- `i`: Technical interest rate (percentage, e.g., 5 for 5%)
- `g`: Growth rate (percentage, e.g., 2 for 2%)
- `m`: Frequency of payments per year
- `method`: Interpolation method ('udd', 'cfm', 'bal')

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import annuities

# Create mortality table
mt = MortalityTable(data_type='q', mt=[0, 0.01, 0.02, 0.03, 1.0])

# Immediate whole life annuity at 5% interest
annuity_value = annuities.ax(mt, x=30, i=5)
print(f"Immediate whole life annuity: {annuity_value:.4f}")

# With monthly payments
monthly_annuity = annuities.ax(mt, x=30, i=5, m=12)
print(f"Monthly payment annuity: {monthly_annuity:.4f}")

# With 2% annual growth
growing_annuity = annuities.ax(mt, x=30, i=5, g=2)
print(f"Growing annuity (2% p.a.): {growing_annuity:.4f}")
```

### Deferred Whole Life Annuities

#### `nax(mt, x, n, i=None, g=0, m=1, method='udd')`
Returns the present value of an n-year deferred whole life annuity.

```python
# 10-year deferred whole life annuity
deferred_annuity = annuities.nax(mt, x=30, n=10, i=5)
print(f"10-year deferred annuity: {deferred_annuity:.4f}")
```

### Temporary Life Annuities

#### `axt(mt, x, t, i=None, g=0, m=1, method='udd')`
Returns the present value of a temporary life annuity for t years.

```python
# 20-year temporary annuity
temp_annuity = annuities.axt(mt, x=30, t=20, i=5)
print(f"20-year temporary annuity: {temp_annuity:.4f}")
```

#### `naxt(mt, x, n, t, i=None, g=0, m=1, method='udd')`
Returns the present value of an n-year deferred, t-year temporary annuity.

```python
# 5-year deferred, 15-year temporary annuity
def_temp_annuity = annuities.naxt(mt, x=30, n=5, t=15, i=5)
print(f"5|15 annuity: {def_temp_annuity:.4f}")
```

### Due Annuities

Functions ending with `_due` calculate annuities-due (payments at the beginning of periods):

```python
# Immediate whole life annuity-due
annuity_due = annuities.ax_due(mt, x=30, i=5)

# Temporary annuity-due
temp_annuity_due = annuities.axt_due(mt, x=30, t=20, i=5)
```

## Advanced Features

### Fractional Payment Frequencies

All annuity functions support fractional payment frequencies:

```python
# Quarterly payments (m=4)
quarterly = annuities.ax(mt, x=30, i=5, m=4)

# Monthly payments (m=12) 
monthly = annuities.ax(mt, x=30, i=5, m=12)

# Weekly payments (m=52)
weekly = annuities.ax(mt, x=30, i=5, m=52)
```

### Growing Annuities

Support for geometrically increasing payments:

```python
# Annuity growing at 3% per year
growing = annuities.ax(mt, x=30, i=5, g=3)

# Deferred growing annuity
def_growing = annuities.nax(mt, x=30, n=10, i=5, g=2)
```

### Generic Annuity Function

#### `annuity_x(mt, x, x_first, x_last, i=None, g=0, m=1, method='udd')`
Computes a general annuity with flexible start and end ages:

```python
# Annuity starting at age 35, ending at age 65
custom_annuity = annuities.annuity_x(
    mt, x=30, x_first=35, x_last=65, i=5, g=2, m=12
)
```

## Complete Function List

### Immediate Annuities
- `ax()` - Immediate whole life annuity
- `ax_due()` - Immediate whole life annuity-due  
- `axt()` - Temporary annuity
- `axt_due()` - Temporary annuity-due

### Deferred Annuities
- `nax()` - Deferred whole life annuity
- `nax_due()` - Deferred whole life annuity-due
- `naxt()` - Deferred temporary annuity  
- `naxt_due()` - Deferred temporary annuity-due

### Special Functions
- `annuity_x()` - Generic annuity with custom payment period
- Various utility functions for specific actuarial calculations

## Usage Tips

1. **Interest Rates**: Always specify as percentages (use 5 for 5%, not 0.05)
2. **Payment Frequency**: Use m=1 for annual, m=12 for monthly, etc.
3. **Growth Rates**: Specified as percentages, applied geometrically
4. **Methods**: 'udd' is most common, 'cfm' for constant force, 'bal' for Balducci
5. **Age Inputs**: Can be fractional (e.g., 30.5 for age 30 and 6 months)