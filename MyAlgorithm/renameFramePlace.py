import os
import sys

path = sys.argv[1]

print("Empieza")
for dirpath, dirnames, filenames in os.walk(path):
    pathWithOutBaseName, id = os.path.split(dirpath)
    for fileName in filenames:
        if fileName != '.DS_Store':
            values = fileName.split("_")
            os.rename(dirpath + "/" + fileName, dirpath + "/" + values[0] + "_" + values[1] + "_" + values[2] + "_" + values[3] + "_"  + id + "_" + "body.jpg")
            print(dirpath + "/" + fileName + "=====>>" + dirpath + "/" + values[0] + "_" + values[1] + "_" + values[2] + "_" + values[3] + "_"  + id + "_" + "body.jpg")

print("Acaba")
