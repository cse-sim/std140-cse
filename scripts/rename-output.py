import os
import shutil
print(os.getcwd())
for dir in os.listdir('../output'):
    shutil.copy('../output/' + dir + '/in.cse','../CSE-Files/Input/'+dir+'.cse')

shutil.copy('../725650TMY3.epw','../CSE-Files/Weather/')
