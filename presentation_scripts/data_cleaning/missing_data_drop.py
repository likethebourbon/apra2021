# Code for dropping rows with missing data

import random

import pandas as pd
import numpy as np

# Define constants used in the code below
RANDOM_SEED = 888
N_ROWS = 101

# Set random seed for reproducible results
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# Create a dummy dataset
df = pd.DataFrame(
    data={
        "id": list(range(1000, 1000 + N_ROWS)),
        "graduation_year": [random.randrange(1970, 2016) for _ in range(N_ROWS)],
    }
)

# Randomly change some data to NaN, representing missing data
df["graduation_year"] = df["graduation_year"].mask(np.random.random(df.shape[0]) < 0.2)

# Drop rows with missing 'graduation_year' values, and change the 'graduation_year' datatype to int
df_dropped_nas = df.dropna(axis=0, subset=["graduation_year"]).astype({"graduation_year": int})

print(
    f"Rows before dropping missing data: {len(df)}\nRows after dropping missing data: {len(df_dropped_nas)}"
)
