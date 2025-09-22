# INF 601 - Advanced Python
# Illia Ivanov
# Mini Project 2

from __future__ import annotations

from pathlib import Path
from datetime import date
import random
from typing import Dict, Tuple, List

import pandas as pd
import matplotlib.pyplot as plt
from faker import Faker

DATA_DIR = Path("data")
DATA_CSV = DATA_DIR / "employees.csv"
CHARTS_DIR = Path("charts")

RANDOM_SEED = 42

DEPARTMENTS: List[str] = [
    "Engineering", "Sales", "Marketing", "HR", "Finance",
    "Support", "Operations", "IT",
]
DEPT_WEIGHTS: List[float] = [0.18, 0.16, 0.11, 0.08, 0.12, 0.14, 0.09, 0.12]

LEVELS: List[str] = ["Junior", "Mid", "Senior"]
LEVEL_WEIGHTS: List[float] = [0.45, 0.40, 0.15]

LEVEL_BASE_RANGES: Dict[str, Tuple[int, int]] = {
    "Junior": (45000, 70000),
    "Mid": (65000, 100000),
    "Senior": (95000, 150000),
}
DEPT_MULTIPLIER: Dict[str, float] = {
    "Engineering": 1.20, "IT": 1.10, "Finance": 1.15,
    "Sales": 1.05, "Marketing": 1.00, "Operations": 0.95,
    "HR": 0.90, "Support": 0.85,
}

EMAIL_DOMAINS: List[str] = [
    "gmail.com", "outlook.com", "yahoo.com", "icloud.com", "proton.me", "company.com"
]
def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

def choose_weighted(options: List[str], weights: List[float]) -> str:
    return random.choices(options, weights=weights, k=1)[0]

def gen_salary(level: str, dept: str) -> int:
    low, high = LEVEL_BASE_RANGES[level]
    base = random.randint(low, high)
    mult = DEPT_MULTIPLIER.get(dept, 1.0)
    return int(base * mult)

def generate_fake_dataset(n: int = 1200, seed: int = RANDOM_SEED) -> pd.DataFrame:
    random.seed(seed)
    Faker.seed(seed)
    fake = Faker()

    today = date.today()
    rows: List[Dict[str, object]] = []

    for i in range(1, n + 1):
        full_name = fake.name()
        level = choose_weighted(LEVELS, LEVEL_WEIGHTS)
        dept = choose_weighted(DEPARTMENTS, DEPT_WEIGHTS)

        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )

        country = fake.country()
        domain = random.choice(EMAIL_DOMAINS)
        email_local = full_name.lower().replace(" ", ".").replace("'", "")
        email = f"{email_local}@{domain}"

        hire_date = fake.date_between(start_date="-10y", end_date="today")
        salary_usd = gen_salary(level, dept)

        rows.append(
            {
                "id": i,
                "full_name": full_name,
                "email": email,
                "email_domain": domain,
                "country": country,
                "department": dept,
                "position_level": level,
                "salary_usd": salary_usd,
                "birth_date": birth_date,
                "age": age,
                "hire_date": hire_date,
            }
        )

    return pd.DataFrame(rows)

def apply_schema(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["full_name", "email", "email_domain"]:
        df[col] = df[col].astype("string")

    for col in ["birth_date", "hire_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    df["id"] = df["id"].astype("int64")
    df["salary_usd"] = df["salary_usd"].astype("int64")
    df["age"] = pd.to_numeric(df["age"], errors="coerce").astype("Int64")

    df["country"] = df["country"].astype("category")
    df["department"] = pd.Categorical(df["department"], categories=DEPARTMENTS, ordered=True)
    df["position_level"] = pd.Categorical(df["position_level"], categories=LEVELS, ordered=True)
    return df

def plot_salary_by_department(df: pd.DataFrame) -> Path:
    avg = (
        df.groupby("department", observed=True)["salary_usd"]
        .mean()
        .sort_values(ascending=False)
        .round(0)
    )
    ax = avg.plot.bar(figsize=(9, 5))
    ax.set_title("Average Salary by Department (USD)")
    ax.set_xlabel("Department")
    ax.set_ylabel("Average Salary")
    ax.grid(True, axis="y", alpha=0.3)
    plt.xticks(rotation=30, ha="right")
    out = CHARTS_DIR / "salary_by_department.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def plot_department_popularity(df: pd.DataFrame) -> Path:
    counts = df["department"].value_counts().reindex(DEPARTMENTS).fillna(0).astype(int)
    ax = counts.plot.bar(figsize=(9, 5))
    ax.set_title("Department Popularity (Count)")
    ax.set_xlabel("Department")
    ax.set_ylabel("Count")
    ax.grid(True, axis="y", alpha=0.3)
    plt.xticks(rotation=30, ha="right")
    out = CHARTS_DIR / "department_popularity.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def plot_age_histogram(df: pd.DataFrame) -> Path:
    ax = df["age"].dropna().plot.hist(bins=24, figsize=(9, 5))
    ax.set_title("Age Distribution")
    ax.set_xlabel("Age")
    ax.set_ylabel("Count")
    ax.grid(True, alpha=0.3)
    out = CHARTS_DIR / "age_hist.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def main() -> None:
    ensure_dirs()
    df = generate_fake_dataset(n=1200, seed=RANDOM_SEED)
    df = apply_schema(df)
    df.to_csv(DATA_CSV, index=False)
    print(f"dataset: {df.shape} -> {DATA_CSV.resolve()}")

    paths = [
        plot_salary_by_department(df),
        plot_department_popularity(df),
        plot_age_histogram(df),
    ]
    print("charts saved:")
    for p in paths:
        print(" -", p.resolve())

if __name__ == "__main__":
    main()