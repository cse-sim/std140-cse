from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List


from dimes import LinesOnly, DimensionalPlot, DisplayData
import pandas as pd


def capitalize_and_remove_underscores(string: str):
    return " ".join(
        [sub_string.capitalize() for sub_string in string.replace("-", "_").split("_")]
    )


def get_date_time():
    date_time = pd.date_range(
        start=datetime(2000, 1, 1, 0), end=datetime(2000, 12, 31, 23), freq="h"
    )
    # pylint: disable=E1101,E1101
    return date_time[~((date_time.month == 2) & (date_time.day == 29))]


def get_detailed_data_frame(case: str, excel_tab: str) -> pd.DataFrame:

    df = pd.read_excel(
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


@dataclass
class PlotDetails:

    excel_tab: str
    native_units: str
    y_axis_name: str
    visible_zones: List[str]


@dataclass
class ColumnDisplayName:
    column_name: str
    display_name: str


@dataclass
class BottomPerimeterSouth:
    y_axis_name: str
    native_units: str
    column_display_names: List[ColumnDisplayName]


excel_tabs_plots_details = [
    PlotDetails(
        "Hourly-ZoneAirTemp", "degC", "Indoor Dry Bulb Temperature", ["Bottom_Core_1"]
    ),
    PlotDetails(
        "Hourly-PlugLoadPower",
        "kW",
        "Equipment Power",
        ["Bottom_Core_1", "Bottom_Corner_Northeast"],
    ),
]
bottom_perimeter_south_plot_details: List[BottomPerimeterSouth] = [
    BottomPerimeterSouth(
        "Infiltration Mass Flow Rate",
        "kg/m**3",
        [
            ColumnDisplayName(
                "Infiltration mass flow rate [kg/s] b", "Infiltration Mass Flow Rate"
            )
        ],
    )
]
plot_directory = Path("output", "std-140", "GRAPHS")

date_time = get_date_time()

cases = ["CB1000"]


def plot_basic_data():
    for case in cases:
        for plot_details in excel_tabs_plots_details:
            excel_tab = plot_details.excel_tab
            native_units = plot_details.native_units
            y_axis_name = plot_details.y_axis_name
            visible_zones = plot_details.visible_zones
            df = pd.read_excel(
                Path("reports", "std-140", f"Std140_CB_Output_{case}.xlsx"),
                sheet_name=excel_tab,
                skiprows=1,
            )
            plot = DimensionalPlot(list(date_time))
            for column in df.columns.drop("Date/Time"):
                y_values = list(df[column])
                plot.add_display_data(
                    DisplayData(
                        y_values,
                        name=capitalize_and_remove_underscores(column),
                        native_units=native_units,
                        y_axis_name=y_axis_name,
                        line_properties=LinesOnly(line_width=2),
                        is_visible=True if column in visible_zones else False,
                    )
                )
            plot.write_html_plot(Path(plot_directory, f"{excel_tab}.html"))


def plot_detailed_data():
    for case in cases:
        excel_tab = "Hourly-Bottom_Perimeter_South"
        df = get_detailed_data_frame(case=case, excel_tab=excel_tab)

        for plot_details in bottom_perimeter_south_plot_details:
            y_axis_name = plot_details.y_axis_name
            native_units = plot_details.native_units
            column_display_names = plot_details.column_display_names
            plot = DimensionalPlot(
                list(date_time), title=f"Bottom Perimeter South<br>{y_axis_name}"
            )
            for column_display_name in column_display_names:
                column_name = column_display_name.column_name
                display_name = column_display_name.display_name
                y_values = list(df[column_name])
                plot.add_display_data(
                    DisplayData(
                        y_values,
                        name=capitalize_and_remove_underscores(display_name),
                        native_units=native_units,
                        y_axis_name=y_axis_name,
                        line_properties=LinesOnly(line_width=2),
                    )
                )
        plot.write_html_plot(Path(plot_directory, f"{excel_tab}-{y_axis_name}.html"))


def plot_nsteps_temperature_comparison():
    file_name_substring = "Std140_CB_Output_CB1000-"
    zone = "Bottom_Core_1"
    nsteps = [1, 5, 120]
    plot = DimensionalPlot(
        list(date_time),
        title="nSubSteps Impact on Zone Dry Bulb Temperature<br>ASHRAE Standard 140 Full Scale Efficiency Measure Modeling Test Suite<br>Case CB1000 - Zone Bottom Core 1",
    )

    for nstep in nsteps:
        nstep_zfill = str(nstep).zfill(3)
        file_name = f"{file_name_substring}{nstep_zfill}.xlsx"
        df = pd.read_excel(
            Path(file_name),
            sheet_name="Hourly-ZoneAirTemp",
            skiprows=1,
        )
        y_values = list(df[zone])
        plot.add_display_data(
            DisplayData(
                y_values,
                name=f"nsteps = {nstep}",
                native_units="degC",
                y_axis_name="Dry Bulb Temperature",
                line_properties=LinesOnly(line_width=2),
                # is_visible=True if column in visible_zones else False,
            )
        )
    plot.write_html_plot(Path(plot_directory, f"nsteps.html"))


plot_basic_data()
plot_detailed_data()
plot_nsteps_temperature_comparison()
