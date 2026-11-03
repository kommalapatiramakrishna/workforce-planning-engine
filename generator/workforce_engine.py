import os
import json
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

FIXED_SEED = 20261022
np.random.seed(FIXED_SEED)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "workforce_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("[1/6] Generating Master Data...")
ROLES_DATA = [
    ("ROL-000001", "Cloud Infrastructure Architect", "Cloud", 185.00),
    ("ROL-000002", "Senior Site Reliability Engineer", "Cloud", 155.00),
    ("ROL-000003", "Data Platform Engineer", "Data", 160.00),
    ("ROL-000004", "Machine Learning Systems Engineer", "AI/ML", 175.00),
    ("ROL-000005", "Distributed Backend Engineer", "Engineering", 140.00),
    ("ROL-000006", "Fullstack Systems Developer", "Engineering", 130.00),
    ("ROL-000007", "Enterprise Security Analyst", "Security", 150.00),
    ("ROL-000008", "Technical Product Delivery Manager", "Delivery", 145.00)
]
df_role = pd.DataFrame(ROLES_DATA, columns=["role_id", "role_title", "job_family", "base_bill_rate"])

skill_prefixes = [
    "Kubernetes", "AWS-Core", "GCP-Core", "Azure-DevOps", "Terraform",
    "Python-Distributed", "Rust-Systems", "Golang-Microservices", "Kafka-Streams",
    "PostgreSQL-Internals", "Snowflake-DW", "PyTorch-Inference", "LLM-FineTuning",
    "OAuth-ZeroTrust", "CI-CD-Argo", "Docker-Security", "GraphQL-Mesh", "React-Architecture"
]
categories = ["Cloud", "Data", "AI/ML", "Backend", "Security", "Infrastructure"]

skills_list = []
for i in range(1, 301):
    base = skill_prefixes[i % len(skill_prefixes)]
    skills_list.append({
        "skill_id": f"SKL-{i:06d}",
        "skill_name": f"{base}-Spec-{i}",
        "category": categories[i % len(categories)],
        "validity_months": int(np.random.choice([12, 18, 24, 36], p=[0.2, 0.4, 0.3, 0.1]))
    })
df_skill = pd.DataFrame(skills_list)

first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Sam", "Chris", "Pat", "Riley", "Avery"]
last_names = ["Chen", "Smith", "Patel", "Garcia", "Johnson", "Kim", "Muller", "Tanaka", "Silva", "Gupta"]
role_ids = df_role["role_id"].tolist()

employees = []
for i in range(1, 5001):
    emp_type = np.random.choice(["FULL_TIME", "PART_TIME", "CONTRACTOR"], p=[0.82, 0.12, 0.06])
    base_h = 40.0 if emp_type == "FULL_TIME" else (20.0 if emp_type == "PART_TIME" else 35.0)
    employees.append({
        "employee_id": f"EMP-{i:06d}",
        "full_name": f"{np.random.choice(first_names)} {np.random.choice(last_names)}-{i}",
        "primary_role_id": np.random.choice(role_ids),
        "employment_type": emp_type,
        "weekly_base_hours": base_h,
        "lifecycle_status": "ACTIVE"
    })
df_employee = pd.DataFrame(employees)

emp_skills, esk_c, base_dt = [], 1, datetime(2026, 1, 1)
all_sids = df_skill["skill_id"].values
for emp_id in df_employee["employee_id"]:
    for sid in np.random.choice(all_sids, size=np.random.randint(2, 6), replace=False):
        emp_skills.append({
            "emp_skill_id": f"ESK-{esk_c:08d}",
            "employee_id": emp_id,
            "skill_id": sid,
            "proficiency_level": int(np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.25, 0.35, 0.2, 0.1])),
            "last_verified_date": (base_dt - timedelta(days=int(np.random.randint(30, 900)))).strftime("%Y-%m-%d"),
            "is_verified": True
        })
        esk_c += 1
df_emp_skill = pd.DataFrame(emp_skills)

projects = []
for p in range(1, 501):
    start_wk = np.random.randint(1, 20)
    dur_wks = np.random.randint(25, 45)
    projects.append({
        "project_id": f"PRJ-2026-{p:06d}",
        "project_name": f"Initiative-{p}",
        "priority": np.random.choice(["CRITICAL", "HIGH", "MEDIUM", "LOW"], p=[0.15, 0.35, 0.35, 0.15]),
        "start_date": (base_dt + timedelta(weeks=int(start_wk))).strftime("%Y-%m-%d"),
        "end_date": (base_dt + timedelta(weeks=int(dur_wks))).strftime("%Y-%m-%d"),
        "status": "ACTIVE"
    })
df_project = pd.DataFrame(projects)

print("[2/6] Generating Demand & Availability...")
weeks = [f"2026-W{w:02d}" for w in range(1, 53)]
demand_records = []
for _, prj in df_project.iterrows():
    p_id = prj["project_id"]
    for r_id in np.random.choice(role_ids, size=np.random.randint(2, 4), replace=False):
        for w in np.random.choice(weeks, size=np.random.randint(15, 30), replace=False):
            demand_records.append({
                "demand_id": f"DEM-{p_id}-{w.replace('-', '')}",
                "project_id": p_id,
                "role_id": r_id,
                "primary_skill_id": np.random.choice(all_sids),
                "min_proficiency": int(np.random.choice([2, 3, 4])),
                "calendar_week": w,
                "required_hours": float(np.random.choice([20.0, 40.0, 60.0]))
            })
df_demand = pd.DataFrame(demand_records).drop_duplicates(subset=["demand_id"])

crit_wks = [f"2026-W{w:02d}" for w in range(1, 13)]
avail_records, avl_c = [], 1
for _, emp in df_employee.iterrows():
    base_h, e_id = emp["weekly_base_hours"], emp["employee_id"]
    for w in crit_wks:
        leave = float(np.random.choice([8.0, 16.0, 40.0])) if np.random.rand() < 0.08 else 0.0
        leave = min(leave, base_h)
        avail_records.append({
            "avail_id": f"AVL-{avl_c:08d}",
            "employee_id": e_id,
            "calendar_week": w,
            "gross_capacity": base_h,
            "approved_leave_hours": leave,
            "net_available_hours": round(base_h - leave, 1)
        })
        avl_c += 1
df_avail = pd.DataFrame(avail_records)

print("[3/6] Allocating & Injecting Anomalies...")
allocations, gt, alc_c = [], [], 1
q1_dem = df_demand[df_demand["calendar_week"].isin(crit_wks)].copy()
emp_avail_map = df_avail.set_index(["employee_id", "calendar_week"])["net_available_hours"].to_dict()
assigned = {}

for _, d in q1_dem.head(4000).iterrows():
    cand = df_employee[df_employee["primary_role_id"] == d["role_id"]]["employee_id"].values
    if len(cand) == 0:
        continue
    sel = np.random.choice(cand)
    net = emp_avail_map.get((sel, d["calendar_week"]), 40.0)
    cur = assigned.get((sel, d["calendar_week"]), 0.0)
    alloc_h = min(d["required_hours"], max(0.0, net - cur))
    if alloc_h > 0:
        allocations.append({
            "allocation_id": f"ALLOC-2026-{alc_c:06d}",
            "demand_id": d["demand_id"],
            "employee_id": sel,
            "calendar_week": d["calendar_week"],
            "allocated_hours": alloc_h,
            "allocation_state": "CONFIRMED"
        })
        assigned[(sel, d["calendar_week"])] = cur + alloc_h
        alc_c += 1

# Anomaly 1: Over-allocation
t_emp = df_employee["employee_id"].iloc[10]
t_dem = q1_dem[q1_dem["calendar_week"] == "2026-W04"]["demand_id"].iloc[0]
over_alloc_id = f"ALLOC-2026-{alc_c:06d}"
alc_c += 1
allocations.append({
    "allocation_id": over_alloc_id,
    "demand_id": t_dem,
    "employee_id": t_emp,
    "calendar_week": "2026-W04",
    "allocated_hours": 48.0,
    "allocation_state": "CONFIRMED"
})
gt.append({
    "entity_type": "Allocation",
    "record_id": over_alloc_id,
    "anomaly_type": "ALLOCATION_EXCEEDS_AVAILABILITY",
    "description": "Allocated 48h exceeds capacity",
    "severity": "CRITICAL"
})

# Anomaly 2: Stale skill
stale_id = df_emp_skill["emp_skill_id"].iloc[50]
df_emp_skill.loc[df_emp_skill["emp_skill_id"] == stale_id, "last_verified_date"] = "2022-01-15"
gt.append({
    "entity_type": "EmployeeSkill",
    "record_id": stale_id,
    "anomaly_type": "STALE_SKILL_TREATED_AS_CURRENT",
    "description": "Expired verification date",
    "severity": "HIGH"
})

df_alloc = pd.DataFrame(allocations)
df_gt = pd.DataFrame(gt)

print("[4/6] Computing Training & Gaps...")
df_trn = pd.DataFrame([
    {
        "training_id": f"TRN-{i+1:06d}",
        "skill_id": sid,
        "curriculum_name": f"Mastery in {sid}",
        "duration_weeks": 8,
        "target_proficiency": 4,
        "cost_usd": 3000.0
    }
    for i, sid in enumerate(df_skill["skill_id"].head(50))
])

alloc_sum = df_alloc.groupby("demand_id")["allocated_hours"].sum().to_dict()
gaps, g_c = [], 1
for _, d in q1_dem.iterrows():
    short = max(0.0, d["required_hours"] - alloc_sum.get(d["demand_id"], 0.0))
    risk = "NONE" if short == 0 else ("LOW" if short <= 20 else "HIGH")
    act = "ASSIGNED" if short == 0 else ("UPSKILL" if short <= 20 else "HIRE_EXTERNAL")
    gaps.append({
        "gap_id": f"GAP-2026-{g_c:06d}",
        "demand_id": d["demand_id"],
        "shortfall_hours": round(short, 1),
        "proficiency_deficit": 0,
        "risk_category": risk,
        "recommended_action": act
    })
    g_c += 1
df_gap = pd.DataFrame(gaps)

print("[5/6] Exporting Datasets and Manifest...")
tables = {
    "roles": df_role,
    "skills": df_skill,
    "employees": df_employee,
    "employee_skills": df_emp_skill,
    "projects": df_project,
    "demand_plans": df_demand,
    "availability": df_avail,
    "allocations": df_alloc,
    "training_catalog": df_trn,
    "gap_analysis": df_gap,
    "ground_truth": df_gt
}

cks = {}
for k, df in tables.items():
    p = os.path.join(OUTPUT_DIR, f"{k}.csv")
    df.to_csv(p, index=False)
    with open(p, "rb") as f:
        cks[k] = hashlib.sha256(f.read()).hexdigest()

with open(os.path.join(OUTPUT_DIR, "manifest.json"), "w") as f:
    json.dump({
        "generator_seed": FIXED_SEED,
        "row_counts": {k: len(v) for k, v in tables.items()},
        "sha256_checksums": cks
    }, f, indent=2)

print("[6/6] Complete! Output written to:", os.path.abspath(OUTPUT_DIR))