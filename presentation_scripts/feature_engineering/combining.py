"""Code for combining columns to create new features. Giving velocities and accelerations are explained below."""

import datetime
import dateutil
from typing import Callable, Any


import numpy as np
import pandas as pd
from tqdm import tqdm


# Define constants used in the code below
RANDOM_SEED = 888
ID_COUNT = 1000
NULL_PCT = 0.15
MAX_GIFTS_PER_YEAR = 6
YEARS = [year for year in range(1990, 2022)]
CURRENT_FISCAL_YEAR = (
    datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=6)
).year


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
df = (
    df.groupby(["id", "fiscal_year"])
    .agg(
        amount_given=("amount_given", "sum"),
        gift_count=("amount_given", "count"),
    )
    .reset_index()
)


# Functions to calculate velocities and accelerations for all fiscal years
def calculate_simple_velocity(
    df: pd.DataFrame,
    fiscal_year: str = "fiscal_year",
    id_column: str = "id",
    amount: str = "amount_given",
    current_year: int = CURRENT_FISCAL_YEAR,
    window: int = 5,
    velocity: str = "simple_velocity",
) -> pd.Series:
    """Calculate giving velocity for a specified fiscal year.

        Giving velocity reflects the proportion of a donor's giving that
        occurred with a specified window (5 years by default). Peter Wylie
        wrote about it here: http://bit.ly/2nFqmZU.


    Arguments:
        df {pd.DataFrame} -- A DataFrame containing grouped and
            aggregated giving data.

    Keyword Arguments:
        fiscal_year {str} -- Name of the column containing the
            fiscal year (default: {'fiscal_year'})
        id_column {str} -- Name of the column containing the
            donor's ID (default: {'id'})
        amount {str} -- Name of the column containing the amount
            given (default: {'amount_given'})
        current_year {int} -- The current
            fiscal year (default: {CURRENT_FISCAL_YEAR})
        window {int} -- The number of years in the numerator of
            the calculation (default: {5})
        velocity {str} -- Name of the column containing the simple
            velocity (default: {'simple_velocity'})

    Returns:
        pd.Series -- MultiIndexed Series containing the simple velocity
    """
    recent_giving_df = (
        df[(df[fiscal_year] >= (current_year - window)) & (df[fiscal_year] <= current_year)]
        .groupby(id_column)
        .agg(recent_giving=(amount, "sum"))
    )
    total_giving_df = (
        df[(df[fiscal_year] <= current_year)].groupby(id_column).agg(total_giving=(amount, "sum"))
    )
    velocity_df = recent_giving_df.join(total_giving_df)
    velocity_df[velocity] = velocity_df["recent_giving"] / velocity_df["total_giving"]
    velocity_df[fiscal_year] = current_year
    velocity_df = velocity_df.reset_index().set_index([id_column, fiscal_year])[velocity]
    return velocity_df


def calculate_rolling_velocity(
    df: pd.DataFrame,
    fiscal_year: str = "fiscal_year",
    id_column: str = "id",
    amount: str = "amount_given",
    current_year: int = CURRENT_FISCAL_YEAR,
    window: int = 3,
    velocity: str = "rolling_velocity",
) -> pd.Series:
    """Calculate rolling giving velocity for a specified fiscal year.

        Rolling giving velocity reflects the escalation or de-escalation
        of a donor's giving in a specified window (3 years by default).
        Blackbaud includes this score in ResearchPoint, though their
        knowledgebase does not go into great detail. See the link here:
        https://www.kb.blackbaud.com/articles/Article/57194.


    Arguments:
        df {pd.DataFrame} -- A DataFrame containing grouped and
            aggregated giving data.

    Keyword Arguments:
        fiscal_year {str} -- Name of the column containing the
            fiscal year (default: {FISCAL_YEAR})
        id_column {str} -- Name of the column containing the
            donor's ID (default: {ACCOUNT_ID})
        amount {str} -- Name of the column containing the amount
            given (default: {AMOUNT})
        current_year {int} -- The current
            fiscal year (default: {CURRENT_FISCAL_YEAR})
        window {int} -- The number of years in the numerator of
            the calculation (default: {3})
        velocity {str} -- Name of the column containing the rolling
            velocity (default: {'rolling_velocity'})

    Returns:
        pd.Series -- MultiIndexed Series containing the rolling velocity
    """
    rolling_mean_df = (
        df[(df[fiscal_year] >= (current_year - window)) & (df[fiscal_year] < current_year)]
        .groupby(id_column)
        .agg(rolling_mean=(amount, "mean"))
    )
    prev_fy_giving_df = (
        df[df[fiscal_year] == (current_year - 1)]
        .groupby(id_column)
        .agg(prev_fy_giving=(amount, "sum"))
    )
    rolling_velocity_df = prev_fy_giving_df.join(rolling_mean_df, on=id_column)
    rolling_velocity_df[velocity] = (
        rolling_velocity_df["prev_fy_giving"] / rolling_velocity_df["rolling_mean"]
    )
    rolling_velocity_df[fiscal_year] = current_year
    rolling_velocity_df = rolling_velocity_df.reset_index().set_index([id_column, fiscal_year])[
        velocity
    ]
    rolling_velocity_df = rolling_velocity_df.fillna(0)
    return rolling_velocity_df


def calculate_acceleration(
    df: pd.DataFrame, id_column: str, velocity_column: str, acceleration_column: str
) -> pd.Series:
    """Calculate the difference between velocity calculations for each donor.

    Defined as velocity(year) - velocity(previous year) for any given year.
    Though this is not a true derivative of velocity, it comes close:
    [change in velocity(time)] / [change in time] as time approaches the
    smallest possible value. For this dataset, the smallest value of time
    is one year.

    Arguments:
        df {pd.DataFrame} -- A DataFrame that contains, at a minimum, an
            ID column and a velocity column.
        id_column {str} -- Name of the ID column.
        velocity_column {str} -- Name of the velocity column.
        acceleration_column {str} -- Name of the resulting acceleration column.

    Returns:
        pd.Series -- A Series of acceleration for a given velocity column.
    """
    acceleration = pd.DataFrame(df.groupby(id_column)[velocity_column].diff())
    acceleration = acceleration.fillna(0)
    acceleration.columns = [acceleration_column]
    return acceleration


def fill_missing_fiscal_years(
    df: pd.DataFrame,
    id_column: str = "id",
    fiscal_year: str = "fiscal_year",
    amount: str = "amount_given",
) -> pd.DataFrame:
    """Add fiscal years in which donors did not give to the DataFrame.

        Several calculations for churn and recovery modeling require
        donors to have data points for every fiscal year after their
        first gift. This code does that, and fills the newly-created
        data points with a value of 0.

    Arguments:
        df {pd.DataFrame} -- A DataFrame containing grouped and
            aggregated giving data.

    Keyword Arguments:
        id_column {str} -- Name of the column containing the donor's ID (default: {'id'})
        fiscal_year {str} -- Name of the column containing the fiscal year (default: {'fiscal_year'})
        amount {str} -- Name of the column containing the amount given (default: {'amount_given'})

    Returns:
        pd.DataFrame -- A DataFrame with missing fiscal years added
    """
    temp_df = df.set_index([id_column, fiscal_year]).copy()
    temp_df = temp_df.unstack(level=[fiscal_year], fill_value=0).stack(
        level=[fiscal_year], dropna=False
    )
    temp_df = temp_df.reset_index()
    first_gift_year_df = df.groupby(id_column).agg(first_gift_year=(fiscal_year, "min"))
    temp_df = temp_df.join(first_gift_year_df, on=id_column)
    temp_df = temp_df[temp_df[fiscal_year] >= temp_df["first_gift_year"]]
    temp_df = temp_df.drop("first_gift_year", axis=1)
    return temp_df


def apply_to_all_years(
    df: pd.DataFrame,
    func_name: Callable,
    start_year: int,
    end_year: int = CURRENT_FISCAL_YEAR,
    fillna_value: Any = 0,
    *args,
    **kwargs,
) -> pd.DataFrame:
    """Apply calculations for a single fiscal year to multiple years.

        This function makes it easy to apply velocity calculations
        to every fiscal year in a dataset.

    Arguments:
        df {pd.DataFrame} -- A DataFrame used by the specified callable
        func_name {Callable} -- Function or other callable that makes
            a calculation for a single year
        start_year {int} -- The first fiscal year to apply the callable to

    Keyword Arguments:
        end_year {int} -- The last fiscal year to apply the callable to
            (default: {CURRENT_FISCAL_YEAR})
        fillna_value {Any} -- The desired value for any missing data
            (default: {0})

    Returns:
        pd.DataFrame -- A MultiIndexed DataFrame containing the passed
            calculation applied to all specified years
    """
    df_to_join = pd.DataFrame()
    to_iterate = tqdm(list(range(start_year, end_year + 1)))
    column_name = None
    for year in to_iterate:
        to_iterate.set_description(f"Applying {func_name.__name__} to {year}")
        temp_df = func_name(df, current_year=year, *args, **kwargs)
        if column_name is None:
            column_name = temp_df.name
        df_to_join = pd.concat([df_to_join, temp_df])
    # Create a MultiIndex so returned DataFrame can be joined on
    # `id_column` and `fiscal_year`
    df_to_join.index = pd.MultiIndex.from_tuples(df_to_join.index)
    df_to_join.columns = [column_name]
    df_to_join = df_to_join.fillna(fillna_value)
    return df_to_join


def add_velocities(df):
    result = df.copy()
    for func in [calculate_simple_velocity, calculate_rolling_velocity]:
        temp_df = apply_to_all_years(result, func, result["fiscal_year"].min())
        result = result.join(temp_df, on=["id", "fiscal_year"])
    result = result.fillna(0)
    return result


def add_accelerations(df):
    result = df.copy()
    velocity_dict = {
        "simple_velocity": "simple_acceleration",
        "rolling_velocity": "rolling_acceleration",
    }
    for velocity, acceleration in velocity_dict.items():
        result[acceleration] = calculate_acceleration(result, "id", velocity, acceleration)
    return result


# Add combined columns to the dataset
df = fill_missing_fiscal_years(df)
df = add_velocities(df)
df = add_accelerations(df)

df.head(20)
