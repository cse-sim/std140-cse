require 'fileutils'

def compose(c, tests)
  file_base = File.basename(c,".*")

  output_dir = 'output/' + tests + '/' + file_base
  #Create output directory
  unless File.directory?(output_dir)
    FileUtils.mkdir_p(output_dir)
  end

  src = ['#{tests}.pxt', 'CSE.exe', 'DRYCOLD_CSW2.csv', c]
  target = output_dir + '/in.cse'

  puts "================="
  puts "Running case " + file_base + ":"
  puts "=================\n"

  # Compose with Modelkit
  success = nil
  if !(FileUtils.uptodate?(target, src))
    puts "\ncomposing...\n\n"
    success = system(%Q|modelkit template-compose -f "#{c}" -o "#{output_dir + '/in.cse'}"  #{tests}.pxt|)
  else
    puts "  ...input already up-to-date."
    success = true
  end
  return success
end

def sim(c, tests)
  file_base = File.basename(c,".*")

  output_dir = 'output/' + tests + '/' + file_base

  src = [output_dir + '/in.cse']
  if tests == 'thermal-fabric'
  target = [output_dir + '/in.rep', output_dir + '/DETAILED.csv']
  elsif tests == 'weather-drivers'
  target = [output_dir + '/in.rep', output_dir + '/HOURLY.csv']
  end

  success = nil
  if !(FileUtils.uptodate?(target[0], src)) or !(FileUtils.uptodate?(target[1], src))
    puts "\nsimulating..."
    Dir.chdir(output_dir){
      success = system(%Q|..\\..\\..\\CSE.exe in.cse|)
    }
    puts "\n"
  else
    puts "  ...output already up-to-date.\n"
    success = true
  end
  return success
end

def write_report(tests)
  src = Dir['output/#{tests}/*/DETAILED.csv'] + ["scripts/#{tests}/write-results.py", "reports/#{tests}/S140outNotes-Template.txt"]
  if tests == 'thermal-fabric'
    target = ['reports/#{tests}/Std140_TF_Output.xlsx', 'reports/#{tests}/S140outNotes.txt']
  elsif tests == 'weather-drivers'
    target = ['reports/#{tests}/WeatherDriversResultsSubmittal.xlsx', 'reports/#{tests}/S140outNotes.txt']
  end
  puts "\n================="
  puts "     REPORTS     "
  puts "=================\n"
  success = nil
  if !(FileUtils.uptodate?(target[0], src)) or !(FileUtils.uptodate?(target[1], src))
    Dir.chdir('scripts/' + tests){
      success = system(%Q|python write-results.py|)
    }
  else
    puts "\n  ...report already up-to-date."
    success = true
  end
  return success
end

task :sim, [:filter] do |t, args|
  args.with_defaults(:filter=>'thermal-fabric')
  tests = args.fetch(:filter) # 'thermal-fabric', 'weather-drivers'
  cases = Dir['cases/' + tests + '/*.*']
  for c in cases
    if !compose(c, tests)
      puts "\nERROR: Composition failed..."
      exit
    end
    if !sim(c, tests)
      puts "\nERROR: Simulation failed..."
      exit
    end
  end
  if !write_report(tests)
    puts "\nERROR: Failed to generate reports..."
    exit
  end
end

task :default, [:filter] => [:sim]
