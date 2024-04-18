print("\nInitializing Python...\n")
import openpyxl as xl
import pandas as pd
from datetime import datetime
import os, glob
from pathlib import Path


def call_csv(path):
    data = pd.read_csv(path)
    return pd.DataFrame(data)


# delete output file
def delete_output_file(path):
    for file in glob.glob(f"{path}*"):
        os.remove(file)


test = "rp-1052"
analytical = "Analytical"
simulated = "Simulated"

output_columns_simulated = [
    "Interior Surface Temperature [C]",
    "Exterior Surface Temperature [C]",
    "Exterior Surface Heat Flux [Wh/m2]",
]

output_columns_air_temperatures = [
    "Interior",
    "Exterior",
]

current_directory = os.path.dirname(os.path.dirname(os.getcwd()))

# template file contains analytical results and simulated result template
template_file = f"docs/{test}/output-template.xlsx"

# air temperature file
air_temperature_file = f"docs/{test}/air-temperatures-template.csv"

# results file contains CSE simulation results
results_file = f"output/{test}/TC1/OUTPUT.CSV"

# file path for output file to plot results
output_file_simulated = Path(current_directory, f"reports/{test}/tc1-results.xlsx")
output_file_air_temperatures = Path(
    current_directory, f"reports/{test}/air-temperatures.csv"
)

df_analytical = pd.read_excel(
    Path(current_directory, template_file), sheet_name=analytical
)
df_simualted = pd.read_excel(
    Path(current_directory, template_file), sheet_name=simulated
)
df_air_temperature = pd.DataFrame(
    pd.read_csv(Path(current_directory, air_temperature_file))
)
df_results = pd.DataFrame(pd.read_csv(Path(current_directory, results_file)))

# add number of hours elapsed in year to results dataframe
df_results["Hour_Year"] = df_results.apply(lambda x: x.name + 1, axis=1)

# filter results dataframe to only include 100 hours, which matches the analytical results
df_results = df_results[
    (df_results["Hour_Year"] >= 2160) & (df_results["Hour_Year"] <= 2260)
]

for column in output_columns_simulated:
    df_simualted[column] = df_results[column].tolist()

for column in output_columns_air_temperatures:
    df_air_temperature[column] = df_results[column].tolist()


print("Done processing cases.")
print("Writing results to XLSX ...")

final_dictionary = {"Analytical": df_analytical, "Simulated": df_simualted}

with pd.ExcelWriter(output_file_simulated) as writer:
    for sheet_name, dataframe in final_dictionary.items():
        dataframe.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False,
        )

df_air_temperature.to_csv(output_file_air_temperatures, index=False)
