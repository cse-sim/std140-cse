import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta
from pathlib import Path
from shutil import rmtree
import os


class HeatFluxPlots:

    def __init__(self):

        self.GRID_LINE_COLOR = "rgba(128,128,128,0.3)"
        self.GRID_LINE_WIDTH = 1.5
        self.SURFACE_SUB_STRING = "surface total convective and radiative flux"
        self.INSIDE_SURFACE_SUB_STRING = (
            "inside surface total convective and radiative flux"
        )

        self.plot_data = {
            "ET110A1": {
                "Ceiling Path 1": {
                    "measured_average_heat_flux": 4.096,
                    "color": sns.color_palette("Greens_r")[0],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "Ceiling Path 2": {
                    "measured_average_heat_flux": 4.485,
                    "color": sns.color_palette("Greens_r")[1],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "Floor Path 1": {
                    "measured_average_heat_flux": 8.541,
                    "color": sns.color_palette("Blues_r")[0],
                    "visible": True,
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "Floor Path 2": {
                    "measured_average_heat_flux": 11.059,
                    "color": sns.color_palette("Blues_r")[1],
                    "visible": True,
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "Floor Path 3": {
                    "measured_average_heat_flux": 18.834,
                    "color": sns.color_palette("Blues_r")[2],
                    "visible": True,
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "North wall": {
                    "measured_average_heat_flux": 16.994,
                    "color": sns.color_palette("Reds_r")[0],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "Door": {
                    "measured_average_heat_flux": 15.604,
                    "color": sns.color_palette("Reds_r")[1],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "East wall": {
                    "measured_average_heat_flux": 9.741,
                    "color": sns.color_palette("Purples_r")[0],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "East window Path 1": {
                    "measured_average_heat_flux": 5.465,
                    "color": sns.color_palette("Purples_r")[1],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
                "East window Path 2": {
                    "measured_average_heat_flux": 5.558,
                    "color": sns.color_palette("Purples_r")[2],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
                "East window Path 3": {
                    "measured_average_heat_flux": 97.086,
                    "color": sns.color_palette("Purples_r")[3],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
                "South wall": {
                    "measured_average_heat_flux": 9.393,
                    "color": sns.color_palette("Greys_r")[0],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "South window Path 1": {
                    "measured_average_heat_flux": 5.524,
                    "color": sns.color_palette("Greys_r")[1],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
                "South window Path 2": {
                    "measured_average_heat_flux": 5.618,
                    "color": sns.color_palette("Greys_r")[2],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
                "South window Path 3": {
                    "measured_average_heat_flux": 98.141,
                    "color": sns.color_palette("Greys_r")[3],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
                "West wall": {
                    "measured_average_heat_flux": 7.189,
                    "color": sns.color_palette("BrBG")[0],
                    "visible": True,
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
            },
            "ET110B1": {
                "Ceiling Path 1": {
                    "measured_average_heat_flux": 3.814,
                    "color": sns.color_palette("Greens_r")[0],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "Ceiling Path 2": {
                    "measured_average_heat_flux": 4.228,
                    "color": sns.color_palette("Greens_r")[1],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "Floor Path 1": {
                    "measured_average_heat_flux": 9.956,
                    "color": sns.color_palette("Blues_r")[0],
                    "visible": True,
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "Floor Path 2": {
                    "measured_average_heat_flux": 12.787,
                    "color": sns.color_palette("Blues_r")[1],
                    "visible": True,
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "Floor Path 3": {
                    "measured_average_heat_flux": 21.198,
                    "color": sns.color_palette("Blues_r")[2],
                    "visible": True,
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "North wall": {
                    "measured_average_heat_flux": 16.156,
                    "color": sns.color_palette("Reds_r")[0],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "Door": {
                    "measured_average_heat_flux": 14.736,
                    "color": sns.color_palette("Reds_r")[1],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "East wall": {
                    "measured_average_heat_flux": 6.298,
                    "color": sns.color_palette("BrBG")[0],
                    "visible": True,
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "South wall": {
                    "measured_average_heat_flux": 11.448,
                    "color": sns.color_palette("Greys_r")[0],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "South window Path 1": {
                    "measured_average_heat_flux": 5.707,
                    "color": sns.color_palette("Greys_r")[1],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
                "South window Path 2": {
                    "measured_average_heat_flux": 5.753,
                    "color": sns.color_palette("Greys_r")[2],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
                "South window Path 3": {
                    "measured_average_heat_flux": 99.393,
                    "color": sns.color_palette("Greys_r")[3],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
                "West wall": {
                    "measured_average_heat_flux": 8.740,
                    "color": sns.color_palette("Purples_r")[0],
                    "visible": "legendonly",
                    "column_name_sub_string": self.INSIDE_SURFACE_SUB_STRING,
                },
                "West window Path 1": {
                    "measured_average_heat_flux": 5.713,
                    "color": sns.color_palette("Purples_r")[1],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
                "West window Path 2": {
                    "measured_average_heat_flux": 5.760,
                    "color": sns.color_palette("Purples_r")[2],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
                "West window Path 3": {
                    "measured_average_heat_flux": 99.513,
                    "color": sns.color_palette("Purples_r")[3],
                    "visible": "legendonly",
                    "column_name_sub_string": self.SURFACE_SUB_STRING,
                },
            },
        }

        self.layout_data = {
            "x_axis_limits": {
                "start": datetime(2000, 2, 2, 12, 0),
                "end": datetime(2000, 2, 11, 9, 0),
            },
            "steady_state": {
                "start": datetime(2000, 2, 10, 16, 0),
                "end": datetime(2000, 2, 11, 9, 0),
            },
        }

    def find_measured_file_path(self, path):
        for file in os.listdir(path):
            if file.startswith("CSE-ET100series"):
                return os.path.join(path, file)

    def call_csv(self, path):
        data = pd.read_csv(path, encoding="unicode_escape")
        df = pd.DataFrame(data)
        return df

    def get_relative_heat_flux(self, values, experiment, surface):
        measured_average_heat_flux = self.plot_data[experiment][surface][
            "measured_average_heat_flux"
        ]
        return (values - measured_average_heat_flux) / measured_average_heat_flux * 100

    def get_color(self, experiment, surface):
        rgb_values_255 = tuple(
            int(round(value * 255))
            for value in self.plot_data[experiment][surface]["color"]
        )
        return f"rgb{rgb_values_255}"

    def get_x_axis_limits(self):
        start_date = self.layout_data["x_axis_limits"]["start"]
        end_date = self.layout_data["x_axis_limits"]["end"]
        return [start_date, end_date]

    def get_y_axis_limits(self, values, y_axis_limits):
        min_value = min(values)
        max_value = max(values)
        y_axis_limits["min_values"].append(min_value)
        y_axis_limits["max_values"].append(max_value)
        return y_axis_limits

    def plot_steady_state_period(self, y_min, y_max):
        start_date = self.layout_data["steady_state"]["start"]
        end_date = self.layout_data["steady_state"]["end"]

        self.fig.add_trace(
            go.Scatter(
                x=[start_date, start_date, end_date, end_date],
                y=[y_min, y_max, y_max, y_min],
                fill="toself",
                mode="none",
                fillcolor="rgba(26,150,65,0.1)",
                name="Steady State",
            )
        )

    def get_heat_flux_plots(self):

        simulated_data_path = self.find_measured_file_path("reports/etna")

        experiments = ["ET110A1", "ET110B1"]
        dataframes = {}
        for experiment in experiments:
            df = pd.read_excel(
                simulated_data_path,
                sheet_name=experiment,
                header=2,
                skiprows=[3, 4],
                engine="openpyxl",
            )
            dataframes.update({experiment: df})

        plot_output_directory = Path("output\etna\OUTPUTS\GRAPHS")

        for experiment in experiments:
            # Get x-axis data
            df = dataframes[experiment]
            df.columns.values[0] = "Time"

            for index in df.index[:-1]:
                df.loc[index + 1, "Time"] = df.loc[index, "Time"] + timedelta(hours=1)

            # start_date = layout_data["x_axis_limits"]["start"]
            # end_date = layout_data["x_axis_limits"]["end"]
            # df = df[(df["Time"] >= start_date) & (df["Time"] <= end_date)]
            x_data = df["Time"]

            y_axis_limits = {"min_values": [], "max_values": []}

            self.fig = go.Figure()
            for surface in self.plot_data[experiment].keys():
                column_name_sub_string = self.plot_data[experiment][surface][
                    "column_name_sub_string"
                ]
                column_name = f"{surface} {column_name_sub_string}"
                y_data = self.get_relative_heat_flux(
                    df[column_name], experiment, surface
                )
                color = self.get_color(experiment, surface)
                self.fig.add_trace(
                    go.Scatter(
                        x=x_data,
                        y=y_data,
                        name=surface,
                        mode="lines",
                        line={"color": color},
                        # hoveron="points+fills",
                        visible=self.plot_data[experiment][surface]["visible"],
                    )
                )
                y_axis_limits = self.get_y_axis_limits(y_data, y_axis_limits)
            y_min = min(y_axis_limits["min_values"])
            y_max = max(y_axis_limits["max_values"])
            self.plot_steady_state_period(y_min, y_max)

            self.fig.update_layout(
                title=f"{experiment}<br>Surface Heat Flux Relative to Average Measured Surface Heat Flux",
                xaxis_title="Time",
                yaxis_title="Percentage",
                title_x=0.5,
                plot_bgcolor="white",
                font_color="black",
                xaxis=dict(
                    zeroline=True,
                    zerolinecolor=self.GRID_LINE_COLOR,
                    zerolinewidth=self.GRID_LINE_WIDTH,
                ),
                yaxis=dict(
                    zeroline=True,
                    zerolinecolor="black",
                    zerolinewidth=self.GRID_LINE_WIDTH,
                ),
            )
            self.fig.update_xaxes(
                showline=True,
                linecolor="black",
                linewidth=self.GRID_LINE_WIDTH,
                mirror=True,
                showgrid=True,
                gridcolor=self.GRID_LINE_COLOR,
                gridwidth=self.GRID_LINE_WIDTH,
                fixedrange=False,
                ticks="outside",
                tickson="boundaries",
                tickwidth=self.GRID_LINE_WIDTH,
                tickcolor="black",
                range=self.get_x_axis_limits(),
            )
            self.fig.update_yaxes(
                showline=True,
                linecolor="black",
                linewidth=self.GRID_LINE_WIDTH,
                mirror=True,
                showgrid=True,
                gridcolor=self.GRID_LINE_COLOR,
                gridwidth=self.GRID_LINE_WIDTH,
                fixedrange=False,
                ticks="outside",
                tickson="boundaries",
                tickwidth=self.GRID_LINE_WIDTH,
                tickcolor="black",
                range=[y_min, y_max],
            )

            file_path = Path(plot_output_directory) / f"{experiment}-heat-flux.html"
            self.fig.write_html(file_path)
