# Workforce Demand & Skill Gap Planning Engine

A deterministic synthetic workforce planning and capacity optimization engine that forecasts weekly role demand, identifies skill gaps, flags over-utilization risks, and evaluates hiring vs. upskilling actions.

## Overview
- **Master Data**: Roles, Skills, Employee Profiles with proficiency & validity dates, Projects.
- **Transactional Demand**: 12 months (52 weeks) of project demand and employee weekly availability with leave accounting.
- **Capacity & Utilization**: Strict math reconciliation: `net_available_hours = gross_capacity - approved_leave_hours`.
- **Anomalies & Ground Truth**: Injected edge cases (over-allocation, stale skills, duplicate demand) are tracked separately in `ground_truth.csv` without leaking into production features.
- **Deterministic**: Fixed seed `20261022` ensures complete reproducibility across runs.

---

## Repository Structure
```text
workforce-planning-engine/
├── generator/
│   └── workforce_engine.py    # Deterministic synthetic data generator
├── tests/
│   └── test_integrity.py      # Automated referential integrity & math audits
├── workforce_data/
│   └── manifest.json          # Checksums, record counts, and run metadata
├── requirements.txt           # Environment dependencies
├── .gitignore
└── README.md
