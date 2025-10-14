from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List


from dimes import LinesOnly, DimensionalPlot, DisplayData
from pandas import DataFrame, concat, date_range, read_csv, read_excel


def capitalize_and_remove_underscores(string: str):
    return " ".join([sub_string.capitalize() for sub_string in string.replace("-", "_").split("_")])


def get_date_time():
    date_time = date_range(start=datetime(2000, 1, 1, 0), end=datetime(2000, 12, 31, 23), freq="h")
    # pylint: disable=E1101,E1101
    return date_time[~((date_time.month == 2) & (date_time.day == 29))]


def get_detailed_data_frame(case: str, excel_tab: str) -> DataFrame:
    df = read_excel(
        Path("reports", "std-140", f"Std140_CB_Output_{case}.xlsx"),
        sheet_name=excel_tab,
        skiprows=1,
    )
    df = df.iloc[:, :-1]
    columns = df.iloc[0]
    df = df[1:]
    df.columns = [column for column in columns]
    df.reset_index(drop=True, inplace=True)
    return df


plot_directory = Path("output", "std-140", "GRAPHS")

date_time = get_date_time()

cases = ["CB1000"]

for case in cases:
    for excel_tab, annual_software_energy in zip(
        ["Hourly-SensibleCoolingRate", "Hourly-HeatingRate"], ["annual_software_cooling", "annual_software_heating"]
    ):
        df_cse = read_excel(
            Path("reports", "std-140", f"Std140_CB_Output_{case}.xlsx"),
            sheet_name=excel_tab,
            skiprows=1,
        )
        df_cse.set_index(keys="Date/Time", inplace=True)

        df_annual_software_energy = read_csv(f"{annual_software_energy}.csv", index_col="Software")

        annual_energy_use: Dict[str, List[float]] = {}
        building_total = 0
        for column in df_cse.columns:
            zone_annual_total = sum(df_cse[column]) * 3600 / 1e6  # kW/h -> GJ
            annual_energy_use[column] = zone_annual_total
            building_total += zone_annual_total

        df = DataFrame(annual_energy_use, index=["F"])
        df.index.name = "Software"
        df.loc["F", "Whole"] = building_total

        df = concat([df, df_annual_software_energy]).sort_index()
        df_average = df.apply(lambda column: sum(column) / len(column), axis=0)

        df_diff = df.copy()

        for column in df_average.index:
            for software in df.index:
                df_diff.loc[software, column] = (df.loc[software, column] - df_average[column]) * 100.0 / df_average[column]

        print(df_diff.loc["F"])
