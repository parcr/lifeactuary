# Release Notes

## Version 1.3.2 (Current)

### Major Changes

- **Enhanced Life Annuity Functions**: All life annuity functions now operate without requiring commutation table computation, providing more direct and efficient calculations.

- **New Mortality Insurance Class**: Developed a new `mortality_insurance.py` module where functions for evaluating life insurance contracts are available without the need to compute the commutation table.

- **Two-Life Functionality**: New class for evaluating annuities and life insurance for groups of two individuals, supporting both joint-life and last-survivor methods.

### Bug Fixes and Improvements

- **Present Value Function**: Small correction to the `present_value` function
- **Commutation Table Functions**: Large correction to the functions `t_nIArx` and `t_nIArx_` in `commutation_table.py`
- **Integral Functions**: Small correction to the function `get_integral_px_method` in the `mortality_table` class
- **Annuity Functions**: Small correction to the function `annuity_x` in the `annuities` class
- **Fractional Calculations**: Small correction to the `npx` and `nqx` functions in the `mortality_table` module when producing fractional commutation tables using the Balducci and Constant Mortality Force methods

### New Features

- Comprehensive test suite with extensive examples
- Enhanced documentation and user manual
- Support for SOA (Society of Actuaries) mortality tables
- Improved fractional age and payment frequency handling

### Compatibility

- Python >= 3.6
- NumPy compatibility improvements
- Pandas integration enhancements

## Version 1.2.1

### Features Added

- **SOA Table Reader**: Included the file `read_soa_table_xml.py` for reading Society of Actuaries mortality tables in XML format
- Enhanced support for standard actuarial mortality tables

### Files Added

- `soa_tables/read_soa_table_xml.py` - XML mortality table reader
- Additional SOA mortality tables in XML format

## Version 1.2.0

### Major Features

- **Fractional Commutation Tables**: Support for fractional ages and payment frequencies
- **Enhanced Mortality Insurance**: More comprehensive life insurance calculations
- **Improved Performance**: Optimized calculation algorithms
- **Extended Examples**: More practical examples and use cases

### API Changes

- Enhanced `MortalityTable` class with better interpolation methods
- Extended annuity functions with more flexible parameters
- Improved two-life calculations

## Version 1.0.0

### Initial Release

- **Core Mortality Tables**: Basic mortality table operations
- **Life Annuities**: Immediate, deferred, and temporary annuities
- **Life Insurance**: Basic life insurance calculations
- **Commutation Functions**: Traditional actuarial commutation symbols
- **SOA Tables**: Support for Society of Actuaries mortality tables

### Core Modules

- `mortality_table.py` - Basic mortality table functionality
- `annuities.py` - Life annuity calculations
- `mortality_insurance.py` - Life insurance calculations
- `commutation_table.py` - Traditional commutation functions

## Upgrade Guide

### Upgrading from 1.2.x to 1.3.2

The upgrade to version 1.3.2 is generally backward compatible, but there are some improvements you should be aware of:

#### New Direct Calculation Methods

**Before (1.2.x):**
```python
# Required commutation table for annuity calculations
from lifeActuary.commutation_table import CommutationFunctions
ct = CommutationFunctions(i=5, data_type='q', mt=qx_values)
annuity_value = ct.Nx[30] / ct.Dx[30]
```

**After (1.3.2):**
```python
# Direct calculation without commutation table
from lifeActuary import annuities
annuity_value = annuities.ax(mt, x=30, i=5)
```

#### Enhanced Two-Life Support

**New in 1.3.2:**
```python
from lifeActuary import life_2heads

# Joint-life annuity
joint_annuity = life_2heads.ax_2heads(mt1, mt2, x=65, y=62, i=5)

# Last-survivor annuity
survivor_annuity = life_2heads.ax_2heads_ls(mt1, mt2, x=65, y=62, i=5)
```

#### Corrected Functions

If you were using the following functions, please verify your calculations:

- `t_nIArx` and `t_nIArx_` in commutation tables
- `present_value` function
- `annuity_x` function
- Fractional calculations with Balducci and CFM methods

### Upgrading from 1.0.x to 1.3.2

This is a major upgrade with significant new functionality:

1. **Update Import Statements**: Some functions have moved to new modules
2. **Review Calculations**: Many calculations are now more accurate with bug fixes
3. **Consider New Features**: Take advantage of two-life calculations and enhanced fractional support
4. **Update SOA Table Loading**: Use the new XML reader for SOA tables

## Known Issues

### Current Limitations

- **Memory Usage**: Large mortality tables with fine fractional divisions can consume significant memory
- **Performance**: Very high-frequency calculations (daily or more frequent) may be slow for large datasets
- **Dependence**: Two-life calculations assume independence between lives (no correlation modeling)

### Workarounds

**Memory Issues:**
- Use appropriate fractional divisions (monthly instead of daily)
- Consider chunking large calculations

**Performance Issues:**
- Cache commutation tables for repeated calculations
- Use vectorized operations where possible

**Dependence Modeling:**
- Apply adjustment factors to independent calculations
- Consider external copula models for advanced applications

## Deprecation Notices

### Functions to be Deprecated

Currently, no functions are scheduled for deprecation, but users are encouraged to:

- Use direct calculation methods instead of commutation tables where possible
- Migrate to the new two-life functions for multiple-life scenarios
- Update to the latest SOA table reading methods

### Future Changes

Version 2.0 (tentative) may include:

- **Stochastic Mortality**: Support for stochastic mortality models
- **Advanced Dependence**: Built-in copula models for two-life calculations
- **Performance Optimization**: Compiled extensions for computationally intensive operations
- **Extended SOA Support**: Support for more recent SOA mortality table formats

## Migration Examples

### Example 1: Migrating Annuity Calculations

**Old Method:**
```python
from lifeActuary.commutation_table import CommutationFunctions

ct = CommutationFunctions(i=5, data_type='q', mt=qx_values)
whole_life = ct.Nx[30] / ct.Dx[30]
temp_20 = (ct.Nx[30] - ct.Nx[50]) / ct.Dx[30]
```

**New Method:**
```python
from lifeActuary import annuities
from lifeActuary.mortality_table import MortalityTable

mt = MortalityTable(data_type='q', mt=qx_values)
whole_life = annuities.ax(mt, x=30, i=5)
temp_20 = annuities.axt(mt, x=30, t=20, i=5)
```

### Example 2: Adding Two-Life Functionality

**New Capability:**
```python
from lifeActuary import life_2heads
from lifeActuary.mortality_table import MortalityTable

# Create tables for both lives
mt_male = MortalityTable(data_type='q', mt=male_qx)
mt_female = MortalityTable(data_type='q', mt=female_qx)

# Joint-life calculations
joint_annuity = life_2heads.ax_2heads(mt_male, mt_female, x=65, y=62, i=5)
survivor_annuity = life_2heads.ax_2heads_ls(mt_male, mt_female, x=65, y=62, i=5)
```

## Bug Reports and Support

### Reporting Issues

If you encounter bugs or issues:

1. Check the [GitHub Issues](https://github.com/parcr/lifeactuary/issues) page
2. Provide a minimal reproducible example
3. Include your Python and package versions
4. Describe expected vs. actual behavior

### Getting Help

- Review this documentation and examples
- Check the GitHub repository for updates
- Review the manual (PDF) for detailed explanations
- Consider the essay examples for implementation patterns

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request with clear description

The package continues to evolve based on user feedback and actuarial practice needs.