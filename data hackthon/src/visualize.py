import pandas as pd
import matplotlib.pyplot as plt

# =================================================
# 1. State-wise enrolment share (%)
# =================================================
state_share_df = pd.read_csv(
    "output/summary_tables/state_enrolment_share.csv"
)

top_states = state_share_df.head(10).set_index("state")

plt.figure()
top_states["state_enrolment_share_percent"].plot(kind="bar")
plt.title("Top States by Share of Aadhaar Enrolment (%)")
plt.xlabel("State")
plt.ylabel("Enrolment Share (%)")
plt.tight_layout()
plt.savefig("output/charts/state_enrolment_share.png")
plt.show()

# =================================================
# 2. Regional enrolment share (%)
# =================================================
regional_share_df = pd.read_csv(
    "output/summary_tables/regional_enrolment_share.csv"
)

plt.figure()
regional_share_df.set_index("region")[
    "enrolment_share_percent"
].plot(kind="bar")

plt.title("Regional Share of Aadhaar Enrolment (%)")
plt.xlabel("Region")
plt.ylabel("Enrolment Share (%)")
plt.tight_layout()
plt.savefig("output/charts/regional_enrolment_share.png")
plt.show()

# =================================================
# 3. Top 5 districts per region
# =================================================
district_df = pd.read_csv(
    "output/summary_tables/district_enrolment_by_region.csv"
)

regions = district_df["region"].unique()

for region in regions:
    region_data = (
        district_df[district_df["region"] == region]
        .head(5)
        .set_index("district")
    )

    plt.figure()
    region_data["total_enrolment"].plot(kind="bar")
    plt.title(f"Top 5 Districts by Aadhaar Enrolment – {region}")
    plt.xlabel("District")
    plt.ylabel("Total Enrolment")
    plt.tight_layout()
    plt.savefig(f"output/charts/top_districts_{region}.png")
    plt.show()

# =================================================
# 4. Monthly enrolment trend + forecast
# =================================================
monthly_df = pd.read_csv(
    "output/summary_tables/monthly_enrolment_trend.csv"
)
forecast_df = pd.read_csv(
    "output/summary_tables/enrolment_forecast.csv"
)

monthly_df["month"] = monthly_df["month"].astype(str)
actual_x = monthly_df["month"].tolist()
forecast_x = [f"Future {i+1}" for i in range(len(forecast_df))]

plt.figure(figsize=(10, 5))
plt.plot(actual_x, monthly_df["total_enrolment"], marker="o", label="Actual")
plt.plot(forecast_x, forecast_df["predicted_enrolment"],
         linestyle="--", marker="o", label="Forecast")

plt.title("Monthly Aadhaar Enrolment Trend & Forecast")
plt.xlabel("Time")
plt.ylabel("Total Enrolment")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("output/charts/enrolment_forecast.png")
plt.show()

# =================================================
# 5. Generational share by region
# =================================================
gen_region_df = pd.read_csv(
    "output/summary_tables/generation_share_by_region.csv"
)

gen_region_df.set_index("region").plot(
    kind="bar", stacked=True, figsize=(8, 5)
)

plt.title("Generational Share of Aadhaar Enrolment by Region (2025)")
plt.xlabel("Region")
plt.ylabel("Percentage Share (%)")
plt.legend(["Gen Alpha (0–5)", "Gen Z (5–17)", "Adults (18+)"])
plt.tight_layout()
plt.savefig("output/charts/generation_share_by_region.png")
plt.show()

# =================================================
# 6. Top districts by Gen Alpha share
# =================================================
district_gen_df = pd.read_csv(
    "output/summary_tables/district_generation_intensity.csv"
)

top_alpha = (
    district_gen_df
    .sort_values("gen_alpha_share", ascending=False)
    .head(10)
    .set_index("district")
)

plt.figure(figsize=(10, 5))
top_alpha["gen_alpha_share"].plot(kind="bar")
plt.title("Top Districts by Gen Alpha Aadhaar Share (2025)")
plt.xlabel("District")
plt.ylabel("Gen Alpha Share (%)")
plt.tight_layout()
plt.savefig("output/charts/top_gen_alpha_districts.png")
plt.show()

# =================================================
# 7. Behavioural & structural signatures (stacked)
# =================================================
sig_df = pd.read_csv(
    "output/summary_tables/region_behavioural_signatures_2025.csv"
)

sig_df.set_index("region")[
    ["gen_alpha_share", "gen_z_share", "adult_share"]
].plot(kind="bar", stacked=True, figsize=(9, 5))

plt.title("Behavioural & Structural Signatures by Region (2025)")
plt.xlabel("Region")
plt.ylabel("Share of Enrolment (%)")
plt.legend(["Gen Alpha", "Gen Z", "Adults"])
plt.tight_layout()
plt.savefig("output/charts/region_behavioural_signatures_2025.png")
plt.show()

# =================================================
# 8. Enrolment Stress Index (ESI)
# =================================================
esi_df = pd.read_csv(
    "output/summary_tables/enrolment_stress_index_2025.csv"
)

plt.figure(figsize=(9, 5))
esi_df.set_index("region")["ESI"].plot(kind="bar")

plt.title("Enrolment Stress Index (ESI) by Region – 2025")
plt.xlabel("Region")
plt.ylabel("Stress Index (Higher = More Stress)")
plt.tight_layout()
plt.savefig("output/charts/enrolment_stress_index_2025.png")
plt.show()

# =================================================
# 9. Silent Under-Service detector
# =================================================
silent_df = pd.read_csv(
    "output/summary_tables/silent_under_service_regions.csv"
)

silent_df["silent_under_service_flag"].value_counts().plot(
    kind="bar", figsize=(6, 4)
)

plt.title("Silent Under-Service Regions (2025)")
plt.xlabel("Category")
plt.ylabel("Number of Regions")
plt.tight_layout()
plt.savefig("output/charts/silent_under_service.png")
plt.show()

# =================================================
# 10. Behavioural labels distribution
# =================================================
behaviour_df = pd.read_csv(
    "output/summary_tables/region_behavioural_labels_2025.csv"
)

behaviour_df["behavioural_label"].value_counts().plot(
    kind="bar", figsize=(6, 4)
)

plt.title("Behavioural Classification of Regions (2025)")
plt.xlabel("Behaviour Type")
plt.ylabel("Number of Regions")
plt.tight_layout()
plt.savefig("output/charts/behavioural_labels_distribution.png")
plt.show()

# =================================================
# 11. Heat-Pressure priority
# =================================================
priority_df = pd.read_csv(
    "output/summary_tables/heat_pressure_priority_table.csv"
)

plt.figure(figsize=(9, 5))
priority_df.set_index("region")["ESI"].plot(kind="bar")
plt.title("Heat-Pressure Priority by Region (2025)")
plt.xlabel("Region")
plt.ylabel("ESI")
plt.tight_layout()
plt.savefig("output/charts/heat_pressure_priority.png")
plt.show()

# =================================================
# 12. Enrolment inequality score
# =================================================
ineq_df = pd.read_csv(
    "output/summary_tables/region_inequality_score.csv"
)

plt.figure(figsize=(9, 5))
ineq_df.set_index("region")["inequality_score"].plot(kind="bar")
plt.title("Enrolment Inequality Score by Region")
plt.xlabel("Region")
plt.ylabel("Max ÷ Min District Enrolment")
plt.tight_layout()
plt.savefig("output/charts/region_inequality_score.png")
plt.show()

# =================================================
# 13. No-intervention ESI projection
# =================================================
proj_df = pd.read_csv(
    "output/summary_tables/esi_no_intervention_projection.csv"
)

proj_df.set_index("region")[["ESI", "projected_ESI"]].plot(
    kind="bar", figsize=(10, 5)
)

plt.title("ESI Under No-Intervention Scenario")
plt.xlabel("Region")
plt.ylabel("Stress Index")
plt.legend(["Current ESI", "Projected ESI"])
plt.tight_layout()
plt.savefig("output/charts/esi_no_intervention_projection.png")
plt.show()

print("✅ ALL visualizations generated successfully.")
