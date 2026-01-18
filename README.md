# 📘 Aadhaar Enrolment Data Hackathon (2025)

## Overview

This project analyzes the **UIDAI Aadhaar Enrolment Dataset (2025 only)** to extract **operational, societal, and structural insights** that can support **policy decisions, infrastructure planning, and inclusion strategies**.

The work goes beyond basic exploratory data analysis (EDA) by introducing **explainable composite indices, behavioural classification, and scenario-based reasoning**, while respecting the limitation of **single-year data**.

---

## 🎯 Objective

- Analyze Aadhaar enrolment patterns across **states, districts, regions, and age groups**
- Identify **stress points**, **inequality**, and **silent under-service**
- Produce **decision-ready outputs** rather than descriptive statistics
- Ensure all insights are **explainable, defensible, and actionable**

📌 Note: Since the dataset covers **only 2025**, all insights are **cross-sectional snapshots**, not long-term trends.

---

## 📂 Dataset

- **Source:** UIDAI Aadhaar Enrolment Dataset
- **Year:** 2025
- **Granularity:**
  - State
  - District
  - Month
  - Age Groups:
    - `age_0_5`
    - `age_5_17`
    - `age_18_greater`
    - `total_enrolment`

---

## 🛠️ Project Structure

```

data/
└─ cleaned_aadhaar_data.csv

src/
├─ analysis.py        # All analysis, metrics, indices
└─ visualize.py       # Visualization logic

output/
├─ summary_tables/    # CSV outputs
└─ charts/            # PNG visualizations

```

---

## 🧹 Data Cleaning & Standardization

- Standardized:
  - State names
  - District names
  - Date format
- Added:
  - `region` column using a state → region mapping:
    - North, South, West, Central, East, Northeast, Islands
- Output:
  - `cleaned_aadhaar_data.csv`

---

## 📊 Core Analysis Performed

### 1. Descriptive Metrics
- State-wise total enrolment
- State-wise enrolment share (%)
- Region-wise enrolment share
- Top districts per region
- Monthly enrolment aggregation

📁 Saved in:
```

output/summary_tables/

```

---

## 🤖 Forecasting (Explainable ML)

- Used **Linear Regression** for short-term enrolment continuation
- Purpose: **scenario reasoning**, not prediction claims
- Inputs limited strictly to 2025 monthly data

Outputs:
- `monthly_enrolment_trend.csv`
- `enrolment_forecast.csv`

---

## 🧬 Generational Analysis (2025-Aligned)

Age groups mapped correctly for **2025 only**:

| Generation | Dataset Column   | Interpretation               |
|----------|------------------|------------------------------|
| Gen Alpha | `age_0_5`        | Early childhood enrolment    |
| Gen Z    | `age_5_17`       | School-age enrolment         |
| Adults   | `age_18_greater` | Adult enrolment / updates    |

Analysis levels:
- Region
- District

Outputs:
- `generation_share_by_region.csv`
- `district_generation_intensity.csv`

---

## 🧠 Behavioural & Structural Signatures

Regions classified by **current enrolment composition**:

- **Early-Inclusion Strong**
- **School-Driven**
- **Adult-Heavy**

Output:
- `region_behavioural_signatures_2025.csv`

---

## 🔥 Enrolment Stress Index (ESI) ⭐

### Purpose
Identify regions where **Aadhaar infrastructure is under maximum operational stress**.

### Formula (Explainable)
```

ESI =
Enrolment Share
× District Concentration Index
× (1 − Gen Alpha Share)

```

### What It Captures
- Volume load
- District-level imbalance
- Future backlog risk

Output:
- `enrolment_stress_index_2025.csv`

---

## 🚨 Silent Under-Service Detector

Identifies regions that:
- Are neither top nor bottom in enrolment
- But have **low Gen Alpha and Gen Z participation**

These regions appear stable but are **quietly falling behind**.

Output:
- `silent_under_service_regions.csv`

---

## 🧭 Operational Behaviour Labels

Regions classified into:
- **Deadline-Driven**
- **Steady Adopters**
- **Catch-Up Regions**

Output:
- `region_behavioural_labels_2025.csv`

---

## ⚖️ Enrolment Inequality Score

Measures **within-region disparity**:

```

Top District Enrolment ÷ Bottom District Enrolment

```

Highlights hidden exclusion behind good regional averages.

Output:
- `region_inequality_score.csv`

---

## 🔮 “No Intervention” Stress Scenario

- Applied forecast growth factor to ESI
- Shows how stress escalates **if no policy action is taken**

Output:
- `esi_no_intervention_projection.csv`

---

## 🧯 Heat-Pressure Priority Framework

Converted ESI into actionable priority bands:
- **High** → Immediate action
- **Medium** → Monitor
- **Low** → Stable

Output:
- `heat_pressure_priority_table.csv`

---

## 📈 Visualization Layer

Implemented in `visualize.py`:
- Enrolment shares
- District leaders
- Generational composition
- Behavioural signatures
- ESI & projected ESI
- Silent under-service
- Inequality

📁 Saved in:
```

output/charts/

```

---

## 🏆 What Makes This Project Stand Out

- Uses **only UIDAI data**
- Correctly handles **single-year limitations**
- Introduces:
  - Composite indices
  - Behavioural segmentation
  - Stress-based prioritization
  - Scenario reasoning
- All outputs are **policy and operations ready**

---

## 🔄 Possible Extensions

- Modify region mapping logic
- Re-weight or redesign ESI formula
- Add district-level ESI
- Replace Linear Regression with another interpretable model
- Convert outputs into:
  - Dashboard
  - Policy brief
  - Decision memo

---

## 📌 Guiding Principle

> **Clarity > Complexity**  
> Every metric is explainable, defensible, and actionable.

---

## 👤 Author / Team

Hackathon Project — Aadhaar Enrolment Analytics (2025)
