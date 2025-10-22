# Annuities Random Variables

Statistical analysis of actuarial present value random variables for life annuities.

::: lifeActuary.annuities_rv

## Overview

The annuities_rv module provides tools for analyzing the random variable nature of actuarial present values. While actuarial functions typically return expected values, this module enables analysis of the full probability distribution of present values.

## Key Concepts

### Actuarial Present Value Random Variable

The present value of a life annuity is a random variable because:
- The number of payments depends on survival (random)
- Each possible survival scenario has a different present value
- The expected value is the traditional actuarial present value

### Statistical Measures

Key statistical measures for annuity random variables:
- **Mean**: Expected present value (traditional actuarial value)
- **Variance**: Measure of risk/uncertainty
- **Standard Deviation**: Square root of variance
- **Distribution**: Probability of each possible outcome

## Basic Functions

### Whole Life Annuity Random Variable

#### `ax_n_rv(mt, x, i, m=1, method='udd')`
Returns statistics for the present value random variable of a whole life annuity.

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import annuities_rv

# Create mortality table
mt = MortalityTable(data_type='q', mt=[0, 0.01, 0.02, 0.05, 0.1, 1.0])

# Analyze whole life annuity random variable
rv_stats = annuities_rv.ax_n_rv(mt, x=30, i=5)

print(f"Mean (expected PV): {rv_stats['mean']:.4f}")
print(f"Variance: {rv_stats['variance']:.6f}")
print(f"Standard deviation: {rv_stats['std_dev']:.4f}")
print(f"Coefficient of variation: {rv_stats['cv']:.4f}")
```

### Temporary Annuity Random Variable

#### `axt_n_rv(mt, x, t, i, m=1, method='udd')`
Returns statistics for a temporary life annuity random variable.

```python
# 20-year temporary annuity random variable
temp_rv = annuities_rv.axt_n_rv(mt, x=30, t=20, i=5)

print(f"20-year temporary annuity:")
print(f"  Mean: {temp_rv['mean']:.4f}")
print(f"  Std Dev: {temp_rv['std_dev']:.4f}")
print(f"  Risk (CV): {temp_rv['cv']:.4f}")
```

## Detailed Distribution Analysis

### Complete Distribution

#### `annuity_distribution(mt, x, i, t=None, m=1, method='udd')`
Returns the complete probability distribution of annuity present values.

```python
# Get complete distribution for whole life annuity
distribution = annuities_rv.annuity_distribution(mt, x=30, i=5)

print("Annuity Distribution:")
print(f"Possible outcomes: {len(distribution)}")
for outcome in distribution[:5]:  # Show first 5 outcomes
    years = outcome['years_survived']
    pv = outcome['present_value']
    prob = outcome['probability']
    print(f"  {years} years: PV={pv:.4f}, P={prob:.6f}")
```

### Percentiles and Risk Measures

```python
# Calculate risk measures
import numpy as np

# Extract present values and probabilities
outcomes = annuity_distribution(mt, x=30, i=5)
pvs = [outcome['present_value'] for outcome in outcomes]
probs = [outcome['probability'] for outcome in outcomes]

# Calculate percentiles
def calculate_percentile(values, probabilities, percentile):
    sorted_indices = np.argsort(values)
    cumulative_prob = 0
    for idx in sorted_indices:
        cumulative_prob += probabilities[idx]
        if cumulative_prob >= percentile/100:
            return values[idx]
    return values[-1]

# Risk measures
percentile_5 = calculate_percentile(pvs, probs, 5)
percentile_95 = calculate_percentile(pvs, probs, 95)
median = calculate_percentile(pvs, probs, 50)

print(f"5th percentile: {percentile_5:.4f}")
print(f"Median: {median:.4f}")
print(f"95th percentile: {percentile_95:.4f}")
print(f"Value at Risk (5%): {rv_stats['mean'] - percentile_5:.4f}")
```

## Comparison of Annuity Types

### Risk Comparison

```python
# Compare risk across different annuity types
ages = [30, 40, 50, 60]
terms = [10, 20, None]  # None for whole life

print("Risk Analysis (Coefficient of Variation):")
print("Age  | 10-year | 20-year | Whole Life")
print("-" * 40)

for age in ages:
    cv_10 = annuities_rv.axt_n_rv(mt, x=age, t=10, i=5)['cv']
    cv_20 = annuities_rv.axt_n_rv(mt, x=age, t=20, i=5)['cv']
    cv_whole = annuities_rv.ax_n_rv(mt, x=age, i=5)['cv']
    
    print(f"{age:2d}   | {cv_10:7.4f} | {cv_20:8.4f} | {cv_whole:10.4f}")
```

### Impact of Interest Rates

```python
# Analyze impact of interest rates on risk
interest_rates = [3, 4, 5, 6, 7]

print("\nInterest Rate Impact on Annuity Risk:")
print("Rate | Mean    | Std Dev | CV")
print("-" * 30)

for rate in interest_rates:
    stats = annuities_rv.ax_n_rv(mt, x=30, i=rate)
    print(f"{rate:2d}%  | {stats['mean']:7.4f} | {stats['std_dev']:7.4f} | {stats['cv']:6.4f}")
```

## Monte Carlo Simulation

### Simulation Verification

```python
# Verify analytical results with Monte Carlo simulation
import random

def simulate_annuity_pv(mt, x, i, n_simulations=10000):
    """Monte Carlo simulation of annuity present value"""
    present_values = []
    
    for _ in range(n_simulations):
        age = x
        pv = 0
        year = 0
        
        while age <= mt.w:  # While alive
            # Check if survives this year
            if random.random() > mt.nqx(age, 1):
                # Survived - receives payment
                pv += (1 + i/100) ** (-year)
                age += 1
                year += 1
            else:
                # Died - no more payments
                break
    
    present_values.append(pv)
    
    return {
        'mean': np.mean(present_values),
        'std_dev': np.std(present_values),
        'variance': np.var(present_values)
    }

# Compare analytical vs. simulation
analytical = annuities_rv.ax_n_rv(mt, x=30, i=5)
simulated = simulate_annuity_pv(mt, x=30, i=5)

print("Analytical vs. Simulation:")
print(f"Mean:     {analytical['mean']:.4f} vs {simulated['mean']:.4f}")
print(f"Std Dev:  {analytical['std_dev']:.4f} vs {simulated['std_dev']:.4f}")
print(f"Variance: {analytical['variance']:.6f} vs {simulated['variance']:.6f}")
```

## Practical Applications

### Pension Risk Management

```python
# Assess pension liability risk for a group
group_size = 1000
individual_mean = annuities_rv.ax_n_rv(mt, x=65, i=5)['mean']
individual_variance = annuities_rv.ax_n_rv(mt, x=65, i=5)['variance']

# Portfolio statistics (assuming independence)
portfolio_mean = group_size * individual_mean
portfolio_std_dev = np.sqrt(group_size * individual_variance)
portfolio_cv = portfolio_std_dev / portfolio_mean

print(f"Pension Portfolio Risk (n={group_size}):")
print(f"Expected liability: ${portfolio_mean:,.0f}")
print(f"Standard deviation: ${portfolio_std_dev:,.0f}")
print(f"Coefficient of variation: {portfolio_cv:.4f}")
print(f"95% confidence interval: ${portfolio_mean - 1.96*portfolio_std_dev:,.0f} to ${portfolio_mean + 1.96*portfolio_std_dev:,.0f}")
```

### Reserve Requirements

```python
# Calculate reserve requirements based on risk tolerance
confidence_level = 0.95  # 95% confidence
target_age = 30
interest_rate = 5

stats = annuities_rv.ax_n_rv(mt, x=target_age, i=interest_rate)
mean_pv = stats['mean']
std_dev = stats['std_dev']

# Conservative reserve (mean + 2 std deviations)
conservative_reserve = mean_pv + 2 * std_dev

# Risk-based reserve (95th percentile)
distribution = annuities_rv.annuity_distribution(mt, x=target_age, i=interest_rate)
pvs = [outcome['present_value'] for outcome in distribution]
probs = [outcome['probability'] for outcome in distribution]
risk_based_reserve = calculate_percentile(pvs, probs, 95)

print(f"Reserve Analysis:")
print(f"Mean reserve: {mean_pv:.4f}")
print(f"Conservative (μ + 2σ): {conservative_reserve:.4f}")
print(f"Risk-based (95th %ile): {risk_based_reserve:.4f}")
print(f"Safety margin: {(conservative_reserve/mean_pv - 1)*100:.1f}%")
```

## Mathematical Background

### Variance Formula

For a whole life annuity, the variance can be calculated as:

```
Var[PV] = ²Ax - (Ax)²
```

Where ²Ax is the second moment of the insurance random variable.

### Relationship to Insurance

The annuity and insurance random variables are related:

```python
# Verify the relationship: PV_annuity + PV_insurance = constant
from lifeActuary import mortality_insurance_rv

annuity_stats = annuities_rv.ax_n_rv(mt, x=30, i=5)
insurance_stats = mortality_insurance_rv.Ax_n_rv(mt, x=30, i=5)

# The sum should have zero variance (constant)
sum_variance = annuity_stats['variance'] + insurance_stats['variance'] + 2*covariance
print(f"Sum variance (should be 0): {sum_variance:.8f}")
```

## Usage Tips

1. **Risk Assessment**: Use coefficient of variation to compare relative risk
2. **Portfolio Effects**: Individual variances add for independent lives
3. **Interest Sensitivity**: Higher rates generally reduce variance
4. **Age Effects**: Older ages typically have lower variance
5. **Validation**: Compare with simulations for complex scenarios
6. **Applications**: Reserve setting, capital requirements, risk management