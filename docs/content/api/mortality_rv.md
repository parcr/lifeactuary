# Mortality Random Variables

Statistical analysis of mortality-related random variables and their distributions.

::: lifeActuary.mortality_rv

## Overview

The mortality_rv module provides comprehensive tools for analyzing the stochastic nature of mortality patterns. It enables calculation of probability distributions, moments, and statistical measures for various mortality-related random variables.

## Key Random Variables

### Time Until Death (Tx)
The future lifetime random variable representing time until death from age x.

### Number of Complete Years (Kx)  
The curtate future lifetime - number of complete years lived from age x.

### Present Value Variables
Random variables representing present values of life contingent payments.

## Basic Distribution Functions

### Future Lifetime Distribution

#### `T_x_distribution(mt, x, method='udd')`
Returns the complete distribution of the future lifetime random variable T_x.

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import mortality_rv

# Create mortality table
mt = MortalityTable(data_type='q', mt=[0, 0.01, 0.02, 0.05, 0.1, 0.3, 1.0])

# Get future lifetime distribution for age 30
T_x_dist = mortality_rv.T_x_distribution(mt, x=30)

print("Future Lifetime Distribution (first 10 years):")
print("Year | Probability | Cumulative")
print("-" * 35)
for i in range(min(10, len(T_x_dist))):
    year = T_x_dist[i]['time']
    prob = T_x_dist[i]['probability']
    cum_prob = sum([T_x_dist[j]['probability'] for j in range(i+1)])
    print(f"{year:4.1f} | {prob:11.6f} | {cum_prob:10.6f}")
```

### Curtate Lifetime Distribution

#### `K_x_distribution(mt, x, method='udd')`
Returns the distribution of complete years lived (curtate lifetime).

```python
# Curtate lifetime distribution
K_x_dist = mortality_rv.K_x_distribution(mt, x=30)

print("\nCurtate Lifetime Distribution:")
print("Years | P(K_x = k) | P(K_x ≤ k)")
print("-" * 35)
for outcome in K_x_dist[:10]:  # First 10 years
    k = outcome['years']
    prob = outcome['probability']
    cum_prob = outcome['cumulative_prob']
    print(f"{k:5d} | {prob:10.6f} | {cum_prob:9.6f}")
```

## Statistical Moments

### Moments of Future Lifetime

#### `T_x_moments(mt, x, method='udd')`
Calculates moments and statistics for the future lifetime random variable.

```python
# Statistical analysis of future lifetime
moments = mortality_rv.T_x_moments(mt, x=30)

print("Future Lifetime Statistics:")
print(f"Mean (life expectancy): {moments['mean']:.4f} years")
print(f"Variance: {moments['variance']:.4f}")
print(f"Standard deviation: {moments['std_dev']:.4f} years")
print(f"Skewness: {moments['skewness']:.4f}")
print(f"Kurtosis: {moments['kurtosis']:.4f}")
print(f"Coefficient of variation: {moments['cv']:.4f}")
```

### Moments of Curtate Lifetime

#### `K_x_moments(mt, x, method='udd')`
Calculates moments for the curtate lifetime random variable.

```python
# Statistical analysis of curtate lifetime
curtate_moments = mortality_rv.K_x_moments(mt, x=30)

print("\nCurtate Lifetime Statistics:")
print(f"Mean: {curtate_moments['mean']:.4f} complete years")
print(f"Variance: {curtate_moments['variance']:.4f}")
print(f"Standard deviation: {curtate_moments['std_dev']:.4f} years")
```

## Survival Function Analysis

### Survival Probability Function

#### `survival_function(mt, x, t_max=None, method='udd')`
Returns the survival function S(t) = P(T_x > t) for various time points.

```python
# Generate survival function
survival_func = mortality_rv.survival_function(mt, x=30, t_max=50)

print("Survival Function S(t) = P(T_30 > t):")
print("Time | S(t)")
print("-" * 15)
for point in survival_func[::5]:  # Every 5th point
    time = point['time']
    prob = point['survival_prob']
    print(f"{time:4.1f} | {prob:.6f}")
```

### Hazard Rate Function

#### `hazard_function(mt, x, method='udd')`
Calculates the hazard (force of mortality) function.

```python
# Hazard rate analysis
hazard_func = mortality_rv.hazard_function(mt, x=30)

print("\nHazard Function μ(x+t):")
print("Age  | Hazard Rate")
print("-" * 20)
for point in hazard_func[:20]:  # First 20 years
    age = point['age']
    hazard = point['hazard_rate']
    print(f"{age:4.1f} | {hazard:.8f}")
```

## Percentile Analysis

### Survival Percentiles

#### `survival_percentiles(mt, x, percentiles=[25, 50, 75, 90, 95], method='udd')`
Calculates survival time percentiles.

```python
# Calculate key survival percentiles
percentiles = mortality_rv.survival_percentiles(mt, x=30, percentiles=[10, 25, 50, 75, 90, 95])

print("Survival Percentiles for Age 30:")
for pct, time in percentiles.items():
    print(f"{pct:2d}th percentile: {time:.2f} years")
    
# Interpretation
median_survival = percentiles[50]
print(f"\nMedian future lifetime: {median_survival:.2f} years")
print(f"50% will survive beyond age {30 + median_survival:.1f}")
```

## Age-Specific Analysis

### Life Expectancy by Age

#### `life_expectancy_table(mt, ages=None, method='udd')`
Generates a life expectancy table for multiple ages.

```python
# Life expectancy analysis by age
ages = list(range(20, 81, 5))
life_exp_table = mortality_rv.life_expectancy_table(mt, ages=ages)

print("Life Expectancy by Age:")
print("Age | Complete | Curtate | Std Dev")
print("-" * 40)
for entry in life_exp_table:
    age = entry['age']
    complete = entry['complete_expectation']
    curtate = entry['curtate_expectation']
    std_dev = entry['std_deviation']
    print(f"{age:3d} | {complete:8.2f} | {curtate:7.2f} | {std_dev:7.2f}")
```

## Distribution Fitting

### Parametric Distribution Fitting

#### `fit_parametric_distribution(mt, x, distributions=['exponential', 'weibull', 'gamma'])`
Fits parametric distributions to the lifetime data.

```python
# Fit parametric distributions
fitted_dists = mortality_rv.fit_parametric_distribution(mt, x=30)

print("Parametric Distribution Fitting:")
for dist_name, params in fitted_dists.items():
    print(f"\n{dist_name.capitalize()} Distribution:")
    for param_name, value in params.items():
        print(f"  {param_name}: {value:.6f}")
    
    # Goodness of fit
    if 'goodness_of_fit' in params:
        print(f"  R²: {params['goodness_of_fit']:.4f}")
```

## Applications

### Insurance Risk Assessment

```python
# Risk assessment for insurance pricing
age = 35
coverage_amount = 500000

# Get distribution statistics
stats = mortality_rv.T_x_moments(mt, x=age)
percentiles = mortality_rv.survival_percentiles(mt, x=age, percentiles=[5, 10, 25, 50])

# Risk measures
prob_claim_10_years = 1 - mt.npx(age, 10)
prob_claim_20_years = 1 - mt.npx(age, 20)

print(f"Insurance Risk Assessment (Age {age}):")
print(f"Expected lifetime: {stats['mean']:.2f} years")
print(f"Standard deviation: {stats['std_dev']:.2f} years")
print(f"10-year claim probability: {prob_claim_10_years:.4f}")
print(f"20-year claim probability: {prob_claim_20_years:.4f}")
print(f"5th percentile survival: {percentiles[5]:.2f} years")
```

### Pension Liability Analysis

```python
# Pension liability risk analysis
retirement_age = 65
current_age = 30
pension_amount = 30000

# Future lifetime at retirement
retirement_stats = mortality_rv.T_x_moments(mt, x=retirement_age)

# Probability distributions
survival_to_retirement = mt.npx(current_age, retirement_age - current_age)
percentiles_retirement = mortality_rv.survival_percentiles(mt, x=retirement_age)

print(f"Pension Analysis (Current Age {current_age}):")
print(f"Survival to retirement ({retirement_age}): {survival_to_retirement:.4f}")
print(f"Expected retirement duration: {retirement_stats['mean']:.2f} years")
print(f"Standard deviation: {retirement_stats['std_dev']:.2f} years")
print(f"25th percentile duration: {percentiles_retirement[25]:.2f} years")
print(f"75th percentile duration: {percentiles_retirement[75]:.2f} years")

# Total expected pension payments
expected_payments = pension_amount * retirement_stats['mean']
print(f"Expected total pension: ${expected_payments:,.0f}")
```

### Population Mortality Analysis

```python
# Population-level mortality analysis
ages_of_interest = [0, 20, 40, 60, 80]

print("Population Mortality Summary:")
print("Age | Life Exp | Std Dev | CV    | Median")
print("-" * 45)

for age in ages_of_interest:
    if age <= mt.w:
        stats = mortality_rv.T_x_moments(mt, x=age)
        percentiles = mortality_rv.survival_percentiles(mt, x=age, percentiles=[50])
        
        print(f"{age:3d} | {stats['mean']:8.2f} | {stats['std_dev']:7.2f} | {stats['cv']:5.3f} | {percentiles[50]:6.2f}")
```

## Advanced Statistical Analysis

### Mortality Rate Variability

```python
# Analyze variability in mortality rates by age
mortality_stats = []
for age in range(30, min(80, mt.w)):
    if age < mt.w:
        hazard = mt.force_mortality(age)
        mortality_stats.append({
            'age': age,
            'hazard_rate': hazard,
            'annual_prob': mt.nqx(age, 1)
        })

# Find peak mortality acceleration
max_acceleration_age = max(mortality_stats, key=lambda x: x['hazard_rate'])['age']
print(f"Peak mortality acceleration at age: {max_acceleration_age}")
```

### Conditional Survival Analysis

```python
# Conditional survival analysis
base_age = 30
condition_ages = [40, 50, 60, 70]

print(f"Conditional Survival Analysis (Base Age {base_age}):")
print("Condition Age | Conditional Life Exp | Unconditional")
print("-" * 55)

unconditional = mortality_rv.T_x_moments(mt, x=base_age)['mean']

for cond_age in condition_ages:
    if cond_age <= mt.w:
        # Conditional on surviving to cond_age
        survival_prob = mt.npx(base_age, cond_age - base_age)
        if survival_prob > 0:
            conditional_stats = mortality_rv.T_x_moments(mt, x=cond_age)
            total_expected = (cond_age - base_age) + conditional_stats['mean']
            
            print(f"{cond_age:12d} | {total_expected:19.2f} | {unconditional:12.2f}")
```

## Usage Tips

1. **Memory Management**: Distribution functions can be memory-intensive for large mortality tables
2. **Computational Complexity**: Statistical moments require integration over entire lifetime
3. **Interpretation**: Always consider confidence intervals with point estimates
4. **Validation**: Compare calculated life expectancy with published life tables
5. **Applications**: Use for risk assessment, capital modeling, and population studies
6. **Precision**: Higher precision mortality tables yield more accurate statistics