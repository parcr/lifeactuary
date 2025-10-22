# Two Lives Functions

Functions for calculating actuarial values involving two lives, including joint-life and last-survivor scenarios.

::: lifeActuary.life_2heads

## Overview

The life_2heads module provides comprehensive functionality for actuarial calculations involving two lives. This includes joint-life probabilities (both must survive), last-survivor probabilities (at least one survives), and related annuity and insurance calculations.

## Key Concepts

### Joint-Life Status
Both lives must survive for benefits to continue. Denoted as (xy).

### Last-Survivor Status  
Benefits continue until both lives have died. Denoted as (x̄ȳ).

### Independence Assumption
Calculations assume the two lives are independent unless otherwise specified.

## Basic Probability Functions

### Joint-Life Survival

#### `npx_2heads(mt1, mt2, x, y, n, method='udd', dependent=False)`
Probability that both (x) and (y) survive n years.

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import life_2heads

# Create mortality tables for two lives
mt1 = MortalityTable(data_type='q', mt=[0, 0.01, 0.02, 0.05, 1.0])
mt2 = MortalityTable(data_type='q', mt=[0, 0.008, 0.015, 0.04, 1.0])

# Joint survival probability for 10 years
joint_surv = life_2heads.npx_2heads(mt1, mt2, x=30, y=28, n=10)
print(f"10-year joint survival: {joint_surv:.4f}")
```

### Last-Survivor Survival

#### `npx_2heads_ls(mt1, mt2, x, y, n, method='udd', dependent=False)`
Probability that at least one of (x) or (y) survives n years.

```python
# Last-survivor probability for 10 years
last_surv = life_2heads.npx_2heads_ls(mt1, mt2, x=30, y=28, n=10)
print(f"10-year last-survivor: {last_surv:.4f}")

# Verification: P(at least one survives) = 1 - P(both die)
both_die = 1 - life_2heads.npx_2heads(mt1, mt2, x=30, y=28, n=10)
individual_surv1 = mt1.npx(30, 10)
individual_surv2 = mt2.npx(28, 10)
calculated_last_surv = individual_surv1 + individual_surv2 - joint_surv

print(f"Verification: {abs(last_surv - calculated_last_surv):.8f}")
```

## Joint-Life Annuities

### Immediate Joint-Life Annuity

#### `ax_2heads(mt1, mt2, x, y, i, g=0, m=1, method='udd')`
Present value of joint-life annuity (payments while both alive).

```python
# Joint-life immediate annuity
joint_annuity = life_2heads.ax_2heads(mt1, mt2, x=65, y=62, i=5)
print(f"Joint-life annuity: {joint_annuity:.4f}")

# Compare to single life annuities
single_annuity_x = annuities.ax(mt1, x=65, i=5)
single_annuity_y = annuities.ax(mt2, x=62, i=5)
print(f"Single life (x): {single_annuity_x:.4f}")
print(f"Single life (y): {single_annuity_y:.4f}")
print(f"Joint life is lower: {joint_annuity < min(single_annuity_x, single_annuity_y)}")
```

### Temporary Joint-Life Annuity

#### `axt_2heads(mt1, mt2, x, y, t, i, g=0, m=1, method='udd')`
Present value of temporary joint-life annuity.

```python
# 20-year temporary joint-life annuity
temp_joint = life_2heads.axt_2heads(mt1, mt2, x=45, y=42, t=20, i=5)
print(f"20-year temporary joint annuity: {temp_joint:.4f}")
```

## Last-Survivor Annuities

### Immediate Last-Survivor Annuity

#### `ax_2heads_ls(mt1, mt2, x, y, i, g=0, m=1, method='udd')`
Present value of last-survivor annuity (payments until both die).

```python
# Last-survivor immediate annuity
last_surv_annuity = life_2heads.ax_2heads_ls(mt1, mt2, x=65, y=62, i=5)
print(f"Last-survivor annuity: {last_surv_annuity:.4f}")

# Relationship: Last-survivor = Individual annuities - Joint annuity
relationship_check = single_annuity_x + single_annuity_y - joint_annuity
print(f"Relationship check: {abs(last_surv_annuity - relationship_check):.6f}")
```

### Temporary Last-Survivor Annuity

#### `axt_2heads_ls(mt1, mt2, x, y, t, i, g=0, m=1, method='udd')`
Present value of temporary last-survivor annuity.

```python
# 20-year temporary last-survivor annuity
temp_last_surv = life_2heads.axt_2heads_ls(mt1, mt2, x=45, y=42, t=20, i=5)
print(f"20-year temporary last-survivor: {temp_last_surv:.4f}")
```

## Life Insurance for Two Lives

### Joint-Life Insurance

#### `Ax_2heads(mt1, mt2, x, y, i, g=0, method='udd')`
Expected present value of joint-life insurance (pays on first death).

```python
# Joint-life insurance (pays on first death)
joint_insurance = life_2heads.Ax_2heads(mt1, mt2, x=30, y=28, i=5)
print(f"Joint-life insurance: {joint_insurance:.4f}")
```

### Last-Survivor Insurance

#### `Ax_2heads_ls(mt1, mt2, x, y, i, g=0, method='udd')`
Expected present value of last-survivor insurance (pays on second death).

```python
# Last-survivor insurance (pays on second death)
last_surv_insurance = life_2heads.Ax_2heads_ls(mt1, mt2, x=30, y=28, i=5)
print(f"Last-survivor insurance: {last_surv_insurance:.4f}")
```

## Practical Applications

### Pension Planning for Couples

```python
# Retirement planning for married couple
husband_age = 65
wife_age = 62
interest_rate = 5

# Different annuity options
single_life = annuities.ax(mt1, x=husband_age, i=interest_rate)
joint_life = life_2heads.ax_2heads(mt1, mt2, husband_age, wife_age, interest_rate)
last_survivor = life_2heads.ax_2heads_ls(mt1, mt2, husband_age, wife_age, interest_rate)

print("Pension Options (per $1 of premium):")
print(f"Single life (husband): {single_life:.4f}")
print(f"Joint life (50% to survivor): {joint_life:.4f}")
print(f"Last survivor (100% to survivor): {last_survivor:.4f}")

# Cost comparison for equal benefits
base_benefit = 50000  # Annual pension
single_cost = base_benefit / single_life
joint_cost = base_benefit / joint_life
last_cost = base_benefit / last_survivor

print("\nCost for $50,000 annual benefit:")
print(f"Single life: ${single_cost:,.0f}")
print(f"Joint life: ${joint_cost:,.0f}")
print(f"Last survivor: ${last_cost:,.0f}")
```

### Life Insurance for Couples

```python
# Life insurance options
coverage_amount = 500000

# First-to-die insurance (joint life)
first_die_cost = coverage_amount * joint_insurance
print(f"First-to-die insurance cost: ${first_die_cost:,.2f}")

# Second-to-die insurance (last survivor)  
second_die_cost = coverage_amount * last_surv_insurance
print(f"Second-to-die insurance cost: ${second_die_cost:,.2f}")

# Individual policies
individual_cost_1 = coverage_amount * mortality_insurance.Ax(mt1, x=30, i=5)
individual_cost_2 = coverage_amount * mortality_insurance.Ax(mt2, x=28, i=5)
total_individual = individual_cost_1 + individual_cost_2

print(f"Total individual policies: ${total_individual:,.2f}")
print(f"Savings with first-to-die: ${total_individual - first_die_cost:,.2f}")
```

## Mathematical Relationships

### Key Identities

```python
# Verify fundamental relationships
x, y = 30, 28
i = 5

# Get components
ax_x = annuities.ax(mt1, x=x, i=i)
ax_y = annuities.ax(mt2, x=y, i=i)
ax_xy = life_2heads.ax_2heads(mt1, mt2, x, y, i)
ax_xy_ls = life_2heads.ax_2heads_ls(mt1, mt2, x, y, i)

# Relationship 1: ax_xy_ls = ax_x + ax_y - ax_xy
relationship1 = abs(ax_xy_ls - (ax_x + ax_y - ax_xy))
print(f"Annuity relationship error: {relationship1:.8f}")

# Relationship 2: Ax + ax = 1 (for each status)
Ax_xy = life_2heads.Ax_2heads(mt1, mt2, x, y, i)
insurance_annuity_sum = Ax_xy + ax_xy
print(f"Ax + ax for joint life: {insurance_annuity_sum:.6f}")
```

## Advanced Features

### Different Mortality Tables

```python
# Using different mortality tables for male/female
mt_male = MortalityTable(data_type='q', mt=[0, 0.012, 0.025, 0.06, 1.0])
mt_female = MortalityTable(data_type='q', mt=[0, 0.008, 0.018, 0.045, 1.0])

# Gender-specific calculations
male_female_joint = life_2heads.ax_2heads(mt_male, mt_female, x=65, y=62, i=5)
print(f"Male-female joint annuity: {male_female_joint:.4f}")
```

### Dependent Lives

Some functions support dependence between lives:

```python
# With dependence (where supported)
dependent_prob = life_2heads.npx_2heads(
    mt1, mt2, x=30, y=28, n=10, dependent=True
)
```

## Usage Tips

1. **Mortality Tables**: Can use same or different tables for the two lives
2. **Age Differences**: Common in spouse calculations (age gaps)
3. **Interest Rates**: Same principles as single-life calculations
4. **Applications**: Pension design, estate planning, insurance optimization
5. **Verification**: Use mathematical relationships to check calculations
6. **Independence**: Default assumption; consider dependence for accuracy in some applications