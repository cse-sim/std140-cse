require 'fileutils'

def compose(c, tests)
  file_base = File.basename(c,".*")

  output_dir = 'output/' + tests + '/' + file_base
  #Create output directory
  unless File.directory?(output_dir)
    FileUtils.mkdir_p(output_dir)
  end
  puts Dir.entries(".")
  src = ['base-#{tests}.pxt', 'CSE.exe', 'DRYCOLD_CSW2.csv', c]
  target = output_dir + '/in.cse'

  puts "================="
  puts "Running case " + file_base + ":"
  puts "=================\n"

  # Compose with Modelkit
  success = nil
  if !(FileUtils.uptodate?(target, src))
    puts "\ncomposing...\n\n"
    puts "#{c}"
    puts "#{output_dir + '/in.cse'}"
    puts "base-#{tests}.pxt"
    success = system(%Q| echo base-#{tests}.pxt \| modelkit template-compose -f "#{c}" -o "#{output_dir + '/in.cse'}" |)
  else
    puts "  ...input already up-to-date."
    success = true
  end
  puts "Modelkit done"
  return success
end

def sim(c, tests)
  file_base = File.basename(c,".*")

  output_dir = 'output/' + tests + '/' + file_base

  src = [output_dir + '/in.cse']
  if tests == 'section-5'
  target = [output_dir + '/in.rep', output_dir + '/DETAILED.csv']
  elsif tests == 'weather-drivers'
  target = [output_dir + '/in.rep', output_dir + '/HOURLY.csv']
  end

  success = nil
  if !(FileUtils.uptodate?(target[0], src)) or !(FileUtils.uptodate?(target[1], src))
    puts "\nsimulating..."
    Dir.chdir(output_dir){
      success = system(%Q|..\\..\\..\\CSE.exe in.cse|)
      puts Dir.entries(".")
      puts Dir.pwd
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
  if tests == 'section-5'
    target = ['reports/#{tests}/Sec5-2Aout.xlsx', 'reports/#{tests}/S140outNotes.txt']
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
  args.with_defaults(:filter=>'section-5')
  tests = args.fetch(:filter) # 'section-5', 'weather-drivers'
  cases = Dir['cases/' + tests + '/*.*']
  for c in cases
    if !compose(c, tests)
      abort("\nERROR: Composition failed...")
    end
    if !sim(c, tests)
      abort("\nERROR: Simulation failed...")
    end
  end
  if !write_report(tests)
    abort("\nERROR: Failed to generate reports...")
  end
end

task :default, [:filter] => [:sim]
