# Code for imputing missing data

import pandas as pd
import numpy as np

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

RANDOM_SEED = 888
N_ROWS = 101
