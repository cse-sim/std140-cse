print("\nInitializing Python...\n")
import openpyxl as xl
import pandas as pd
from datetime import datetime
import mako.template as mk
import os
import pytz
import os, glob
from openpyxl import load_workbook
from pathlib import Path
from openpyxl.utils.dataframe import dataframe_to_rows


def call_csv(path):
    data = pd.read_csv(path)
    return pd.DataFrame(data)


# delete output file
def delete_output_file(path):
    for file in glob.glob(f"{path}*"):
        os.remove(file)


# prints date and time with time zone on each plot
def find_todays_date():
    utc_timezone = pytz.timezone("America/Denver")
    current_date_time = datetime.now(utc_timezone)
    return current_date_time.strftime("%b %d, %Y")


template_column_row = 2
first_data_row = template_column_row + 1
last_data_row = first_data_row + 8760

template_file_root = "Std140_CB_Output"
test_suite = "std-140"
# current_directory = os.path.dirname(os.path.dirname(os.getcwd()))
current_directory = os.getcwd()
template_file_name = f"{template_file_root}_Template.xlsx"
template_file_path = Path(f"{current_directory}/docs/{test_suite}/{template_file_name}")

results_file_name = "OUTPUT.csv"
results_directory = Path(f"{current_directory}/output/{test_suite}")

todays_date = find_todays_date()

cases = ["CB1000", "CB1010", "CB1020", "CB1100"]


annual_tab = "AnnualOutputs"
hourly_sheets = [
    "ZoneAirTemp",
    "SensibleCoolingRate",
    "HeatingRate",
    "LightingPower",
    "PlugLoadPower",
]

for case in cases:
    template = xl.load_workbook(filename=template_file_path)

    information_sheet = template["Information"]
    information_sheet.cell(row=2, column=2, value=case)
    information_sheet.cell(row=3, column=2, value="CSE 0.923.0")
    information_sheet.cell(row=4, column=2, value="Dec 18, 2024")
    information_sheet.cell(row=5, column=2, value="Big Ladder Software")
    information_sheet.cell(
        row=6,
        column=2,
        value="neal.kruis@bigladdersoftware.com; nathan.oliver@bigladdersoftware.com; chipbarnaby@gmail.com",
    )
    information_sheet.cell(row=7, column=2, value=todays_date)

    output_file_name = f"{template_file_root}_{case}.xlsx"
    output_file_path = Path(
        f"{current_directory}/reports/{test_suite}/{output_file_name}"
    )
    delete_output_file(output_file_path)

    results_file_path = Path(results_directory, case, results_file_name)
    df_case_data = pd.read_csv(results_file_path)

    sheets = pd.read_excel(template, sheet_name=None, engine="openpyxl", header=1)

    for hourly_sheet in hourly_sheets:
        hourly_sheet_name = f"Hourly-{hourly_sheet}"
        df_sheet = sheets[hourly_sheet_name]
        columns = df_sheet.columns[1:]
        for column in columns:
            case_data_column = f"{hourly_sheet}_{column}"
            df_sheet[column] = df_case_data[case_data_column]

        sheet = template[
            hourly_sheet_name
        ]  # Access the corresponding sheet in the template
        for row_idx, row in enumerate(
            dataframe_to_rows(df_sheet, index=False, header=False), start=2
        ):
            for col_idx, value in enumerate(row, start=1):
                sheet.cell(row=row_idx + 1, column=col_idx, value=value)
        print("Data successfully added to the XLSX file.")
    print(f"Done processing case {case}.")
    print("Writing results to XLSX ...")
    template.save(f"{current_directory}/reports/{test_suite}/{output_file_name}")
print(f"\nDone processing all cases.")
