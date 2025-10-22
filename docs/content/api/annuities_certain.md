# Annuities Certain

Financial mathematics functions for annuities certain (annuities without life contingencies).

::: lifeActuary.annuities_certain

## Overview

Annuities certain are series of payments that are guaranteed to be made regardless of survival. These form the foundation of financial mathematics and are used in both life insurance and pure financial calculations.

## Key Functions

### Immediate Annuity Certain

#### `annuity_certain(n, i, m=1, g=0)`
Present value of an immediate annuity certain with n payments.

**Parameters:**
- `n`: Number of payment periods
- `i`: Interest rate per period (as percentage)
- `m`: Payment frequency per period
- `g`: Growth rate per period (as percentage)

```python
from lifeActuary import annuities_certain

# 20-year immediate annuity at 5% interest
pv = annuities_certain.annuity_certain(n=20, i=5)
print(f"Present value: {pv:.4f}")

# Monthly payments
pv_monthly = annuities_certain.annuity_certain(n=20, i=5, m=12)
print(f"Monthly payments PV: {pv_monthly:.4f}")

# Growing at 2% per year
pv_growing = annuities_certain.annuity_certain(n=20, i=5, g=2)
print(f"Growing annuity PV: {pv_growing:.4f}")
```

### Annuity Due Certain

#### `annuity_due_certain(n, i, m=1, g=0)`
Present value of an annuity due certain (payments at beginning of periods).

```python
# Annuity due vs. immediate annuity
pv_immediate = annuities_certain.annuity_certain(n=20, i=5)
pv_due = annuities_certain.annuity_due_certain(n=20, i=5)

print(f"Immediate: {pv_immediate:.4f}")
print(f"Due: {pv_due:.4f}")
print(f"Ratio: {pv_due/pv_immediate:.4f}")  # Should be (1 + i)
```

### Deferred Annuity Certain

#### `deferred_annuity_certain(n, k, i, m=1, g=0)`
Present value of a k-year deferred, n-payment annuity certain.

```python
# 5-year deferred, 15-payment annuity
pv_deferred = annuities_certain.deferred_annuity_certain(n=15, k=5, i=5)
print(f"Deferred annuity PV: {pv_deferred:.4f}")
```

## Perpetuities

### Immediate Perpetuity

#### `perpetuity(i, m=1, g=0)`
Present value of a perpetual annuity.

```python
# Immediate perpetuity at 5%
pv_perp = annuities_certain.perpetuity(i=5)
print(f"Perpetuity PV: {pv_perp:.4f}")  # Should be 20.0

# Growing perpetuity at 2% per year
pv_grow_perp = annuities_certain.perpetuity(i=5, g=2)
print(f"Growing perpetuity PV: {pv_grow_perp:.4f}")
```

### Deferred Perpetuity

#### `deferred_perpetuity(k, i, m=1, g=0)`
Present value of a k-year deferred perpetuity.

```python
# 10-year deferred perpetuity
pv_def_perp = annuities_certain.deferred_perpetuity(k=10, i=5)
print(f"Deferred perpetuity PV: {pv_def_perp:.4f}")
```

## Future Value Functions

### Future Value of Annuity

#### `future_value_annuity(n, i, m=1, g=0)`
Future value of an immediate annuity certain.

```python
# Future value of 20-year annuity
fv = annuities_certain.future_value_annuity(n=20, i=5)
print(f"Future value: {fv:.4f}")
```

## Practical Examples

### Loan Calculations

```python
# Calculate loan payment for given present value
principal = 100000  # Loan amount
years = 30
rate = 6

# Present value factor for 30 years at 6%
pv_factor = annuities_certain.annuity_certain(n=years, i=rate)
monthly_payment = principal / pv_factor
print(f"Annual payment: ${monthly_payment:,.2f}")

# For monthly payments
pv_factor_monthly = annuities_certain.annuity_certain(n=years, i=rate, m=12)
monthly_payment = principal / pv_factor_monthly
print(f"Monthly payment: ${monthly_payment:.2f}")
```

### Retirement Planning

```python
# How much to save annually to accumulate target amount
target_amount = 1000000  # $1M retirement goal
saving_years = 30
return_rate = 7

# Future value factor
fv_factor = annuities_certain.future_value_annuity(n=saving_years, i=return_rate)
annual_savings = target_amount / fv_factor
print(f"Required annual savings: ${annual_savings:,.2f}")
```

### Growing Annuity Applications

```python
# Retirement income with inflation protection
initial_income = 50000  # First year income
inflation = 3  # 3% annual inflation
discount_rate = 6
years = 25

# Present value of growing annuity
pv_real_income = initial_income * annuities_certain.annuity_certain(
    n=years, i=discount_rate, g=inflation
)
print(f"PV of inflation-adjusted income: ${pv_real_income:,.2f}")
```

## Mathematical Relationships

### Standard Formulas

The functions implement these standard formulas:

**Immediate Annuity:**
```
a_n = (1 - v^n) / i
```

**Annuity Due:**
```
ä_n = (1 - v^n) / d
```

**Growing Annuity:**
```
(Ia)_n = [a_n - nv^n] / i  (when g = i)
```

**Perpetuity:**
```
a_∞ = 1 / i
```

### Verification Examples

```python
# Verify mathematical relationships
n, i = 20, 5

# Relationship between immediate and due
immediate = annuities_certain.annuity_certain(n=n, i=i)
due = annuities_certain.annuity_due_certain(n=n, i=i)
print(f"Due / Immediate: {due/immediate:.6f}")  # Should equal 1.05

# Relationship to present value
v = 1 / (1 + i/100)
manual_calc = (1 - v**n) / (i/100)
print(f"Formula check: {abs(immediate - manual_calc):.8f}")  # Should be ~0
```

## Usage Tips

1. **Interest Rates**: Specify as percentages (5 for 5%, not 0.05)
2. **Payment Timing**: Use annuity_certain for end-of-period, annuity_due_certain for beginning
3. **Growth Rates**: For inflation-adjusted calculations
4. **Frequency**: m=12 for monthly, m=4 for quarterly payments
5. **Verification**: Use mathematical relationships to verify calculations