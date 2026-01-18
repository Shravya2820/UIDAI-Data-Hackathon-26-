import pandas as pd

# Load CSV files
df1 = pd.read_csv("data/api_data_aadhar_enrolment_0_500000.csv")
df2 = pd.read_csv("data/api_data_aadhar_enrolment_500000_1000000.csv")
df3 = pd.read_csv("data/api_data_aadhar_enrolment_1000000_1006029.csv")

# Merge all datasets
df = pd.concat([df1, df2, df3], ignore_index=True)

# Basic checks
print("Total rows:", df.shape[0])
print("Total columns:", df.shape[1])
print(df.head())

# Save merged dataset
df.to_csv("data/merged_aadhaar_data.csv", index=False)

print("Merged dataset saved as data/merged_aadhaar_data.csv")
