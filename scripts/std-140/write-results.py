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

m_ft = 3.28084
south_perimeter_volume = 40.7643 * 4.5732 * 2.7432

template_file_root = "Std140_CB_Output"
test_suite = "std-140"
current_directory = os.path.dirname(
    os.path.dirname(os.getcwd())
)  # Use when called from rakefile
# current_directory = os.getcwd()  # Use when running script directly
template_file_name = f"{template_file_root}_Template.xlsx"
template_file_path = Path(f"{current_directory}/docs/{test_suite}/{template_file_name}")

hourly_results_file_name = "OUTPUT_HOURLY.csv"
sub_hourly_results_file_name = "OUTPUT_SUB_HOURLY.csv"

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
zone_sheet = "Hourly-Bottom_Perimeter_South"

infiltration_mass_flow_rate = "Infiltration mass flow rate [kg/s] b"
ventilation_mass_flow_rate = "Ventilation mass flow rate [kg/s] b"
ventilation_sensible_heat_transfer_rate = (
    "Sensible heat transfer rate into the zone due to ventilation [kW] c"
)
ventilation_latent_heat_transfer_rate = (
    "Latent heat transfer rate into the zone due to ventilation [kW] c"
)


window_net_heat_transfer_rate = (
    "Total net heat transfer rate through the windows [kW] c,e"
)
window_net_heat_transfer_rate_conduction = f"{window_net_heat_transfer_rate} Conduction"
window_net_heat_transfer_rate_radiation = (
    f"{window_net_heat_transfer_rate} Incident Radiation"
)

zone_columns = [
    "Current outdoor air density a [kg/m3]",
    infiltration_mass_flow_rate,
    "Sensible heat transfer rate into the zone due to infiltration [kW] c",
    "Latent heat transfer rate into the zone due to infiltration [kW] c",
    ventilation_mass_flow_rate,
    ventilation_sensible_heat_transfer_rate,
    ventilation_latent_heat_transfer_rate,
    "Total window transmitted solar radiation rate [kW] c,d",
    window_net_heat_transfer_rate,
    "Total exterior surface conduction heat transfer rate [kW] c",
    "Total exterior surface incident solar radiation rate [kW] d",
    "Total exterior surface convection heat transfer rate [kW] f",
    "Total interior surface conduction heat transfer rate [kW] c*",
    "Total interior surface convection heat transfer rate [kW] f*",
    "Total interior surface conduction heat transfer rate [kW] c^",
    "Total interior surface convection heat transfer rate [kW] f^",
]


sub_hourly_average = [
    "Dry Air Mass",
    "ACH",
    "Moist Air Density [kg/m3]",
    window_net_heat_transfer_rate_conduction,
]
sub_hourly_sum = [
    ventilation_latent_heat_transfer_rate,
]


def post_processing(df_hourly: pd.DataFrame, df_sub_hourly: pd.DataFrame):
    df_sub_hourly["Minute"] = (df_sub_hourly["SubHour"] - 1) * 10
    df_sub_hourly["Datetime"] = pd.to_datetime(
        df_sub_hourly[["Month", "Day", "Hour", "Minute"]].assign(year=2024)
    )
    df_hourly["Datetime"] = pd.to_datetime(
        df_hourly[["Month", "Day", "Hour"]].assign(year=2024)
    )
    df_sub_hourly.index = df_sub_hourly["Datetime"]
    df_hourly.index = df_hourly["Datetime"]
    for column in df_sub_hourly.columns:
        if column in sub_hourly_average:
            df_hourly[column] = df_sub_hourly[column].resample("H").mean()
        elif column in sub_hourly_sum:
            df_hourly[column] = df_sub_hourly[column].resample("H").sum()

    df_hourly[infiltration_mass_flow_rate] = (
        df_hourly["ACH"]
        / 3600
        * df_hourly["Moist Air Density [kg/m3]"]
        * south_perimeter_volume
        - df_hourly[ventilation_mass_flow_rate]
    )  # df_hourly["Moist Air Density [kg/m3]"] * south_perimeter_volume could be replaced with zone air mass

    df_hourly[ventilation_sensible_heat_transfer_rate] = (
        df_hourly[ventilation_mass_flow_rate]
        * df_hourly["Air Specific Enthalpy Change [kJ/kg]"]
    )

    df_hourly[window_net_heat_transfer_rate] = (
        df_hourly[window_net_heat_transfer_rate_conduction]
        + df_hourly[window_net_heat_transfer_rate_radiation]
    )
    df_hourly.index = [value for value in range(8760)]
    return df_hourly


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

    hourly_results_file_path = Path(results_directory, case, hourly_results_file_name)
    sub_hourly_results_file_path = Path(
        results_directory, case, sub_hourly_results_file_name
    )

    df_case_data_hourly = pd.read_csv(hourly_results_file_path)
    df_case_data_sub_hourly = pd.read_csv(sub_hourly_results_file_path)

    df_case_data_hourly = post_processing(df_case_data_hourly, df_case_data_sub_hourly)

    sheets = pd.read_excel(template, sheet_name=None, engine="openpyxl", header=1)

    for hourly_sheet in hourly_sheets:
        hourly_sheet_name = f"Hourly-{hourly_sheet}"
        df_sheet = sheets[hourly_sheet_name]
        columns = df_sheet.columns[1:]
        for column in columns:
            case_data_column = f"{hourly_sheet}_{column}"
            df_sheet[column] = df_case_data_hourly[case_data_column]

        sheet = template[
            hourly_sheet_name
        ]  # Access the corresponding sheet in the template
        for row_idx, row in enumerate(
            dataframe_to_rows(df_sheet, index=False, header=False), start=2
        ):
            for col_idx, value in enumerate(row, start=1):
                sheet.cell(row=row_idx + 1, column=col_idx, value=value)
        print("Data successfully added to the XLSX file.")

    df_sheet = sheets[zone_sheet]
    df_sheet = df_sheet.iloc[:, :-1]
    df_sheet.columns = df_sheet.iloc[0]
    df_sheet = df_sheet[1:]
    for zone_column in zone_columns:
        df_sheet[zone_column] = df_case_data_hourly[zone_column]

    sheet = template[zone_sheet]  # Access the corresponding sheet in the template
    for row_idx, row in enumerate(
        dataframe_to_rows(df_sheet, index=False, header=False), start=3
    ):
        for col_idx, value in enumerate(row, start=1):
            sheet.cell(row=row_idx + 1, column=col_idx, value=value)

    print(f"Done processing case {case}.")
    print("Writing results to XLSX ...")
    template.save(f"{current_directory}/reports/{test_suite}/{output_file_name}")
print(f"\nDone processing all cases.")
