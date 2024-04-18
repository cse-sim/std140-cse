import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import os
from pathlib import Path
from shutil import rmtree

current_directory = os.getcwd()
input_directory = Path(os.getcwd(), "reports/rp-1052")
output_directory = Path(os.getcwd(), "output/rp-1052")
xls_file = pd.ExcelFile(Path(input_directory, "tc1-results.xlsx"))
df_cell_temperature = pd.DataFrame(
    pd.read_csv(Path(input_directory, "air-temperatures.csv"))
)


sheets = xls_file.sheet_names

dataframes = {}
ADJUSTMENT = 0.1

TITLE = "CSE<br>ASHRAE 1052<br>TC1 Test"
X_AXIS_TITLE = "Hour"
Y_AXIS1_TITLE = "Temperature [C]"
Y_AXIS2_TITLE = "Heat Flux [Wh/m2]"
INTERIOR_AIR_TEMPERATURE = "Interior"
EXTERIOR_AIR_TEMPERATURE = "Exterior"
INTERIOR_SURFACE_TEMPERATURE = "Interior Surface Temperature [C]"
EXTERIOR_SURFACE_TEMPERATURE = "Exterior Surface Temperature [C]"
EXTERIOR_HEAT_FLUX = "Exterior Surface Heat Flux [Wh/m2]"


def get_rgb_color(color):
    return f"rgb{tuple(int(round(value * 255)) for value in color)}"


for sheet in sheets:
    dataframes.update({sheet: xls_file.parse(sheet)})

temperature_columns = [
    INTERIOR_SURFACE_TEMPERATURE,
    EXTERIOR_SURFACE_TEMPERATURE,
]
visible_columns = [
    EXTERIOR_AIR_TEMPERATURE,
    INTERIOR_AIR_TEMPERATURE,
    INTERIOR_SURFACE_TEMPERATURE,
]
air_temperatures = {
    EXTERIOR_AIR_TEMPERATURE: "black",
    INTERIOR_AIR_TEMPERATURE: get_rgb_color(sns.color_palette("Greens_r")[0]),
}

colors = {
    "Analytical": "Reds_r",
    "Simulated": "Blues_r",
}

line_types = {
    INTERIOR_SURFACE_TEMPERATURE: "dash",
    EXTERIOR_SURFACE_TEMPERATURE: "dot",
    EXTERIOR_HEAT_FLUX: "solid",
}

y_range = {"y1": {"max": [], "min": []}, "y2": {"max": [], "min": []}}


def update_y_range(y_axis, y_values):
    y_range[y_axis]["min"].append(min(y_values))
    y_range[y_axis]["max"].append(max(y_values))


def get_y_range(y_axis, y_range):
    y_min = min(y_range[y_axis]["min"])
    y_max = max(y_range[y_axis]["max"])
    value_range = y_max - y_min
    return [y_min - value_range * ADJUSTMENT, y_max + value_range * ADJUSTMENT]


fig = go.Figure()
fig = make_subplots(specs=[[{"secondary_y": True}]])
x_values = dataframes["Analytical"]["Hour"]
x_range = [min(x_values), max(x_values)]

cell_temperature_column = list(df_cell_temperature.columns)[1]
cell_temperature_values = df_cell_temperature[cell_temperature_column]

for air_temperature, color in air_temperatures.items():
    air_temperature_values = df_cell_temperature[air_temperature]
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=air_temperature_values,
            legendgroup="Simulated Air Temperatures [C]",
            legendgrouptitle={"text": "Simulated Air Temperatures [C]"},
            name=air_temperature,
            mode="lines",
            yaxis="y1",
            line={
                "color": color,
                "dash": "solid",
            },
            connectgaps=True,
            visible=(
                True if EXTERIOR_AIR_TEMPERATURE in visible_columns else "legendonly"
            ),
        ),
    )
    update_y_range("y1", air_temperature_values)


for dataframe_name, df in dataframes.items():
    y_columns = df.columns.drop("Hour")
    for index, column in enumerate(y_columns):
        y_values = df[column]
        y_axis = "y1" if column in temperature_columns else "y2"
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=y_values,
                legendgroup=column,
                legendgrouptitle={"text": column},
                name=dataframe_name,
                mode="lines",
                yaxis=y_axis,
                line={
                    "color": get_rgb_color(
                        sns.color_palette((colors[dataframe_name]))[0]
                    ),
                    "dash": line_types[column],
                },
                connectgaps=True,
                visible=(True if column in visible_columns else "legendonly"),
            )
        )
        update_y_range(y_axis, y_values)


fig.update_xaxes(
    mirror=True, ticks="outside", showline=True, linecolor="black", range=x_range
)
fig.update_yaxes(
    mirror=True,
    title=Y_AXIS1_TITLE,
    ticks="outside",
    showline=True,
    linecolor="black",
    range=get_y_range("y1", y_range),
    secondary_y=False,
)
fig.update_yaxes(
    mirror=True,
    title=Y_AXIS2_TITLE,
    ticks="outside",
    showline=True,
    linecolor="black",
    range=get_y_range("y2", y_range),
    secondary_y=True,
)
fig.update_layout(
    xaxis_title=X_AXIS_TITLE,
    title=TITLE,
    title_x=0.5,
    plot_bgcolor="white",
    font_color="black",
)

file_path = Path(output_directory, "cse-1052-tc1.html")
fig.write_html(file_path)
