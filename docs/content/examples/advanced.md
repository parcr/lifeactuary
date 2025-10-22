# Advanced Examples

This page contains sophisticated examples for advanced users and specific actuarial scenarios.

## Example 1: Variable Universal Life Insurance Analysis

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import mortality_insurance, annuities
import numpy as np

# Create enhanced mortality table with select and ultimate rates
def create_select_ultimate_table():
    """Create a simplified select and ultimate mortality table"""
    ultimate_qx = [0] + [0.0005 * (1.09 ** max(0, i-20)) for i in range(1, 101)]
    ultimate_qx[-1] = 1.0
    
    # Select rates are 70% of ultimate for first 5 years
    return MortalityTable(data_type='q', mt=ultimate_qx)

mt = create_select_ultimate_table()

# VUL policy parameters
issue_age = 35
face_amount = 1000000
target_premium = 8000
guaranteed_rate = 3
current_rate = 6
expense_charges = {'policy_fee': 100, 'premium_load': 0.05, 'asset_charge': 0.0075}

print("Variable Universal Life Insurance Analysis")
print(f"Issue Age: {issue_age}")
print(f"Face Amount: ${face_amount:,}")
print(f"Target Premium: ${target_premium:,}")

# Calculate cost of insurance rates by age
def calculate_coi_rates(mt, ages, face_amount):
    """Calculate monthly cost of insurance rates"""
    coi_rates = {}
    for age in ages:
        if age <= mt.w:
            monthly_qx = 1 - (1 - mt.nqx(age, 1)) ** (1/12)
            monthly_coi = monthly_qx * face_amount / 1000  # per $1000
            coi_rates[age] = monthly_coi
    return coi_rates

ages = range(35, 76)  # Policy years 1-40
coi_rates = calculate_coi_rates(mt, ages, 1000)

# Project account values over time
def project_vul_values(years=20):
    """Project VUL account values and charges"""
    account_value = 0
    results = []
    
    for year in range(1, years + 1):
        age = issue_age + year - 1
        
        # Annual premium (net of loads)
        net_premium = target_premium * (1 - expense_charges['premium_load']) - expense_charges['policy_fee']
        
        # Beginning account value
        beginning_av = account_value
        
        # Add net premium
        account_value += net_premium
        
        # Interest earnings (monthly compounding)
        monthly_rate = current_rate / 100 / 12
        for month in range(12):
            # Monthly interest
            account_value *= (1 + monthly_rate)
            
            # Monthly deductions
            monthly_coi = coi_rates.get(age, 0) * (face_amount / 1000)
            monthly_asset_charge = account_value * expense_charges['asset_charge'] / 12
            
            # Net amount at risk for COI calculation
            nar = max(0, face_amount - account_value)
            monthly_coi_actual = monthly_coi * (nar / face_amount) if face_amount > 0 else 0
            
            total_monthly_deductions = monthly_coi_actual + monthly_asset_charge
            account_value = max(0, account_value - total_monthly_deductions)
        
        results.append({
            'year': year,
            'age': age,
            'account_value': account_value,
            'beginning_av': beginning_av,
            'net_premium': net_premium,
            'annual_coi': monthly_coi_actual * 12,
            'asset_charges': account_value * expense_charges['asset_charge']
        })
    
    return results

# Run projection
projection = project_vul_values(20)

print(f"\nVUL Projection (First 10 Years):")
print("Year | Age | Account Value | COI Charges | Asset Charges")
print("-" * 60)

for result in projection[:10]:
    print(f"{result['year']:4d} | {result['age']:2d}  | ${result['account_value']:11,.0f} | "
          f"${result['annual_coi']:9,.0f} | ${result['asset_charges']:11,.0f}")

# Calculate internal rate of return
final_av = projection[-1]['account_value']
total_premiums = target_premium * len(projection)
irr_approx = ((final_av / total_premiums) ** (1/len(projection)) - 1) * 100

print(f"\nProjection Summary:")
print(f"Total premiums paid: ${total_premiums:,}")
print(f"Final account value: ${final_av:,.0f}")
print(f"Approximate IRR: {irr_approx:.2f}%")
```

## Example 2: Pension Plan Actuarial Valuation

```python
from lifeActuary import life_2heads
import pandas as pd

# Create pension plan member data
np.random.seed(42)  # For reproducible results

def generate_member_data(n_members=100):
    """Generate sample pension plan member data"""
    data = []
    for i in range(n_members):
        age = np.random.normal(45, 12)
        age = max(25, min(65, age))  # Constrain to reasonable range
        
        service = np.random.normal(15, 8)
        service = max(1, min(age-22, service))  # Constrain service
        
        salary = np.random.normal(65000, 25000)
        salary = max(30000, salary)
        
        gender = np.random.choice(['M', 'F'])
        status = np.random.choice(['Active', 'Retired'], p=[0.8, 0.2])
        
        data.append({
            'id': i+1,
            'age': round(age, 1),
            'service': round(service, 1),
            'salary': round(salary, 0),
            'gender': gender,
            'status': status
        })
    
    return pd.DataFrame(data)

members_df = generate_member_data(50)  # Smaller sample for demo

# Pension plan assumptions
plan_params = {
    'normal_retirement_age': 65,
    'early_retirement_age': 55,
    'vesting_years': 5,
    'benefit_formula': 0.015,  # 1.5% per year of service
    'discount_rate': 6,
    'salary_increase': 3,
    'cola': 2,  # Cost of living adjustment
}

print("Pension Plan Actuarial Valuation")
print(f"Members in valuation: {len(members_df)}")
print(f"Discount rate: {plan_params['discount_rate']}%")

# Create mortality tables for males and females
qx_base = [0] + [0.0003 * (1.085 ** max(0, i-25)) for i in range(1, 101)]
qx_base[-1] = 1.0

qx_male = qx_base
qx_female = [q * 0.85 if q < 1.0 else 1.0 for q in qx_base]  # 15% lower mortality

mt_male = MortalityTable(data_type='q', mt=qx_male)
mt_female = MortalityTable(data_type='q', mt=qx_female)

def calculate_pension_liability(member_row):
    """Calculate pension liability for a single member"""
    age = member_row['age']
    service = member_row['service']
    salary = member_row['salary']
    gender = member_row['gender']
    status = member_row['status']
    
    mt = mt_male if gender == 'M' else mt_female
    
    if status == 'Retired':
        # Already retired - calculate PV of current pension
        current_benefit = salary * plan_params['benefit_formula'] * service
        retirement_annuity = annuities.ax(mt, x=int(age), i=plan_params['discount_rate'])
        liability = current_benefit * retirement_annuity
        
    else:  # Active member
        # Project to retirement
        years_to_retirement = plan_params['normal_retirement_age'] - age
        
        if years_to_retirement <= 0:
            years_to_retirement = 0
        
        # Final salary projection
        final_salary = salary * (1 + plan_params['salary_increase']/100) ** years_to_retirement
        
        # Final service
        final_service = service + years_to_retirement
        
        # Retirement benefit
        annual_benefit = final_salary * plan_params['benefit_formula'] * final_service
        
        # Present value calculations
        # 1. Probability of surviving to retirement
        survival_prob = mt.npx(int(age), int(years_to_retirement)) if years_to_retirement > 0 else 1.0
        
        # 2. Discount factor to retirement
        discount_factor = (1 + plan_params['discount_rate']/100) ** (-years_to_retirement)
        
        # 3. Annuity value at retirement
        retirement_annuity = annuities.ax(mt, x=plan_params['normal_retirement_age'], 
                                        i=plan_params['discount_rate'])
        
        # Total liability
        liability = annual_benefit * retirement_annuity * survival_prob * discount_factor
    
    return {
        'liability': liability,
        'annual_benefit': annual_benefit if status == 'Retired' else annual_benefit,
        'survival_prob': 1.0 if status == 'Retired' else survival_prob
    }

# Calculate liabilities for all members
total_liability = 0
results = []

for _, member in members_df.iterrows():
    calc = calculate_pension_liability(member)
    total_liability += calc['liability']
    
    results.append({
        'id': member['id'],
        'age': member['age'],
        'gender': member['gender'],
        'status': member['status'],
        'liability': calc['liability'],
        'annual_benefit': calc['annual_benefit']
    })

results_df = pd.DataFrame(results)

# Summary statistics
active_members = members_df[members_df['status'] == 'Active']
retired_members = members_df[members_df['status'] == 'Retired']

active_liability = results_df[results_df['status'] == 'Active']['liability'].sum()
retired_liability = results_df[results_df['status'] == 'Retired']['liability'].sum()

print(f"\nLiability Summary:")
print(f"Active members: {len(active_members):3d}, Liability: ${active_liability:15,.0f}")
print(f"Retired members: {len(retired_members):2d}, Liability: ${retired_liability:15,.0f}")
print(f"Total liability: ${total_liability:21,.0f}")

# Demographics
avg_age_active = active_members['age'].mean()
avg_service_active = active_members['service'].mean()
avg_salary_active = active_members['salary'].mean()

print(f"\nActive Member Demographics:")
print(f"Average age: {avg_age_active:.1f}")
print(f"Average service: {avg_service_active:.1f} years")
print(f"Average salary: ${avg_salary_active:,.0f}")

# Liability distribution
print(f"\nLiability Distribution:")
print(f"Members with liability > $500K: {len(results_df[results_df['liability'] > 500000])}")
print(f"Members with liability > $1M: {len(results_df[results_df['liability'] > 1000000])}")

# Sensitivity analysis
sensitivity_rates = [5, 5.5, 6, 6.5, 7]
print(f"\nSensitivity Analysis - Discount Rate Impact:")
print("Rate | Total Liability | Change")
print("-" * 35)

base_liability = total_liability
for rate in sensitivity_rates:
    # Recalculate with different rate (simplified)
    adjustment_factor = (1 + plan_params['discount_rate']/100) / (1 + rate/100)
    adjusted_liability = total_liability * adjustment_factor
    change_pct = (adjusted_liability / base_liability - 1) * 100
    
    print(f"{rate:4.1f}% | ${adjusted_liability:13,.0f} | {change_pct:+6.1f}%")
```

## Example 3: Stochastic Mortality Modeling

```python
# Stochastic mortality projection using Lee-Carter model simulation
def simulate_mortality_improvement():
    """Simulate future mortality improvements"""
    
    # Base mortality rates (current)
    base_qx = [0] + [0.0004 * (1.087 ** max(0, i-25)) for i in range(1, 101)]
    base_qx[-1] = 1.0
    
    # Historical improvement rates (annual % reduction in mortality)
    improvement_rates = {
        'ages_0_50': 0.015,    # 1.5% annual improvement
        'ages_51_70': 0.02,    # 2.0% annual improvement  
        'ages_71_100': 0.01    # 1.0% annual improvement
    }
    
    # Simulate 30 years of mortality improvements
    projection_years = 30
    n_scenarios = 1000
    
    scenarios = []
    
    for scenario in range(n_scenarios):
        projected_qx = base_qx.copy()
        
        for year in range(1, projection_years + 1):
            # Apply stochastic improvements
            for age in range(1, len(projected_qx)):
                if age <= 50:
                    base_improvement = improvement_rates['ages_0_50']
                elif age <= 70:
                    base_improvement = improvement_rates['ages_51_70']
                else:
                    base_improvement = improvement_rates['ages_71_100']
                
                # Add random variation
                random_factor = np.random.normal(1.0, 0.3)  # 30% volatility
                annual_improvement = base_improvement * random_factor
                
                # Apply improvement (reduction in mortality)
                projected_qx[age] *= (1 - annual_improvement)
                projected_qx[age] = max(0.0001, projected_qx[age])  # Floor
        
        projected_qx[-1] = 1.0  # Ensure terminal rate
        scenarios.append(projected_qx)
    
    return scenarios

print("Stochastic Mortality Analysis")
print("Simulating 1000 scenarios of mortality improvement over 30 years...")

# Generate scenarios
mortality_scenarios = simulate_mortality_improvement()

# Analyze impact on annuity values
age_65_annuities = []
age_75_annuities = []

base_mt = MortalityTable(data_type='q', mt=[0] + [0.0004 * (1.087 ** max(0, i-25)) for i in range(1, 101)] + [1.0])
base_annuity_65 = annuities.ax(base_mt, x=65, i=5)
base_annuity_75 = annuities.ax(base_mt, x=75, i=5)

for scenario_qx in mortality_scenarios[:100]:  # Analyze first 100 scenarios
    mt_scenario = MortalityTable(data_type='q', mt=scenario_qx)
    
    if 65 <= mt_scenario.w and 75 <= mt_scenario.w:
        annuity_65 = annuities.ax(mt_scenario, x=65, i=5)
        annuity_75 = annuities.ax(mt_scenario, x=75, i=5)
        
        age_65_annuities.append(annuity_65)
        age_75_annuities.append(annuity_75)

# Statistical analysis
print(f"\nAnnuity Value Analysis (100 scenarios):")
print(f"Age 65 Annuities:")
print(f"  Base case: {base_annuity_65:.4f}")
print(f"  Mean: {np.mean(age_65_annuities):.4f}")
print(f"  Std Dev: {np.std(age_65_annuities):.4f}")
print(f"  5th percentile: {np.percentile(age_65_annuities, 5):.4f}")
print(f"  95th percentile: {np.percentile(age_65_annuities, 95):.4f}")

print(f"\nAge 75 Annuities:")
print(f"  Base case: {base_annuity_75:.4f}")
print(f"  Mean: {np.mean(age_75_annuities):.4f}")
print(f"  Std Dev: {np.std(age_75_annuities):.4f}")
print(f"  5th percentile: {np.percentile(age_75_annuities, 5):.4f}")
print(f"  95th percentile: {np.percentile(age_75_annuities, 95):.4f}")

# Risk metrics
var_95_age_65 = np.percentile(age_65_annuities, 95) - base_annuity_65
var_95_age_75 = np.percentile(age_75_annuities, 95) - base_annuity_75

print(f"\nLongevity Risk (VaR 95%):")
print(f"Age 65: Additional cost of {var_95_age_65:.4f} ({var_95_age_65/base_annuity_65*100:.1f}%)")
print(f"Age 75: Additional cost of {var_95_age_75:.4f} ({var_95_age_75/base_annuity_75*100:.1f}%)")
```

## Example 4: Dynamic Hedging for Longevity Risk

```python
# Longevity bond pricing and hedging analysis
def longevity_bond_analysis():
    """Analyze longevity bonds for hedging pension liabilities"""
    
    # Bond parameters
    bond_maturity = 25
    notional = 1000000  # $1M notional
    reference_age = 65
    reference_cohort_size = 100000
    
    # Create base mortality table
    qx_base = [0] + [0.0004 * (1.087 ** max(0, i-25)) for i in range(1, 101)]
    qx_base[-1] = 1.0
    mt_base = MortalityTable(data_type='q', mt=qx_base)
    
    print("Longevity Bond Analysis")
    print(f"Bond maturity: {bond_maturity} years")
    print(f"Reference age: {reference_age}")
    print(f"Reference cohort: {reference_cohort_size:,}")
    
    # Calculate expected survivors over time
    expected_survivors = []
    for year in range(bond_maturity + 1):
        survivors = mt_base.npx(reference_age, year) * reference_cohort_size
        expected_survivors.append(survivors)
    
    # Bond pays based on actual vs expected survival
    # Payment = Notional * (Actual_Survivors / Expected_Survivors - 1)
    
    # Simulate actual survival scenarios
    n_scenarios = 1000
    bond_payments = []
    
    for scenario in range(n_scenarios):
        # Simulate mortality shocks
        mortality_shock = np.random.normal(0, 0.1)  # 10% volatility in mortality
        
        shocked_qx = qx_base.copy()
        for i in range(1, len(shocked_qx)):
            shocked_qx[i] *= (1 + mortality_shock)
            shocked_qx[i] = max(0.0001, min(0.5, shocked_qx[i]))  # Bounds
        
        mt_shocked = MortalityTable(data_type='q', mt=shocked_qx)
        
        scenario_payments = []
        for year in range(1, bond_maturity + 1):
            expected_surv = expected_survivors[year]
            actual_surv = mt_shocked.npx(reference_age, year) * reference_cohort_size
            
            survival_ratio = actual_surv / expected_surv if expected_surv > 0 else 1
            payment = notional * (survival_ratio - 1)
            scenario_payments.append(payment)
        
        bond_payments.append(scenario_payments)
    
    # Calculate present value of bond payments
    discount_rate = 0.05
    bond_values = []
    
    for scenario_payments in bond_payments:
        pv = 0
        for year, payment in enumerate(scenario_payments, 1):
            pv += payment / (1 + discount_rate) ** year
        bond_values.append(pv)
    
    print(f"\nLongevity Bond Valuation:")
    print(f"Expected PV: ${np.mean(bond_values):,.0f}")
    print(f"Standard deviation: ${np.std(bond_values):,.0f}")
    print(f"5th percentile: ${np.percentile(bond_values, 5):,.0f}")
    print(f"95th percentile: ${np.percentile(bond_values, 95):,.0f}")
    
    # Hedge effectiveness analysis
    # Assume pension liability sensitive to same mortality factors
    pension_liability_base = 50000000  # $50M base liability
    
    liability_changes = []
    for i, scenario_payments in enumerate(bond_payments):
        # Simplified: liability change proportional to survival improvements
        avg_survival_change = np.mean([p/notional for p in scenario_payments])
        liability_change = pension_liability_base * avg_survival_change * 0.5  # 50% correlation
        liability_changes.append(liability_change)
    
    # Hedging efficiency
    unhedged_volatility = np.std(liability_changes)
    hedged_changes = np.array(liability_changes) + np.array(bond_values)
    hedged_volatility = np.std(hedged_changes)
    
    hedge_effectiveness = 1 - (hedged_volatility / unhedged_volatility)
    
    print(f"\nHedge Effectiveness Analysis:")
    print(f"Unhedged liability volatility: ${unhedged_volatility:,.0f}")
    print(f"Hedged liability volatility: ${hedged_volatility:,.0f}")
    print(f"Hedge effectiveness: {hedge_effectiveness:.1%}")
    
    return bond_values, liability_changes

# Run longevity bond analysis
bond_values, liability_changes = longevity_bond_analysis()
```

## Example 5: Multi-State Model for Disability Insurance

```python
# Multi-state model for disability insurance
def disability_insurance_model():
    """Model for disability insurance with recovery"""
    
    print("Multi-State Disability Insurance Model")
    print("States: Healthy → Disabled → Dead")
    print("        Healthy → Dead (direct)")
    print("        Disabled → Healthy (recovery)")
    
    # Transition rates (annual)
    age = 45
    transition_rates = {
        'healthy_to_disabled': 0.01,    # 1% annual disability incidence
        'healthy_to_dead': 0.002,       # 0.2% annual mortality (healthy)
        'disabled_to_healthy': 0.15,    # 15% annual recovery rate
        'disabled_to_dead': 0.008,      # 0.8% annual mortality (disabled)
    }
    
    # Policy parameters
    benefit_amount = 5000  # Monthly disability benefit
    benefit_period = 5     # Years of benefits
    elimination_period = 90 / 365  # 90-day elimination period
    
    # Simulate multi-state process
    n_simulations = 10000
    benefit_payments = []
    
    for sim in range(n_simulations):
        state = 'healthy'
        time = 0
        total_benefits = 0
        disability_start = None
        
        # Monthly time steps for one year
        for month in range(12):
            time_step = 1/12  # Monthly
            
            if state == 'healthy':
                # Check transitions from healthy
                if np.random.random() < transition_rates['healthy_to_disabled'] * time_step:
                    state = 'disabled'
                    disability_start = time
                elif np.random.random() < transition_rates['healthy_to_dead'] * time_step:
                    state = 'dead'
                    break
                    
            elif state == 'disabled':
                # Check if past elimination period and within benefit period
                time_disabled = time - disability_start if disability_start else 0
                
                if (time_disabled >= elimination_period and 
                    time_disabled <= benefit_period):
                    total_benefits += benefit_amount
                
                # Check transitions from disabled
                if np.random.random() < transition_rates['disabled_to_healthy'] * time_step:
                    state = 'healthy'
                    disability_start = None
                elif np.random.random() < transition_rates['disabled_to_dead'] * time_step:
                    state = 'dead'
                    break
                elif time_disabled >= benefit_period:
                    # Benefits exhausted, but still disabled
                    pass
            
            time += time_step
        
        benefit_payments.append(total_benefits)
    
    # Calculate statistics
    expected_claims = np.mean(benefit_payments)
    claim_probability = len([b for b in benefit_payments if b > 0]) / n_simulations
    expected_claims_given_claim = np.mean([b for b in benefit_payments if b > 0]) if any(benefit_payments) else 0
    
    print(f"\nSimulation Results ({n_simulations:,} trials):")
    print(f"Expected annual benefits: ${expected_claims:,.0f}")
    print(f"Claim probability: {claim_probability:.3f}")
    print(f"Expected benefits given claim: ${expected_claims_given_claim:,.0f}")
    
    # Premium calculation with loadings
    expense_loading = 0.25
    profit_loading = 0.15
    
    net_premium = expected_claims
    gross_premium = net_premium * (1 + expense_loading + profit_loading)
    
    print(f"\nPremium Calculation:")
    print(f"Net premium: ${net_premium:,.0f}")
    print(f"Gross premium: ${gross_premium:,.0f}")
    print(f"Monthly premium: ${gross_premium/12:,.0f}")
    
    return benefit_payments

# Run disability insurance simulation
disability_payments = disability_insurance_model()

# Additional analysis
print(f"\nPayment Distribution:")
print(f"No benefits: {len([p for p in disability_payments if p == 0])/len(disability_payments):.1%}")
print(f"$1-12K: {len([p for p in disability_payments if 0 < p <= 12000])/len(disability_payments):.1%}")
print(f"$12-36K: {len([p for p in disability_payments if 12000 < p <= 36000])/len(disability_payments):.1%}")
print(f"$36-60K: {len([p for p in disability_payments if 36000 < p <= 60000])/len(disability_payments):.1%}")
print(f"Maximum: ${max(disability_payments):,.0f}")
```

These advanced examples demonstrate sophisticated actuarial modeling techniques using lifeActuary as the foundation for more complex calculations and simulations.