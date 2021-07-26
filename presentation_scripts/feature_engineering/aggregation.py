"""Code for aggregating data using the groupby method on a pandas DataFrame."""

import pandas as pd
import numpy as np


# Define constants used in the code below
RANDOM_SEED = 888
ID_COUNT = 1000
NULL_PCT = 0.15
MAX_GIFTS_PER_YEAR = 6
YEARS = [year for year in range(1990, 2022)]


# Set random seed for reproducible results
np.random.seed(RANDOM_SEED)

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
# Sum gifts in each donor's fiscal years for 'amount_given'
# Add a new column 'gift_count' to count each donor's gifts in each fiscal year
aggregated_df = (
    df.groupby(["id", "fiscal_year"])
    .agg(
        amount_given=("amount_given", "sum"),
        gift_count=("amount_given", "count"),
    )
    .reset_index()
)

print(aggregated_df.head(10))
