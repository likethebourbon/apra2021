"""Code for matching, filtering, and transforming text with regular expressions."""

import pandas as pd
import numpy as np


# Define constants used in the code below
RANDOM_SEED = 888
N_ROWS = 1000
JD = {"pattern": r"(Juris Doctor|Bachelor of Laws)", "flag_column_name": "degree_jd"}
LLM = {
    "pattern": r"((^(Executive )?LLM)|(^MC|MI|ML)|(^Master of (Comp|Envir|Laws|Studies)))",
    "flag_column_name": "degree_llm",
}
SJD = {"pattern": r"(Doctor of (Juridical|Comparative))", "flag_column_name": "degree_sjd"}

DEGREES = [
    "Juris Doctor",
    "Bachelor of Laws",
    "BA-Bachelor of Arts",
    "BSBA-Bachelor of Science in Business Admin",
    "BS-Bachelor of Science",
    "LLM-Master of Laws",
    "LLM-Taxation",
    "LLM-Sec and Financial Reg",
    "LLM-Intl Legal Studies",
    "MLT-Master of Laws (Tax)",
    "Master of Divinity",
    "Doctor of Juridical Science",
]


# Create data set
df = pd.DataFrame(
    data={
        "id": list(range(1000, 1000 + N_ROWS)),
        "degree": np.random.choice([k for k in DEGREES], size=N_ROWS),
    }
)


# Flag degree types with regex patterns
def flag_degrees(df, pattern, flag_column_name):
    result = df[df["degree"].str.contains(pattern, na=False, regex=True)]
    result[flag_column_name] = 1
    return result


alumni_jd = flag_degrees(df, JD["pattern"], JD["flag_column_name"])
alumni_llm = flag_degrees(df, LLM["pattern"], LLM["flag_column_name"])
alumni_sjd = flag_degrees(df, SJD["pattern"], SJD["flag_column_name"])

alumni_jd.head()
alumni_llm.head()
alumni_sjd.head()
