"""Code for transforming data into another form without reducing the number of rows."""

import datetime
import time

import numpy as np
import pandas as pd

# Define constants used in the code below
RANDOM_SEED = 888
ROW_COUNT = 1000
LAST_FISCAL_MONTH = 6


# Code to create the dataset
def random_date():
    d = np.random.randint(1, int(time.time()))
    return datetime.datetime.fromtimestamp(d).date()


df = pd.DataFrame({"date": [random_date() for _ in range(ROW_COUNT)]})


# Transform each date into a fiscal year beginning on July 1
df["fiscal_year"] = (pd.to_datetime(df["date"]) + pd.DateOffset(months=LAST_FISCAL_MONTH)).dt.year
