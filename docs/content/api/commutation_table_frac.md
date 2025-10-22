# Commutation Tables (Fractional)

Advanced commutation functions supporting fractional ages and payment frequencies.

::: lifeActuary.commutation_table_frac

## Overview

The commutation_table_frac module extends traditional commutation functions to handle fractional ages and fractional payment frequencies. This provides more precise calculations for real-world scenarios where ages and payment times are not restricted to integer values.

## Key Features

- **Fractional Ages**: Calculations for any fractional age (e.g., 30.5, 45.25)
- **Fractional Payments**: Support for monthly, quarterly, and other payment frequencies
- **Enhanced Precision**: More accurate calculations for intermediate time points
- **Continuous Limits**: Approximations for continuous payment streams

## Basic Fractional Commutation Functions

### Fractional Commutation Symbols

#### Class: `CommutationFunctionsFrac(i, g=0, data_type='q', mt=None, perc=100, fraction=12)`

```python
from lifeActuary.commutation_table_frac import CommutationFunctionsFrac

# Create fractional commutation table with monthly divisions
qx_values = [0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 1.0]

ct_frac = CommutationFunctionsFrac(
    i=5,          # 5% annual interest
    g=0,          # No benefit growth
    data_type='q', 
    mt=qx_values,
    fraction=12   # Monthly calculations
)

# Access fractional commutation values
print(f"D_30: {ct_frac.Dx(30):.6f}")
print(f"D_30.5: {ct_frac.Dx(30.5):.6f}")  # Mid-year value
print(f"N_30: {ct_frac.Nx(30):.6f}")
print(f"C_30.25: {ct_frac.Cx(30.25):.6f}")  # Quarterly point
```

### Enhanced Precision Calculations

```python
# Compare standard vs. fractional precision
from lifeActuary.commutation_table import CommutationFunctions

# Standard annual commutation table
ct_annual = CommutationFunctions(i=5, data_type='q', mt=qx_values)

# Fractional commutation table
ct_monthly = CommutationFunctionsFrac(i=5, data_type='q', mt=qx_values, fraction=12)

# Compare annuity calculations
annual_annuity = ct_annual.Nx[30] / ct_annual.Dx[30]
monthly_annuity = ct_monthly.Nx(30) / ct_monthly.Dx(30)

print(f"Annual calculation: {annual_annuity:.6f}")
print(f"Monthly calculation: {monthly_annuity:.6f}")
print(f"Difference: {monthly_annuity - annual_annuity:.6f}")
```

## Fractional Age Applications

### Mid-Year Policy Issues

```python
# Insurance issued at mid-year
issue_age = 35.5  # Age 35 and 6 months
term_years = 20

# Calculate insurance values at fractional age
whole_life_frac = ct_frac.Mx(issue_age) / ct_frac.Dx(issue_age)
term_insurance_frac = (ct_frac.Mx(issue_age) - ct_frac.Mx(issue_age + term_years)) / ct_frac.Dx(issue_age)

print(f"Whole life insurance at age {issue_age}: {whole_life_frac:.6f}")
print(f"{term_years}-year term at age {issue_age}: {term_insurance_frac:.6f}")

# Compare with integer ages
whole_life_35 = ct_frac.Mx(35) / ct_frac.Dx(35)
whole_life_36 = ct_frac.Mx(36) / ct_frac.Dx(36)

print(f"Whole life at age 35: {whole_life_35:.6f}")
print(f"Whole life at age 36: {whole_life_36:.6f}")
print(f"Fractional interpolation accurate: {whole_life_35 > whole_life_frac > whole_life_36}")
```

### Quarterly Premium Calculations

```python
# Calculate quarterly premiums
coverage_amount = 100000
quarterly_frequency = 4

# EPV of quarterly-paid insurance
quarterly_insurance = ct_frac.Mx(30) / ct_frac.Dx(30) * coverage_amount

# EPV of quarterly premium annuity
quarterly_annuity = ct_frac.Nx(30) / ct_frac.Dx(30)

# Adjust for quarterly payment frequency
quarterly_premium = quarterly_insurance / (quarterly_annuity / quarterly_frequency)

print(f"Quarterly premium: ${quarterly_premium:.2f}")
print(f"Annual equivalent: ${quarterly_premium * quarterly_frequency:.2f}")
```

## Advanced Fractional Calculations

### Variable Payment Timing

```python
# Calculate values for irregular payment timing
payment_times = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5]  # Irregular schedule

def custom_annuity_value(ct, x, payment_times, annual_benefit):
    """Calculate annuity with custom payment timing"""
    total_pv = 0
    for t in payment_times:
        if x + t <= ct.w:  # Within mortality table range
            survival_discount = ct.Dx(x + t) / ct.Dx(x)
            payment_pv = annual_benefit * survival_discount
            total_pv += payment_pv
    return total_pv

custom_value = custom_annuity_value(ct_frac, 30, payment_times, 10000)
print(f"Custom timing annuity value: ${custom_value:.2f}")
```

### Continuous Payment Approximation

```python
# Approximate continuous payments using fine divisions
fine_fraction = 365  # Daily calculations

ct_daily = CommutationFunctionsFrac(
    i=5, data_type='q', mt=qx_values, fraction=fine_fraction
)

# Very frequent payment approximation
daily_annuity = ct_daily.Nx(30) / ct_daily.Dx(30)
print(f"Daily payment approximation: {daily_annuity:.6f}")

# Theoretical continuous limit
# For comparison with analytical continuous formulas
from lifeActuary import annuities
discrete_annual = annuities.ax(ct_annual.mt, x=30, i=5)
print(f"Annual discrete: {discrete_annual:.6f}")
print(f"Daily approximation: {daily_annuity:.6f}")
print(f"Continuous effect: {daily_annuity - discrete_annual:.6f}")
```

## Practical Applications

### Universal Life Insurance

```python
# Universal life with flexible premiums and fractional calculations
policy_age = 40.25  # Policy issued quarterly
target_premium = 2500  # Annual target
admin_frequency = 12   # Monthly administration

# Cost of insurance calculation
monthly_coi_rate = ct_frac.Cx(policy_age + 1/12) / ct_frac.Dx(policy_age)
annual_coi_rate = ct_frac.Mx(policy_age) / ct_frac.Dx(policy_age)

print(f"Monthly COI rate: {monthly_coi_rate:.8f}")
print(f"Annual COI rate: {annual_coi_rate:.6f}")
print(f"Ratio: {monthly_coi_rate * 12 / annual_coi_rate:.4f}")

# Premium allocation with monthly deductions
monthly_premium = target_premium / 12
monthly_cost = coverage_amount * monthly_coi_rate
net_to_account = monthly_premium - monthly_cost

print(f"Monthly premium: ${monthly_premium:.2f}")
print(f"Monthly cost: ${monthly_cost:.2f}")
print(f"Net to account: ${net_to_account:.2f}")
```

### Pension Calculations with Fractional Service

```python
# Pension calculation with fractional years of service
entry_age = 25.75   # Started mid-year
retirement_age = 65
service_years = retirement_age - entry_age  # Fractional service

# Final average salary pension
final_salary = 75000
benefit_rate = 0.02  # 2% per year of service
annual_pension = final_salary * benefit_rate * service_years

# Present value of pension
pension_annuity_factor = ct_frac.Nx(retirement_age) / ct_frac.Dx(entry_age)
pension_present_value = annual_pension * pension_annuity_factor

print(f"Service years: {service_years:.2f}")
print(f"Annual pension: ${annual_pension:,.2f}")
print(f"Present value: ${pension_present_value:,.2f}")
```

### Group Insurance with Staggered Entries

```python
# Group insurance with members entering throughout the year
group_members = [
    {'age': 28.25, 'coverage': 50000},
    {'age': 32.75, 'coverage': 75000},
    {'age': 45.5, 'coverage': 100000},
    {'age': 38.1, 'coverage': 60000}
]

total_premium = 0
for member in group_members:
    age = member['age']
    coverage = member['coverage']
    
    # Insurance premium using fractional age
    insurance_rate = ct_frac.Mx(age) / ct_frac.Dx(age)
    member_premium = coverage * insurance_rate
    
    total_premium += member_premium
    print(f"Age {age:5.2f}: ${member_premium:8.2f} for ${coverage:,} coverage")

print(f"Total group premium: ${total_premium:,.2f}")
```

## Computational Considerations

### Memory and Performance

```python
# Compare computational requirements
import time

# Timing comparison
start_time = time.time()
for i in range(1000):
    value = ct_annual.Nx[30] / ct_annual.Dx[30]
annual_time = time.time() - start_time

start_time = time.time()
for i in range(1000):
    value = ct_frac.Nx(30) / ct_frac.Dx(30)
fractional_time = time.time() - start_time

print(f"Annual table: {annual_time:.6f} seconds")
print(f"Fractional table: {fractional_time:.6f} seconds")
print(f"Speed ratio: {fractional_time/annual_time:.2f}x")
```

### Accuracy vs. Performance Trade-offs

```python
# Compare different fractional divisions
fractions = [1, 4, 12, 52, 365]
test_age = 30

print("Accuracy vs. Performance Analysis:")
print("Fraction | Annuity Value | Computation")
print("-" * 40)

for frac in fractions:
    if frac == 1:
        ct = CommutationFunctions(i=5, data_type='q', mt=qx_values)
        value = ct.Nx[test_age] / ct.Dx[test_age]
    else:
        ct = CommutationFunctionsFrac(i=5, data_type='q', mt=qx_values, fraction=frac)
        value = ct.Nx(test_age) / ct.Dx(test_age)
    
    print(f"{frac:8d} | {value:13.6f} | {'Fast' if frac <= 12 else 'Slow'}")
```

## Validation and Testing

### Consistency Checks

```python
# Verify consistency between annual and fractional methods
test_ages = [25, 30, 35, 40, 50, 60]

print("Consistency Verification:")
print("Age | Annual   | Fractional | Difference")
print("-" * 45)

for age in test_ages:
    if age <= min(len(qx_values)-1, ct_frac.w):
        annual_val = ct_annual.Nx[age] / ct_annual.Dx[age]
        frac_val = ct_frac.Nx(age) / ct_frac.Dx(age)
        diff = abs(frac_val - annual_val)
        
        print(f"{age:3d} | {annual_val:.6f} | {frac_val:.6f} | {diff:.8f}")
```

### Interpolation Accuracy

```python
# Test interpolation accuracy at fractional ages
base_age = 35
frac_age = 35.5

# Linear interpolation expectation
linear_approx = (ct_frac.Dx(35) + ct_frac.Dx(36)) / 2
actual_frac = ct_frac.Dx(35.5)

print(f"D_35: {ct_frac.Dx(35):.6f}")
print(f"D_36: {ct_frac.Dx(36):.6f}")
print(f"D_35.5 (actual): {actual_frac:.6f}")
print(f"D_35.5 (linear): {linear_approx:.6f}")
print(f"Interpolation accuracy: {abs(actual_frac - linear_approx):.8f}")
```

## Usage Tips

1. **Fraction Selection**: Use 12 for monthly, 4 for quarterly calculations
2. **Performance**: Higher fractions require more computation time
3. **Accuracy**: Fractional tables provide better interpolation than linear approximation  
4. **Memory Usage**: Fractional tables use more memory than annual tables
5. **Applications**: Essential for mid-year issues and flexible products
6. **Validation**: Always verify against annual calculations for integer ages
7. **Precision**: Use appropriate precision for the application (monthly often sufficient)