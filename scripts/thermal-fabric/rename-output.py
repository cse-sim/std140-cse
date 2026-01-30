import os
import shutil

file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)
os.chdir(dir_path)

tests = "thermal-fabric"


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)


createFolder("../../CSE-Files/" + tests + "/Input")
createFolder("../../CSE-Files/" + tests + "/Weather")

for dir in os.listdir("../../output/" + tests + "/"):
    shutil.copy(
        "../../output/" + tests + "/" + dir + "/in.cse",
        "../../CSE-Files/" + tests + "/Input/" + dir + ".cse",
    )

shutil.copy(
    "../../weather/" + tests + "/725650TMY3.epw",
    "../../CSE-Files/" + tests + "/Weather/",
)
