import os

path = "/Users/ignacio/TFG/TFG/data/Reidentification"

for dirpath, dirnames, filenames in os.walk(path):
    print("Ruta actual:", dirpath)
    print("Carpetas:", ", ".join(dirnames))
    print("Archivos:", ", ".join(filenames))
    pathWithOutBaseName, id = os.path.split(dirpath)
    for fileName in filenames:
        values = fileName.split("_")
        os.rename(dirpath + "/" + fileName, dirpath + "/" + values[0] + "_" + values[1] + "_" + values[2] + "_" + values[3] + "_"  + id + "_" + "body.jpg")

