import glob
import shutil
import os

pathOrigin = "/content/gdrive/My Drive/TFG/data/"
pathDestiny = "/content/gdrive/My Drive/TFG/data/Reidentification/"
#places = ["Vegueta", "Tafira", "Universidad"]
#bodies = ["Bodies_LPATrail20", "Bodies_LPATrail19", "Bodies_LPATrail21"]
places = ["Universidad"]
bodies = ["Bodies_LPATrail21"]


for place, body in zip(places, bodies):
    if not os.path.exists(pathDestiny + place):
        os.makedirs(pathDestiny + place)

    for pathPng1 in sorted(glob.glob(pathOrigin + body + "/" + "*.jpg")):
        pathWithOutBaseName, baseName = os.path.split(pathPng1)
        id = baseName.split("_")[4]
        if not os.path.exists(pathDestiny + place + "/" + id):
            os.makedirs(pathDestiny + place + "/" + id)
        shutil.copy(pathPng1,pathDestiny + place + "/" + id + "/" + baseName)