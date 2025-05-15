from pathlib import Path

import pandas as pd


input_file_path = Path("output", "nist-infiltration", "results.csv")
report_path = Path("reports", "nist-infiltration", "report.csv")

df = pd.read_csv(input_file_path)

data = df.drop(columns=["Month", "Day", "Hour"], axis=1).T[0]

column_map = {}

original_columns = df.columns.drop(["Month", "Day", "Hour"])

for original_column in original_columns:
    substrings = original_column.split("_")
    name_number = substrings[0]
    name = name_number[:-1]
    number = name_number[-1]

    if "Pressure" in substrings:
        new_column = f"{name} {number} Pressure [Pa]"
    else:
        new_column = f"{name} {number} Flow Rate [kg/s]"
    column_map.update({new_column: original_column})

restructured_df = {new_column: [] for new_column in column_map.keys()}

for new_column in restructured_df.keys():
    original_column = column_map[new_column]
    restructured_df[new_column].append(data[original_column])


pd.DataFrame(restructured_df).to_csv(report_path)
