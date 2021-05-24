import glob
import shutil
import os

pathOrigin = "/Users/ignacio/TFG/TFG/data/LPATrail19Prueba/"
pathDestiny = "/Users/ignacio/TFG/TFG/data/Reidentification/"
place = "Vegueta"

if not os.path.exists(pathDestiny + place):
    os.makedirs(pathDestiny + place)

for pathJpg1 in sorted(glob.glob(pathOrigin + "*.jpg")):
    pathWithOutBaseName, baseName = os.path.split(pathJpg1)
    id = baseName.split("_")[4]
    if not os.path.exists(pathDestiny + place + "/" + id):
        os.makedirs(pathDestiny + place + "/" + id)
    shutil.copy(pathJpg1,pathDestiny + place + "/" + id + "/" + baseName)