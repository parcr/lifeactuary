# Tutorials

This section provides step-by-step tutorials for common actuarial tasks using lifeActuary.

## Tutorial 1: Building Your First Mortality Table

### Step 1: Understanding Mortality Data

Mortality tables can be created from three types of data:
- **qx**: Mortality rates (probability of death)
- **lx**: Number of survivors
- **px**: Survival rates (probability of survival)

```python
from lifeActuary.mortality_table import MortalityTable
import numpy as np

# Example: Create a simple mortality table
# Let's build a table for ages 0-5 with increasing mortality

# Method 1: Using mortality rates (qx)
qx_data = [
    0,      # Age 0 (placeholder)
    0.001,  # Age 1: 0.1% mortality rate
    0.002,  # Age 2: 0.2% mortality rate  
    0.005,  # Age 3: 0.5% mortality rate
    0.010,  # Age 4: 1.0% mortality rate
    1.000   # Age 5: 100% (terminal age)
]

mt = MortalityTable(data_type='q', mt=qx_data)
print("Mortality table created successfully!")
```

### Step 2: Exploring Your Table

```python
# Access basic properties
print(f"Terminal age: {mt.w}")
print(f"First age: {mt.x0}")

# Get survival probabilities
for age in range(1, 5):
    px_1yr = mt.npx(age, 1)  # 1-year survival probability
    qx_1yr = mt.nqx(age, 1)  # 1-year mortality probability
    print(f"Age {age}: P(survive 1 year) = {px_1yr:.4f}, P(die) = {qx_1yr:.4f}")

# Life expectancy
for age in range(1, 5):
    life_exp = mt.ex(age)
    print(f"Life expectancy at age {age}: {life_exp:.2f} years")
```

### Step 3: Validation

```python
# Verify that probabilities sum to 1
for age in range(1, 5):
    px = mt.npx(age, 1)
    qx = mt.nqx(age, 1)
    total = px + qx
    print(f"Age {age}: px + qx = {total:.6f} {'✓' if abs(total - 1.0) < 1e-6 else '✗'}")
```

## Tutorial 2: Calculating Life Annuities

### Step 1: Basic Immediate Annuity

```python
from lifeActuary import annuities

# Create a more realistic mortality table
ages = list(range(0, 101))
qx_realistic = [0] + [0.0001 * (1.08 ** max(0, i-20)) for i in range(1, 101)]
qx_realistic[-1] = 1.0

mt_real = MortalityTable(data_type='q', mt=qx_realistic)

# Calculate immediate whole life annuity
age = 65
interest_rate = 5  # 5% annual interest

immediate_annuity = annuities.ax(mt_real, x=age, i=interest_rate)
print(f"Immediate whole life annuity at age {age}: {immediate_annuity:.4f}")
print(f"This means $1 per year for life is worth ${immediate_annuity:.2f} today")
```

### Step 2: Different Payment Frequencies

```python
# Compare payment frequencies
frequencies = {
    1: "Annual",
    2: "Semi-annual", 
    4: "Quarterly",
    12: "Monthly"
}

print(f"Payment Frequency Analysis (Age {age}):")
for m, description in frequencies.items():
    annuity_value = annuities.ax(mt_real, x=age, i=interest_rate, m=m)
    print(f"{description:12}: {annuity_value:.4f}")
```

### Step 3: Temporary and Deferred Annuities

```python
# 20-year temporary annuity
temp_annuity = annuities.axt(mt_real, x=age, t=20, i=interest_rate)
print(f"20-year temporary annuity: {temp_annuity:.4f}")

# 5-year deferred annuity
deferred_annuity = annuities.nax(mt_real, x=age, n=5, i=interest_rate)
print(f"5-year deferred annuity: {deferred_annuity:.4f}")

# 5-year deferred, 15-year temporary
def_temp_annuity = annuities.naxt(mt_real, x=age, n=5, t=15, i=interest_rate)
print(f"5-year deferred, 15-year temporary: {def_temp_annuity:.4f}")
```

### Step 4: Growing Annuities

```python
# Annuities with growth
growth_rates = [0, 1, 2, 3]

print(f"Impact of Growth on Annuity Values:")
for g in growth_rates:
    growing_annuity = annuities.ax(mt_real, x=age, i=interest_rate, g=g)
    print(f"Growth rate {g}%: {growing_annuity:.4f}")
```

## Tutorial 3: Life Insurance Calculations

### Step 1: Basic Life Insurance

```python
from lifeActuary import mortality_insurance

# Whole life insurance
whole_life_epv = mortality_insurance.Ax(mt_real, x=age, i=interest_rate)
print(f"Whole life insurance EPV: {whole_life_epv:.4f}")

# Verify the fundamental relationship: Ax + ax ≈ 1
verification = whole_life_epv + immediate_annuity
print(f"Ax + ax = {verification:.6f} (should be close to 1.0)")
```

### Step 2: Term Insurance

```python
# Different term lengths
terms = [10, 20, 30]

print(f"Term Insurance EPVs (Age {age}):")
for term in terms:
    term_epv = mortality_insurance.Axt(mt_real, x=age, t=term, i=interest_rate)
    print(f"{term:2d}-year term: {term_epv:.4f}")
```

### Step 3: Endowment Insurance

```python
# Endowment insurance (pays on death OR survival)
endowment_epv = mortality_insurance.Axt_end(mt_real, x=age, t=20, i=interest_rate)
term_epv = mortality_insurance.Axt(mt_real, x=age, t=20, i=interest_rate)

print(f"20-year term insurance: {term_epv:.4f}")
print(f"20-year endowment: {endowment_epv:.4f}")
print(f"Pure endowment component: {endowment_epv - term_epv:.4f}")
```

## Tutorial 4: Working with Two Lives

### Step 1: Creating Tables for Two Lives

```python
from lifeActuary import life_2heads

# Create male and female mortality tables
# Assume female mortality is 20% lower
qx_male = qx_realistic
qx_female = [q * 0.8 if q < 1.0 else 1.0 for q in qx_realistic]

mt_male = MortalityTable(data_type='q', mt=qx_male)
mt_female = MortalityTable(data_type='q', mt=qx_female)

# Ages for husband and wife
husband_age = 67
wife_age = 64
```

### Step 2: Joint-Life Calculations

```python
# Joint-life probabilities (both must survive)
joint_survival_10 = life_2heads.npx_2heads(mt_male, mt_female, husband_age, wife_age, n=10)
print(f"10-year joint survival probability: {joint_survival_10:.4f}")

# Joint-life annuity
joint_annuity = life_2heads.ax_2heads(mt_male, mt_female, husband_age, wife_age, i=interest_rate)
print(f"Joint-life annuity: {joint_annuity:.4f}")
```

### Step 3: Last-Survivor Calculations

```python
# Last-survivor probabilities (at least one survives)
last_survivor_10 = life_2heads.npx_2heads_ls(mt_male, mt_female, husband_age, wife_age, n=10)
print(f"10-year last-survivor probability: {last_survivor_10:.4f}")

# Last-survivor annuity
survivor_annuity = life_2heads.ax_2heads_ls(mt_male, mt_female, husband_age, wife_age, i=interest_rate)
print(f"Last-survivor annuity: {survivor_annuity:.4f}")
```

### Step 4: Pension Options Analysis

```python
# Individual annuities
husband_annuity = annuities.ax(mt_male, x=husband_age, i=interest_rate)
wife_annuity = annuities.ax(mt_female, x=wife_age, i=interest_rate)

print(f"Pension Option Analysis:")
print(f"Husband only: {husband_annuity:.4f}")
print(f"Wife only: {wife_annuity:.4f}")
print(f"Joint life: {joint_annuity:.4f}")
print(f"Last survivor: {survivor_annuity:.4f}")

# Verify relationship
calculated_survivor = husband_annuity + wife_annuity - joint_annuity
print(f"Calculated survivor (H+W-J): {calculated_survivor:.4f}")
print(f"Direct calculation: {survivor_annuity:.4f}")
print(f"Difference: {abs(survivor_annuity - calculated_survivor):.6f}")
```

## Tutorial 5: Using SOA Mortality Tables

### Step 1: Loading SOA Tables

```python
# Example of loading SOA mortality tables
# Note: You need to download the soa_tables folder from GitHub

try:
    from soa_tables.read_soa_table_xml import SoaTable
    
    # Load CSO 1941 table
    cso_1941 = SoaTable('soa_tables/CSO_1941.xml')
    mt_cso = MortalityTable(data_type='q', mt=cso_1941.qx)
    
    print("Successfully loaded CSO 1941 mortality table")
    print(f"Table covers ages {cso_1941.min_age} to {cso_1941.max_age}")
    
except FileNotFoundError:
    print("SOA tables not found. Please download from GitHub repository.")
    # Use our realistic table instead
    mt_cso = mt_real
    print("Using synthetic table for demonstration")
```

### Step 2: Comparing Different Tables

```python
# Compare annuity values across different tables
test_ages = [30, 40, 50, 60, 70]

print("Annuity Comparison Across Tables:")
print("Age | Synthetic | CSO 1941")
print("-" * 30)

for age in test_ages:
    if age <= mt_real.w and age <= mt_cso.w:
        synthetic_annuity = annuities.ax(mt_real, x=age, i=5)
        cso_annuity = annuities.ax(mt_cso, x=age, i=5)
        
        print(f"{age:2d}  | {synthetic_annuity:8.4f} | {cso_annuity:8.4f}")
```

## Tutorial 6: Practical Application - Retirement Planning

### Step 1: Define the Scenario

```python
# Comprehensive retirement planning example
current_age = 35
retirement_age = 65
current_salary = 80000
salary_growth = 3  # 3% annual salary growth
target_replacement_ratio = 0.8  # 80% income replacement
investment_return = 7  # 7% annual return
inflation = 2.5  # 2.5% inflation
```

### Step 2: Calculate Required Capital

```python
# Final salary at retirement
years_to_retirement = retirement_age - current_age
final_salary = current_salary * (1 + salary_growth/100) ** years_to_retirement
target_income = final_salary * target_replacement_ratio

print(f"Retirement Planning Analysis:")
print(f"Current salary: ${current_salary:,}")
print(f"Final salary: ${final_salary:,.0f}")
print(f"Target retirement income: ${target_income:,.0f}")

# Required capital using life annuity
real_return = ((1 + investment_return/100) / (1 + inflation/100)) - 1
retirement_annuity = annuities.ax(mt_real, x=retirement_age, i=real_return*100)
required_capital = target_income / retirement_annuity

print(f"Real return rate: {real_return*100:.2f}%")
print(f"Retirement annuity factor: {retirement_annuity:.4f}")
print(f"Required capital: ${required_capital:,.0f}")
```

### Step 3: Savings Strategy

```python
from lifeActuary import annuities_certain

# Calculate required annual savings
savings_fv_factor = annuities_certain.future_value_annuity(
    n=years_to_retirement, 
    i=investment_return
)
required_annual_savings = required_capital / savings_fv_factor

print(f"Required annual savings: ${required_annual_savings:,.0f}")
print(f"Required monthly savings: ${required_annual_savings/12:,.0f}")
print(f"Savings rate: {required_annual_savings/current_salary*100:.1f}% of current salary")
```

### Step 4: Sensitivity Analysis

```python
# Test different scenarios
scenarios = [
    {"return": 6, "inflation": 3, "name": "Conservative"},
    {"return": 7, "inflation": 2.5, "name": "Base Case"},
    {"return": 8, "inflation": 2, "name": "Optimistic"}
]

print(f"\nSensitivity Analysis:")
print("Scenario     | Real Return | Required Capital | Annual Savings")
print("-" * 65)

for scenario in scenarios:
    real_ret = ((1 + scenario["return"]/100) / (1 + scenario["inflation"]/100)) - 1
    ret_annuity = annuities.ax(mt_real, x=retirement_age, i=real_ret*100)
    req_capital = target_income / ret_annuity
    
    savings_fv = annuities_certain.future_value_annuity(n=years_to_retirement, i=scenario["return"])
    req_savings = req_capital / savings_fv
    
    print(f"{scenario['name']:12} | {real_ret*100:10.2f}% | ${req_capital:13,.0f} | ${req_savings:12,.0f}")
```

This tutorial structure provides hands-on learning with progressively complex examples. Each tutorial builds on previous concepts while introducing new functionality.