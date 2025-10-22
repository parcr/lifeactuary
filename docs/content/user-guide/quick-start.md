# Quick Start Guide

This guide will get you up and running with lifeActuary quickly. We'll cover the most common use cases and basic patterns.

## Basic Workflow

The typical workflow in lifeActuary follows these steps:

1. **Create a mortality table** from mortality rates
2. **Calculate actuarial values** using the table
3. **Analyze results** and perform comparisons

## Your First Calculation

Let's start with a simple example:

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import annuities

# Step 1: Create a simple mortality table
# Ages 0-4 with mortality rates: 0%, 1%, 2%, 5%, 100%
mortality_rates = [0, 0.01, 0.02, 0.05, 1.0]

mt = MortalityTable(data_type='q', mt=mortality_rates)

# Step 2: Calculate a life annuity
# Immediate whole life annuity for someone age 1 at 5% interest
annuity_value = annuities.ax(mt, x=1, i=5)

print(f"Life annuity value: {annuity_value:.4f}")
```

## Working with Mortality Tables

### Creating Tables from Different Input Types

```python
# From mortality rates (qx)
qx_data = [0, 0.001, 0.002, 0.005, 0.01, 0.02, 1.0]
mt_q = MortalityTable(data_type='q', mt=qx_data)

# From number of survivors (lx)
lx_data = [100000, 99900, 99800, 99500, 99000, 98000, 0]
mt_l = MortalityTable(data_type='l', mt=lx_data)

# From survival probabilities (px)
px_data = [0, 0.999, 0.998, 0.995, 0.99, 0.98, 0.0]
mt_p = MortalityTable(data_type='p', mt=px_data)
```

### Basic Table Operations

```python
# Access survival and mortality probabilities
prob_survive_1yr = mt_q.npx(x=30, n=1)  # 1-year survival from age 30
prob_die_1yr = mt_q.nqx(x=30, n=1)      # 1-year mortality from age 30

print(f"1-year survival probability: {prob_survive_1yr:.6f}")
print(f"1-year mortality probability: {prob_die_1yr:.6f}")
print(f"Sum should be 1.0: {prob_survive_1yr + prob_die_1yr:.6f}")

# Life expectancy
life_expectancy = mt_q.ex(x=30)
print(f"Life expectancy at age 30: {life_expectancy:.2f} years")
```

## Common Actuarial Calculations

### Life Annuities

```python
from lifeActuary import annuities

# Immediate whole life annuity
immediate_annuity = annuities.ax(mt_q, x=30, i=5)

# 20-year temporary annuity
temporary_annuity = annuities.axt(mt_q, x=30, t=20, i=5)

# 10-year deferred annuity
deferred_annuity = annuities.nax(mt_q, x=30, n=10, i=5)

# Monthly payments (m=12)
monthly_annuity = annuities.ax(mt_q, x=30, i=5, m=12)

print(f"Immediate annuity: {immediate_annuity:.4f}")
print(f"20-year temporary: {temporary_annuity:.4f}")
print(f"10-year deferred: {deferred_annuity:.4f}")
print(f"Monthly payments: {monthly_annuity:.4f}")
```

### Life Insurance

```python
from lifeActuary import mortality_insurance

# Whole life insurance
whole_life = mortality_insurance.Ax(mt_q, x=30, i=5)

# 20-year term insurance
term_life = mortality_insurance.Axt(mt_q, x=30, t=20, i=5)

# 20-year endowment
endowment = mortality_insurance.Axt_end(mt_q, x=30, t=20, i=5)

print(f"Whole life insurance: {whole_life:.4f}")
print(f"20-year term: {term_life:.4f}")
print(f"20-year endowment: {endowment:.4f}")

# Verify fundamental relationship: Ax + ax ≈ 1
total = whole_life + immediate_annuity
print(f"Ax + ax = {total:.6f} (should be ≈ 1.0)")
```

## Realistic Example: Retirement Planning

Let's work through a practical retirement planning scenario:

```python
# Retirement planning for a 30-year-old
current_age = 30
retirement_age = 65
interest_rate = 4  # 4% annual return

# Create a more realistic mortality table
# This is a simplified version - in practice, use SOA tables
realistic_qx = [0] + [0.001 * (1.08 ** (i-20)) for i in range(1, 81)] + [1.0]
mt_realistic = MortalityTable(data_type='q', mt=realistic_qx)

# Survival to retirement
survival_to_retirement = mt_realistic.npx(current_age, retirement_age - current_age)
print(f"Probability of surviving to retirement: {survival_to_retirement:.4f}")

# Life expectancy at retirement
retirement_life_expectancy = mt_realistic.ex(retirement_age)
print(f"Life expectancy at retirement: {retirement_life_expectancy:.1f} years")

# Retirement annuity value
retirement_annuity = annuities.ax(mt_realistic, x=retirement_age, i=interest_rate)
print(f"$1 retirement annuity value: {retirement_annuity:.4f}")

# How much needed for $50,000 annual retirement income
target_income = 50000
required_capital = target_income / retirement_annuity
print(f"Capital needed for ${target_income:,} annual income: ${required_capital:,.0f}")

# Required annual savings
years_to_retirement = retirement_age - current_age
from lifeActuary import annuities_certain
savings_annuity = annuities_certain.future_value_annuity(n=years_to_retirement, i=interest_rate)
annual_savings = required_capital / savings_annuity
print(f"Required annual savings: ${annual_savings:,.0f}")
```

## Working with Two Lives

```python
from lifeActuary import life_2heads

# Create mortality tables for husband and wife
mt_male = MortalityTable(data_type='q', mt=realistic_qx)
mt_female = MortalityTable(data_type='q', mt=[x * 0.8 for x in realistic_qx])  # Lower female mortality

husband_age = 67
wife_age = 64

# Joint life annuity (pays while both alive)
joint_annuity = life_2heads.ax_2heads(mt_male, mt_female, husband_age, wife_age, i=4)

# Last survivor annuity (pays until both die)
survivor_annuity = life_2heads.ax_2heads_ls(mt_male, mt_female, husband_age, wife_age, i=4)

# Individual annuities
husband_annuity = annuities.ax(mt_male, x=husband_age, i=4)
wife_annuity = annuities.ax(mt_female, x=wife_age, i=4)

print(f"Husband individual annuity: {husband_annuity:.4f}")
print(f"Wife individual annuity: {wife_annuity:.4f}")
print(f"Joint life annuity: {joint_annuity:.4f}")
print(f"Last survivor annuity: {survivor_annuity:.4f}")

# Pension option comparison
pension_amount = 60000
print(f"\nPension Options for ${pension_amount:,} base benefit:")
print(f"Single life: ${pension_amount:,}")
print(f"50% joint survivor: ${pension_amount * 0.5 / joint_annuity * husband_annuity:,.0f}")
print(f"100% joint survivor: ${pension_amount / survivor_annuity * husband_annuity:,.0f}")
```

## Using SOA Tables

```python
# Example of loading and using SOA mortality tables
# (Assumes you have downloaded the soa_tables folder)

from soa_tables.read_soa_table_xml import SoaTable

# Load a standard mortality table
try:
    cso_table = SoaTable('soa_tables/CSO_1941.xml')
    mt_cso = MortalityTable(data_type='q', mt=cso_table.qx)
    
    # Use the professional table
    annuity_cso = annuities.ax(mt_cso, x=30, i=5)
    print(f"CSO 1941 annuity value: {annuity_cso:.4f}")
    
except FileNotFoundError:
    print("SOA tables not found. Download from GitHub repository.")
```

## Common Patterns and Tips

### Interest Rate Sensitivity Analysis

```python
# Analyze how annuity values change with interest rates
rates = [2, 3, 4, 5, 6, 7, 8]
age = 65

print("Interest Rate Sensitivity:")
print("Rate | Annuity Value | % Change")
print("-" * 35)

base_rate = 5
base_value = annuities.ax(mt_realistic, x=age, i=base_rate)

for rate in rates:
    value = annuities.ax(mt_realistic, x=age, i=rate)
    pct_change = (value / base_value - 1) * 100
    print(f"{rate:3d}% | {value:11.4f} | {pct_change:7.1f}%")
```

### Age Sensitivity Analysis

```python
# How annuity values change by age
ages = list(range(50, 81, 5))
rate = 5

print("Age Sensitivity:")
print("Age | Annuity Value | Life Expectancy")
print("-" * 40)

for age in ages:
    if age <= mt_realistic.w:
        value = annuities.ax(mt_realistic, x=age, i=rate)
        life_exp = mt_realistic.ex(age)
        print(f"{age:2d}  | {value:11.4f} | {life_exp:13.1f}")
```

### Payment Frequency Comparison

```python
# Compare different payment frequencies
frequencies = [1, 2, 4, 12, 52]  # Annual, semi-annual, quarterly, monthly, weekly
age = 65
rate = 5

print("Payment Frequency Analysis:")
print("Frequency | Description | Annuity Value | vs Annual")
print("-" * 55)

annual_value = annuities.ax(mt_realistic, x=age, i=rate, m=1)

for m in frequencies:
    value = annuities.ax(mt_realistic, x=age, i=rate, m=m)
    ratio = value / annual_value
    descriptions = {1: "Annual", 2: "Semi-annual", 4: "Quarterly", 12: "Monthly", 52: "Weekly"}
    
    print(f"{m:8d}  | {descriptions[m]:11} | {value:11.4f} | {ratio:7.4f}")
```

## Error Handling and Validation

```python
# Always validate your inputs
def safe_annuity_calculation(mt, x, i, **kwargs):
    """Safely calculate annuity with error checking"""
    try:
        # Check age is within table range
        if x < 0 or x > mt.w:
            raise ValueError(f"Age {x} outside table range [0, {mt.w}]")
        
        # Check interest rate is reasonable
        if i <= 0 or i > 20:
            raise ValueError(f"Interest rate {i}% seems unreasonable")
        
        result = annuities.ax(mt, x=x, i=i, **kwargs)
        
        # Validate result
        if result <= 0 or result > 50:
            print(f"Warning: Unusual annuity value {result:.4f}")
        
        return result
        
    except Exception as e:
        print(f"Error calculating annuity: {e}")
        return None

# Example usage
value = safe_annuity_calculation(mt_realistic, x=65, i=5)
if value:
    print(f"Safely calculated annuity: {value:.4f}")
```

## Next Steps

Now that you understand the basics:

1. **Explore the [Tutorials](tutorials.md)** for more detailed examples
2. **Check the [API Reference](../api/mortality_table.md)** for complete function documentation
3. **Try the [Examples](../examples/basic.md)** for practical applications
4. **Experiment** with your own mortality tables and scenarios

## Quick Reference

### Essential Imports
```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import annuities, mortality_insurance, life_2heads
```

### Key Functions
- `MortalityTable()` - Create mortality tables
- `annuities.ax()` - Immediate life annuity
- `mortality_insurance.Ax()` - Whole life insurance
- `mt.ex()` - Life expectancy
- `mt.npx()` - Survival probability

### Remember
- Interest rates as percentages (5 for 5%, not 0.05)
- First parameter is always the mortality table
- Age parameters can be fractional
- Use `method='udd'` for uniform distribution of deaths (default)