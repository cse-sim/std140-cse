require 'csv'
require 'time'
require 'fileutils'

class WriteInputData
	def self.write_input_data

		puts "============================="
		puts "writing ETNA input data files"
		puts "============================="

		# create INPUTS folder if it does not exist
		folder_path = 'output/etna/INPUTS'
		unless Dir.exist?(folder_path)
			FileUtils.mkdir_p(folder_path)
		end

			# paths for case temperature file and 8760 template file
		@temperature_files = [
			{:file_name => "ET100A-Measurements-GMT+1 (071123).csv", :case_name => "ET100A", :case_series => "ET100"},
			{:file_name => "ET100B-Measurements-GMT+1 (071123).csv", :case_name => "ET100B", :case_series => "ET100"},
			{:file_name => "ET110A-Measurements-GMT+1 (071123).csv", :case_name => "ET110A", :case_series => "ET110"},
			{:file_name => "ET110B-Measurements-GMT+1 (071123).csv", :case_name => "ET110B", :case_series => "ET110"}
		]

		@input_directory = "docs/etna/"
		@output_directory = "output/etna/INPUTS/"

		# define temperature for 'fake' temperature data
		# CSE requires an entire year's worth of temperature data
		# ETNA temperature data does not encompass an entire year, therefore filler data is used.
		@FAKE_TEMPERATURE_GUARDS = 10
		@FAKE_FAN_HOURLY_ENERGY_CONSUMPTION = 0
		@FAKE_FAN_VOLUMETRIC_FLOW_RATE = 925
		@FAKE_HEATER_HOURLY_ENERGY_CONSUMPTION = 0

		for temperature_file in @temperature_files
			# set fake cell temeprature depending on case
			if temperature_file[:case_series] == "ET100"
				@FAKE_TEMPERATURE_CELL = 35
			else
				@FAKE_TEMPERATURE_CELL = 10
			end
			temperature_file_path = @input_directory+temperature_file[:file_name]
			template_file = 'docs/etna/template_8760.csv'

			# create array using ETNA temperature data
			rows = []
			CSV.foreach(temperature_file_path, encoding: 'ISO-8859-1') do |row|
				rows.append(row)
			end

			# define start and end dates and times of ETNA experimental data
			start_date = DateTime.strptime(rows[4][0], "%m/%d/%Y %k:%M")
			end_date = DateTime.strptime(rows[-1][0], "%m/%d/%Y %k:%M")

			# create intermediary file that contains ETNA datetimes and cell temperatures
			CSV.open('new-temp.csv','w') do |csv|
				# create header
				csv << ['Month','Day','Hour'].append(rows[2][1,10]).flatten
				for i in (4..rows.length - 1) do
					date = DateTime.strptime(rows[i][0], "%m/%d/%Y %k:%M")
					# add row for each set of datetimes and cell temperatures
					csv << [date.month,date.day,date.hour].append([rows[i][1,10]]).flatten
				end
			end

			# initialize arrays and constant
			template_rows = []
			end_template_rows = []
			temperature_rows = []
			end_template_value = 0

			# create array of 8760 template file datetimes (template_rows)
			# create array of 8760 template file datetimes after ETNA data ends (end_template_data)
			CSV.foreach(template_file, encoding: 'ISO-8859-1') do |row|
				template_rows.append(row)
				month = row[0].to_i
				day = row[1].to_i
				hour = row[2].to_i
				# end_template_rows array adds datetimes after ETNA data end date
				if end_template_value == 1
					end_template_rows.append(row)
				end
				# determines if ETNA data has ended
				if (month == end_date.month) && (day == end_date.day) && (hour == end_date.hour)
					end_template_value = 1
				end
			end

			# creates array of intermediary file that contains ETNA experimental data datetimes and cell temperatures
			CSV.foreach('new-temp.csv', encoding: 'ISO-8859-1') do |row|
				temperature_rows.append(row)
			end

			final_csv = []
			# create file of datetimes and temperatures for an entire year to be used in CSE
			CSV.open('final-temps.csv','w') do |csv|
				# create header as defined in CSE
				csv << temperature_rows[0].flatten
				final_csv.append(temperature_rows[0].flatten)
				# delete first row from array (header)
				# deletion prevents another header from being added to data before ENTA experimental data start date
				temperature_rows = temperature_rows.drop(1)
				# add temperature data to 8760 temperature file
				for template_row in template_rows do
					month = template_row[0].to_i
					day = template_row[1].to_i
					hour = template_row[2].to_i
					# add ETNA temperature data
					if (month == start_date.month) && (day == start_date.day) && (hour == start_date.hour)
						for temperature_row in temperature_rows do
							temperature_row.map! { |str| str.gsub(",", "") }
							csv << temperature_row
							final_csv.append(temperature_row)
						end
					break
					# add fake temperature data before start date
					elsif month > 0
						csv << [month,day,hour,[@FAKE_TEMPERATURE_GUARDS]*6,@FAKE_TEMPERATURE_CELL,@FAKE_FAN_HOURLY_ENERGY_CONSUMPTION,@FAKE_FAN_VOLUMETRIC_FLOW_RATE,@FAKE_HEATER_HOURLY_ENERGY_CONSUMPTION].flatten
						final_csv.append([month,day,hour,[@FAKE_TEMPERATURE_GUARDS]*6,@FAKE_TEMPERATURE_CELL,@FAKE_FAN_HOURLY_ENERGY_CONSUMPTION,@FAKE_FAN_VOLUMETRIC_FLOW_RATE,@FAKE_HEATER_HOURLY_ENERGY_CONSUMPTION].flatten)
					end
				end
				# add fake temperature data after end date
				for end_template_row in end_template_rows
					month = end_template_row[0].to_i
					day = end_template_row[1].to_i
					hour = end_template_row[2].to_i
					csv << [month,day,hour,[@FAKE_TEMPERATURE_GUARDS]*6,@FAKE_TEMPERATURE_CELL,@FAKE_FAN_HOURLY_ENERGY_CONSUMPTION,@FAKE_FAN_VOLUMETRIC_FLOW_RATE,@FAKE_HEATER_HOURLY_ENERGY_CONSUMPTION].flatten
					final_csv.append([month,day,hour,[@FAKE_TEMPERATURE_GUARDS]*6,@FAKE_TEMPERATURE_CELL,@FAKE_FAN_HOURLY_ENERGY_CONSUMPTION,@FAKE_FAN_VOLUMETRIC_FLOW_RATE,@FAKE_HEATER_HOURLY_ENERGY_CONSUMPTION].flatten)
				end
			end

			# Add header and shift hours up 1 (0-23 becomes 1-24) for CSE compatability
			header = 0
			CSV.open(@output_directory+temperature_file[:case_name]+"-measured-data.csv",'w') do |csv|
				csv << [temperature_file[:case_name],0]
				csv << [Time.now.getutc]
				csv << ["#{temperature_file[:case_name]} Input Data","Hour"]
				for row in final_csv
					if header == 1
						row[2] = row[2].to_i + 1
					end
					csv << row
					header = 1
				end
			end
		end

		File.delete("final-temps.csv")
		File.delete("new-temp.csv")
	
	end
end