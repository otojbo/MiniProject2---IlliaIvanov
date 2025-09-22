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
