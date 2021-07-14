"""Code for imputing missing data."""

import pandas as pd
import numpy as np


# Define constants used in the code below
RANDOM_SEED = 888
N_ROWS = 100
MISSING_DISTRICT_LATITUDE = 38.5
MISSING_DISTRICT_LONGITUDE = -68


# Set random seed for reproducible results
np.random.seed(RANDOM_SEED)


# Define central latitude/longitude for district centers
district_centers = {
    "New York": [40.7306, -73.9352],
    "Washington DC": [38.9072, -77.0369],
    "Chicago": [41.8781, -87.6298],
    "Houston": [29.7604, -95.3698],
    "San Francisco": [37.7749, -122.4194],
    "Seattle": [47.6062, -122.3321],
    "Los Angeles": [34.0522, -118.2437],
}


# Create dummy dataset
df = pd.DataFrame(
    data={
        "id": list(range(1000, 1000 + N_ROWS)),
        "district": np.random.choice([k for k in district_centers], size=N_ROWS),
    }
)


df["latitude"] = df["district"].map({k: v[0] for k, v in district_centers.items()}) + [
    np.random.random() for _ in range(N_ROWS)
]
df["longitude"] = df["district"].map({k: v[1] for k, v in district_centers.items()}) + [
    np.random.random() for _ in range(N_ROWS)
]


# Randomly delete some data
mask_array = np.random.random(N_ROWS)
df["district"] = df["district"].mask(mask_array < 0.1)
df["latitude"] = df["latitude"].mask((mask_array < 0.1) | (mask_array > 0.9))
df["longitude"] = df["longitude"].mask(
    (mask_array < 0.1) | ((mask_array > 0.7) & (mask_array < 0.8))
)

print(f"Missing data by column before imputing:\n{df.isna().sum()}")


# Create values to fill in missing data by averaging each district's latitude and longitude
district_means = df.groupby("district").agg({"latitude": "mean", "longitude": "mean"})


# Fill in (impute) missing values for each district
df_imputed = df.copy()
df_imputed["latitude"] = df_imputed["latitude"].fillna(
    df["district"].map(district_means["latitude"])
)
df_imputed["longitude"] = df_imputed["longitude"].fillna(
    df["district"].map(district_means["longitude"])
)


# Fill in (impute) lat/lon for rows with no district data
# This data is off the East Coast for visibility and easy filtering
# This is one way to find donors who need addresses
df_imputed["latitude"] = df_imputed["latitude"].fillna(MISSING_DISTRICT_LATITUDE)
df_imputed["longitude"] = df_imputed["longitude"].fillna(MISSING_DISTRICT_LONGITUDE)

print(f"Missing data by column after imputing:\n{df_imputed.isna().sum()}")
