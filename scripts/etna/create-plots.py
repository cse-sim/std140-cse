import pandas as pd
from datetime import datetime, timedelta
import openpyxl as xl
import plotly.graph_objects as go
from pathlib import Path
from shutil import rmtree
import warnings
import pytz

warnings.filterwarnings("ignore")

pd.set_option("display.max_rows",500)
pd.set_option("display.max_columns",100)

def create_or_replace_folder(path):
    if path.exists():
        rmtree(path)
    path.mkdir(exist_ok=True)

outputs_file_path = Path("output/etna/OUTPUTS")
dataframe_file_path = Path(outputs_file_path,"DATA")
graphs_file_path = Path(outputs_file_path,"GRAPHS")
create_or_replace_folder(outputs_file_path)
create_or_replace_folder(dataframe_file_path)
create_or_replace_folder(graphs_file_path)

def call_csv(path):
	data = pd.read_csv(path,encoding='unicode_escape')
	df = pd.DataFrame(data)
	return df

# prints date and time with time zone on each plot
def find_todays_date():
	utc_timezone = pytz.timezone("America/Denver")
	current_date_time = datetime.now(utc_timezone)
	return current_date_time.strftime("%Y%m%d")

measured_data_directory = "docs/etna"
output_file = f"CSE-ET100series-{find_todays_date()}"
simulated_data_path = f"reports/etna/{output_file}.xlsx"

measured_data = {
    "ET100":{
        "ET100A":"ET100A-Measurements-GMT+1 (071123).csv",
        "ET100B":"ET100B-Measurements-GMT+1 (071123).csv"},
    "ET110":{
        "ET110A":"ET110A-Measurements-GMT+1 (071123).csv",
        "ET110B":"ET110B-Measurements-GMT+1 (071123).csv"}
}

def find_dates(series):
    df = call_csv(f"{measured_data_directory}/{series}B-Measurements-GMT+1 (071123).csv")
    df.columns = df.iloc[1]
    df = df.drop([0,1,2]).reset_index()
    return pd.DataFrame([datetime.strptime(date,'%m/%d/%Y %H:%M') for date in list(df["Date (XLS format)"])],columns=["Date"])

df_ET100 = find_dates("ET100")
df_ET110 = find_dates("ET110")

def call_df_measured(series):
    if series == "ET100":
        global df_ET100
        return df_ET100
    elif series == "ET110":
        global df_ET110
        return df_ET110

for series in measured_data.keys():
    df_measured = call_df_measured(series)
    for case, file in measured_data[series].items():
        df = call_csv(f"{measured_data_directory}/{file}")
        df.columns = df.iloc[1]
        df = df.drop([0,1,2]).reset_index()
        if case == "ET100A":
            df.loc[len(df.index)] = None
        df_measured[f"{case} Heater Energy Consumption (Wh) - Measured"] = df["Qhtr"]
        
template = xl.load_workbook(filename=simulated_data_path)
cases = template.sheetnames

simulated_data = {
     "ET100":
     {'ET100A1', 'ET100B1', 'ET100A3', 'ET100B3'},
     "ET110":
     {'ET110A1', 'ET110A2', 'ET110B1', 'ET110B2'}
     }


for case in cases:
    if case in simulated_data["ET100"]:
        df = df_ET100
    else:
        df = df_ET110
    df_simulated = pd.read_excel(simulated_data_path, sheet_name=case, header=3)
    df_simulated = df_simulated.drop([0]).reset_index()
    if case in ["ET100A1","ET100A3"]:
        df_simulated.loc[len(df.index)] = None
    df[f"{case} Heater Energy Consumption (Wh) - Simulated"] = list(df_simulated["Qhtr"])

df_ET100.to_csv(f"{dataframe_file_path}/ET100_Series.csv",index=False)
df_ET110.to_csv(f"{dataframe_file_path}/ET110_Series.csv",index=False)

output_cases = {"ET100":{"A":{
                        "Measured":
                            {"ET100A"},
                        "Simulated":
                            {"ET100A1",
                             "ET100A3"}},
                        "B":{
                        "Measured":
                            {"ET100B"},
                        "Simulated":
                            {"ET100B1",
                             "ET100B3"}}},
                "ET110":{"A":{
                        "Measured":
                            {"ET110A"},
                        "Simulated":
                            {"ET110A1",
                             "ET110A2"}},
                        "B":{
                        "Measured":
                            {"ET110B"},
                        "Simulated":
                            {"ET110B1",
                             "ET110B2"}}}
                }

experiment_dates = {"ET100":{"start date":datetime(2000,9,8,16,0),
                            "end date":datetime(2000,9,18,14,0)},
                    "ET110":{"start date":datetime(2000,1,26,12,0),
                            "end date":datetime(2000,2,11,9,0)}}

steady_state_dates =    {"ET100":{"start date":datetime(2000,9,16,8,0),
                            "end date":datetime(2000,9,18,14,0)},
                        "ET110":{"start date":datetime(2000,2,10,16,0),
                            "end date":datetime(2000,2,11,9,0)}}

error = {"ET100A":0.007,
         "ET100B":0.009,
         "ET110A":0.014,
         "ET110B":0.015}

def define_line_type(simualted_or_measured,case):
    if simualted_or_measured == "Measured":
        return dict(color="black",dash='dot')
    else:
        if case[-1] == "1":
            return dict(color="red")
        else:
            return dict(color="blue")

for series in output_cases.keys():
    df = call_df_measured(series)
    for cell in output_cases[series].keys():
        fig = go.Figure()
        for simulated_or_measured in output_cases[series][cell].keys():
            y_max=[]
            for case in output_cases[series][cell][simulated_or_measured]:
                start_date = steady_state_dates[series]["start date"]
                end_date = steady_state_dates[series]["end date"]
                experiment_end_date = experiment_dates[series]["end date"]
                if case in ["ET100B","ET100B1","ET100B3"]:
                    experiment_end_date += timedelta(hours=1)
                y_values = df[f"{case} Heater Energy Consumption (Wh) - {simulated_or_measured}"].astype(float)
                fig.add_trace(go.Scatter(
                                x=df["Date"],
                                y=y_values,
                                name=f"{case}-{simulated_or_measured}",
                                mode="lines",
                                line=define_line_type(simulated_or_measured,case),
                                ))
                y_max.append(max(y_values))
                if simulated_or_measured == "Measured":
                    df_uncertainty_band = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
                    y_values_df_uncertainty_band = df_uncertainty_band[f"{case} Heater Energy Consumption (Wh) - {simulated_or_measured}"].astype(float)
                    y_average = sum(y_values_df_uncertainty_band)/len(y_values_df_uncertainty_band)
                    y_upper_band = [y_average*(1+error[f"{series}{cell}"]) for n in range(len(y_values_df_uncertainty_band))]
                    y_lower_band = [y_average*(1-error[f"{series}{cell}"]) for n in range(len(y_values_df_uncertainty_band))]
                    fig.add_trace(go.Scatter(
                                    x=df_uncertainty_band["Date"],
                                    y=y_lower_band,
                                    line=dict(color='rgba(50,50,50,0.25)',dash='solid'),
                                    marker=dict(
                                        opacity=0
                                    ),
                                    showlegend=False
                                    ))
                    fig.add_trace(go.Scatter(
                                    x=df_uncertainty_band["Date"],
                                    y=y_upper_band,
                                    fill='tonexty',
                                    name="95% Measured Confidence Interval",
                                    mode="lines",
                                    line=dict(color='rgba(50,50,50,0.25)',dash='solid'),
                                    marker=dict(
                                        opacity=0
                                    ),
                                    ))
        y_max = max(y_max)
        fig.add_trace(go.Scatter(
            x=[start_date,start_date,end_date,end_date],
            y=[0,y_max,y_max,0],
            fill='tozeroy',
            mode='none',
            fillcolor='rgba(26,150,65,0.1)',
            name="Steady State"
        ))
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            range=[experiment_dates[series]["start date"],experiment_end_date]
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            range=[0,y_max]
        )
        fig.update_layout(
            yaxis_title=f"Heater Energy Consumtpion (Wh)",
            xaxis_title="Time",
            title=f"{series}{cell}",
            title_x=0.5,
            plot_bgcolor='white',
            font_color='black',
            )
        file_path = f"{graphs_file_path}/{series}{cell}-Heater.html"
        fig.write_html(file_path)
