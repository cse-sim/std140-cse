print("\nInitializing Python...\n")
import openpyxl as xl
import pandas as pd
from datetime import datetime
import mako.template as mk
import os

def call_csv(path):
	data = pd.read_csv(path)
	return pd.DataFrame(data)

tests = 'etna'
output_file = "ET100series-Output-GMT+1 (071023a)"
current_directory = os.path.dirname(os.path.dirname(os.getcwd()))
template = xl.load_workbook(filename=f"{current_directory}/reports/etna/{output_file}-Template.xlsx")
cases = template.sheetnames
case_results_path = "output/etna"
cases_cell_A = ["ET100A1","ET100A3","ET110A1","ET110A2"]
cases_insulated_windows = ["ET110A1","ET110A2","ET110B1","ET110B2"]

experiment_dates = {"cases_insulated_windows":  {"start_date": datetime(2000,1,26,12),
                                                 "end_date":   datetime(2000,2,11, 9)},
                    "cases_uninsulated_windows":{"start_date": datetime(2000,9, 8,16),
                                                 "end_date":   datetime(2000,9,18,14)}}

output_columns = {
"cases_cell_A":{
  "CeilingPath1 Surface Temperature - Simulation [C]":2,
  "FloorPath1 Surface Temperature - Simulation [C]":3,
  "NorthWall Surface Temperature - Simulation [C]":4,
  "EastWall Surface Temperature - Simulation [C]":5,
  "SouthWall Surface Temperature - Simulation [C]":6,
  "WestWall Surface Temperature - Simulation [C]":7,
  "Cell Temperature - Simulation [C]":8,
  "Fan-Simulation [Wh]":9,
  "Heater-Simulation [Wh]":11,
  "CeilingPath1 Heat Flux [Wh/m2]":14,
  "CeilingPath2 Heat Flux [Wh/m2]":17,
  "FloorPath1 Heat Flux [Wh/m2]":20,
  "FloorPath2 Heat Flux [Wh/m2]":23,
  "FloorPath3 Heat Flux [Wh/m2]":26,
  "NorthWall Heat Flux [Wh/m2]":29,
  "NorthWallPath2 Heat Flux [Wh/m2]":32,
  "EastWall Heat Flux [Wh/m2]":35,
  "WindowsPath1East Heat Flux [Wh/m2]":38,
  "WindowsPath2East Heat Flux [Wh/m2]":41,
  "WindowsPath3East Heat Flux [Wh/m2]":44,
  "SouthWall Heat Flux [Wh/m2]":47,
  "WindowsPath1South Heat Flux [Wh/m2]":50,
  "WindowsPath2South Heat Flux [Wh/m2]":53,
  "WindowsPath3South Heat Flux [Wh/m2]":56,
  "WestWall Heat Flux [Wh/m2]":59},
"cases_cell_B":{
  "CeilingPath1 Surface Temperature - Simulation [C]":2,
  "FloorPath1 Surface Temperature - Simulation [C]":3,
  "NorthWall Surface Temperature - Simulation [C]":4,
  "EastWall Surface Temperature - Simulation [C]":5,
  "SouthWall Surface Temperature - Simulation [C]":6,
  "WestWall Surface Temperature - Simulation [C]":7,
  "Cell Temperature - Simulation [C]":8,
  "Fan-Simulation [Wh]":9,
  "Heater-Simulation [Wh]":11,
  "CeilingPath1 Heat Flux [Wh/m2]":14,
  "CeilingPath2 Heat Flux [Wh/m2]":17,
  "FloorPath1 Heat Flux [Wh/m2]":20,
  "FloorPath2 Heat Flux [Wh/m2]":23,
  "FloorPath3 Heat Flux [Wh/m2]":26,
  "NorthWall Heat Flux [Wh/m2]":29,
  "NorthWallPath2 Heat Flux [Wh/m2]":32,
  "EastWall Heat Flux [Wh/m2]":35,
  "SouthWall Heat Flux [Wh/m2]":38,
  "WindowsPath1South Heat Flux [Wh/m2]":41,
  "WindowsPath2South Heat Flux [Wh/m2]":44,
  "WindowsPath3South Heat Flux [Wh/m2]":47,
  "WestWall Heat Flux [Wh/m2]":50,
"WindowsPath1West Heat Flux [Wh/m2]":53,
"WindowsPath2West Heat Flux [Wh/m2]":56,
"WindowsPath3West Heat Flux [Wh/m2]":59,
}}

def find_case_specifics(case):
  global experiment_dates
  global cases_insulated_windows
  global cases_cell_A

  if case in cases_insulated_windows:
    start_date, end_date = experiment_dates["cases_insulated_windows"]["start_date"],experiment_dates["cases_insulated_windows"]["end_date"]
  else:
    start_date, end_date = experiment_dates["cases_uninsulated_windows"]["start_date"],experiment_dates["cases_uninsulated_windows"]["end_date"]
  if case in cases_cell_A:
    cell = "cases_cell_A"
  else:
    cell = "cases_cell_B"
  return cell, start_date, end_date

for case in cases:
  cell, start_date, end_date = find_case_specifics(case)
  case_template = template[case]
  case_results = call_csv(f"{current_directory}/{case_results_path}/{case}/OUTPUT.CSV")
  case_results["Datetime"] = [datetime(2000,case_results.loc[index,"Month"],case_results.loc[index,"Day"],case_results.loc[index,"Hour"]-1) for index in range(len(case_results))]
  case_results = case_results[(case_results["Datetime"] >= start_date) & (case_results["Datetime"] <= end_date)].reset_index()

  for index in range(len(case_results)):
    for output_column, template_column in output_columns[cell].items():
      case_template.cell(column=template_column, row=index+6).value = case_results.loc[index,output_column] 

print("Done processing cases.")
print("Writing results to XLSX ...")

template.save(filename=f"{current_directory}/reports/{tests}/{output_file}.xlsx")
