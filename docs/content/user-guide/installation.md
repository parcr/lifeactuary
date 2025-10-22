# Installation

## Requirements

lifeActuary requires Python 3.6 or higher and the following dependencies:

- **NumPy**: For numerical computations
- **Pandas**: For data manipulation (used in some modules)

## Installation Methods

### Option 1: Direct Download (Recommended)

Since lifeActuary is not currently available on PyPI, you can install it directly from the source:

1. **Download the source code** from the [GitHub repository](https://github.com/parcr/lifeactuary)

2. **Extract the files** to your desired location

3. **Install dependencies**:
   ```bash
   pip install numpy pandas
   ```

4. **Add to Python path** or copy the `lifeActuary` folder to your project directory

### Option 2: Git Clone

If you have Git installed:

```bash
# Clone the repository
git clone https://github.com/parcr/lifeactuary.git

# Navigate to the directory
cd lifeactuary

# Install dependencies
pip install numpy pandas
```

### Option 3: Using setup.py (if available)

If a setup.py file is provided:

```bash
# Download and extract the source
# Navigate to the lifeactuary directory
cd lifeactuary

# Install the package
python setup.py install
```

## Virtual Environment Setup (Recommended)

For better dependency management, use a virtual environment:

```bash
# Create virtual environment
python -m venv lifeactuary_env

# Activate virtual environment
# On Windows:
lifeactuary_env\Scripts\activate
# On macOS/Linux:
source lifeactuary_env/bin/activate

# Install dependencies
pip install numpy pandas

# Add lifeActuary to the environment
```

## Verification

Test your installation by running:

```python
# Test basic import
try:
    from lifeActuary.mortality_table import MortalityTable
    from lifeActuary import annuities
    print("lifeActuary successfully imported!")
except ImportError as e:
    print(f"Import error: {e}")

# Test basic functionality
mt = MortalityTable(data_type='q', mt=[0, 0.1, 0.2, 0.3, 1.0])
result = annuities.ax(mt, x=0, i=5)
print(f"Test calculation result: {result:.4f}")
```

## SOA Tables Download

Don't forget to download the SOA (Society of Actuaries) mortality tables:

1. Visit the [GitHub repository](https://github.com/parcr/lifeactuary)
2. Download the `soa_tables` folder
3. Place it in your working directory or note its path for later use

The SOA tables include standard mortality tables like:
- CSO (Commissioners Standard Ordinary) tables
- GAM (Group Annuity Mortality) tables
- Various international tables

## IDE Setup

### VS Code

1. Install the Python extension
2. Set your Python interpreter to the one with lifeActuary installed
3. Add the lifeActuary path to your workspace settings if needed

### Jupyter Notebook

```python
# Add to your notebook path
import sys
sys.path.append('/path/to/lifeactuary')

from lifeActuary.mortality_table import MortalityTable
```

### PyCharm

1. Add the lifeActuary directory to your project structure
2. Mark the parent directory as a "Sources Root"
3. Ensure numpy and pandas are installed in your project interpreter

## Troubleshooting

### Common Issues

**ImportError: No module named 'lifeActuary'**
- Ensure the lifeActuary folder is in your Python path
- Check that you're using the correct Python environment

**ImportError: No module named 'numpy'**
```bash
pip install numpy
```

**ImportError: No module named 'pandas'**
```bash
pip install pandas
```

**Calculation results seem incorrect**
- Verify you're using the correct mortality table format
- Check that interest rates are specified as percentages (5 for 5%, not 0.05)

### Python Path Issues

If you're having import issues, you can add the path programmatically:

```python
import sys
import os

# Add lifeActuary to path
lifeactuary_path = '/path/to/your/lifeactuary/directory'
if lifeactuary_path not in sys.path:
    sys.path.append(lifeactuary_path)

# Now import should work
from lifeActuary.mortality_table import MortalityTable
```

### Version Compatibility

lifeActuary has been tested with:
- Python 3.6+
- NumPy 1.15+
- Pandas 0.24+

If you encounter issues with newer versions, try:

```bash
# Install specific versions
pip install numpy==1.19.5 pandas==1.2.0
```

## Development Installation

If you plan to modify or contribute to lifeActuary:

```bash
# Clone the repository
git clone https://github.com/parcr/lifeactuary.git
cd lifeactuary

# Create development environment
python -m venv dev_env
source dev_env/bin/activate  # or dev_env\Scripts\activate on Windows

# Install in development mode
pip install -e .

# Install additional development dependencies (if any)
pip install pytest pytest-cov sphinx
```

## Next Steps

Once installed, proceed to:
1. [Quick Start Guide](quick-start.md) - Learn basic usage
2. [Tutorials](tutorials.md) - Work through detailed examples
3. [API Reference](../api/mortality_table.md) - Explore all available functions

## Getting Help

If you encounter installation issues:

1. Check the [GitHub Issues](https://github.com/parcr/lifeactuary/issues)
2. Verify your Python and dependency versions
3. Try the troubleshooting steps above
4. Create a new issue with your error details and system information