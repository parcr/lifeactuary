# lifeActuary

Package **lifeActuary** is a Python library to perform actuarial mathematics on life contingencies and classical financial mathematics computations. Versatile, simple and easy to use. The main functions are implemented using the usual actuarial approach, making it a natural choice for the life actuary.

## Overview

lifeActuary provides comprehensive tools for:

- **Mortality Tables**: Complete mortality table operations with support for different interpolation methods
- **Life Annuities**: Immediate and deferred annuities, with support for growing payments
- **Life Insurance**: Various types of life insurance calculations 
- **Commutation Functions**: Traditional actuarial commutation symbols (Dx, Nx, Sx, Cx, Mx, Rx)
- **Multiple Lives**: Joint-life and last-survivor calculations for two lives
- **Random Variables**: Actuarial present value random variables for annuities and insurance

## Key Features

- **Flexible Mortality Tables**: Support for qx, px, or lx input formats
- **Multiple Interpolation Methods**: UDD (Uniform Distribution of Deaths), CFM (Constant Force of Mortality), and Balducci
- **Growing Payments**: Support for geometrically increasing payments in annuities and insurance
- **SOA Table Support**: Built-in support for Society of Actuaries mortality tables
- **Comprehensive Testing**: Extensive test suite ensuring accuracy of calculations

## Version 1.3.2 Highlights

- Enhanced life annuity functions that don't require commutation table computation
- New mortality insurance class with direct calculations
- Two-life functionality for joint-life and last-survivor scenarios
- Improved fractional age calculations
- Extensive documentation and examples

## Quick Example

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import annuities

# Create a mortality table
mt = MortalityTable(data_type='q', mt=[0, 0.1, 0.2, 0.3, 1.0])

# Calculate immediate whole life annuity
annuity_value = annuities.ax(mt, x=0, i=5)
print(f"Immediate whole life annuity: {annuity_value:.4f}")
```

## Getting Started

1. [Installation Guide](user-guide/installation.md) - How to install and set up lifeActuary
2. [Quick Start](user-guide/quick-start.md) - Basic usage patterns and examples
3. [API Reference](api/mortality_table.md) - Complete function reference
4. [Examples](examples/basic.md) - Practical examples and use cases

## Requirements

- Python >= 3.6
- NumPy
- Pandas

## License

This package is distributed under the [MIT License](about/license.md).

## Disclaimer

This package and functions herein are provided as is, without any guarantee regarding the accuracy of calculations. The authors disclaim any liability arising by any losses due to direct or indirect use of this package.