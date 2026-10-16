import numpy as np
import pandas as pd

# ============================================================
# Employee Dataset Generator
# ============================================================

# Configuration
NUM_RECORDS = 500_000
OUTPUT_FILE = "employee.csv"

# Reproducibility
np.random.seed(42)

# ------------------------------------------------------------
# Reference data
# ------------------------------------------------------------

departments = [
    "Technology",
    "Finance",
    "Human Resources",
    "Sales",
    "Operations"
]

department_probabilities = [0.30, 0.18, 0.12, 0.18, 0.22]

positions_by_department = {
    "Technology": [
        "Software Engineer",
        "Data Analyst",
        "Data Scientist",
        "DevOps Engineer",
        "Systems Analyst",
        "IT Support Specialist",
        "Cybersecurity Analyst",
        "Cloud Engineer",
        "Product Manager",
        "Technology Manager"
    ],
    "Finance": [
        "Financial Analyst",
        "Accountant",
        "Financial Controller",
        "Treasury Analyst",
        "Tax Analyst",
        "Auditor",
        "Finance Manager",
        "Accounts Payable Analyst",
        "Accounts Receivable Analyst"
    ],
    "Human Resources": [
        "HR Analyst",
        "Recruiter",
        "HR Business Partner",
        "Training Specialist",
        "Payroll Analyst",
        "Talent Acquisition Specialist",
        "HR Coordinator",
        "HR Manager"
    ],
    "Sales": [
        "Sales Representative",
        "Account Executive",
        "Sales Analyst",
        "Business Development Representative",
        "Key Account Manager",
        "Sales Coordinator",
        "Sales Manager",
        "Commercial Analyst"
    ],
    "Operations": [
        "Operations Analyst",
        "Operations Coordinator",
        "Logistics Analyst",
        "Process Analyst",
        "Operations Specialist",
        "Quality Analyst",
        "Operations Supervisor",
        "Operations Manager"
    ]
}

seniority_levels = [
    "Intern",
    "Junior",
    "Mid-Level",
    "Senior",
    "Lead",
    "Manager"
]

status_options = [
    "Active",
    "On Leave",
    "Terminated",
    "Resigned",
    "Retired"
]

exit_reasons = [
    "Career Change",
    "Better Opportunity",
    "Low Salary",
    "Relocation",
    "Personal Reasons",
    "Performance",
    "Company Restructuring",
    "Retirement",
    "Health Reasons",
    "End of Contract",
    "N/A"
]

# ------------------------------------------------------------
# Generate basic employee information
# ------------------------------------------------------------

employee_ids = [
    f"EMP{str(i).zfill(7)}"
    for i in range(1, NUM_RECORDS + 1)
]

department = np.random.choice(
    departments,
    size=NUM_RECORDS,
    p=department_probabilities
)

age = np.random.randint(18, 61, size=NUM_RECORDS)

years_at_company = np.random.randint(1, 21, size=NUM_RECORDS)

# ------------------------------------------------------------
# Generate seniority
# ------------------------------------------------------------

seniority = np.empty(NUM_RECORDS, dtype=object)

for i in range(NUM_RECORDS):
    years = years_at_company[i]
    employee_age = age[i]

    if employee_age < 22:
        level = "Intern"
    elif years <= 2:
        level = "Junior"
    elif years <= 6:
        level = "Mid-Level"
    elif years <= 12:
        level = "Senior"
    elif years <= 16:
        level = "Lead"
    else:
        level = "Manager"

    seniority[i] = level

# ------------------------------------------------------------
# Generate positions based on department
# ------------------------------------------------------------

position = np.empty(NUM_RECORDS, dtype=object)

for dept in departments:
    mask = department == dept
    count = mask.sum()

    if count > 0:
        position[mask] = np.random.choice(
            positions_by_department[dept],
            size=count
        )

# ------------------------------------------------------------
# Generate salaries based on seniority
# Salary is represented in BRL
# ------------------------------------------------------------

salary_ranges = {
    "Intern": (1800, 3000),
    "Junior": (3000, 6000),
    "Mid-Level": (5500, 10000),
    "Senior": (9000, 18000),
    "Lead": (15000, 25000),
    "Manager": (18000, 40000)
}

salary = np.zeros(NUM_RECORDS)

for level, (minimum, maximum) in salary_ranges.items():
    mask = seniority == level
    salary[mask] = np.random.uniform(
        minimum,
        maximum,
        mask.sum()
    )

salary = np.round(salary, 2)

# ------------------------------------------------------------
# Performance evaluation
# Scale: 1 to 5
# ------------------------------------------------------------

performance_rating = np.clip(
    np.random.normal(
        loc=3.6,
        scale=0.75,
        size=NUM_RECORDS
    ),
    1,
    5
)

performance_rating = np.round(performance_rating, 1)

# ------------------------------------------------------------
# Absenteeism
# Number of absent days per year
# ------------------------------------------------------------

absenteeism = np.clip(
    np.random.poisson(
        lam=5,
        size=NUM_RECORDS
    ),
    0,
    30
)

# ------------------------------------------------------------
# Promotions
# Number of promotions during employment
# ------------------------------------------------------------

promotions = np.zeros(NUM_RECORDS, dtype=int)

for i in range(NUM_RECORDS):
    years = years_at_company[i]

    # Average promotion approximately every 3-5 years
    maximum_promotions = max(0, years // 3)

    if maximum_promotions > 0:
        promotions[i] = np.random.randint(
            0,
            maximum_promotions + 1
        )

# ------------------------------------------------------------
# Overtime hours
# Monthly overtime hours
# ------------------------------------------------------------

overtime_hours = np.clip(
    np.random.normal(
        loc=10,
        scale=8,
        size=NUM_RECORDS
    ),
    0,
    60
)

overtime_hours = np.round(overtime_hours, 1)

# ------------------------------------------------------------
# Employee status
# ------------------------------------------------------------

status = np.random.choice(
    status_options,
    size=NUM_RECORDS,
    p=[0.78, 0.04, 0.06, 0.10, 0.02]
)

# ------------------------------------------------------------
# Exit reason
# Only employees who left the company receive an exit reason
# ------------------------------------------------------------

exit_reason = np.full(
    NUM_RECORDS,
    "N/A",
    dtype=object
)

left_company = np.isin(
    status,
    ["Terminated", "Resigned", "Retired"]
)

exit_reason[left_company] = np.random.choice(
    exit_reasons[:-1],
    size=left_company.sum()
)

# Retired employees should have retirement as the reason
retired = status == "Retired"
exit_reason[retired] = "Retirement"

# ------------------------------------------------------------
# Location
# ------------------------------------------------------------

location = np.full(
    NUM_RECORDS,
    "São Paulo",
    dtype=object
)

# ------------------------------------------------------------
# Create DataFrame
# ------------------------------------------------------------

df = pd.DataFrame({
    "Employee ID": employee_ids,
    "Department": department,
    "Position": position,
    "Salary": salary,
    "Years at Company": years_at_company,
    "Age": age,
    "Performance Rating": performance_rating,
    "Absenteeism": absenteeism,
    "Promotions": promotions,
    "Overtime Hours": overtime_hours,
    "Status": status,
    "Exit Reason": exit_reason,
    "Location": location,
    "Seniority": seniority
})

# ------------------------------------------------------------
# Save dataset
# ------------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

print("=" * 60)
print("EMPLOYEE DATASET GENERATED SUCCESSFULLY")
print("=" * 60)
print(f"Number of records: {len(df):,}")
print(f"Number of columns: {len(df.columns)}")
print(f"Output file: {OUTPUT_FILE}")
print()
print("Departments:")
print(df["Department"].value_counts())
print()
print("Seniority:")
print(df["Seniority"].value_counts())
print()
print("Status:")
print(df["Status"].value_counts())
print("=" * 60)