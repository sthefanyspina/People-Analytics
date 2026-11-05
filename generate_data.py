import numpy as np
import pandas as pd

# ============================================================
# PEOPLE ANALYTICS - EMPLOYEE DATASET GENERATOR
# ============================================================

NUM_RECORDS = 500_000
OUTPUT_FILE = "employee.csv"

REFERENCE_DATE = pd.Timestamp("2026-11-05")
START_DATE = pd.Timestamp("2005-01-01")

np.random.seed(42)

# ============================================================
# 1. DEPARTMENTS
# ============================================================

departments = [
    "Technology",
    "Finance",
    "Human Resources",
    "Sales",
    "Operations"
]

department_probabilities = [
    0.30, 0.18, 0.12, 0.18, 0.22
]

# ============================================================
# 2. JOB TITLES
# Intern included in all departments
# ============================================================

positions_by_department = {
    "Technology": [
        "Intern",
        "Software Engineer",
        "Data Analyst",
        "Data Scientist",
        "DevOps Engineer",
        "Systems Analyst",
        "IT Support Specialist",
        "Cybersecurity Analyst",
        "Cloud Engineer",
        "Product Manager",
        "Engineering Manager",
        "Technology Director"
    ],

    "Finance": [
        "Intern",
        "Financial Analyst",
        "Accountant",
        "Financial Controller",
        "Treasury Analyst",
        "Tax Analyst",
        "Auditor",
        "Finance Manager",
        "Finance Director"
    ],

    "Human Resources": [
        "Intern",
        "HR Analyst",
        "Recruiter",
        "HR Business Partner",
        "Training Specialist",
        "Payroll Analyst",
        "Talent Acquisition Specialist",
        "HR Coordinator",
        "HR Manager",
        "HR Director"
    ],

    "Sales": [
        "Intern",
        "Sales Representative",
        "Account Executive",
        "Sales Analyst",
        "Business Development Representative",
        "Key Account Manager",
        "Sales Coordinator",
        "Sales Manager",
        "Sales Director"
    ],

    "Operations": [
        "Intern",
        "Operations Analyst",
        "Operations Coordinator",
        "Logistics Analyst",
        "Process Analyst",
        "Operations Specialist",
        "Quality Analyst",
        "Operations Supervisor",
        "Operations Manager",
        "Operations Director"
    ]
}

# ============================================================
# 3. SENIORITY
# ============================================================

seniority_levels = [
    "Intern",
    "Junior",
    "Mid-Level",
    "Senior",
    "Lead",
    "Manager",
    "Director"
]

seniority_by_position = {

    "Intern": ["Intern"],

    "Software Engineer": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Data Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Data Scientist": ["Junior", "Mid-Level", "Senior", "Lead"],
    "DevOps Engineer": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Systems Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "IT Support Specialist": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Cybersecurity Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Cloud Engineer": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Product Manager": ["Mid-Level", "Senior", "Lead", "Manager"],
    "Engineering Manager": ["Manager", "Director"],
    "Technology Director": ["Director"],

    "Financial Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Accountant": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Financial Controller": ["Senior", "Lead", "Manager"],
    "Treasury Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Tax Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Auditor": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Finance Manager": ["Manager", "Director"],
    "Finance Director": ["Director"],

    "HR Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Recruiter": ["Junior", "Mid-Level", "Senior", "Lead"],
    "HR Business Partner": ["Mid-Level", "Senior", "Lead", "Manager"],
    "Training Specialist": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Payroll Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Talent Acquisition Specialist": ["Junior", "Mid-Level", "Senior", "Lead"],
    "HR Coordinator": ["Junior", "Mid-Level", "Senior"],
    "HR Manager": ["Manager", "Director"],
    "HR Director": ["Director"],

    "Sales Representative": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Account Executive": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Sales Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Business Development Representative": ["Junior", "Mid-Level", "Senior"],
    "Key Account Manager": ["Mid-Level", "Senior", "Lead", "Manager"],
    "Sales Coordinator": ["Junior", "Mid-Level", "Senior"],
    "Sales Manager": ["Manager", "Director"],
    "Sales Director": ["Director"],

    "Operations Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Operations Coordinator": ["Junior", "Mid-Level", "Senior"],
    "Logistics Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Process Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Operations Specialist": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Quality Analyst": ["Junior", "Mid-Level", "Senior", "Lead"],
    "Operations Supervisor": ["Senior", "Lead", "Manager"],
    "Operations Manager": ["Manager", "Director"],
    "Operations Director": ["Director"]
}

# ============================================================
# 4. SALARY RANGES
# Monthly salary in USD
# ============================================================

salary_ranges = {
    "Intern": (1800, 3000),
    "Junior": (3000, 5000),
    "Mid-Level": (5000, 8000),
    "Senior": (8000, 12000),
    "Lead": (11000, 16000),
    "Manager": (14000, 22000),
    "Director": (20000, 35000)
}

# ============================================================
# 5. LOCATIONS
# ============================================================

locations = [
    "New York",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Miami",
    "Las Vegas",
    "San Francisco",
    "Orlando",
    "Seattle",
    "Boston",
    "Dallas",
    "San Diego",
    "Atlanta",
    "Phoenix",
    "Denver",
    "Nashville",
    "Washington, D.C.",
    "Philadelphia",
    "New Orleans",
    "Honolulu"
]

# ============================================================
# 6. BASIC EMPLOYEE INFORMATION
# ============================================================

employee_id = np.array([
    f"EMP{str(i).zfill(7)}"
    for i in range(1, NUM_RECORDS + 1)
])

department = np.random.choice(
    departments,
    size=NUM_RECORDS,
    p=department_probabilities
)

age = np.random.randint(
    18, 61, size=NUM_RECORDS
)

location = np.random.choice(
    locations,
    size=NUM_RECORDS
)

# ============================================================
# 7. JOB TITLE GENERATION
# ============================================================

job_title = np.empty(
    NUM_RECORDS,
    dtype=object
)

for dept in departments:

    mask = department == dept
    count = mask.sum()

    job_title[mask] = np.random.choice(
        positions_by_department[dept],
        size=count
    )

# ============================================================
# 8. SENIORITY GENERATION
# ============================================================

seniority = np.empty(
    NUM_RECORDS,
    dtype=object
)

for position, allowed_levels in seniority_by_position.items():

    mask = job_title == position
    count = mask.sum()

    if count > 0:
        seniority[mask] = np.random.choice(
            allowed_levels,
            size=count
        )

# ============================================================
# 9. HIRE DATE
# ============================================================

reference_day = REFERENCE_DATE.to_datetime64()
start_day = START_DATE.to_datetime64()

earliest_hire = np.maximum(
    start_day,
    reference_day - (
        (age - 18) * 365.25
    ).astype("timedelta64[D]")
)

earliest_hire = earliest_hire.astype(
    "datetime64[D]"
)

earliest_offsets = (
    earliest_hire - start_day
).astype("timedelta64[D]").astype(int)

total_days = (
    reference_day - start_day
).astype("timedelta64[D]").astype(int)

hire_offsets = (
    earliest_offsets +
    (
        np.random.random(NUM_RECORDS) *
        (total_days - earliest_offsets + 1)
    ).astype(int)
)

hire_date = (
    start_day +
    hire_offsets.astype("timedelta64[D]")
)

# ============================================================
# 10. EMPLOYMENT STATUS
# ============================================================

employment_status = np.random.choice(
    ["Active", "On Leave", "Terminated"],
    size=NUM_RECORDS,
    p=[0.82, 0.04, 0.14]
)

is_terminated = (
    employment_status == "Terminated"
)

# ============================================================
# 11. TERMINATION DATE
# ============================================================

termination_date = np.full(
    NUM_RECORDS,
    np.datetime64("NaT"),
    dtype="datetime64[D]"
)

terminated_indices = np.where(
    is_terminated
)[0]

hire_offsets_terminated = hire_offsets[
    terminated_indices
]

max_termination_offsets = (
    total_days - hire_offsets_terminated
)

termination_offsets = np.array([
    np.random.randint(0, max_days + 1)
    for max_days in max_termination_offsets
])

termination_date[terminated_indices] = (
    start_day +
    (
        hire_offsets_terminated +
        termination_offsets
    ).astype("timedelta64[D]")
)

# ============================================================
# 12. TERMINATION TYPE
# ============================================================

termination_type = np.full(
    NUM_RECORDS,
    "Not Applicable",
    dtype=object
)

termination_type[terminated_indices] = np.random.choice(
    ["Voluntary", "Involuntary"],
    size=len(terminated_indices),
    p=[0.70, 0.30]
)

# ============================================================
# 13. EXIT REASON
# ============================================================

voluntary_reasons = [
    "Better Opportunity",
    "Low Salary",
    "Career Change",
    "Relocation",
    "Personal Reasons",
    "Work-Life Balance",
    "Lack of Career Growth"
]

involuntary_reasons = [
    "Poor Performance",
    "Company Restructuring",
    "Attendance Issues",
    "End of Contract",
    "Position Elimination"
]

exit_reason = np.full(
    NUM_RECORDS,
    "Not Applicable",
    dtype=object
)

voluntary_mask = (
    termination_type == "Voluntary"
)

involuntary_mask = (
    termination_type == "Involuntary"
)

exit_reason[voluntary_mask] = np.random.choice(
    voluntary_reasons,
    size=voluntary_mask.sum()
)

exit_reason[involuntary_mask] = np.random.choice(
    involuntary_reasons,
    size=involuntary_mask.sum()
)

# ============================================================
# 14. TENURE
# ============================================================

effective_end_date = np.where(
    is_terminated,
    termination_date,
    reference_day
).astype("datetime64[D]")

tenure_days = (
    effective_end_date - hire_date
).astype("timedelta64[D]").astype(float)

tenure_years = np.round(
    tenure_days / 365.25,
    2
)

# ============================================================
# 15. MONTHLY SALARY
# ============================================================

salary = np.zeros(
    NUM_RECORDS,
    dtype=float
)

for level, (minimum, maximum) in salary_ranges.items():

    mask = seniority == level

    salary[mask] = np.random.uniform(
        minimum,
        maximum,
        mask.sum()
    )

salary = np.round(salary, 2)

# ============================================================
# 16. PERFORMANCE RATING
# ============================================================

performance_rating = np.clip(
    np.random.normal(
        loc=3.6,
        scale=0.75,
        size=NUM_RECORDS
    ),
    1,
    5
)

performance_rating = np.round(
    performance_rating, 1
)

# ============================================================
# 17. ABSENTEEISM
# ============================================================
absenteeism_days = np.clip(
    np.random.poisson(
        lam=5,
        size=NUM_RECORDS
    ),
    0,
    30
)

# ============================================================
# 18. PROMOTIONS
# ============================================================

promotions = np.random.poisson(
    lam=np.minimum(
        tenure_years / 4,
        3
    )
)

promotions = np.minimum(
    promotions,
    6
)

# ============================================================
# 19. OVERTIME HOURS
# ============================================================

overtime_hours = np.clip(
    np.random.normal(
        loc=10,
        scale=8,
        size=NUM_RECORDS
    ),
    0,
    60
)

overtime_hours = np.round(
    overtime_hours, 1
)

# ============================================================
# 20. CREATE DATAFRAME
# ============================================================

df = pd.DataFrame({

    "employee_id": employee_id,
    "department": department,
    "job_title": job_title,
    "seniority": seniority,
    "salary": salary,
    "hire_date": pd.to_datetime(hire_date),
    "termination_date": pd.to_datetime(termination_date),
    "tenure_years": tenure_years,
    "age": age,
    "performance_rating": performance_rating,
    "absenteeism_days": absenteeism_days,
    "promotions": promotions,
    "overtime_hours": overtime_hours,
    "employment_status": employment_status,
    "termination_type": termination_type,
    "exit_reason": exit_reason,
    "location": location
})

# ============================================================
# 21. DATA VALIDATION
# ============================================================

assert df["employee_id"].is_unique

assert df["job_title"].notna().all()

assert df["seniority"].notna().all()

assert df["location"].isin(locations).all()

assert df["seniority"].isin(seniority_levels).all()

# Intern must have Intern seniority
assert (
    df.loc[
        df["job_title"] == "Intern",
        "seniority"
    ] == "Intern"
).all()

# Non-Intern positions cannot have Intern seniority
assert (
    df.loc[
        df["job_title"] != "Intern",
        "seniority"
    ] != "Intern"
).all()

# Terminated employees must have termination dates
assert df.loc[
    df["employment_status"] == "Terminated",
    "termination_date"
].notna().all()

# Active and On Leave employees must not have termination dates
assert df.loc[
    df["employment_status"] != "Terminated",
    "termination_date"
].isna().all()

# Termination date cannot precede hire date
assert (
    df.loc[
        df["employment_status"] == "Terminated",
        "termination_date"
    ] >=
    df.loc[
        df["employment_status"] == "Terminated",
        "hire_date"
    ]
).all()

# ============================================================
# 22. SAVE DATASET
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# ============================================================
# 23. SUMMARY
# ============================================================

print("=" * 65)
print("PEOPLE ANALYTICS DATASET GENERATED SUCCESSFULLY")
print("=" * 65)

print(f"Total employees: {len(df):,}")
print(f"Total columns: {len(df.columns)}")

print(f"\nOutput file: {OUTPUT_FILE}")

print("\nDepartment:")
print(df["department"].value_counts())

print("\nJob Titles:")
print(df["job_title"].value_counts())

print("\nSeniority:")
print(df["seniority"].value_counts())

print("\nEmployment Status:")
print(df["employment_status"].value_counts())

print("\nTermination Type:")
print(df["termination_type"].value_counts())

print("\nExit Reasons:")
print(
    df.loc[
        df["employment_status"] == "Terminated",
        "exit_reason"
    ].value_counts()
)

print("\nLocation:")
print(df["location"].value_counts())

print("\nAverage Monthly Salary:")
print(f"${df['salary'].mean():,.2f}")

print("\nAverage Tenure:")
print(f"{df['tenure_years'].mean():.2f} years")

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDataset Preview:")
print(df.head())

print("=" * 65)
