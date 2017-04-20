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
  target = [output_dir + '/in.rep', output_dir + '/DETAILED.csv', output_dir + '/RESULTS.csv']

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

task :sim, [:filter] do |t, args|
  args.with_defaults(:filter=>'*')
  cases = Dir['cases/' + args.filter + '.*']
  for c in cases
    if (compose(c))
      if !sim(c)
        puts "\nSimulation failed..."
        exit
      end
    else
      puts "\nComposition failed..."
      exit
    end
  end
end

task :default, [:filter] => [:sim]
