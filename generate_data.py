import numpy as np
import pandas as pd
from pathlib import Path

# ============================================================
# TECHCORP - PEOPLE ANALYTICS DATA GENERATOR
# ============================================================
# Dados 100% sintéticos
# Bibliotecas: pandas, numpy
# Saída: 8 arquivos CSV
# ============================================================

# 1. CONFIGURAÇÕES GERAIS

SEED = 42
rng = np.random.default_rng(SEED)

REFERENCE_DATE = pd.Timestamp("2026-11-09")
START_DATE = pd.Timestamp("2023-11-09")

NUM_EMPLOYEES = 10_000
NUM_DEPARTMENTS = 12
NUM_POSITIONS = 100

NUM_SALARIES = 50_000
NUM_REVIEWS = 30_000
NUM_ATTENDANCE = 500_000
NUM_PROMOTIONS = 5_000
NUM_TERMINATIONS = 2_000

OUTPUT_DIR = Path("techcorp_data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EARLIEST_HIRE = pd.Timestamp("2018-11-09")
LATEST_HIRE = pd.Timestamp("2025-11-09")

# ============================================================
# 2. NÍVEIS HIERÁRQUICOS
# ============================================================

SENIORITY_LEVELS = [
    "Intern",
    "Junior",
    "Mid-Level",
    "Senior",
    "Lead",
    "Manager",
    "Senior Manager",
    "Director",
    "Executive"
]

LEVEL_RANK = {
    level: index
    for index, level in enumerate(SENIORITY_LEVELS)
}

SALARY_RANGES = {
    "Intern": (1800, 3000),
    "Junior": (3000, 5000),
    "Mid-Level": (5000, 8000),
    "Senior": (8000, 12000),
    "Lead": (11000, 16000),
    "Manager": (14000, 20000),
    "Senior Manager": (18000, 25000),
    "Director": (22000, 32000),
    "Executive": (30000, 45000)
}

# ============================================================
# 3. DEPARTAMENTOS
# ============================================================

department_names = [
    "Technology",
    "Finance",
    "Human Resources",
    "Sales",
    "Operations",
    "Marketing",
    "Customer Support",
    "Legal",
    "Data & Analytics",
    "Cybersecurity",
    "Product Management",
    "Research & Development"
]

departments = pd.DataFrame({
    "department_id": range(1, 13),
    "department_name": department_names
})

department_probabilities = [
    0.16, 0.07, 0.06, 0.11,
    0.10, 0.07, 0.09, 0.04,
    0.09, 0.07, 0.07, 0.07
]

assert np.isclose(
    sum(department_probabilities), 1
)

# ============================================================
# 4. CARGOS
# ============================================================

roles_by_department = {

    "Technology": [
        "Technology Intern",
        "Software Engineer",
        "Systems Analyst",
        "Cloud Engineer",
        "Senior Engineer",
        "Technical Lead",
        "Engineering Manager",
        "Technology Director",
        "Technology Executive"
    ],

    "Finance": [
        "Finance Intern",
        "Finance Analyst",
        "Accountant",
        "Financial Specialist",
        "Senior Accountant",
        "Finance Lead",
        "Finance Manager",
        "Finance Director",
        "Finance Executive"
    ],

    "Human Resources": [
        "HR Intern",
        "HR Analyst",
        "Recruiter",
        "HR Specialist",
        "Senior HR Analyst",
        "HR Lead",
        "HR Manager",
        "HR Director",
        "HR Executive"
    ],

    "Sales": [
        "Sales Intern",
        "Sales Representative",
        "Account Executive",
        "Sales Analyst",
        "Senior Account Executive",
        "Sales Lead",
        "Sales Manager",
        "Sales Director"
    ],

    "Operations": [
        "Operations Intern",
        "Operations Analyst",
        "Logistics Analyst",
        "Process Specialist",
        "Senior Operations Analyst",
        "Operations Lead",
        "Operations Manager",
        "Operations Director"
    ],

    "Marketing": [
        "Marketing Intern",
        "Marketing Analyst",
        "Content Specialist",
        "Digital Marketing Analyst",
        "Senior Marketing Analyst",
        "Marketing Lead",
        "Marketing Manager",
        "Marketing Director"
    ],

    "Customer Support": [
        "Support Intern",
        "Support Analyst",
        "Customer Specialist",
        "Technical Support Analyst",
        "Senior Support Analyst",
        "Support Lead",
        "Support Manager",
        "Support Director"
    ],

    "Legal": [
        "Legal Intern",
        "Legal Assistant",
        "Legal Analyst",
        "Compliance Specialist",
        "Senior Legal Analyst",
        "Legal Lead",
        "Legal Manager",
        "Legal Director"
    ],

    "Data & Analytics": [
        "Data Intern",
        "Data Analyst",
        "BI Analyst",
        "Data Scientist",
        "Senior Data Scientist",
        "Data Lead",
        "Data Manager",
        "Analytics Director",
        "Analytics Executive"
    ],

    "Cybersecurity": [
        "Security Intern",
        "Security Analyst",
        "Information Security Analyst",
        "Security Engineer",
        "Senior Security Engineer",
        "Security Lead",
        "Security Manager",
        "Security Director"
    ],

    "Product Management": [
        "Product Intern",
        "Product Analyst",
        "Product Specialist",
        "Product Owner",
        "Senior Product Owner",
        "Product Lead",
        "Product Manager",
        "Product Director"
    ],

    "Research & Development": [
        "R&D Intern",
        "Research Analyst",
        "Research Specialist",
        "Development Engineer",
        "Senior Researcher",
        "R&D Lead",
        "R&D Manager",
        "R&D Director"
    ]
}

# ============================================================
# 5. CRIAÇÃO DA TABELA POSITIONS
# ============================================================

positions_data = []

for department_id, department_name in enumerate(
    department_names, start=1
):

    roles = roles_by_department[department_name]

    for index, role in enumerate(roles):

        level = SENIORITY_LEVELS[index]

        positions_data.append({

            "position_id": len(positions_data) + 1,

            "department_id": department_id,

            "position_name": role,

            "seniority_level": level,

            "seniority_rank": LEVEL_RANK[level]

        })

positions = pd.DataFrame(positions_data)

assert len(positions) == NUM_POSITIONS

position_lookup = positions.set_index("position_id")

# ============================================================
# 6. FUNCIONÁRIOS
# ============================================================

employee_ids = [
    f"EMP{i:07d}"
    for i in range(1, NUM_EMPLOYEES + 1)
]

employee_department = rng.choice(
    np.arange(1, NUM_DEPARTMENTS + 1),
    size=NUM_EMPLOYEES,
    p=department_probabilities
)

# Datas de contratação

hire_dates = (
    EARLIEST_HIRE +
    pd.to_timedelta(
        rng.integers(
            0,
            (LATEST_HIRE - EARLIEST_HIRE).days + 1,
            NUM_EMPLOYEES
        ),
        unit="D"
    )
)

hire_dates = pd.to_datetime(hire_dates)

# Idades fictícias

ages = rng.integers(
    18, 61, NUM_EMPLOYEES
)

birth_dates = (
    REFERENCE_DATE -
    pd.to_timedelta(
        ages * 365.25,
        unit="D"
    ) -
    pd.to_timedelta(
        rng.integers(0, 365, NUM_EMPLOYEES),
        unit="D"
    )
).normalize()

# ============================================================
# 7. POSIÇÃO INICIAL DOS FUNCIONÁRIOS
# ============================================================

initial_position_ids = np.zeros(
    NUM_EMPLOYEES,
    dtype=int
)

initial_seniority = np.empty(
    NUM_EMPLOYEES,
    dtype=object
)

for dept_id in range(1, NUM_DEPARTMENTS + 1):

    employee_mask = (
        employee_department == dept_id
    )

    available_positions = positions[
        (positions["department_id"] == dept_id) &
        (positions["seniority_rank"] <= 5)
    ]

    chosen = rng.choice(
        available_positions["position_id"].to_numpy(),
        size=employee_mask.sum()
    )

    initial_position_ids[employee_mask] = chosen

for i, position_id in enumerate(initial_position_ids):

    initial_seniority[i] = position_lookup.loc[
        position_id, "seniority_level"
    ]

# ============================================================
# 8. CARACTERÍSTICAS INDIVIDUAIS SINTÉTICAS
# ============================================================

employee_performance = np.clip(
    rng.normal(3.6, 0.7, NUM_EMPLOYEES),
    1,
    5
)

employee_performance = np.round(
    employee_performance, 2
)

employee_absence_rate = np.clip(
    rng.gamma(2.0, 0.08, NUM_EMPLOYEES),
    0.01,
    0.80
)

employee_overtime_baseline = np.clip(
    rng.normal(8, 4, NUM_EMPLOYEES),
    0,
    25
)

employee_salary_base = np.array([
    rng.uniform(*SALARY_RANGES[level])
    for level in initial_seniority
])

# ============================================================
# 9. JANELA DE OBSERVAÇÃO INDIVIDUAL
# ============================================================

observation_start = pd.to_datetime(
    np.maximum(
        hire_dates.to_numpy(),
        START_DATE.to_datetime64()
    )
)

# Funcionários contratados antes da janela de análise
# começam a ser observados em START_DATE.

# ============================================================
# 10. SELEÇÃO DOS DESLIGAMENTOS
# ============================================================

risk_score = (

    0.30 * (5 - employee_performance) +

    0.025 * employee_overtime_baseline +

    0.60 * employee_absence_rate +

    rng.normal(0, 0.35, NUM_EMPLOYEES)

)

risk_score = risk_score - risk_score.max()

termination_weights = np.exp(risk_score)

termination_weights /= termination_weights.sum()

terminated_indices = rng.choice(
    NUM_EMPLOYEES,
    size=NUM_TERMINATIONS,
    replace=False,
    p=termination_weights
)

is_terminated = np.zeros(
    NUM_EMPLOYEES,
    dtype=bool
)

is_terminated[terminated_indices] = True

# ============================================================
# 11. DATAS DE DESLIGAMENTO
# ============================================================

termination_dates = pd.Series(
    pd.NaT,
    index=range(NUM_EMPLOYEES),
    dtype="datetime64[ns]"
)

for index in terminated_indices:

    first_day = observation_start[index]

    # Pelo menos 180 dias de observação.

    earliest_exit = (
        first_day + pd.Timedelta(days=180)
    )

    days_available = (
        REFERENCE_DATE - earliest_exit
    ).days

    exit_offset = rng.integers(
        0,
        days_available + 1
    )

    termination_dates.iloc[index] = (
        earliest_exit +
        pd.Timedelta(days=int(exit_offset))
    )

# ============================================================
# 12. STATUS DOS FUNCIONÁRIOS
# ============================================================

employment_status = np.full(
    NUM_EMPLOYEES,
    "Active",
    dtype=object
)

non_terminated = np.where(
    ~is_terminated
)[0]

leave_indices = rng.choice(
    non_terminated,
    size=int(0.04 * NUM_EMPLOYEES),
    replace=False
)

employment_status[leave_indices] = "On Leave"

employment_status[is_terminated] = "Terminated"

# Data final de observação

employment_end = pd.Series(
    REFERENCE_DATE,
    index=range(NUM_EMPLOYEES)
)

employment_end.loc[is_terminated] = (
    termination_dates.loc[is_terminated]
)

# ============================================================
# 13. MOTIVOS DOS DESLIGAMENTOS
# ============================================================

termination_type = np.full(
    NUM_EMPLOYEES,
    "Not Applicable",
    dtype=object
)

termination_reason = np.full(
    NUM_EMPLOYEES,
    "Not Applicable",
    dtype=object
)

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

for index in terminated_indices:

    exit_type = rng.choice(
        ["Voluntary", "Involuntary"],
        p=[0.70, 0.30]
    )

    termination_type[index] = exit_type

    if exit_type == "Voluntary":

        termination_reason[index] = rng.choice(
            voluntary_reasons
        )

    else:

        termination_reason[index] = rng.choice(
            involuntary_reasons
        )

# ============================================================
# 14. TABELA EMPLOYEES
# ============================================================

employees = pd.DataFrame({

    "employee_id": employee_ids,

    "department_id": employee_department,

    "position_id": initial_position_ids,

    "hire_date": hire_dates,

    "birth_date": birth_dates,

    "status": employment_status,

    "termination_date": termination_dates,

    "termination_type": termination_type,

    "termination_reason": termination_reason

})

# ============================================================
# 15. BASE AUXILIAR DE OBSERVAÇÃO
# ============================================================

employee_observation = pd.DataFrame({

    "employee_id": employee_ids,

    "department_id": employee_department,

    "hire_date": hire_dates,

    "observation_start": observation_start,

    "employment_end": employment_end,

    "is_terminated": is_terminated,

    "performance": employee_performance,

    "absence_rate": employee_absence_rate,

    "overtime_baseline": employee_overtime_baseline,

    "salary_base": employee_salary_base,

    "initial_position_id": initial_position_ids

})

# ============================================================
# 16. HISTÓRICO DE PROMOÇÕES
# ============================================================

employment_duration_days = (
    pd.to_datetime(employment_end) -
    pd.to_datetime(observation_start)
).dt.days.to_numpy()

promotion_candidates = np.where(

    np.array([
        LEVEL_RANK[level] <= 5
        for level in initial_seniority
    ]) &

    (employment_duration_days >= 90)

)[0]

assert len(promotion_candidates) >= NUM_PROMOTIONS

promoted_indices = rng.choice(
    promotion_candidates,
    size=NUM_PROMOTIONS,
    replace=False
)

promotion_records = []

current_position_ids = initial_position_ids.copy()

for index in promoted_indices:

    employee_id = employee_ids[index]

    department_id = employee_department[index]

    previous_position_id = initial_position_ids[index]

    previous_position = position_lookup.loc[
        previous_position_id
    ]

    previous_level = previous_position[
        "seniority_level"
    ]

    next_level_rank = (
        LEVEL_RANK[previous_level] + 1
    )

    next_positions = positions[
        (positions["department_id"] == department_id) &
        (positions["seniority_rank"] == next_level_rank)
    ]

    if next_positions.empty:

        raise ValueError(
            f"Cargo de promoção não encontrado: {employee_id}"
        )

    new_position = next_positions.iloc[0]

    first_day = (
        observation_start[index] +
        pd.Timedelta(days=90)
    )

    last_day = pd.Timestamp(
        employment_end.iloc[index]
    )

    available_days = (
        last_day - first_day
    ).days

    promotion_date = (
        first_day +
        pd.Timedelta(
            days=int(
                rng.integers(
                    0,
                    available_days + 1
                )
            )
        )
    )

    promotion_records.append({

        "employee_id": employee_id,

        "promotion_date": promotion_date,

        "previous_position": previous_position_id,

        "new_position": int(
            new_position["position_id"]
        )

    })

    current_position_ids[index] = int(
        new_position["position_id"]
    )

promotions = pd.DataFrame(
    promotion_records
)

# Atualiza o cargo atual ou último cargo ocupado.

employees["position_id"] = current_position_ids

# ============================================================
# 17. HISTÓRICO SALARIAL
# ============================================================

salary_records = []

promotion_lookup = {
    employee_id: group.sort_values(
        "promotion_date"
    ).to_dict("records")

    for employee_id, group in promotions.groupby(
        "employee_id"
    )
}

for index in range(NUM_EMPLOYEES):

    employee_id = employee_ids[index]

    start = pd.Timestamp(observation_start[index])
    end = pd.Timestamp(employment_end.iloc[index])

    dates = pd.date_range(
        start=start,
        end=end,
        periods=5
    )

    employee_promotions = promotion_lookup.get(
        employee_id, []
    )

    current_position_id = initial_position_ids[index]

    previous_salary = None

    applied_promotions = set()

    for period, effective_date in enumerate(dates):

        promotion_applied = False

        for promotion in employee_promotions:

            if (
                promotion["promotion_date"] <= effective_date
                and promotion["promotion_date"] not in applied_promotions
            ):

                current_position_id = promotion["new_position"]

                applied_promotions.add(
                    promotion["promotion_date"]
                )

                promotion_applied = True

        current_position = position_lookup.loc[
            current_position_id
        ]

        seniority = current_position["seniority_level"]

        minimum, maximum = SALARY_RANGES[seniority]

        if previous_salary is None:

            salary = np.clip(
                employee_salary_base[index],
                minimum,
                maximum
            )

        elif promotion_applied:

            proposed_salary = rng.uniform(
                minimum,
                maximum
            )

            salary = min(
                max(
                    proposed_salary,
                    previous_salary * 1.08
                ),
                maximum
            )

        else:

            annual_increase = rng.uniform(
                0.01,
                0.035
            )

            salary = min(
                previous_salary * (1 + annual_increase),
                maximum
            )

        salary = round(float(salary), 2)

        salary_records.append({

            "employee_id": employee_id,

            "salary": salary,

            "effective_date": effective_date

        })

        previous_salary = salary

salaries = pd.DataFrame(salary_records)

# ============================================================
# 18. AVALIAÇÕES DE DESEMPENHO
# ============================================================

# 3 avaliações por funcionário.
# Total: 30.000 avaliações.

review_records = []

for index in range(NUM_EMPLOYEES):

    employee_id = employee_ids[index]

    start = pd.Timestamp(
        observation_start[index]
    )

    end = pd.Timestamp(
        employment_end.iloc[index]
    )

    review_dates = pd.date_range(
        start=start,
        end=end,
        periods=3
    )

    for review_date in review_dates:

        score = np.clip(

            employee_performance[index] +
            rng.normal(0, 0.35),

            1,
            5

        )

        review_records.append({

            "employee_id": employee_id,

            "review_date": review_date,

            "score": round(
                float(score),
                2
            )

        })

performance_reviews = pd.DataFrame(
    review_records
)

# ============================================================
# 19. ATTENDANCE - FREQUÊNCIA
# ============================================================

# 50 registros por funcionário.
# Total: 500.000 registros.

attendance_records = []

for index in range(NUM_EMPLOYEES):

    employee_id = employee_ids[index]

    start = pd.Timestamp(
        observation_start[index]
    )

    end = pd.Timestamp(
        employment_end.iloc[index]
    )

    total_available_days = (
        end - start
    ).days + 1

    if total_available_days < 50:

        raise ValueError(
            f"Período insuficiente para {employee_id}"
        )

    selected_days = rng.choice(

        total_available_days,

        size=50,

        replace=False

    )

    selected_days.sort()

    attendance_dates = (
        start +
        pd.to_timedelta(
            selected_days,
            unit="D"
        )
    )

    absence_probability = np.clip(

        employee_absence_rate[index] / 5,

        0.005,

        0.20

    )

    for attendance_date in attendance_dates:

        if rng.random() < absence_probability:

            absence_hours = rng.choice(

                [2, 4, 6, 8],

                p=[0.10, 0.20, 0.20, 0.50]

            )

        else:

            absence_hours = 0

        overtime = max(

            0,

            rng.normal(
                employee_overtime_baseline[index],
                5
            )

        )

        overtime = min(
            overtime,
            12
        )

        attendance_records.append({

            "employee_id": employee_id,

            "date": attendance_date,

            "absence_hours": absence_hours,

            "overtime_hours": round(
                float(overtime),
                2
            )

        })

attendance = pd.DataFrame(
    attendance_records
)

# ============================================================
# 20. TABELA DE DESLIGAMENTOS
# ============================================================

terminations = employees.loc[

    employees["status"] == "Terminated",

    [
        "employee_id",
        "termination_date",
        "termination_type",
        "termination_reason"
    ]

].copy()

terminations = terminations.rename(

    columns={
        "termination_reason": "reason"
    }

)

# ============================================================
# 21. AJUSTES FINAIS NAS TABELAS
# ============================================================

date_columns = {

    "employees": [
        "hire_date",
        "birth_date",
        "termination_date"
    ],

    "salaries": [
        "effective_date"
    ],

    "performance_reviews": [
        "review_date"
    ],

    "attendance": [
        "date"
    ],

    "promotions": [
        "promotion_date"
    ],

    "terminations": [
        "termination_date"
    ]

}

dataframes = {

    "employees": employees,

    "salaries": salaries,

    "performance_reviews": performance_reviews,

    "attendance": attendance,

    "promotions": promotions,

    "terminations": terminations

}

for table_name, columns in date_columns.items():

    for column in columns:

        dataframes[table_name][column] = pd.to_datetime(
            dataframes[table_name][column]
        )

# ============================================================
# 22. CÁLCULO AUXILIAR DE PERMANÊNCIA
# ============================================================

# Funcionários desligados:
# Permanência observada até a data de desligamento.
#
# Funcionários ativos:
# Permanência observada até REFERENCE_DATE.
#
# Os funcionários ativos são observações censuradas.

tenure_end = employees["termination_date"].fillna(
    REFERENCE_DATE
)

employees["tenure_years"] = (

    (
        tenure_end -
        employees["hire_date"]
    ).dt.days / 365.25

).round(2)

# 1 = desligamento observado.
# 0 = funcionário ativo na data de referência.

employees["event_observed"] = (
    employees["status"] == "Terminated"
).astype(int)

# ============================================================
# 23. VALIDAÇÃO DAS QUANTIDADES
# ============================================================

assert len(employees) == NUM_EMPLOYEES

assert len(departments) == NUM_DEPARTMENTS

assert len(positions) == NUM_POSITIONS

assert len(salaries) == NUM_SALARIES

assert len(performance_reviews) == NUM_REVIEWS

assert len(attendance) == NUM_ATTENDANCE

assert len(promotions) == NUM_PROMOTIONS

assert len(terminations) == NUM_TERMINATIONS

# ============================================================
# 24. VALIDAÇÃO DE INTEGRIDADE
# ============================================================

assert employees["employee_id"].is_unique

assert departments["department_id"].is_unique

assert positions["position_id"].is_unique

assert employees["department_id"].isin(
    departments["department_id"]
).all()

assert employees["position_id"].isin(
    positions["position_id"]
).all()

assert employees["status"].isin(
    ["Active", "On Leave", "Terminated"]
).all()

for table in [
    salaries,
    performance_reviews,
    attendance,
    promotions,
    terminations
]:

    assert table["employee_id"].isin(
        employees["employee_id"]
    ).all()

assert (
    employees["status"].value_counts().get(
        "Terminated", 0
    ) == NUM_TERMINATIONS
)

assert employees["event_observed"].isin(
    [0, 1]
).all()

# ============================================================
# 25. VALIDAÇÃO DE DATAS
# ============================================================

terminated_employees = employees[
    employees["status"] == "Terminated"
]

active_employees = employees[
    employees["status"] != "Terminated"
]

assert (
    terminated_employees["termination_date"] >=
    terminated_employees["hire_date"]
).all()

assert (
    active_employees["termination_date"].isna().all()
)

assert (
    employees["hire_date"] <= REFERENCE_DATE
).all()

assert (
    employees["birth_date"] < employees["hire_date"]
).all()

# Eventos dentro da janela de análise.

for table, date_column in [

    (salaries, "effective_date"),

    (performance_reviews, "review_date"),

    (attendance, "date"),

    (promotions, "promotion_date"),

    (terminations, "termination_date")

]:

    assert table[date_column].between(
        START_DATE,
        REFERENCE_DATE
    ).all()

# ============================================================
# 26. VALIDAÇÃO DOS REGISTROS INDIVIDUAIS
# ============================================================

assert (
    salaries.groupby("employee_id").size() == 5
).all()

assert (
    performance_reviews.groupby("employee_id").size() == 3
).all()

assert (
    attendance.groupby("employee_id").size() == 50
).all()

assert promotions["employee_id"].is_unique

assert terminations["employee_id"].is_unique

assert not attendance.duplicated(
    ["employee_id", "date"]
).any()

assert performance_reviews["score"].between(
    1, 5
).all()

assert (attendance["absence_hours"] >= 0).all()

assert (attendance["overtime_hours"] >= 0).all()

assert (attendance["overtime_hours"] <= 12).all()

assert (salaries["salary"] > 0).all()

assert employees["tenure_years"].ge(0).all()

# ============================================================
# 27. VALIDAÇÃO CRONOLÓGICA
# ============================================================

def validate_event_dates(
    event_table,
    event_date_column
):

    check = event_table.merge(

        employees[
            [
                "employee_id",
                "hire_date",
                "termination_date"
            ]
        ],

        on="employee_id",

        how="left",

        validate="many_to_one"

    )

    assert (
        check[event_date_column] >=
        check["hire_date"]
    ).all()

    assert (

        check["termination_date"].isna() |

        (
            check[event_date_column] <=
            check["termination_date"]
        )

    ).all()


validate_event_dates(
    salaries,
    "effective_date"
)

validate_event_dates(
    performance_reviews,
    "review_date"
)

validate_event_dates(
    attendance,
    "date"
)

validate_event_dates(
    promotions,
    "promotion_date"
)

validate_event_dates(
    terminations,
    "termination_date"
)

# ============================================================
# 28. VALIDAÇÃO DAS PROMOÇÕES
# ============================================================

promotion_check = promotions.merge(

    positions[
        [
            "position_id",
            "department_id",
            "seniority_rank"
        ]
    ].rename(

        columns={
            "position_id": "previous_position",
            "department_id": "previous_department",
            "seniority_rank": "previous_rank"
        }

    ),

    on="previous_position",

    how="left"

).merge(

    positions[
        [
            "position_id",
            "department_id",
            "seniority_rank"
        ]
    ].rename(

        columns={
            "position_id": "new_position",
            "department_id": "new_department",
            "seniority_rank": "new_rank"
        }

    ),

    on="new_position",

    how="left"

)

# A promoção não pode mudar o departamento
# neste modelo simplificado.

assert (
    promotion_check["previous_department"] ==
    promotion_check["new_department"]
).all()

# A promoção deve avançar exatamente um nível.

assert (
    promotion_check["new_rank"] ==
    promotion_check["previous_rank"] + 1
).all()

# ============================================================
# 29. VALIDAÇÃO DO HISTÓRICO SALARIAL
# ============================================================

salary_check = salaries.merge(

    employees[
        [
            "employee_id",
            "hire_date",
            "termination_date"
        ]
    ],

    on="employee_id",

    how="left"

)

assert (
    salary_check["effective_date"] >=
    salary_check["hire_date"]
).all()

assert (

    salary_check["termination_date"].isna() |

    (
        salary_check["effective_date"] <=
        salary_check["termination_date"]
    )

).all()

# ============================================================
# 30. VALIDAÇÃO DO HISTÓRICO DE CARGOS
# ============================================================

expected_position = pd.Series(
    initial_position_ids,
    index=range(NUM_EMPLOYEES)
)

for index in promoted_indices:

    employee_id = employee_ids[index]

    new_position = promotions.loc[

        promotions["employee_id"] == employee_id,

        "new_position"

    ].iloc[0]

    expected_position.iloc[index] = new_position

assert np.array_equal(

    employees["position_id"].to_numpy(),

    expected_position.to_numpy()

)

# ============================================================
# 31. VALIDAÇÃO DOS STATUS E DESLIGAMENTOS
# ============================================================

assert (
    employees.loc[
        employees["status"] == "Terminated",
        "termination_type"
    ].isin(
        ["Voluntary", "Involuntary"]
    )
).all()

assert (
    employees.loc[
        employees["status"] == "Terminated",
        "termination_reason"
    ].ne("Not Applicable")
).all()

assert (
    employees.loc[
        employees["status"] != "Terminated",
        "termination_type"
    ].eq("Not Applicable")
).all()

# ============================================================
# 32. TABELAS FINAIS PARA EXPORTAÇÃO
# ============================================================

tables = {

    "employees": employees,

    "departments": departments,

    "positions": positions,

    "salaries": salaries,

    "performance_reviews": performance_reviews,

    "attendance": attendance,

    "promotions": promotions,

    "terminations": terminations

}

# ============================================================
# 33. EXPORTAÇÃO DOS CSVs
# ============================================================

for table_name, dataframe in tables.items():

    output_path = (
        OUTPUT_DIR /
        f"{table_name}.csv"
    )

    dataframe.to_csv(

        output_path,

        index=False,

        encoding="utf-8-sig"

    )

    print(
        f"Arquivo gerado: {output_path}"
    )

# ============================================================
# 34. RELATÓRIO FINAL
# ============================================================

print("\n" + "=" * 65)

print("TECHCORP - DATASET GERADO COM SUCESSO")

print("=" * 65)

print("\nPeríodo de análise:")

print(
    f"{START_DATE.date()} até {REFERENCE_DATE.date()}"
)

print("\nQuantidade de registros:")

for table_name, dataframe in tables.items():

    print(
        f"{table_name:25s}: {len(dataframe):,}"
    )

print("\nStatus dos funcionários:")

print(
    employees["status"].value_counts()
)

print("\nFuncionários por departamento:")

department_summary = employees.merge(

    departments,

    on="department_id"

)

print(
    department_summary[
        "department_name"
    ].value_counts()
)

print("\nTipos de desligamento:")

print(
    terminations["termination_type"].value_counts()
)

print("\nSalário médio:")

print(
    f"US$ {salaries['salary'].mean():,.2f}"
)

print("\nPermanência média observada:")

print(
    f"{employees['tenure_years'].mean():.2f} anos"
)

print("\nMédia de horas extras por registro:")

print(
    f"{attendance['overtime_hours'].mean():.2f} horas"
)

print("\nMédia de ausência por registro:")

print(
    f"{attendance['absence_hours'].mean():.2f} horas"
)

print("\nAvaliação média:")

print(
    f"{performance_reviews['score'].mean():.2f}"
)

print("\nPromoções registradas:")

print(
    len(promotions)
)

print("\nFuncionários com evento de desligamento:")

print(
    employees["event_observed"].sum()
)

print("\nValores ausentes:")

for table_name, dataframe in tables.items():

    missing = dataframe.isnull().sum().sum()

    print(
        f"{table_name:25s}: {missing:,}"
    )

print("\nDiretório de exportação:")

print(
    OUTPUT_DIR.resolve()
)

print("\n" + "=" * 65)

print("TODAS AS VALIDAÇÕES FORAM CONCLUÍDAS.")

print("=" * 65)
