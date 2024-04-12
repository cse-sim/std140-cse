import pandas as pd
from datetime import datetime, timedelta
import openpyxl as xl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from shutil import rmtree
import warnings
import os


class HeaterConsumptionPlots:

    def __init__(self):

        warnings.filterwarnings("ignore")

        pd.set_option("display.max_rows", 500)
        pd.set_option("display.max_columns", 100)

        self.outputs_file_path = Path("output/etna/OUTPUTS")
        self.dataframe_file_path = Path(self.outputs_file_path, "DATA")
        self.graphs_file_path = Path(self.outputs_file_path, "GRAPHS")
        self.create_or_replace_folder(self.outputs_file_path)
        self.create_or_replace_folder(self.dataframe_file_path)
        self.create_or_replace_folder(self.graphs_file_path)

        self.measured_data_directory = "docs/etna"
        self.simulated_data_path = self.find_measured_file_path("reports/etna")

        self.template = xl.load_workbook(filename=self.simulated_data_path)
        self.cases = self.template.sheetnames

        self.measured_data = {
            "ET100": {
                "ET100A": "ET100A-Measurements-GMT+1 (071123).csv",
                "ET100B": "ET100B-Measurements-GMT+1 (071123).csv",
            },
            "ET110": {
                "ET110A": "ET110A-Measurements-GMT+1 (071123).csv",
                "ET110B": "ET110B-Measurements-GMT+1 (071123).csv",
            },
        }

        self.output_cases = {
            "ET100": {
                "A": {"Measured": {"ET100A"}, "Simulated": {"ET100A1", "ET100A3"}},
                "B": {"Measured": {"ET100B"}, "Simulated": {"ET100B1", "ET100B3"}},
            },
            "ET110": {
                "A": {"Measured": {"ET110A"}, "Simulated": {"ET110A1", "ET110A2"}},
                "B": {"Measured": {"ET110B"}, "Simulated": {"ET110B1", "ET110B2"}},
            },
        }

        self.experiment_dates = {
            "ET100": {
                "start date": datetime(2000, 9, 8, 16, 0),
                "end date": datetime(2000, 9, 18, 14, 0),
            },
            "ET110": {
                "start date": datetime(2000, 1, 26, 12, 0),
                "end date": datetime(2000, 2, 11, 9, 0),
            },
        }

        self.steady_state_dates = {
            "ET100": {
                "start date": datetime(2000, 9, 16, 8, 0),
                "end date": datetime(2000, 9, 18, 14, 0),
            },
            "ET110": {
                "start date": datetime(2000, 2, 10, 16, 0),
                "end date": datetime(2000, 2, 11, 9, 0),
            },
        }

        self.error = {
            "ET100A": 0.0071,
            "ET100B": 0.0093,
            "ET110A": 0.0091,
            "ET110B": 0.0102,
        }

        self.simulated_data = {
            "ET100": {"ET100A1", "ET100B1", "ET100A3", "ET100B3"},
            "ET110": {"ET110A1", "ET110A2", "ET110B1", "ET110B2"},
        }

        self.quantity_types = {
            "Heater Energy Consumption (Wh)": {
                "yaxis": "y1",
                "legend_label": "Heater Energy Consumption",
            },
            "Cell Temperature (C)": {
                "yaxis": "y2",
                "legend_label": "Temperature",
            },
        }

        self.hide_legend_cases = ["ET100A3", "ET100B3", "ET110A2", "ET110B2"]

    def create_or_replace_folder(self, path):
        if path.exists():
            rmtree(path)
        path.mkdir(exist_ok=True)

    def call_csv(self, path):
        data = pd.read_csv(path, encoding="unicode_escape")
        df = pd.DataFrame(data)
        return df

    def find_measured_file_path(self, path):
        for file in os.listdir(path):
            if file.startswith("CSE-ET100series"):
                return os.path.join(path, file)

    def find_dates(self, series):
        df = self.call_csv(
            f"{self.measured_data_directory}/{series}B-Measurements-GMT+1 (071123).csv"
        )
        df.columns = df.iloc[1]
        df = df.drop([0, 1, 2]).reset_index()
        return pd.DataFrame(
            [
                datetime.strptime(date, "%m/%d/%Y %H:%M")
                for date in list(df["Date (XLS format)"])
            ],
            columns=["Date"],
        )

    def call_df_measured(self, series):
        if series == "ET100":
            return self.df_ET100
        elif series == "ET110":
            return self.df_ET110

    def define_line_type(self, simualted_or_measured, legend_label, case):
        if legend_label == "Temperature":
            if simualted_or_measured == "Measured":
                return dict(color="black", dash="dot")
            else:
                if case[-1] == "1":
                    return dict(color="red", dash="dot")
                else:
                    return dict(color="blue", dash="dot")
        else:
            if simualted_or_measured == "Measured":
                return dict(color="black")
            else:
                if case[-1] == "1":
                    return dict(color="red")
                else:
                    return dict(color="blue")

    def get_heat_consumption_plots(self):

        self.df_ET100 = self.find_dates("ET100")
        self.df_ET110 = self.find_dates("ET110")

        for case in self.cases:
            if case in self.simulated_data["ET100"]:
                df = self.df_ET100
            else:
                df = self.df_ET110
            df_simulated = pd.read_excel(
                self.simulated_data_path, sheet_name=case, header=3
            )
            df_simulated = df_simulated.drop([0]).reset_index()
            if case in ["ET100A1", "ET100A3"]:
                df_simulated.loc[len(df.index)] = None
            df[f"{case} Heater Energy Consumption (Wh) - Simulated"] = list(
                df_simulated["Qhtr"]
            )
            df[f"{case} Cell Temperature (C) - Simulated"] = df_simulated["Tcell"]

        self.df_ET100.to_csv(
            f"{self.dataframe_file_path}/ET100_Series.csv", index=False
        )
        self.df_ET110.to_csv(
            f"{self.dataframe_file_path}/ET110_Series.csv", index=False
        )

        for (
            series
        ) in (
            self.measured_data.keys()
        ):  # pylint: disable=consider-using-dict-items / E1136
            df_measured = self.call_df_measured(series)
            for case, file in self.measured_data[series].items():
                df = self.call_csv(f"{self.measured_data_directory}/{file}")
                df.columns = df.iloc[1]
                df = df.drop([0, 1, 2]).reset_index()
                if case == "ET100A":
                    df.loc[len(df.index)] = None
                df_measured[f"{case} Heater Energy Consumption (Wh) - Measured"] = df[
                    "Qhtr"
                ]
                df_measured[f"{case} Cell Temperature (C) - Measured"] = df["Tcell"]

        for (
            series
        ) in (
            self.output_cases.keys()
        ):  # pylint: disable=consider-using-dict-items / E1136
            df = self.call_df_measured(series)
            for cell in self.output_cases[series].keys():
                fig = go.Figure()
                fig = make_subplots(specs=[[{"secondary_y": True}]])

                y_max = []
                for simulated_or_measured in self.output_cases[series][cell].keys():
                    for case in self.output_cases[series][cell][simulated_or_measured]:
                        for (
                            quantity_type,
                            quantity_details,
                        ) in self.quantity_types.items():
                            legend_label = quantity_details["legend_label"]
                            yaxis = quantity_details["yaxis"]
                            start_date = self.steady_state_dates[series]["start date"]
                            end_date = self.steady_state_dates[series]["end date"]
                            experiment_end_date = self.experiment_dates[series][
                                "end date"
                            ]
                            if case in ["ET100B", "ET100B1", "ET100B3"]:
                                experiment_end_date += timedelta(hours=1)
                            y_values = df[
                                f"{case} {quantity_type} - {simulated_or_measured}"
                            ].astype(float)
                            fig.add_trace(
                                go.Scatter(
                                    x=df["Date"],
                                    y=y_values,
                                    legendgroup=f"{case}-{simulated_or_measured}",
                                    legendgrouptitle={
                                        "text": f"{case}-{simulated_or_measured}"
                                    },
                                    name=legend_label,
                                    mode="lines",
                                    yaxis=yaxis,
                                    line=self.define_line_type(
                                        simulated_or_measured, legend_label, case
                                    ),
                                    visible=(
                                        "legendonly"
                                        if case in self.hide_legend_cases
                                        else True
                                    ),
                                )
                            )
                            y_max.append(max(y_values))
                            if (simulated_or_measured == "Measured") & (yaxis == "y1"):
                                df_uncertainty_band = df[
                                    (df["Date"] >= start_date)
                                    & (df["Date"] <= end_date)
                                ]
                                y_values_df_uncertainty_band = df_uncertainty_band[
                                    f"{case} Heater Energy Consumption (Wh) - {simulated_or_measured}"
                                ].astype(float)
                                y_average = sum(y_values_df_uncertainty_band) / len(
                                    y_values_df_uncertainty_band
                                )
                                y_upper_band = [
                                    y_average * (1 + self.error[f"{series}{cell}"])
                                    for n in range(len(y_values_df_uncertainty_band))
                                ]
                                y_lower_band = [
                                    y_average * (1 - self.error[f"{series}{cell}"])
                                    for n in range(len(y_values_df_uncertainty_band))
                                ]
                                fig.add_trace(
                                    go.Scatter(
                                        x=df_uncertainty_band["Date"],
                                        y=y_lower_band,
                                        line=dict(
                                            color="rgba(50,50,50,0.25)", dash="solid"
                                        ),
                                        marker=dict(opacity=0),
                                        showlegend=False,
                                    )
                                )
                                fig.add_trace(
                                    go.Scatter(
                                        x=df_uncertainty_band["Date"],
                                        y=y_upper_band,
                                        fill="tonexty",
                                        name="95% Measured Confidence Interval",
                                        mode="lines",
                                        line=dict(
                                            color="rgba(50,50,50,0.25)", dash="solid"
                                        ),
                                        marker=dict(opacity=0),
                                    )
                                )
                y_max = max(y_max)
                fig.add_trace(
                    go.Scatter(
                        x=[start_date, start_date, end_date, end_date],
                        y=[0, y_max, y_max, 0],
                        fill="tozeroy",
                        mode="none",
                        fillcolor="rgba(26,150,65,0.1)",
                        name="Steady State",
                    )
                )
                fig.update_xaxes(
                    mirror=True,
                    ticks="outside",
                    showline=True,
                    linecolor="black",
                    range=[
                        self.experiment_dates[series]["start date"],
                        experiment_end_date,
                    ],
                )
                fig.update_yaxes(
                    mirror=True,
                    ticks="outside",
                    showline=True,
                    linecolor="black",
                    range=[0, y_max],
                    secondary_y=False,
                )
                fig.update_yaxes(
                    mirror=True,
                    ticks="outside",
                    showline=True,
                    linecolor="black",
                    range=[8, 37],
                    secondary_y=True,
                )
                fig.update_layout(
                    yaxis_title=f"Heater Energy Consumtpion (Wh)",
                    xaxis_title="Time",
                    title=f"{series}{cell}",
                    title_x=0.5,
                    plot_bgcolor="white",
                    font_color="black",
                )
                file_path = f"{self.graphs_file_path}/{series}{cell}-heater.html"
                fig.write_html(file_path)
                print(case, y_average, y_upper_band[0], y_lower_band[0])
