# Life Insurance (Fractional)

Functions for life insurance calculations with fractional payment frequencies and ages.

::: lifeActuary.mortality_insurance_frac

## Overview

The mortality_insurance_frac module extends basic life insurance calculations to handle fractional payment frequencies, fractional ages, and more sophisticated benefit payment patterns. This module is particularly useful for realistic insurance modeling where benefits may be paid more frequently than annually.

## Key Features

- **Fractional Payment Frequencies**: Benefits payable monthly, quarterly, etc.
- **Fractional Ages**: Calculations for non-integer ages
- **Variable Benefit Patterns**: Support for increasing, decreasing, and step-function benefits
- **Continuous Approximations**: Functions for continuous benefit payments

## Basic Fractional Insurance

### Whole Life Insurance with Fractional Benefits

#### `Ax_frac(mt, x, i, m=12, method='udd')`
Whole life insurance with benefits payable m times per year.

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import mortality_insurance_frac

# Create mortality table
mt = MortalityTable(data_type='q', mt=[0, 0.01, 0.02, 0.05, 0.1, 1.0])

# Compare annual vs. monthly benefit payments
annual_benefit = mortality_insurance.Ax(mt, x=30, i=5)
monthly_benefit = mortality_insurance_frac.Ax_frac(mt, x=30, i=5, m=12)

print(f"Annual benefit payment: {annual_benefit:.6f}")
print(f"Monthly benefit payment: {monthly_benefit:.6f}")
print(f"Difference: {monthly_benefit - annual_benefit:.6f}")
```

### Term Insurance with Fractional Benefits

#### `Axt_frac(mt, x, t, i, m=12, method='udd')`
Term life insurance with fractional benefit frequency.

```python
# 20-year term with quarterly benefits
quarterly_term = mortality_insurance_frac.Axt_frac(mt, x=30, t=20, i=5, m=4)
annual_term = mortality_insurance.Axt(mt, x=30, t=20, i=5)

print(f"Quarterly benefit term: {quarterly_term:.6f}")
print(f"Annual benefit term: {annual_term:.6f}")
print(f"Fractional premium: {quarterly_term/annual_term:.4f}")
```

## Continuous Benefit Insurance

### Continuous Whole Life Insurance

#### `Ax_continuous(mt, x, i, method='udd')`
Whole life insurance with continuous benefit payments (theoretical limit as m→∞).

```python
# Compare discrete vs. continuous benefits
continuous = mortality_insurance_frac.Ax_continuous(mt, x=30, i=5)
monthly = mortality_insurance_frac.Ax_frac(mt, x=30, i=5, m=12)
weekly = mortality_insurance_frac.Ax_frac(mt, x=30, i=5, m=52)

print(f"Continuous: {continuous:.6f}")
print(f"Monthly:    {monthly:.6f}")
print(f"Weekly:     {weekly:.6f}")
print(f"Convergence to continuous: {abs(weekly - continuous):.8f}")
```

## Fractional Age Calculations

### Insurance Starting at Fractional Ages

```python
# Insurance starting at age 30.5
fractional_age_insurance = mortality_insurance_frac.Ax_frac(
    mt, x=30.5, i=5, m=12
)

# Compare with integer age
integer_age_insurance = mortality_insurance_frac.Ax_frac(
    mt, x=30, i=5, m=12
)

print(f"Age 30.5: {fractional_age_insurance:.6f}")
print(f"Age 30.0: {integer_age_insurance:.6f}")
```

## Variable Benefit Patterns

### Increasing Benefit Insurance

#### `IAx_frac(mt, x, i, m=12, method='udd')`
Insurance with benefits increasing by 1 each year, paid m times per year.

```python
# Increasing benefit insurance with monthly payments
increasing = mortality_insurance_frac.IAx_frac(mt, x=30, i=5, m=12)
level = mortality_insurance_frac.Ax_frac(mt, x=30, i=5, m=12)

print(f"Increasing benefit: {increasing:.6f}")
print(f"Level benefit: {level:.6f}")
print(f"Premium ratio: {increasing/level:.4f}")
```

### Decreasing Benefit Insurance

#### `DAx_frac(mt, x, i, m=12, method='udd')`
Insurance with benefits decreasing each year.

```python
# Decreasing term insurance (common in mortgage protection)
decreasing = mortality_insurance_frac.DAx_frac(mt, x=30, i=5, m=12)
print(f"Decreasing benefit insurance: {decreasing:.6f}")
```

## Practical Applications

### Monthly Premium Life Insurance

```python
# Realistic life insurance with monthly premiums and benefits
face_amount = 250000  # $250,000 coverage
monthly_rate = 5/12   # Monthly interest rate

# Monthly benefit EPV
monthly_epv = mortality_insurance_frac.Ax_frac(mt, x=35, i=5, m=12)
monthly_premium_factor = face_amount * monthly_epv

print(f"Monthly premium factor: ${monthly_premium_factor:.2f}")

# Compare to annual premium equivalent
annual_epv = mortality_insurance.Ax(mt, x=35, i=5)
annual_premium_factor = face_amount * annual_epv

print(f"Annual premium factor: ${annual_premium_factor:.2f}")
print(f"Monthly/Annual ratio: {monthly_premium_factor/annual_premium_factor:.4f}")
```

### Mortgage Protection Insurance

```python
# Decreasing term insurance to match mortgage balance
initial_mortgage = 300000
mortgage_term = 30
mortgage_rate = 4

# Calculate decreasing benefit pattern
yearly_payment = initial_mortgage * (mortgage_rate/100) / (1 - (1 + mortgage_rate/100)**(-mortgage_term))

# Approximate with decreasing term insurance
decreasing_insurance = mortality_insurance_frac.DAx_frac(
    mt, x=30, i=5, m=12
) * initial_mortgage

print(f"Mortgage protection insurance EPV: ${decreasing_insurance:,.2f}")
```

### Universal Life Insurance

```python
# Flexible premium universal life with fractional calculations
target_premium = 2000  # Annual target
cost_of_insurance_rate = mortality_insurance_frac.Ax_frac(mt, x=40, i=4, m=12)
expense_rate = 0.1  # 10% expense loading

net_premium_rate = cost_of_insurance_rate * (1 + expense_rate)
coverage_per_dollar = 1 / net_premium_rate

print(f"Cost of insurance rate: {cost_of_insurance_rate:.6f}")
print(f"Net premium rate: {net_premium_rate:.6f}")
print(f"Coverage per dollar premium: ${coverage_per_dollar:,.0f}")
```

## Advanced Features

### Benefit Payment Timing

```python
# Compare immediate vs. end-of-period benefit payments
immediate_benefit = mortality_insurance_frac.Ax_immediate_frac(mt, x=30, i=5, m=12)
end_period_benefit = mortality_insurance_frac.Ax_frac(mt, x=30, i=5, m=12)

print(f"Immediate benefit: {immediate_benefit:.6f}")
print(f"End-of-period benefit: {end_period_benefit:.6f}")
print(f"Timing difference: {immediate_benefit - end_period_benefit:.8f}")
```

### Multi-State Benefits

```python
# Insurance with different benefits for different causes
# (requires extended mortality table with cause-specific rates)

# Accidental death benefit (higher payout)
accident_multiplier = 2.0
base_benefit = mortality_insurance_frac.Ax_frac(mt, x=30, i=5, m=12)
accident_benefit = base_benefit * accident_multiplier

print(f"Base insurance: {base_benefit:.6f}")
print(f"With accident benefit: {accident_benefit:.6f}")
```

## Mathematical Relationships

### Fractional Premium Approximations

```python
# Verify fractional premium relationships
m_values = [1, 2, 4, 12, 52, 365]
base_annual = mortality_insurance.Ax(mt, x=30, i=5)

print("Payment Frequency Analysis:")
print("m    | Ax(m)    | Ratio | Approximation")
print("-" * 45)

for m in m_values:
    if m == 1:
        ax_m = base_annual
    else:
        ax_m = mortality_insurance_frac.Ax_frac(mt, x=30, i=5, m=m)
    
    ratio = ax_m / base_annual
    # Linear approximation: Ax(m) ≈ Ax * (1 + (m-1)/(2m) * i)
    approx = 1 + (m-1)/(2*m) * (5/100)
    
    print(f"{m:3d}  | {ax_m:.6f} | {ratio:.4f} | {approx:.4f}")
```

### Convergence to Continuous

```python
# Show convergence to continuous limit
continuous_limit = mortality_insurance_frac.Ax_continuous(mt, x=30, i=5)

frequencies = [12, 26, 52, 104, 365]
print("Convergence to Continuous:")
print("Frequency | Value    | Error")
print("-" * 30)

for freq in frequencies:
    discrete_value = mortality_insurance_frac.Ax_frac(mt, x=30, i=5, m=freq)
    error = abs(discrete_value - continuous_limit)
    print(f"{freq:8d}  | {discrete_value:.6f} | {error:.8f}")
```

## Usage Tips

1. **Payment Frequency**: Higher frequencies increase present values slightly
2. **Continuous Limit**: Use for theoretical calculations or high-frequency approximations
3. **Fractional Ages**: Useful for mid-year policy issues
4. **Variable Benefits**: Match insurance to changing needs (mortgages, income replacement)
5. **Computational Cost**: Fractional calculations are more intensive than annual
6. **Practical Applications**: Most real insurance involves fractional elements
7. **Validation**: Compare with annual calculations for consistency checks