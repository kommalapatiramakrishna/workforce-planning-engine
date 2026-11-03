import os
import json
import hashlib
import pandas as pd
import pytest

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "workforce_data")

def test_file_existence():
    expected = [
        "roles.csv", "skills.csv", "employees.csv", "employee_skills.csv",
        "projects.csv", "demand_plans.csv", "availability.csv", "allocations.csv",
        "training_catalog.csv", "gap_analysis.csv", "ground_truth.csv", "manifest.json"
    ]
    for f in expected:
        assert os.path.exists(os.path.join(DATA_DIR, f)), f"Missing {f}"

def test_primary_keys():
    pks = {
        "roles.csv": "role_id",
        "skills.csv": "skill_id",
        "employees.csv": "employee_id",
        "employee_skills.csv": "emp_skill_id",
        "projects.csv": "project_id",
        "demand_plans.csv": "demand_id",
        "availability.csv": "avail_id",
        "allocations.csv": "allocation_id",
        "training_catalog.csv": "training_id",
        "gap_analysis.csv": "gap_id"
    }
    for fn, pk in pks.items():
        assert pd.read_csv(os.path.join(DATA_DIR, fn))[pk].is_unique

def test_foreign_keys():
    r = pd.read_csv(os.path.join(DATA_DIR, "roles.csv"))
    s = pd.read_csv(os.path.join(DATA_DIR, "skills.csv"))
    e = pd.read_csv(os.path.join(DATA_DIR, "employees.csv"))
    p = pd.read_csv(os.path.join(DATA_DIR, "projects.csv"))
    d = pd.read_csv(os.path.join(DATA_DIR, "demand_plans.csv"))
    a = pd.read_csv(os.path.join(DATA_DIR, "allocations.csv"))

    assert e["primary_role_id"].isin(r["role_id"]).all()
    assert d["project_id"].isin(p["project_id"]).all()
    assert d["role_id"].isin(r["role_id"]).all()
    assert d["primary_skill_id"].isin(s["skill_id"]).all()
    assert a["employee_id"].isin(e["employee_id"]).all()
    assert a["demand_id"].isin(d["demand_id"]).all()

def test_capacity_reconciliation():
    av = pd.read_csv(os.path.join(DATA_DIR, "availability.csv"))
    assert ((av["gross_capacity"] - av["approved_leave_hours"] - av["net_available_hours"]).abs() < 1e-4).all()

def test_reproducibility():
    with open(os.path.join(DATA_DIR, "manifest.json")) as f:
        m = json.load(f)
    for t, h in m["sha256_checksums"].items():
        with open(os.path.join(DATA_DIR, f"{t}.csv"), "rb") as f:
            assert hashlib.sha256(f.read()).hexdigest() == h