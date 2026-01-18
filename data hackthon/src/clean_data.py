import pandas as pd

# Load merged dataset
df = pd.read_csv("data/merged_aadhaar_data.csv")

# Basic inspection
print("Shape of dataset:", df.shape)
print("\nColumn names:")
print(df.columns)

print("\nSample records:")
print(df.head())

print("\nData info:")
print(df.info())


# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")

# Standardize state names
df["state"] = df["state"].str.strip().str.title()

# Handle missing values (if any)
df = df.dropna()

# Create total enrolment column
df["total_enrolment"] = (
    df["age_0_5"] + df["age_5_17"] + df["age_18_greater"]
)

print("\nAfter cleaning:")
print(df.info())

# Save cleaned dataset
df.to_csv("data/cleaned_aadhaar_data.csv", index=False)

print("Cleaned dataset saved as data/cleaned_aadhaar_data.csv")
