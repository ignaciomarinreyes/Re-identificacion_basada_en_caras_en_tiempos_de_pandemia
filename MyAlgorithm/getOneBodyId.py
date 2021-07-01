import shutil
import os
import sys

pathOrigin = sys.argv[1]
pathDestiny = sys.argv[2]

if not os.path.exists(pathDestiny):
    os.makedirs(pathDestiny)

idRepetition = []

for dirpath, dirnames, filenames in os.walk(pathOrigin):
    pathWithOutBaseName, id = os.path.split(dirpath)
    for fileName in filenames:
        if fileName != '.DS_Store':
            if id not in idRepetition:
                shutil.copy(dirpath + "/" + fileName, pathDestiny + "/" + fileName)
                idRepetition.append(id)


