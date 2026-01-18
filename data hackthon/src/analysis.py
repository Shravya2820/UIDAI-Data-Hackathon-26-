import pandas as pd

# -------------------------------------------------
# Load cleaned dataset
# -------------------------------------------------
df = pd.read_csv("data/cleaned_aadhaar_data.csv")
print("Dataset shape:", df.shape)

# -------------------------------------------------
# State → Region Mapping (FULL & SCALABLE)
# -------------------------------------------------
state_to_region = {
    # North
    "Jammu And Kashmir": "North", "Himachal Pradesh": "North", "Punjab": "North",
    "Haryana": "North", "Delhi": "North", "Uttarakhand": "North",
    "Uttar Pradesh": "North", "Rajasthan": "North",

    # South
    "Andhra Pradesh": "South", "Telangana": "South", "Tamil Nadu": "South",
    "Karnataka": "South", "Kerala": "South", "Goa": "South", "Puducherry": "South",

    # Northeast
    "Assam": "Northeast", "Meghalaya": "Northeast", "Manipur": "Northeast",
    "Mizoram": "Northeast", "Nagaland": "Northeast", "Tripura": "Northeast",
    "Arunachal Pradesh": "Northeast", "Sikkim": "Northeast",

    # West
    "Gujarat": "West", "Maharashtra": "West",
    "Dadra And Nagar Haveli And Daman And Diu": "West",

    # Central
    "Madhya Pradesh": "Central", "Chhattisgarh": "Central",

    # East
    "West Bengal": "East", "Bihar": "East", "Jharkhand": "East", "Odisha": "East",

    # Islands
    "Andaman And Nicobar Islands": "Islands", "Lakshadweep": "Islands"
}

df["region"] = df["state"].map(state_to_region).fillna("Other")

# -------------------------------------------------
# Analysis 1: State-wise enrolment share (%)
# -------------------------------------------------
state_enrolment = (
    df.groupby("state")["total_enrolment"]
    .sum()
    .reset_index()
)

total_enrolment_all = state_enrolment["total_enrolment"].sum()

state_enrolment["state_enrolment_share_percent"] = (
    state_enrolment["total_enrolment"] / total_enrolment_all
) * 100

state_enrolment = state_enrolment.sort_values(
    by="state_enrolment_share_percent",
    ascending=False
)

state_enrolment.to_csv(
    "output/summary_tables/state_enrolment_share.csv",
    index=False
)

# -------------------------------------------------
# Analysis 2: Regional enrolment share (%)
# -------------------------------------------------
regional_share = (
    df.groupby("region")["total_enrolment"].sum()
    / df["total_enrolment"].sum()
) * 100

regional_share_df = regional_share.reset_index()
regional_share_df.columns = ["region", "enrolment_share_percent"]

regional_share_df.to_csv(
    "output/summary_tables/regional_enrolment_share.csv",
    index=False
)

# -------------------------------------------------
# Analysis 3: District-wise enrolment within each region
# -------------------------------------------------
district_region_enrolment = (
    df.groupby(["region", "state", "district"])["total_enrolment"]
    .sum()
    .reset_index()
)

district_region_enrolment = district_region_enrolment.sort_values(
    by=["region", "total_enrolment"],
    ascending=[True, False]
)

district_region_enrolment.to_csv(
    "output/summary_tables/district_enrolment_by_region.csv",
    index=False
)

print("✅ Analysis completed.")
print("Saved:")
print("- state_enrolment_share.csv")
print("- regional_enrolment_share.csv")
print("- district_enrolment_by_region.csv")

# -------------------------------------------------
# Advanced Stat 1: Monthly enrolment trend
# -------------------------------------------------
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

monthly_enrolment = (
    df.groupby("month")["total_enrolment"]
    .sum()
    .reset_index()
)

monthly_enrolment.to_csv(
    "output/summary_tables/monthly_enrolment_trend.csv",
    index=False
)

# -------------------------------------------------
# Advanced Stat 2: Regional volatility
# -------------------------------------------------
regional_volatility = (
    df.groupby("region")["total_enrolment"]
    .std()
    .reset_index()
)

regional_volatility.columns = ["region", "enrolment_volatility"]

regional_volatility.to_csv(
    "output/summary_tables/regional_volatility.csv",
    index=False
)

# -------------------------------------------------
# Advanced Stat 3: District concentration per region
# -------------------------------------------------
district_share = (
    df.groupby(["region", "district"])["total_enrolment"]
    .sum()
    .reset_index()
)

district_concentration = (
    district_share.groupby("region", group_keys=False)
    .apply(lambda x: x["total_enrolment"].max() / x["total_enrolment"].sum())
    .reset_index(name="district_concentration_index")
)


district_concentration.columns = ["region", "district_concentration_index"]

district_concentration.to_csv(
    "output/summary_tables/district_concentration_index.csv",
    index=False
)

from sklearn.linear_model import LinearRegression
import numpy as np

# -------------------------------------------------
# ML Model: Time-series forecasting
# -------------------------------------------------
monthly_enrolment["time_index"] = np.arange(len(monthly_enrolment))

X = monthly_enrolment[["time_index"]]
y = monthly_enrolment["total_enrolment"]

model = LinearRegression()
model.fit(X, y)

future_index = pd.DataFrame({
    "time_index": np.arange(len(monthly_enrolment), len(monthly_enrolment) + 3)
})

future_predictions = model.predict(future_index)

forecast_df = pd.DataFrame({
    "month": ["Future_1", "Future_2", "Future_3"],
    "predicted_enrolment": future_predictions
})

forecast_df.to_csv(
    "output/summary_tables/enrolment_forecast.csv",
    index=False
)

# -------------------------------------------------
# Gen Alpha & Gen Z Regional Share Analysis
# -------------------------------------------------
gen_region = (
    df.groupby("region")[["age_0_5", "age_5_17", "age_18_greater"]]
    .sum()
    .reset_index()
)

# Convert to percentage share within each region
gen_region_percent = gen_region.copy()
total_by_region = gen_region[["age_0_5", "age_5_17", "age_18_greater"]].sum(axis=1)

gen_region_percent["gen_alpha_percent"] = (gen_region["age_0_5"] / total_by_region) * 100
gen_region_percent["gen_z_percent"] = (gen_region["age_5_17"] / total_by_region) * 100
gen_region_percent["adult_percent"] = (gen_region["age_18_greater"] / total_by_region) * 100

gen_region_percent = gen_region_percent[
    ["region", "gen_alpha_percent", "gen_z_percent", "adult_percent"]
]

gen_region_percent.to_csv(
    "output/summary_tables/generation_share_by_region.csv",
    index=False
)

# -------------------------------------------------
# District-level Gen Alpha & Gen Z intensity
# -------------------------------------------------
district_gen = (
    df.groupby(["region", "state", "district"])[
        ["age_0_5", "age_5_17", "total_enrolment"]
    ]
    .sum()
    .reset_index()
)

district_gen["gen_alpha_share"] = (
    district_gen["age_0_5"] / district_gen["total_enrolment"]
) * 100

district_gen["gen_z_share"] = (
    district_gen["age_5_17"] / district_gen["total_enrolment"]
) * 100

district_gen = district_gen.sort_values(
    by=["region", "gen_alpha_share"],
    ascending=[True, False]
)

district_gen.to_csv(
    "output/summary_tables/district_generation_intensity.csv",
    index=False
)

# -------------------------------------------------
# 2025 Behavioural & Structural Signatures
# -------------------------------------------------

# Region-wise generational composition
region_gen = (
    df.groupby("region")[["age_0_5", "age_5_17", "age_18_greater", "total_enrolment"]]
    .sum()
    .reset_index()
)

# Compute shares
region_gen["gen_alpha_share"] = (region_gen["age_0_5"] / region_gen["total_enrolment"]) * 100
region_gen["gen_z_share"] = (region_gen["age_5_17"] / region_gen["total_enrolment"]) * 100
region_gen["adult_share"] = (region_gen["age_18_greater"] / region_gen["total_enrolment"]) * 100

# Assign behavioural signature
def assign_signature(row):
    if row["gen_alpha_share"] >= max(row["gen_z_share"], row["adult_share"]):
        return "Early-Inclusion Strong"
    elif row["gen_z_share"] >= max(row["gen_alpha_share"], row["adult_share"]):
        return "School-Driven"
    else:
        return "Adult-Heavy"

region_gen["behavioural_signature"] = region_gen.apply(assign_signature, axis=1)

# Save
region_gen[
    ["region", "gen_alpha_share", "gen_z_share", "adult_share", "behavioural_signature"]
].to_csv(
    "output/summary_tables/region_behavioural_signatures_2025.csv",
    index=False
)

print("✅ Regional behavioural signatures generated (2025).")

# -------------------------------------------------
# District-level structural imbalance (2025)
# -------------------------------------------------

district_struct = (
    df.groupby(["region", "state", "district"])[
        ["age_0_5", "age_5_17", "age_18_greater", "total_enrolment"]
    ]
    .sum()
    .reset_index()
)

district_struct["gen_alpha_share"] = (district_struct["age_0_5"] / district_struct["total_enrolment"]) * 100
district_struct["gen_z_share"] = (district_struct["age_5_17"] / district_struct["total_enrolment"]) * 100
district_struct["adult_share"] = (district_struct["age_18_greater"] / district_struct["total_enrolment"]) * 100

district_struct.to_csv(
    "output/summary_tables/district_structural_profile_2025.csv",
    index=False
)

print("✅ District structural profiles saved.")

# -------------------------------------------------
# Enrolment Stress Index (ESI) – 2025
# -------------------------------------------------

# ---- 1. Enrolment share by region (normalized) ----
region_enrolment = (
    df.groupby("region")["total_enrolment"]
    .sum()
    .reset_index()
)

region_enrolment["enrolment_share"] = (
    region_enrolment["total_enrolment"] /
    region_enrolment["total_enrolment"].sum()
)

# ---- 2. District concentration index ----
district_enrolment = (
    df.groupby(["region", "district"])["total_enrolment"]
    .sum()
    .reset_index()
)

district_concentration = (
    district_enrolment.groupby("region")
    .apply(lambda x: x["total_enrolment"].max() / x["total_enrolment"].sum())
    .reset_index(name="district_concentration")
)

# ---- 3. Gen Alpha risk factor (lower = higher risk) ----
gen_alpha_region = (
    df.groupby("region")["age_0_5"]
    .sum()
    .reset_index()
)

gen_alpha_region["gen_alpha_share"] = (
    gen_alpha_region["age_0_5"] /
    df.groupby("region")["total_enrolment"].sum().values
)

gen_alpha_region["gen_alpha_risk"] = 1 - gen_alpha_region["gen_alpha_share"]

# ---- 4. Combine into ESI ----
esi_df = (
    region_enrolment[["region", "enrolment_share"]]
    .merge(district_concentration, on="region")
    .merge(
        gen_alpha_region[["region", "gen_alpha_risk"]],
        on="region"
    )
)

esi_df["ESI"] = (
    esi_df["enrolment_share"] *
    esi_df["district_concentration"] *
    esi_df["gen_alpha_risk"]
)

esi_df = esi_df.sort_values("ESI", ascending=False)

esi_df.to_csv(
    "output/summary_tables/enrolment_stress_index_2025.csv",
    index=False
)

print("✅ Enrolment Stress Index (ESI) computed and saved.")


# -------------------------------------------------
# Silent Under-Service Detector (Region-level)
# -------------------------------------------------

# Use existing region_gen (from behavioural step)
silent_df = region_gen.copy()

# Percentile thresholds
enrolment_low = silent_df["total_enrolment"].quantile(0.25)
enrolment_high = silent_df["total_enrolment"].quantile(0.75)

gen_alpha_median = silent_df["gen_alpha_share"].median()
gen_z_median = silent_df["gen_z_share"].median()

def silent_flag(row):
    if (
        enrolment_low < row["total_enrolment"] < enrolment_high and
        row["gen_alpha_share"] < gen_alpha_median and
        row["gen_z_share"] < gen_z_median
    ):
        return "Silent Under-Service"
    return "Normal"

silent_df["silent_under_service_flag"] = silent_df.apply(silent_flag, axis=1)

silent_df[
    ["region", "total_enrolment", "gen_alpha_share", "gen_z_share", "silent_under_service_flag"]
].to_csv(
    "output/summary_tables/silent_under_service_regions.csv",
    index=False
)

# -------------------------------------------------
# Behavioural Labels (Operational)
# -------------------------------------------------

def behaviour_label(row):
    if row["district_concentration"] > 0.25:
        return "Deadline-Driven"
    elif row["gen_alpha_share"] > row["gen_z_share"]:
        return "Steady Adopters"
    else:
        return "Catch-Up Regions"

behaviour_df = esi_df.merge(
    region_gen[["region", "gen_alpha_share", "gen_z_share"]],
    on="region"
)

behaviour_df["behavioural_label"] = behaviour_df.apply(behaviour_label, axis=1)

behaviour_df[
    ["region", "ESI", "behavioural_label"]
].to_csv(
    "output/summary_tables/region_behavioural_labels_2025.csv",
    index=False
)

# -------------------------------------------------
# Stress Projection (No-Intervention Scenario)
# -------------------------------------------------

# Normalize forecast
forecast_df["forecast_growth_ratio"] = (
    forecast_df["predicted_enrolment"] /
    forecast_df["predicted_enrolment"].iloc[0]
)

# Apply growth to ESI
stress_projection = esi_df.copy()
stress_projection["projected_ESI"] = (
    stress_projection["ESI"] *
    forecast_df["forecast_growth_ratio"].iloc[-1]
)

stress_projection.to_csv(
    "output/summary_tables/esi_no_intervention_projection.csv",
    index=False
)

# -------------------------------------------------
# Heat-Pressure Priority Table
# -------------------------------------------------

def priority_level(esi):
    if esi >= esi_df["ESI"].quantile(0.75):
        return "High – Immediate Action"
    elif esi >= esi_df["ESI"].quantile(0.4):
        return "Medium – Monitor"
    else:
        return "Low – Stable"

priority_df = esi_df.copy()
priority_df["priority"] = priority_df["ESI"].apply(priority_level)

priority_df[
    ["region", "ESI", "priority"]
].to_csv(
    "output/summary_tables/heat_pressure_priority_table.csv",
    index=False
)

# -------------------------------------------------
# Enrolment Inequality Score (Region-wise)
# -------------------------------------------------

district_totals = (
    df.groupby(["region", "district"])["total_enrolment"]
    .sum()
    .reset_index()
)

inequality_df = (
    district_totals.groupby("region")
    .apply(lambda x: x["total_enrolment"].max() / x["total_enrolment"].min())
    .reset_index(name="inequality_score")
)

inequality_df.to_csv(
    "output/summary_tables/region_inequality_score.csv",
    index=False
)
