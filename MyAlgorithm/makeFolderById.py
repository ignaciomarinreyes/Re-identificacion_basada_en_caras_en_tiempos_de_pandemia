import glob
import shutil
import os

pathOrigin = "/Users/ignacio/TFG/TFG/data/Bodies/"
pathDestiny = "/Users/ignacio/TFG/TFG/data/Reidentification/"
place = "Tafira"

if not os.path.exists(pathDestiny + place):
    os.makedirs(pathDestiny + place)

for pathPng1 in sorted(glob.glob(pathOrigin + "*.png")):
    pathWithOutBaseName, baseName = os.path.split(pathPng1)
    id = baseName.split("_")[4]
    if not os.path.exists(pathDestiny + place + "/" + id):
        os.makedirs(pathDestiny + place + "/" + id)
    shutil.copy(pathPng1,pathDestiny + place + "/" + id + "/" + baseName)