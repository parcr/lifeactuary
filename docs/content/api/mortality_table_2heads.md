# Two Lives Mortality Tables

Mortality table operations for two-life scenarios with joint-life and last-survivor functionality.

::: lifeActuary.mortality_table_2heads

## Overview

The mortality_table_2heads module provides mortality table functionality specifically designed for two-life scenarios. It handles joint-life status (both must survive) and last-survivor status (at least one must survive) calculations, which are essential for spouse benefits, survivor pensions, and joint life insurance.

## Key Concepts

### Joint-Life Status (xy)
- Both lives must survive for the status to continue
- Probabilities are products of individual survival probabilities (assuming independence)
- Used for joint annuities and first-to-die insurance

### Last-Survivor Status (x̄ȳ)
- Status continues until both lives have died  
- At least one life must survive
- Used for survivor benefits and second-to-die insurance

## Basic Two-Life Mortality Functions

### Joint-Life Survival Probabilities

#### `npx_joint(mt1, mt2, x, y, n, method='udd')`
Probability that both (x) and (y) survive n years.

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import mortality_table_2heads

# Create mortality tables for two lives
mt1 = MortalityTable(data_type='q', mt=[0, 0.01, 0.02, 0.05, 0.1, 1.0])  # Male
mt2 = MortalityTable(data_type='q', mt=[0, 0.008, 0.015, 0.04, 0.08, 1.0])  # Female

# Joint survival probabilities
joint_1yr = mortality_table_2heads.npx_joint(mt1, mt2, x=30, y=28, n=1)
joint_10yr = mortality_table_2heads.npx_joint(mt1, mt2, x=30, y=28, n=10)
joint_20yr = mortality_table_2heads.npx_joint(mt1, mt2, x=30, y=28, n=20)

print(f"1-year joint survival: {joint_1yr:.6f}")
print(f"10-year joint survival: {joint_10yr:.6f}")
print(f"20-year joint survival: {joint_20yr:.6f}")

# Verify independence assumption
individual_male_10 = mt1.npx(30, 10)
individual_female_10 = mt2.npx(28, 10)
expected_joint_10 = individual_male_10 * individual_female_10

print(f"Calculated joint: {joint_10yr:.6f}")
print(f"Expected (independence): {expected_joint_10:.6f}")
print(f"Difference: {abs(joint_10yr - expected_joint_10):.8f}")
```

### Last-Survivor Probabilities

#### `npx_last_survivor(mt1, mt2, x, y, n, method='udd')`
Probability that at least one of (x) or (y) survives n years.

```python
# Last-survivor probabilities
last_surv_1yr = mortality_table_2heads.npx_last_survivor(mt1, mt2, x=30, y=28, n=1)
last_surv_10yr = mortality_table_2heads.npx_last_survivor(mt1, mt2, x=30, y=28, n=10)
last_surv_20yr = mortality_table_2heads.npx_last_survivor(mt1, mt2, x=30, y=28, n=20)

print(f"1-year last-survivor: {last_surv_1yr:.6f}")
print(f"10-year last-survivor: {last_surv_10yr:.6f}")
print(f"20-year last-survivor: {last_surv_20yr:.6f}")

# Verify relationship: P(at least one) = P(x) + P(y) - P(both)
calc_last_surv = individual_male_10 + individual_female_10 - joint_10yr
print(f"Calculated last-survivor: {last_surv_10yr:.6f}")
print(f"From formula: {calc_last_surv:.6f}")
print(f"Verification: {abs(last_surv_10yr - calc_last_surv):.8f}")
```

## Mortality Probabilities

### Joint-Life Mortality

#### `nqx_joint(mt1, mt2, x, y, n, method='udd')`
Probability that at least one of (x) or (y) dies within n years.

```python
# Joint mortality (first-to-die probability)
joint_mort_10 = mortality_table_2heads.nqx_joint(mt1, mt2, x=30, y=28, n=10)
print(f"10-year first-to-die probability: {joint_mort_10:.6f}")

# Verify: q_joint = 1 - p_joint
verification = 1 - joint_10yr
print(f"Verification (1 - p_joint): {verification:.6f}")
print(f"Difference: {abs(joint_mort_10 - verification):.8f}")
```

### Last-Survivor Mortality

#### `nqx_last_survivor(mt1, mt2, x, y, n, method='udd')`
Probability that both (x) and (y) die within n years.

```python
# Last-survivor mortality (both die)
both_die_10 = mortality_table_2heads.nqx_last_survivor(mt1, mt2, x=30, y=28, n=10)
print(f"10-year probability both die: {both_die_10:.6f}")

# Verify: q_last_survivor = 1 - p_last_survivor
verification_ls = 1 - last_surv_10yr
print(f"Verification (1 - p_last_survivor): {verification_ls:.6f}")
print(f"Difference: {abs(both_die_10 - verification_ls):.8f}")
```

## Life Expectancy Calculations

### Joint-Life Expectancy

#### `ex_joint(mt1, mt2, x, y, method='udd')`
Complete expectation of joint-life status.

```python
# Joint-life expectancies
joint_ex_30_28 = mortality_table_2heads.ex_joint(mt1, mt2, x=30, y=28)
joint_ex_65_62 = mortality_table_2heads.ex_joint(mt1, mt2, x=65, y=62)

print(f"Joint life expectancy (30,28): {joint_ex_30_28:.2f} years")
print(f"Joint life expectancy (65,62): {joint_ex_65_62:.2f} years")

# Compare with individual expectancies
male_ex_30 = mt1.ex(30)
female_ex_28 = mt2.ex(28)

print(f"Male life expectancy at 30: {male_ex_30:.2f} years")
print(f"Female life expectancy at 28: {female_ex_28:.2f} years")
print(f"Joint expectancy is shorter: {joint_ex_30_28 < min(male_ex_30, female_ex_28)}")
```

### Last-Survivor Expectancy

#### `ex_last_survivor(mt1, mt2, x, y, method='udd')`
Complete expectation of last-survivor status.

```python
# Last-survivor life expectancies
last_surv_ex_30_28 = mortality_table_2heads.ex_last_survivor(mt1, mt2, x=30, y=28)
last_surv_ex_65_62 = mortality_table_2heads.ex_last_survivor(mt1, mt2, x=65, y=62)

print(f"Last-survivor expectancy (30,28): {last_surv_ex_30_28:.2f} years")
print(f"Last-survivor expectancy (65,62): {last_surv_ex_65_62:.2f} years")

# Verify relationship: ex_last_survivor = ex_x + ex_y - ex_joint
relationship_check = male_ex_30 + female_ex_28 - joint_ex_30_28
print(f"From relationship: {relationship_check:.2f} years")
print(f"Difference: {abs(last_surv_ex_30_28 - relationship_check):.4f}")
```

## Practical Applications

### Pension Planning for Couples

```python
# Retirement planning analysis for married couple
husband_age = 65
wife_age = 62

# Life expectancies
husband_ex = mt1.ex(husband_age)
wife_ex = mt2.ex(wife_age)
joint_ex = mortality_table_2heads.ex_joint(mt1, mt2, husband_age, wife_age)
survivor_ex = mortality_table_2heads.ex_last_survivor(mt1, mt2, husband_age, wife_age)

print("Retirement Planning Analysis:")
print(f"Husband's life expectancy: {husband_ex:.1f} years")
print(f"Wife's life expectancy: {wife_ex:.1f} years")
print(f"Joint life expectancy: {joint_ex:.1f} years")
print(f"Survivor expectancy: {survivor_ex:.1f} years")

# Pension payment periods
print(f"\nExpected pension payment periods:")
print(f"Single life (husband): {husband_ex:.1f} years")
print(f"Joint & survivor 100%: {survivor_ex:.1f} years")
print(f"Joint & survivor 50%: Mixed calculation needed")

# Probability wife survives husband
prob_wife_survives = mortality_table_2heads.npx_joint(mt2, mt1, wife_age, husband_age, int(husband_ex))
print(f"Probability wife survives husband: {prob_wife_survives:.3f}")
```

### Life Insurance Needs Analysis

```python
# Life insurance analysis for couple
current_ages = (35, 33)
target_retirement = (65, 62)
years_to_retirement = (30, 29)

# First-to-die insurance need (income replacement)
first_die_prob_10 = mortality_table_2heads.nqx_joint(mt1, mt2, *current_ages, n=10)
first_die_prob_20 = mortality_table_2heads.nqx_joint(mt1, mt2, *current_ages, n=20)
first_die_prob_30 = mortality_table_2heads.nqx_joint(mt1, mt2, *current_ages, n=30)

print("First-to-Die Insurance Analysis:")
print(f"10-year claim probability: {first_die_prob_10:.4f}")
print(f"20-year claim probability: {first_die_prob_20:.4f}")
print(f"30-year claim probability: {first_die_prob_30:.4f}")

# Second-to-die insurance need (estate planning)
both_survive_30 = mortality_table_2heads.npx_joint(mt1, mt2, *current_ages, n=30)
second_die_prob_30 = 1 - both_survive_30

print(f"\nSecond-to-Die Insurance Analysis:")
print(f"Both survive 30 years: {both_survive_30:.4f}")
print(f"At least one dies in 30 years: {second_die_prob_30:.4f}")
```

### Social Security Survivor Benefits

```python
# Social Security survivor benefit analysis
claiming_ages = (67, 65)  # Full retirement ages

# Probability scenarios for survivor benefits
years_in_retirement = 20

# Probability husband dies first, wife survives
husband_dies_wife_survives = (
    mortality_table_2heads.nqx_last_survivor(mt1, mt2, *claiming_ages, n=years_in_retirement) - 
    mortality_table_2heads.nqx_joint(mt1, mt2, *claiming_ages, n=years_in_retirement)
)

# Probability wife dies first, husband survives  
wife_dies_husband_survives = (
    mortality_table_2heads.nqx_last_survivor(mt1, mt2, *claiming_ages, n=years_in_retirement) - 
    mortality_table_2heads.nqx_joint(mt1, mt2, *claiming_ages, n=years_in_retirement)
)

print("Social Security Survivor Analysis:")
print(f"Prob. husband dies first: {husband_dies_wife_survives:.4f}")
print(f"Prob. wife dies first: {wife_dies_husband_survives:.4f}")
print(f"Prob. both survive 20 years: {mortality_table_2heads.npx_joint(mt1, mt2, *claiming_ages, n=years_in_retirement):.4f}")
```

## Age Difference Analysis

### Impact of Age Gaps

```python
# Analyze impact of age differences
base_male_age = 65
age_gaps = [-5, -2, 0, 2, 5, 8]  # Female age relative to male

print("Impact of Age Differences on Joint Life Expectancy:")
print("Age Gap | Joint LE | Male LE | Female LE")
print("-" * 45)

for gap in age_gaps:
    female_age = base_male_age + gap
    if female_age > 0 and female_age <= mt2.w:
        joint_le = mortality_table_2heads.ex_joint(mt1, mt2, base_male_age, female_age)
        male_le = mt1.ex(base_male_age)
        female_le = mt2.ex(female_age)
        
        print(f"{gap:7d} | {joint_le:8.2f} | {male_le:7.2f} | {female_le:9.2f}")
```

## Advanced Features

### Different Mortality Tables

```python
# Using different mortality tables (e.g., male vs. female tables)
# Assuming we have gender-specific tables

def compare_mortality_assumptions():
    """Compare using same vs. different mortality tables"""
    
    # Same table for both
    same_table_joint = mortality_table_2heads.ex_joint(mt1, mt1, 65, 62)
    
    # Different tables
    diff_table_joint = mortality_table_2heads.ex_joint(mt1, mt2, 65, 62)
    
    print("Mortality Table Comparison:")
    print(f"Same table for both: {same_table_joint:.2f} years")
    print(f"Different tables: {diff_table_joint:.2f} years")
    print(f"Difference: {abs(diff_table_joint - same_table_joint):.2f} years")

compare_mortality_assumptions()
```

### Dependent vs. Independent Lives

```python
# Demonstration of independence assumption
def show_independence_impact():
    """Show impact of independence assumption"""
    
    x, y, n = 30, 28, 10
    
    # Independent calculation (standard)
    independent_joint = mortality_table_2heads.npx_joint(mt1, mt2, x, y, n)
    
    # If we had dependence (illustration only)
    # Positive dependence would increase joint survival
    correlation_factor = 1.05  # 5% positive correlation illustration
    dependent_joint = min(independent_joint * correlation_factor, 1.0)
    
    print("Independence vs. Dependence (Illustration):")
    print(f"Independent: {independent_joint:.6f}")
    print(f"Dependent (+5%): {dependent_joint:.6f}")
    print(f"Impact: {(dependent_joint/independent_joint - 1)*100:.2f}%")

show_independence_impact()
```

## Validation and Testing

### Mathematical Relationships

```python
# Verify key mathematical relationships
x, y, n = 30, 28, 10

# Get all probabilities
p_x = mt1.npx(x, n)
p_y = mt2.npx(y, n)
p_xy = mortality_table_2heads.npx_joint(mt1, mt2, x, y, n)
p_xy_bar = mortality_table_2heads.npx_last_survivor(mt1, mt2, x, y, n)

# Verify relationships
print("Mathematical Relationship Verification:")
print(f"P_x: {p_x:.6f}")
print(f"P_y: {p_y:.6f}")
print(f"P_xy: {p_xy:.6f}")
print(f"P_xy_bar: {p_xy_bar:.6f}")

# Relationship 1: P_xy = P_x * P_y (independence)
rel1_error = abs(p_xy - (p_x * p_y))
print(f"Independence check error: {rel1_error:.8f}")

# Relationship 2: P_xy_bar = P_x + P_y - P_xy
rel2_calc = p_x + p_y - p_xy
rel2_error = abs(p_xy_bar - rel2_calc)
print(f"Last-survivor formula error: {rel2_error:.8f}")

# Relationship 3: P_xy + Q_xy_bar = 1 (where Q is mortality)
q_xy_bar = mortality_table_2heads.nqx_last_survivor(mt1, mt2, x, y, n)
rel3_calc = p_xy_bar + q_xy_bar
rel3_error = abs(rel3_calc - 1.0)
print(f"Probability sum error: {rel3_error:.8f}")
```

## Usage Tips

1. **Independence Assumption**: Standard calculations assume independent mortality
2. **Age Differences**: Common in spouse scenarios (husband typically older)
3. **Gender Differences**: Use appropriate mortality tables for each life
4. **Validation**: Always verify using mathematical relationships
5. **Applications**: Essential for pension design and life insurance
6. **Computational Efficiency**: Pre-calculate common age combinations
7. **Edge Cases**: Handle cases where ages exceed table limits gracefully