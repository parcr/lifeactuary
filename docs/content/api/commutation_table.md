# Commutation Tables

The `CommutationFunctions` class provides traditional actuarial commutation symbols for efficient calculation of life contingency values.

::: lifeActuary.commutation_table.CommutationFunctions

## Overview

Commutation functions are fundamental tools in traditional actuarial mathematics that pre-compute discounted survival probabilities and related values. They enable efficient calculation of annuities and insurance values without repeated computation of basic probabilities.

## Key Commutation Symbols

### Life Functions
- **Dx**: Discounted number of survivors at age x
- **Nx**: Sum of Dx values from age x to terminal age
- **Sx**: Sum of Nx values from age x to terminal age

### Death Functions  
- **Cx**: Discounted deaths at age x
- **Mx**: Sum of Cx values from age x to terminal age
- **Rx**: Sum of Mx values from age x to terminal age

## Usage Examples

### Creating a Commutation Table

```python
from lifeActuary.commutation_table import CommutationFunctions

# Define mortality rates (qx values)
qx_values = [0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 1.0]

# Create commutation table at 5% interest
ct = CommutationFunctions(
    i=5,  # 5% interest rate
    g=0,  # No growth in benefits
    data_type='q', 
    mt=qx_values
)

# Access commutation values
print(f"D30: {ct.Dx[30]:.2f}")
print(f"N30: {ct.Nx[30]:.2f}")
print(f"C30: {ct.Cx[30]:.4f}")
print(f"M30: {ct.Mx[30]:.4f}")
```

### Growing Benefits

```python
# Commutation table with 2% growth in benefits
ct_growing = CommutationFunctions(
    i=5,     # 5% interest rate
    g=2,     # 2% annual growth
    data_type='q',
    mt=qx_values
)
```

## Calculating Annuities with Commutation Functions

### Immediate Whole Life Annuity

```python
# Manual calculation using commutation functions
def whole_life_annuity(ct, x):
    return ct.Nx[x] / ct.Dx[x]

# Using built-in method
annuity_value = ct.whole_life_annuity(30)
print(f"Whole life annuity at age 30: {annuity_value:.4f}")

# Compare with manual calculation
manual_calc = ct.Nx[30] / ct.Dx[30]
print(f"Manual calculation: {manual_calc:.4f}")
```

### Temporary Annuity

```python
# 20-year temporary annuity
def temp_annuity(ct, x, n):
    return (ct.Nx[x] - ct.Nx[x + n]) / ct.Dx[x]

temp_20 = temp_annuity(ct, 30, 20)
print(f"20-year temporary annuity: {temp_20:.4f}")

# Using built-in method
temp_builtin = ct.temporary_annuity(30, 20)
print(f"Built-in method: {temp_builtin:.4f}")
```

### Deferred Annuity

```python
# 10-year deferred whole life annuity
def deferred_annuity(ct, x, n):
    return ct.Nx[x + n] / ct.Dx[x]

deferred_10 = deferred_annuity(ct, 30, 10)
print(f"10-year deferred annuity: {deferred_10:.4f}")
```

## Calculating Insurance with Commutation Functions

### Whole Life Insurance

```python
# Whole life insurance
def whole_life_insurance(ct, x):
    return ct.Mx[x] / ct.Dx[x]

insurance_value = whole_life_insurance(ct, 30)
print(f"Whole life insurance at age 30: {insurance_value:.4f}")

# Using built-in method
insurance_builtin = ct.whole_life_insurance(30)
print(f"Built-in method: {insurance_builtin:.4f}")
```

### Term Insurance

```python
# 20-year term insurance
def term_insurance(ct, x, n):
    return (ct.Mx[x] - ct.Mx[x + n]) / ct.Dx[x]

term_20 = term_insurance(ct, 30, 20)
print(f"20-year term insurance: {term_20:.4f}")
```

### Endowment Insurance

```python
# 20-year endowment insurance
def endowment_insurance(ct, x, n):
    term_part = (ct.Mx[x] - ct.Mx[x + n]) / ct.Dx[x]
    pure_endowment = ct.Dx[x + n] / ct.Dx[x]
    return term_part + pure_endowment

endowment_20 = endowment_insurance(ct, 30, 20)
print(f"20-year endowment insurance: {endowment_20:.4f}")
```

## Advanced Features

### Fractional Ages and Payments

The commutation table supports fractional calculations:

```python
# Calculate values for fractional ages
value_30_5 = ct.Dx[30.5]  # If fractional ages supported
```

### Multiple Payment Frequencies

```python
# For monthly payments, adjust by payment frequency
monthly_annuity = ct.Nx[30] / ct.Dx[30] / 12
```

### Verification Against Direct Methods

```python
from lifeActuary import annuities, mortality_insurance

# Compare commutation vs. direct calculation
ct_value = ct.whole_life_annuity(30)
direct_value = annuities.ax(ct.mt, x=30, i=5)

print(f"Commutation method: {ct_value:.6f}")
print(f"Direct method: {direct_value:.6f}")
print(f"Difference: {abs(ct_value - direct_value):.8f}")
```

## Benefits of Commutation Functions

1. **Computational Efficiency**: Pre-computed values for faster calculations
2. **Traditional Approach**: Familiar to actuaries trained in classical methods
3. **Relationship Visualization**: Clear mathematical relationships between functions
4. **Manual Verification**: Easy to verify calculations by hand
5. **Educational Value**: Helps understand underlying actuarial mathematics

## Key Methods

### Basic Commutation Values
- `Dx`: Discounted survivors at age x
- `Nx`: Accumulated Dx values from age x onwards
- `Sx`: Accumulated Nx values from age x onwards
- `Cx`: Discounted deaths at age x  
- `Mx`: Accumulated Cx values from age x onwards
- `Rx`: Accumulated Mx values from age x onwards

### Derived Calculations
- `whole_life_annuity(x)`: Immediate whole life annuity
- `temporary_annuity(x, n)`: n-year temporary annuity
- `deferred_annuity(x, n)`: n-year deferred annuity
- `whole_life_insurance(x)`: Whole life insurance
- `term_insurance(x, n)`: n-year term insurance
- `endowment_insurance(x, n)`: n-year endowment

## Usage Tips

1. **Interest Rate**: Specify as percentage (5 for 5%)
2. **Growth Rate**: Use for benefits that increase geometrically
3. **Memory Efficiency**: Commutation tables store all ages, consider memory for large tables
4. **Verification**: Always verify against direct calculations for critical applications
5. **Documentation**: Traditional actuarial notation helps with textbook references