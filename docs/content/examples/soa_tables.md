# SOA Tables

This page demonstrates how to work with Society of Actuaries (SOA) mortality tables in lifeActuary.

## Overview

The SOA provides standard mortality tables used throughout the insurance industry. lifeActuary includes support for reading and using these tables through the XML format provided by the SOA.

## Available SOA Tables

The `soa_tables` folder includes several standard mortality tables:

### U.S. Tables
- **CSO_1941.xml** - 1941 Commissioners Standard Ordinary
- **CSO_1958.xml** - 1958 Commissioners Standard Ordinary  
- **CSO_1980.xml** - 1980 Commissioners Standard Ordinary

### Group Tables
- **GAM71.xml** - 1971 Group Annuity Mortality
- **GAM83.xml** - 1983 Group Annuity Mortality

### International Tables
- **AF80.xml** - French Assured Lives 1980
- **AM80.xml** - French Assured Lives 1980 (Male)
- **GRF95.xml** - German Population 1995 (Female)
- **GRM95.xml** - German Population 1995 (Male)

### Portuguese Tables
- **197982PortugalMale.xml** - Portugal 1979-82 Male
- **197982PortugalFemale.xml** - Portugal 1979-82 Female

## Loading SOA Tables

### Basic Loading

```python
from soa_tables.read_soa_table_xml import SoaTable
from lifeActuary.mortality_table import MortalityTable

# Load a specific SOA table
try:
    # Load CSO 1941 table
    cso_1941 = SoaTable('soa_tables/CSO_1941.xml')
    
    # Create lifeActuary mortality table
    mt_cso = MortalityTable(data_type='q', mt=cso_1941.qx)
    
    print("CSO 1941 Table Information:")
    print(f"Description: {cso_1941.description}")
    print(f"Age range: {cso_1941.min_age} to {cso_1941.max_age}")
    print(f"Number of ages: {len(cso_1941.qx)}")
    
except FileNotFoundError:
    print("SOA tables not found. Please download from GitHub repository.")
except Exception as e:
    print(f"Error loading table: {e}")
```

### Loading Multiple Tables

```python
import os

def load_all_soa_tables():
    """Load all available SOA tables"""
    soa_tables = {}
    soa_folder = 'soa_tables'
    
    if not os.path.exists(soa_folder):
        print("SOA tables folder not found. Please download from GitHub.")
        return {}
    
    # Get all XML files in the SOA tables folder
    xml_files = [f for f in os.listdir(soa_folder) if f.endswith('.xml')]
    
    for xml_file in xml_files:
        try:
            table_path = os.path.join(soa_folder, xml_file)
            soa_table = SoaTable(table_path)
            mt = MortalityTable(data_type='q', mt=soa_table.qx)
            
            table_name = xml_file.replace('.xml', '')
            soa_tables[table_name] = {
                'soa_table': soa_table,
                'mortality_table': mt,
                'description': soa_table.description,
                'age_range': (soa_table.min_age, soa_table.max_age)
            }
            
            print(f"Loaded: {table_name}")
            
        except Exception as e:
            print(f"Failed to load {xml_file}: {e}")
    
    return soa_tables

# Load all tables
all_tables = load_all_soa_tables()
print(f"\nLoaded {len(all_tables)} SOA tables")
```

## Table Analysis and Comparison

### Comparing Different Tables

```python
from lifeActuary import annuities

def compare_soa_tables(tables_dict, ages=[30, 40, 50, 60, 70]):
    """Compare annuity values across different SOA tables"""
    
    if not tables_dict:
        print("No tables loaded for comparison")
        return
    
    interest_rate = 5  # 5% interest
    
    print(f"Annuity Value Comparison (i={interest_rate}%):")
    print("Age |", end="")
    
    # Print table headers
    table_names = list(tables_dict.keys())[:5]  # Limit to first 5 tables
    for name in table_names:
        print(f" {name[:8]:>8} |", end="")
    print()
    
    print("-" * (6 + len(table_names) * 11))
    
    # Calculate annuities for each age and table
    for age in ages:
        print(f"{age:3d} |", end="")
        
        for table_name in table_names:
            mt = tables_dict[table_name]['mortality_table']
            
            if age <= mt.w:
                annuity_value = annuities.ax(mt, x=age, i=interest_rate)
                print(f" {annuity_value:8.3f} |", end="")
            else:
                print(f" {'N/A':>8} |", end="")
        print()

# Run comparison if tables are loaded
if all_tables:
    compare_soa_tables(all_tables)
```

### Life Expectancy Analysis

```python
def analyze_life_expectancy(tables_dict):
    """Analyze life expectancy across different SOA tables"""
    
    if not tables_dict:
        print("No tables loaded for analysis")
        return
    
    ages_to_analyze = [0, 20, 40, 60, 80]
    
    print("Life Expectancy Analysis:")
    print("Table Name           | Age 0  | Age 20 | Age 40 | Age 60 | Age 80")
    print("-" * 70)
    
    for table_name, table_data in list(tables_dict.items())[:10]:  # Limit output
        mt = table_data['mortality_table']
        print(f"{table_name[:18]:18} |", end="")
        
        for age in ages_to_analyze:
            if age <= mt.w:
                life_exp = mt.ex(age)
                print(f" {life_exp:6.1f} |", end="")
            else:
                print(f" {'N/A':>6} |", end="")
        print()

# Run life expectancy analysis
if all_tables:
    analyze_life_expectancy(all_tables)
```

### Mortality Rate Patterns

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_mortality_patterns(tables_dict, selected_tables=None):
    """Plot mortality rate patterns for selected tables"""
    
    if not tables_dict:
        print("No tables loaded for plotting")
        return
    
    # Select tables to plot
    if selected_tables is None:
        selected_tables = list(tables_dict.keys())[:3]  # First 3 tables
    
    plt.figure(figsize=(12, 8))
    
    for table_name in selected_tables:
        if table_name not in tables_dict:
            continue
            
        soa_table = tables_dict[table_name]['soa_table']
        
        # Get ages and mortality rates
        ages = list(range(soa_table.min_age, soa_table.max_age + 1))
        qx_values = soa_table.qx[soa_table.min_age:]
        
        # Plot on log scale for better visualization
        plt.semilogy(ages, qx_values, label=table_name, linewidth=2)
    
    plt.xlabel('Age')
    plt.ylabel('Mortality Rate (qx)')
    plt.title('Mortality Rate Patterns - SOA Tables')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 100)
    plt.ylim(0.0001, 1.0)
    
    plt.tight_layout()
    plt.show()

# Example plotting (would work in Jupyter notebook)
# if all_tables:
#     plot_mortality_patterns(all_tables, ['CSO_1941', 'GRM95', '197982PortugalMale'])
```

## Practical Applications with SOA Tables

### Insurance Premium Calculation

```python
from lifeActuary import mortality_insurance

def calculate_insurance_premium_soa(table_name, age, coverage_amount, term_years):
    """Calculate insurance premium using SOA table"""
    
    if table_name not in all_tables:
        print(f"Table {table_name} not available")
        return None
    
    mt = all_tables[table_name]['mortality_table']
    interest_rate = 4  # 4% interest assumption
    
    print(f"Insurance Premium Calculation - {table_name}")
    print(f"Age: {age}, Coverage: ${coverage_amount:,}, Term: {term_years} years")
    
    # Calculate EPV of benefits
    if term_years == 'WL':  # Whole life
        insurance_epv = mortality_insurance.Ax(mt, x=age, i=interest_rate)
        premium_annuity = annuities.ax(mt, x=age, i=interest_rate)
    else:  # Term insurance
        insurance_epv = mortality_insurance.Axt(mt, x=age, t=term_years, i=interest_rate)
        premium_annuity = annuities.axt(mt, x=age, t=term_years, i=interest_rate)
    
    # Calculate net premium
    net_annual_premium = (coverage_amount * insurance_epv) / premium_annuity
    
    # Add loadings
    expense_loading = 0.20  # 20% expense loading
    gross_annual_premium = net_annual_premium * (1 + expense_loading)
    
    print(f"Insurance EPV factor: {insurance_epv:.6f}")
    print(f"Premium annuity factor: {premium_annuity:.4f}")
    print(f"Net annual premium: ${net_annual_premium:.2f}")
    print(f"Gross annual premium: ${gross_annual_premium:.2f}")
    print(f"Monthly premium: ${gross_annual_premium/12:.2f}")
    
    return gross_annual_premium

# Example calculations
if all_tables and 'CSO_1941' in all_tables:
    print("Example: Term Life Insurance Premium")
    calculate_insurance_premium_soa('CSO_1941', age=35, coverage_amount=500000, term_years=20)
```

### Pension Annuity Pricing

```python
def price_pension_annuity_soa(table_name, age, monthly_benefit):
    """Price a pension annuity using SOA table"""
    
    if table_name not in all_tables:
        print(f"Table {table_name} not available")
        return None
    
    mt = all_tables[table_name]['mortality_table']
    interest_rate = 3.5  # Lower rate for annuities
    
    print(f"Pension Annuity Pricing - {table_name}")
    print(f"Age: {age}, Monthly Benefit: ${monthly_benefit:,}")
    
    # Calculate present value of monthly annuity
    annual_benefit = monthly_benefit * 12
    annuity_factor = annuities.ax(mt, x=age, i=interest_rate, m=12)
    
    present_value = annual_benefit * annuity_factor
    
    print(f"Annuity factor (monthly): {annuity_factor:.4f}")
    print(f"Present value: ${present_value:,.0f}")
    print(f"Life expectancy: {mt.ex(age):.1f} years")
    
    # Break-even analysis
    life_exp = mt.ex(age)
    total_expected_payments = annual_benefit * life_exp
    
    print(f"Expected total payments: ${total_expected_payments:,.0f}")
    print(f"Break-even years: {present_value / annual_benefit:.1f}")
    
    return present_value

# Example annuity pricing
if all_tables and 'GRM95' in all_tables:
    print("\nExample: Immediate Annuity Pricing")
    price_pension_annuity_soa('GRM95', age=65, monthly_benefit=3000)
```

### International Comparison

```python
def compare_international_tables():
    """Compare mortality between different countries"""
    
    international_tables = {
        'US': 'CSO_1941',
        'Germany_M': 'GRM95',
        'Germany_F': 'GRF95', 
        'Portugal_M': '197982PortugalMale',
        'Portugal_F': '197982PortugalFemale'
    }
    
    available_tables = {k: v for k, v in international_tables.items() 
                       if v in all_tables}
    
    if not available_tables:
        print("No international tables available for comparison")
        return
    
    age = 65
    interest_rate = 4
    
    print(f"International Mortality Comparison (Age {age}):")
    print("Country/Gender    | Life Exp | Annuity Factor | Difference")
    print("-" * 60)
    
    base_annuity = None
    
    for country, table_name in available_tables.items():
        mt = all_tables[table_name]['mortality_table']
        
        if age <= mt.w:
            life_exp = mt.ex(age)
            annuity_factor = annuities.ax(mt, x=age, i=interest_rate)
            
            if base_annuity is None:
                base_annuity = annuity_factor
                difference = 0.0
            else:
                difference = ((annuity_factor / base_annuity) - 1) * 100
            
            print(f"{country:16} | {life_exp:8.1f} | {annuity_factor:12.4f} | {difference:+8.1f}%")

# Run international comparison
if all_tables:
    compare_international_tables()
```

## Advanced SOA Table Features

### Gender-Specific Analysis

```python
def gender_mortality_analysis():
    """Analyze gender differences in mortality"""
    
    male_tables = [name for name in all_tables.keys() 
                   if any(indicator in name.lower() for indicator in ['male', 'm80', 'grm'])]
    female_tables = [name for name in all_tables.keys() 
                     if any(indicator in name.lower() for indicator in ['female', 'f80', 'grf'])]
    
    print("Gender Mortality Analysis:")
    print("Age | Male LE | Female LE | Difference")
    print("-" * 40)
    
    ages = [30, 40, 50, 60, 70, 80]
    
    for age in ages:
        male_le_avg = 0
        female_le_avg = 0
        male_count = 0
        female_count = 0
        
        # Calculate average life expectancy for males
        for table_name in male_tables:
            mt = all_tables[table_name]['mortality_table']
            if age <= mt.w:
                male_le_avg += mt.ex(age)
                male_count += 1
        
        # Calculate average life expectancy for females
        for table_name in female_tables:
            mt = all_tables[table_name]['mortality_table']
            if age <= mt.w:
                female_le_avg += mt.ex(age)
                female_count += 1
        
        if male_count > 0 and female_count > 0:
            male_le_avg /= male_count
            female_le_avg /= female_count
            difference = female_le_avg - male_le_avg
            
            print(f"{age:2d}  | {male_le_avg:7.1f} | {female_le_avg:9.1f} | {difference:+10.1f}")

# Run gender analysis
if all_tables:
    gender_mortality_analysis()
```

### Table Validation

```python
def validate_soa_table(table_name):
    """Validate SOA table for consistency"""
    
    if table_name not in all_tables:
        print(f"Table {table_name} not available")
        return
    
    soa_table = all_tables[table_name]['soa_table']
    mt = all_tables[table_name]['mortality_table']
    
    print(f"Validation Report for {table_name}:")
    print("-" * 40)
    
    # Check mortality rates are reasonable
    max_qx = max(soa_table.qx[1:-1])  # Exclude first and last
    min_qx = min([q for q in soa_table.qx[1:-1] if q > 0])
    
    print(f"Mortality rate range: {min_qx:.6f} to {max_qx:.6f}")
    
    # Check for decreasing mortality (shouldn't happen except infant mortality)
    decreasing_count = 0
    for i in range(10, len(soa_table.qx) - 1):  # Skip infant mortality
        if soa_table.qx[i] > soa_table.qx[i + 1]:
            decreasing_count += 1
    
    print(f"Decreasing mortality instances: {decreasing_count}")
    
    # Check life expectancy at birth vs age 65
    if 0 <= mt.w and 65 <= mt.w:
        le_birth = mt.ex(0)
        le_65 = mt.ex(65)
        print(f"Life expectancy at birth: {le_birth:.1f}")
        print(f"Life expectancy at 65: {le_65:.1f}")
    
    # Check final mortality rate
    print(f"Terminal mortality rate: {soa_table.qx[-1]:.3f}")
    
    print("Validation complete.")

# Validate a table
if all_tables and 'CSO_1941' in all_tables:
    validate_soa_table('CSO_1941')
```

## Usage Tips

1. **Download Required**: SOA tables must be downloaded separately from the GitHub repository
2. **File Format**: Tables are in XML format and require the `read_soa_table_xml.py` module
3. **Age Ranges**: Different tables cover different age ranges - always check `min_age` and `max_age`
4. **Applications**: Use appropriate tables for your specific application (population vs. insured lives)
5. **Updates**: SOA regularly updates tables - ensure you're using current versions for production work
6. **Validation**: Always validate table data before using in critical applications

## Next Steps

- Explore specific tables relevant to your application
- Compare results with published actuarial values
- Consider using multiple tables for sensitivity analysis
- Review SOA documentation for table construction methodology