"""Code for creating the target variable for churn analysis."""

import pandas as pd
import numpy as np


# Define constants used in the code below
# RANDOM_SEED = 888
ID_COUNT = 1000
NULL_PCT = 0.15
MAX_GIFTS_PER_YEAR = 6
YEARS = [year for year in range(1990, 2022)]


# Set random seed for reproducible results
# np.random.seed(RANDOM_SEED)

# Create dataset
df = pd.DataFrame()

for donor_id in range(ID_COUNT):
    start_year = np.random.choice(YEARS)
    donor_years = list(range(start_year, 2022))
    years_given = np.ma.array(
        donor_years, mask=(np.array([np.random.random() for _ in donor_years]) < NULL_PCT)
    ).compressed()
    years_given = np.repeat(
        years_given, np.random.randint(1, MAX_GIFTS_PER_YEAR, size=len(years_given))
    )
    gifts = np.round(np.random.exponential(scale=250, size=len(years_given)), 2)
    temp_df = pd.DataFrame(
        data={"id": donor_id + 1000, "fiscal_year": years_given, "amount_given": gifts}
    )
    df = pd.concat([df, temp_df], ignore_index=True)


# Aggregate data
aggregated_df = (
    df.groupby(["id", "fiscal_year"])
    .agg(
        amount_given=("amount_given", "sum"),
        gift_count=("amount_given", "count"),
    )
    .reset_index()
)

# Fill in fiscal years without gifts
aggregated_df = aggregated_df.set_index(["id", "fiscal_year"])
aggregated_df = aggregated_df.unstack(level=["fiscal_year"], fill_value=0).stack(
    level=["fiscal_year"], dropna=False
)


# Calculate churn
def calculate_churn(df):
    result = df.copy()
    result["next_year_amount"] = result.groupby("id")["amount_given"].shift(-1).fillna(0)
    return np.where(((result["next_year_amount"] <= 0) & (result["amount_given"] > 0)), 1, 0)


aggregated_df["churn"] = calculate_churn(aggregated_df)

aggregated_df = aggregated_df.reset_index()

print(aggregated_df.head(30))
