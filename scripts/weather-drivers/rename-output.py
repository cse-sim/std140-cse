import os
import shutil

file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)
os.chdir(dir_path)

tests = 'weather-drivers'

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

createFolder('../../CSE-Files/' + tests + '/Input')
createFolder('../../CSE-Files/' + tests + '/Weather')

for dir in os.listdir('../../output/' + tests + '/'):
    shutil.copy('../../output/' + tests + '/' + dir + '/in.cse','../../CSE-Files/' + tests + '/Input/' + dir + '.cse')

shutil.copy('../../weather/' + tests + '/421810.epw','../../CSE-Files/' + tests + '/Weather/')
shutil.copy('../../weather/' + tests + '/700260.epw','../../CSE-Files/' + tests + '/Weather/')
shutil.copy('../../weather/' + tests + '/722190.epw','../../CSE-Files/' + tests + '/Weather/')
shutil.copy('../../weather/' + tests + '/725650.epw','../../CSE-Files/' + tests + '/Weather/')
shutil.copy('../../weather/' + tests + '/855740.epw','../../CSE-Files/' + tests + '/Weather/')
