# Life Insurance

The mortality insurance module provides functions for calculating the expected present value (EPV) of various types of life insurance policies.

::: lifeActuary.mortality_insurance

## Key Functions

### Whole Life Insurance

#### `Ax(mt, x, i=None, g=0, method='udd')`
Returns the EPV of a whole life insurance that pays 1 at the end of the year of death.

**Parameters:**
- `mt`: Mortality table for life x
- `x`: Age at the beginning of the contract
- `i`: Technical interest rate (percentage)
- `g`: Growth rate for benefits (percentage)
- `method`: Interpolation method ('udd', 'cfm', 'bal')

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import mortality_insurance

# Create mortality table
mt = MortalityTable(data_type='q', mt=[0, 0.01, 0.02, 0.03, 1.0])

# Whole life insurance at 5% interest
insurance_value = mortality_insurance.Ax(mt, x=30, i=5)
print(f"Whole life insurance EPV: {insurance_value:.4f}")

# With growing benefits (2% annual increase)
growing_insurance = mortality_insurance.Ax(mt, x=30, i=5, g=2)
print(f"Growing life insurance EPV: {growing_insurance:.4f}")
```

### Term Life Insurance

#### `Axt(mt, x, t, i=None, g=0, method='udd')`
Returns the EPV of a t-year term life insurance.

```python
# 20-year term life insurance
term_insurance = mortality_insurance.Axt(mt, x=30, t=20, i=5)
print(f"20-year term insurance EPV: {term_insurance:.4f}")
```

### Deferred Life Insurance

#### `nAx(mt, x, n, i=None, g=0, method='udd')`
Returns the EPV of an n-year deferred whole life insurance.

```python
# 10-year deferred whole life insurance
deferred_insurance = mortality_insurance.nAx(mt, x=30, n=10, i=5)
print(f"10-year deferred insurance EPV: {deferred_insurance:.4f}")
```

### Endowment Insurance

#### `Axt_end(mt, x, t, i=None, g=0, method='udd')`
Returns the EPV of a t-year endowment insurance (pays on death or survival to end of term).

```python
# 20-year endowment insurance
endowment = mortality_insurance.Axt_end(mt, x=30, t=20, i=5)
print(f"20-year endowment EPV: {endowment:.4f}")
```

## Advanced Insurance Functions

### Generic Life Insurance

#### `A_x(mt, x, x_first, x_last, i=None, g=0, method='udd')`
Computes EPV of life insurance with flexible coverage period.

```python
# Insurance covering ages 35 to 65
custom_insurance = mortality_insurance.A_x(
    mt, x=30, x_first=35, x_last=65, i=5, g=1
)
print(f"Custom period insurance EPV: {custom_insurance:.4f}")
```

### Varying Insurance Benefits

The package supports insurance with benefits that vary by age or time:

```python
# Insurance with benefits increasing at 2% annually
increasing_insurance = mortality_insurance.Ax(mt, x=30, i=5, g=2)

# Insurance with benefits decreasing over time  
decreasing_insurance = mortality_insurance.Ax(mt, x=30, i=5, g=-1)
```

## Complete Function List

### Basic Life Insurance
- `Ax()` - Whole life insurance
- `Axt()` - Term life insurance
- `nAx()` - Deferred whole life insurance
- `nAxt()` - Deferred term life insurance
- `Axt_end()` - Endowment insurance

### Advanced Functions
- `A_x()` - Generic life insurance with custom coverage period
- `IA()` - Increasing whole life insurance
- `IAx()` - Increasing whole life insurance (alternative formulation)
- `IAAx()` - Increasing whole life insurance (yet another formulation)

### Special Insurance Types
- Functions for various combinations of term, whole life, and endowment
- Support for deferred benefits
- Increasing and decreasing benefit patterns

## Relationship to Annuities

Life insurance and annuities are closely related through the fundamental identity:

```
Ax + ax = 1 (at the same interest rate)
```

This relationship can be verified:

```python
# Calculate both insurance and annuity
insurance = mortality_insurance.Ax(mt, x=30, i=5)
annuity = annuities.ax(mt, x=30, i=5)

# They should sum to approximately 1
total = insurance + annuity
print(f"Ax + ax = {total:.6f}")  # Should be close to 1.0
```

## Usage Examples

### Comparing Insurance Types

```python
# Compare different insurance products for a 30-year-old
whole_life = mortality_insurance.Ax(mt, x=30, i=5)
term_20 = mortality_insurance.Axt(mt, x=30, t=20, i=5)
endowment_20 = mortality_insurance.Axt_end(mt, x=30, t=20, i=5)

print(f"Whole life insurance: {whole_life:.4f}")
print(f"20-year term: {term_20:.4f}")
print(f"20-year endowment: {endowment_20:.4f}")
```

### Impact of Interest Rates

```python
# Show impact of different interest rates
for rate in [3, 4, 5, 6]:
    epv = mortality_insurance.Ax(mt, x=30, i=rate)
    print(f"At {rate}% interest: {epv:.4f}")
```

### Growing vs. Level Benefits

```python
# Compare level vs. growing benefits
level_benefit = mortality_insurance.Ax(mt, x=30, i=5, g=0)
growing_benefit = mortality_insurance.Ax(mt, x=30, i=5, g=2)

print(f"Level benefit: {level_benefit:.4f}")
print(f"Growing benefit (+2% p.a.): {growing_benefit:.4f}")
print(f"Premium ratio: {growing_benefit/level_benefit:.2f}")
```

## Usage Tips

1. **Interest Rates**: Specify as percentages (5 for 5%, not 0.05)
2. **Growth Rates**: Positive for increasing benefits, negative for decreasing
3. **Method Selection**: 'udd' is standard, other methods for special situations
4. **Age Specifications**: Can use fractional ages for more precision
5. **Validation**: Use the Ax + ax = 1 identity to check calculations