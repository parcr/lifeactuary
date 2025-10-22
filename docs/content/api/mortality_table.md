# Mortality Tables

The `MortalityTable` class is the foundation of the lifeActuary package, providing comprehensive mortality table functionality with support for various input formats and interpolation methods.

::: lifeActuary.mortality_table.MortalityTable

## Usage Examples

### Creating a Mortality Table from qx values

```python
from lifeActuary.mortality_table import MortalityTable

# Example mortality rates (qx values)
qx_values = [0, 0.001, 0.002, 0.003, 0.005, 0.008, 0.012, 0.018, 1.0]

# Create mortality table
mt = MortalityTable(data_type='q', mt=qx_values, perc=100)

# Access survival probability
p_30_1 = mt.npx(30, n=1)  # 1-year survival probability at age 30
print(f"1-year survival probability at age 30: {p_30_1:.6f}")

# Access mortality probability  
q_30_1 = mt.nqx(30, n=1)  # 1-year mortality probability at age 30
print(f"1-year mortality probability at age 30: {q_30_1:.6f}")
```

### Creating from lx values

```python
# Example lx values (number of survivors)
lx_values = [100000, 99900, 99780, 99630, 99440, 99200, 98900, 98520, 0]

mt = MortalityTable(data_type='l', mt=lx_values)
```

### Creating from px values

```python
# Example px values (survival probabilities)
px_values = [0, 0.999, 0.998, 0.997, 0.995, 0.992, 0.988, 0.982, 0.0]

mt = MortalityTable(data_type='p', mt=px_values)
```

## Key Methods

### Survival and Mortality Probabilities

- **`npx(x, n, method='udd')`**: n-year survival probability from age x
- **`nqx(x, n, method='udd')`**: n-year mortality probability from age x
- **`tpx(x, t, method='udd')`**: t-year survival probability (fractional ages)
- **`tqx(x, t, method='udd')`**: t-year mortality probability (fractional ages)

### Life Expectancy

- **`ex(x, method='udd')`**: Complete life expectancy at age x
- **`ex_curtate(x, method='udd')`**: Curtate life expectancy at age x

### Table Properties

- **`lx`**: Array of survivors at each age
- **`qx`**: Array of mortality rates
- **`px`**: Array of survival rates
- **`dx`**: Array of deaths at each age
- **`w`**: Terminal age of the table

## Interpolation Methods

The package supports three interpolation methods for fractional ages:

### UDD (Uniform Distribution of Deaths)
The default method assuming deaths are uniformly distributed within each year.

```python
# Using UDD method (default)
prob = mt.tpx(30.5, 1.5, method='udd')
```

### CFM (Constant Force of Mortality)
Assumes constant force of mortality within each year.

```python
# Using CFM method
prob = mt.tpx(30.5, 1.5, method='cfm')
```

### Balducci Assumption
Assumes linearly decreasing conditional survival probability.

```python
# Using Balducci method
prob = mt.tpx(30.5, 1.5, method='bal')
```

## Advanced Features

### Force of Mortality

```python
# Calculate force of mortality at exact age
mu_x = mt.force_mortality(x=30.5)
print(f"Force of mortality at age 30.5: {mu_x:.6f}")
```

### Fractional Age Calculations

```python
# Calculate survival probability for fractional periods
t_px = mt.tpx(x=30, t=2.5, method='udd')  # 2.5-year survival from age 30
print(f"2.5-year survival probability: {t_px:.6f}")
```

### Life Table Statistics

```python
# Get complete expectation of life
e_30 = mt.ex(30)
print(f"Complete life expectancy at age 30: {e_30:.2f} years")

# Get curtate expectation of life  
e_30_curtate = mt.ex_curtate(30)
print(f"Curtate life expectancy at age 30: {e_30_curtate:.2f} years")
```