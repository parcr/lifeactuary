# Basic Examples

This page provides practical examples of common actuarial calculations using lifeActuary.

## Example 1: Individual Life Insurance Pricing

Let's calculate the premium for a $500,000 20-year term life insurance policy for a 35-year-old.

```python
from lifeActuary.mortality_table import MortalityTable
from lifeActuary import mortality_insurance, annuities

# Create a realistic mortality table (simplified)
ages = list(range(0, 101))
qx_values = [0] + [0.001 * (1.07 ** max(0, (i-25))) for i in range(1, 101)]
qx_values[-1] = 1.0  # Ensure last value is 1.0

mt = MortalityTable(data_type='q', mt=qx_values)

# Policy parameters
age = 35
term = 20
coverage = 500000
interest_rate = 4  # 4% annual interest

# Calculate expected present value of benefits
insurance_epv = mortality_insurance.Axt(mt, x=age, t=term, i=interest_rate)
total_benefit_cost = coverage * insurance_epv

# Calculate present value of premium annuity
premium_annuity = annuities.axt(mt, x=age, t=term, i=interest_rate)

# Calculate level annual premium
level_premium = total_benefit_cost / premium_annuity

print(f"20-Year Term Life Insurance Analysis (Age {age})")
print(f"Coverage Amount: ${coverage:,}")
print(f"Insurance EPV factor: {insurance_epv:.6f}")
print(f"Premium annuity factor: {premium_annuity:.4f}")
print(f"Level annual premium: ${level_premium:.2f}")
print(f"Monthly premium: ${level_premium/12:.2f}")

# Add expense loading
expense_loading = 0.15  # 15% for expenses and profit
loaded_premium = level_premium * (1 + expense_loading)
print(f"Loaded annual premium: ${loaded_premium:.2f}")
print(f"Loaded monthly premium: ${loaded_premium/12:.2f}")
```

## Example 2: Retirement Income Planning

Calculate required savings for retirement income and compare payout options.

```python
# Retirement planning scenario
current_age = 30
retirement_age = 65
target_annual_income = 75000  # Desired annual retirement income
current_savings = 50000      # Current retirement savings
expected_return = 6          # Expected annual return

# Calculate required capital at retirement
retirement_annuity_factor = annuities.ax(mt, x=retirement_age, i=expected_return)
required_capital = target_annual_income / retirement_annuity_factor

print(f"Retirement Planning Analysis")
print(f"Target retirement income: ${target_annual_income:,}")
print(f"Required capital at retirement: ${required_capital:,.0f}")

# Calculate required annual savings
from lifeActuary import annuities_certain
years_to_retirement = retirement_age - current_age

# Future value of current savings
future_value_current = current_savings * (1 + expected_return/100) ** years_to_retirement

# Required additional capital
additional_capital_needed = required_capital - future_value_current

# Future value annuity factor for savings
savings_fv_factor = annuities_certain.future_value_annuity(n=years_to_retirement, i=expected_return)
required_annual_savings = additional_capital_needed / savings_fv_factor

print(f"Current savings: ${current_savings:,}")
print(f"Future value of current savings: ${future_value_current:,.0f}")
print(f"Additional capital needed: ${additional_capital_needed:,.0f}")
print(f"Required annual savings: ${required_annual_savings:,.0f}")
print(f"Required monthly savings: ${required_annual_savings/12:,.0f}")

# Compare payout options at retirement
print(f"\nRetirement Payout Options:")

# Life annuity
life_annuity_income = required_capital / retirement_annuity_factor
print(f"Life annuity: ${life_annuity_income:,.0f} annually")

# 20-year certain annuity
certain_20_factor = annuities_certain.annuity_certain(n=20, i=expected_return)
certain_20_income = required_capital / certain_20_factor
print(f"20-year certain: ${certain_20_income:,.0f} annually")

# 4% withdrawal rule
withdrawal_rule_income = required_capital * 0.04
print(f"4% withdrawal rule: ${withdrawal_rule_income:,.0f} annually")
```

## Example 3: Pension Plan Comparison

Compare different pension options for a married couple.

```python
from lifeActuary import life_2heads

# Create mortality tables for male and female
# Female mortality typically 20% lower than male
mt_male = mt  # Use the same table as above
mt_female_qx = [q * 0.8 if q < 1.0 else 1.0 for q in qx_values]
mt_female = MortalityTable(data_type='q', mt=mt_female_qx)

# Couple information
husband_age = 65
wife_age = 62
pension_rate = 4  # 4% discount rate
monthly_pension_base = 4000  # Base monthly pension

print(f"Pension Option Analysis")
print(f"Husband age: {husband_age}, Wife age: {wife_age}")
print(f"Base monthly pension: ${monthly_pension_base:,}")

# Option 1: Single life annuity (husband only)
husband_annuity = annuities.ax(mt_male, x=husband_age, i=pension_rate, m=12)
option1_value = monthly_pension_base * husband_annuity
option1_monthly = monthly_pension_base

print(f"\nOption 1 - Single Life (Husband):")
print(f"Monthly payment: ${option1_monthly:,}")
print(f"Present value: ${option1_value:,.0f}")

# Option 2: Joint and 50% survivor
joint_annuity = life_2heads.ax_2heads(mt_male, mt_female, husband_age, wife_age, i=pension_rate, m=12)
survivor_annuity = life_2heads.ax_2heads_ls(mt_male, mt_female, husband_age, wife_age, i=pension_rate, m=12)

# 50% survivor means wife gets 50% after husband dies
# This is approximately: full benefit while both alive + 50% of benefit for survivor period
option2_factor = joint_annuity + 0.5 * (survivor_annuity - joint_annuity)
option2_monthly = option1_value / option2_factor
option2_value = option1_value  # Same present value

print(f"\nOption 2 - Joint & 50% Survivor:")
print(f"Monthly payment (while both alive): ${option2_monthly:,.0f}")
print(f"Monthly payment (survivor): ${option2_monthly * 0.5:,.0f}")
print(f"Present value: ${option2_value:,.0f}")

# Option 3: Joint and 100% survivor
option3_factor = survivor_annuity
option3_monthly = option1_value / option3_factor
option3_value = option1_value

print(f"\nOption 3 - Joint & 100% Survivor:")
print(f"Monthly payment: ${option3_monthly:,.0f}")
print(f"Present value: ${option3_value:,.0f}")

# Calculate life expectancies for context
husband_le = mt_male.ex(husband_age)
wife_le = mt_female.ex(wife_age)
joint_le = husband_le  # Approximate
survivor_le = max(husband_le, wife_le)  # Approximate

print(f"\nLife Expectancies (approximate):")
print(f"Husband: {husband_le:.1f} years")
print(f"Wife: {wife_le:.1f} years")
print(f"Expected total payments:")
print(f"  Option 1: ${option1_monthly * 12 * husband_le:,.0f}")
print(f"  Option 2: ${(option2_monthly * 12 * joint_le + option2_monthly * 0.5 * 12 * max(0, survivor_le - joint_le)):,.0f}")
print(f"  Option 3: ${option3_monthly * 12 * survivor_le:,.0f}")
```

## Example 4: Life Insurance Needs Analysis

Determine life insurance needs for a family.

```python
# Family financial situation
primary_earner_age = 35
spouse_age = 33
annual_income = 100000
annual_expenses = 75000
years_until_retirement = 30
years_of_income_replacement = 10  # Years of income needed for family
mortgage_balance = 350000
education_fund_needed = 200000  # College costs for children
final_expenses = 25000

print(f"Life Insurance Needs Analysis")
print(f"Primary earner age: {primary_earner_age}")
print(f"Annual income: ${annual_income:,}")

# Method 1: Human Life Value
discount_rate = 4
income_growth_rate = 2

# Present value of future earnings
net_annual_contribution = annual_income - annual_expenses
human_life_value = 0

for year in range(1, years_until_retirement + 1):
    future_income = net_annual_contribution * (1 + income_growth_rate/100) ** year
    present_value = future_income / (1 + discount_rate/100) ** year
    human_life_value += present_value

print(f"\nMethod 1 - Human Life Value:")
print(f"Net annual contribution: ${net_annual_contribution:,}")
print(f"Present value of future contributions: ${human_life_value:,.0f}")

# Method 2: Needs-based approach
immediate_needs = mortgage_balance + education_fund_needed + final_expenses

# Income replacement fund
income_replacement_annuity = annuities_certain.annuity_certain(n=years_of_income_replacement, i=discount_rate)
income_replacement_fund = net_annual_contribution * income_replacement_annuity

total_needs = immediate_needs + income_replacement_fund

print(f"\nMethod 2 - Needs-Based Approach:")
print(f"Immediate needs:")
print(f"  Mortgage payoff: ${mortgage_balance:,}")
print(f"  Education fund: ${education_fund_needed:,}")
print(f"  Final expenses: ${final_expenses:,}")
print(f"  Subtotal: ${immediate_needs:,}")
print(f"Income replacement fund: ${income_replacement_fund:,.0f}")
print(f"Total insurance needed: ${total_needs:,.0f}")

# Calculate premium for needed coverage
insurance_needed = max(human_life_value, total_needs)
term_length = 20

# Premium calculation
insurance_epv = mortality_insurance.Axt(mt, x=primary_earner_age, t=term_length, i=discount_rate)
premium_annuity = annuities.axt(mt, x=primary_earner_age, t=term_length, i=discount_rate)
annual_premium = insurance_needed * insurance_epv / premium_annuity

print(f"\nInsurance Premium Calculation:")
print(f"Recommended coverage: ${insurance_needed:,.0f}")
print(f"{term_length}-year term premium: ${annual_premium:,.0f} annually")
print(f"Monthly premium: ${annual_premium/12:,.0f}")
print(f"Premium as % of income: {annual_premium/annual_income*100:.1f}%")
```

## Example 5: Immediate Annuity Purchase

Compare immediate annuity options for a retiree.

```python
# Retiree considering immediate annuity purchase
retiree_age = 70
purchase_amount = 250000  # Amount available for annuity purchase
interest_rate = 3  # Current interest environment

print(f"Immediate Annuity Analysis")
print(f"Age: {retiree_age}")
print(f"Purchase amount: ${purchase_amount:,}")

# Option 1: Life annuity
life_annuity_factor = annuities.ax(mt, x=retiree_age, i=interest_rate)
life_annual_payment = purchase_amount / life_annuity_factor
life_monthly_payment = life_annual_payment / 12

print(f"\nOption 1 - Life Annuity:")
print(f"Annual payment: ${life_annual_payment:,.0f}")
print(f"Monthly payment: ${life_monthly_payment:,.0f}")

# Option 2: Life annuity with 10-year certain
certain_10_factor = annuities_certain.annuity_certain(n=10, i=interest_rate)
life_after_10_factor = annuities.nax(mt, x=retiree_age, n=10, i=interest_rate)
life_10_certain_factor = certain_10_factor + life_after_10_factor
life_10_certain_payment = purchase_amount / life_10_certain_factor
life_10_certain_monthly = life_10_certain_payment / 12

print(f"\nOption 2 - Life with 10-Year Certain:")
print(f"Annual payment: ${life_10_certain_payment:,.0f}")
print(f"Monthly payment: ${life_10_certain_monthly:,.0f}")

# Option 3: 20-year certain annuity
certain_20_factor = annuities_certain.annuity_certain(n=20, i=interest_rate)
certain_20_payment = purchase_amount / certain_20_factor
certain_20_monthly = certain_20_payment / 12

print(f"\nOption 3 - 20-Year Certain:")
print(f"Annual payment: ${certain_20_payment:,.0f}")
print(f"Monthly payment: ${certain_20_monthly:,.0f}")

# Analysis
life_expectancy = mt.ex(retiree_age)
breakeven_years = purchase_amount / life_annual_payment

print(f"\nAnalysis:")
print(f"Life expectancy: {life_expectancy:.1f} years")
print(f"Breakeven point (life annuity): {breakeven_years:.1f} years")

# Total payments if live to life expectancy
total_life_payments = life_annual_payment * life_expectancy
total_10_certain_payments = life_10_certain_payment * life_expectancy
total_20_certain_payments = certain_20_payment * min(20, life_expectancy)

print(f"Total payments if live to life expectancy:")
print(f"  Life annuity: ${total_life_payments:,.0f}")
print(f"  Life with 10-certain: ${total_10_certain_payments:,.0f}")
print(f"  20-year certain: ${total_20_certain_payments:,.0f}")

# Risk analysis
prob_live_10 = mt.npx(retiree_age, 10)
prob_live_20 = mt.npx(retiree_age, 20)

print(f"\nRisk Analysis:")
print(f"Probability of living 10+ years: {prob_live_10:.3f}")
print(f"Probability of living 20+ years: {prob_live_20:.3f}")
```

## Example 6: Group Life Insurance

Calculate group life insurance premiums for a small company.

```python
# Employee data
employees = [
    {'age': 28, 'salary': 45000},
    {'age': 34, 'salary': 65000},
    {'age': 41, 'salary': 80000},
    {'age': 29, 'salary': 50000},
    {'age': 52, 'salary': 95000},
    {'age': 38, 'salary': 70000},
    {'age': 45, 'salary': 85000},
    {'age': 31, 'salary': 55000},
]

# Group insurance parameters
coverage_multiple = 2.0  # 2x annual salary
group_interest_rate = 4
expense_loading = 0.25  # 25% loading for expenses

print(f"Group Life Insurance Premium Calculation")
print(f"Coverage: {coverage_multiple}x annual salary")
print(f"Number of employees: {len(employees)}")

total_coverage = 0
total_premium = 0

print(f"\nEmployee Details:")
print(f"Age | Salary    | Coverage   | Annual Premium")
print(f"-" * 50)

for emp in employees:
    age = emp['age']
    salary = emp['salary']
    coverage = salary * coverage_multiple
    
    # Calculate individual premium
    insurance_epv = mortality_insurance.Ax(mt, x=age, i=group_interest_rate)
    base_premium = coverage * insurance_epv
    loaded_premium = base_premium * (1 + expense_loading)
    
    total_coverage += coverage
    total_premium += loaded_premium
    
    print(f"{age:2d}  | ${salary:7,} | ${coverage:9,.0f} | ${loaded_premium:11.2f}")

average_age = sum(emp['age'] for emp in employees) / len(employees)
average_premium_rate = total_premium / total_coverage * 1000  # Per $1000 of coverage

print(f"\nGroup Summary:")
print(f"Total coverage: ${total_coverage:,}")
print(f"Total annual premium: ${total_premium:,.2f}")
print(f"Average age: {average_age:.1f}")
print(f"Average premium rate: ${average_premium_rate:.2f} per $1,000")
print(f"Monthly premium per employee: ${total_premium/12/len(employees):.2f}")

# Compare to simplified group rate
group_insurance_epv = mortality_insurance.Ax(mt, x=int(average_age), i=group_interest_rate)
simplified_total_premium = total_coverage * group_insurance_epv * (1 + expense_loading)

print(f"\nComparison to simplified group rate:")
print(f"Individual calculation: ${total_premium:,.2f}")
print(f"Simplified group rate: ${simplified_total_premium:,.2f}")
print(f"Difference: ${abs(total_premium - simplified_total_premium):,.2f}")
```

These examples demonstrate practical applications of lifeActuary for common actuarial problems. Each example includes realistic assumptions and shows how to interpret the results in business contexts.