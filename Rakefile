require 'fileutils'

def compose(c)
  file_base = File.basename(c,".*")

  output_dir = 'output/' + file_base
  #Create output directory
  unless File.directory?(output_dir)
    FileUtils.mkdir_p(output_dir)
  end

  src = ['base.pxt', 'CSE.exe', 'DRYCOLD_CSW2.csv', c]
  target = output_dir + '/in.cse'

  puts "================="
  puts "Running case " + file_base + ":"
  puts "=================\n"

  # Compose with params
  success = nil
  if !(FileUtils.uptodate?(target, src))
    puts "\ncomposing...\n\n"
    success = system(%Q|params compose -f "#{c}" -o "#{output_dir + '/in.cse'}"  base.pxt|)
  else
    puts "  ...input already up-to-date."
    success = true
  end
  return success
end

def sim(c)
  file_base = File.basename(c,".*")

  output_dir = 'output/' + file_base

  src = [output_dir + '/in.cse']
  target = [output_dir + '/in.rep', output_dir + '/DETAILED.csv']

  success = nil
  if !(FileUtils.uptodate?(target[0], src)) or !(FileUtils.uptodate?(target[1], src))
    puts "\nsimulating..."
    Dir.chdir(output_dir){
      success = system(%Q|..\\..\\CSE.exe in.cse|)
    }
    puts "\n"
  else
    puts "  ...output already up-to-date.\n"
    success = true
  end
  return success
end

def write_report()
  src = Dir['output/*/DETAILED.csv']
  target = ['reports/Sec5-2Aout.xlsx', 'reports/S140outNotes.txt']
  puts "\n================="
  puts "     REPORTS     "
  puts "=================\n"
  success = nil
  if !(FileUtils.uptodate?(target[0], src)) or !(FileUtils.uptodate?(target[1], src))
    Dir.chdir('scripts'){
      success = system(%Q|python write-results.py|)
    }
  else
    puts "\n  ...report already up-to-date."
    success = true
  end
  return success
end

task :sim, [:filter] do |t, args|
  args.with_defaults(:filter=>'*')
  cases = Dir['cases/' + args.filter + '.*']
  for c in cases
    if !compose(c)
      puts "\nERROR: Composition failed..."
      exit
    end
    if !sim(c)
      puts "\nERROR: Simulation failed..."
      exit
    end
  end
  if !write_report()
    puts "\nERROR: Failed to generate reports..."
    exit
  end
end

task :default, [:filter] => [:sim]
