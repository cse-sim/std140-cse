from write_heater_consumption_plots import HeaterConsumptionPlots
from write_heat_flux_plots import HeatFluxPlots

heater_consumption_plots = HeaterConsumptionPlots()
heater_consumption_plots.get_heat_consumption_plots()

heat_flux_plots = HeatFluxPlots()
heat_flux_plots.get_heat_flux_plots()
