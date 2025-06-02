from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List


import pandas as pd
from plotly.subplots import make_subplots

import plotly.graph_objects as go


@dataclass
class PlotDetails:
    name: str
    color: str
    marker_type: str
    marker_size: int
    data_frame: pd.DataFrame = field(default_factory=pd.DataFrame)


class Variable(Enum):
    PRESSURE = "Pressure"
    FLOW_RATE = "FlowRate"


input_file_path = Path("output", "nist-infiltration", "results.csv")
report_directory_path = Path("reports", "nist-infiltration")
report_path = Path(report_directory_path, "report.csv")
link_pressures_report_path = Path(report_directory_path, "report_link_pressures.csv")
compare_results_path = Path("docs", "nist-infiltration", "test_description_table_3.csv")

df = pd.read_csv(input_file_path)
df_compare = pd.read_csv(compare_results_path)
df_compare.set_index(keys="Name", drop=True, inplace=True)
df_compare = abs(df_compare)

substrings = [
    column.split("_") for column in df_compare.columns if len(column.split("_")) == 2
]

variables = [substring[0] for substring in substrings]
softwares = [substring[1] for substring in substrings]

variables_set = []
softwares_set = []

for variable, software in zip(variables, softwares):
    if variable not in variables_set:
        variables_set.append(variable)
    if software not in softwares_set:
        softwares_set.append(software)


multi_indices = pd.MultiIndex.from_arrays(
    [variables, softwares], names=["Variable", "Software"]
)
df_compare.columns = multi_indices

for variable in variables_set:
    indices = [(variable, software) for software in softwares_set]
    df_compare[(variable, "Average")] = df_compare[indices].apply(
        lambda x: x[indices].sum() / len(x[indices]), axis=1
    )
    df_compare[(variable, "Max")] = df_compare[indices].max(axis=1)
    df_compare[(variable, "Min")] = df_compare[indices].min(axis=1)
data = df.drop(columns=["Month", "Day", "Hour"], axis=1).T[0]
index_link_absolute_pressures = [
    index for index in data.index if ("Zone" in index) and ("Link" in index)
]
data_columns = [
    column for column in data.index if column not in index_link_absolute_pressures
]


column_map: Dict[str, str] = {}
restructured_data: Dict[str, List[float]] = {}

for original_column in data.index:
    substrings = original_column.split("_")
    name_number = substrings[0]
    name = name_number[:-1]
    number = name_number[-1]
    name_number = f"{name} {number}"

    if "Pressure" in substrings:
        new_column = f"{name} {number} {Variable.PRESSURE.value}"
    else:  # Flow Rate
        new_column = f"{name} {number} {Variable.FLOW_RATE.value}"

    column_map.update({original_column: name_number})
    if name_number not in restructured_data.keys():
        restructured_data.update({name_number: [0] * 2})

for original_column, name_number in column_map.items():

    if "Pressure" in original_column:
        index = 0
    else:  # Flow Rate
        index = 1

    restructured_data[name_number][index] = data[original_column]

cse_df = pd.DataFrame(
    data=restructured_data, index=[Variable.PRESSURE.value, Variable.FLOW_RATE.value]
).T
cse_df = abs(cse_df)

for variable in variables_set:
    variable_average = df_compare[(variable, "Average")]
    df_compare[(variable, "CSE")] = cse_df[variable].values
    variable_cse_results = df_compare[(variable, "CSE")]
    df_compare[(variable, "Absolute Difference")] = (
        variable_average - variable_cse_results
    )
    df_compare[(variable, "Percent Difference")] = (
        ((variable_average - variable_cse_results)) / variable_average * 100
    )

softwares_set.extend(["Average", "CSE", "Absolute Difference", "Percent Difference"])
final_indices = [
    (variable, software) for variable in variables_set for software in softwares_set
]

df_compare[final_indices].to_csv(report_path)

data_link_pressures = data[index_link_absolute_pressures]

link_pressures_restructured_data: Dict[str, List[float]] = {"Zone A": [], "Zone B": []}
indices = []

fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Zone Pressure",
        "Link Pressure",
        "Zone Flow Rate",
        "Link Flow Rate",
    ),
)

plot_details = {
    "CSE": PlotDetails(
        name="CSE",
        color="red",
        marker_type="circle",
        marker_size=8,
    ),
    "Max": PlotDetails(
        name="Bounds",
        color="black",
        marker_type="line-ew-open",
        marker_size=12,
    ),
    "Min": PlotDetails(
        name="Bounds",
        color="black",
        marker_type="line-ew-open",
        marker_size=12,
    ),
}

show_legend_group = []

for column_index, zone_or_link in enumerate(["Zone", "Link"]):
    df_plot = df_compare[df_compare.index.str.contains(zone_or_link)]
    for row_index, variable in enumerate(variables_set):
        plot_details["CSE"].data_frame = df_plot[(variable, "CSE")]
        plot_details["Min"].data_frame = df_plot[(variable, "Min")]
        plot_details["Max"].data_frame = df_plot[(variable, "Max")]
        for plot_detail in plot_details.values():
            if plot_detail.name not in show_legend_group:
                show_legend = True
                show_legend_group.append(plot_detail.name)
            else:
                show_legend = False
            data_frame = plot_detail.data_frame
            fig.add_trace(
                go.Scatter(
                    name=plot_detail.name,
                    x=data_frame.index,
                    y=data_frame.values,
                    mode="markers",
                    showlegend=show_legend,
                    marker={
                        "color": plot_detail.color,
                        "size": plot_detail.marker_size,
                        "symbol": plot_detail.marker_type,
                    },
                ),
                row=row_index + 1,
                col=column_index + 1,
            )
fig.update_yaxes(title_text="Pressure [Pa]", row=1, col=1)
fig.update_yaxes(title_text="Flow Rate [kg/s]", row=2, col=1)
fig.write_html("nist-infiltration-results.html")


for index in list(data_link_pressures.index):
    substrings = index.split("_")
    link_name = substrings[0]
    zone_name = substrings[1]
    value = data_link_pressures[index]
    if link_name not in indices:
        indices.append(link_name)
        link_pressures_restructured_data["Zone A"].append(value)
    else:
        link_pressures_restructured_data["Zone B"].append(value)

pd.DataFrame(link_pressures_restructured_data, index=indices).to_csv(
    link_pressures_report_path
)
