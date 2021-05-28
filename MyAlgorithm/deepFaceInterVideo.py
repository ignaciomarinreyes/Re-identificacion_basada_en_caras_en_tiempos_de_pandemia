from deepface import DeepFace
import os

path="/content/gdrive/My Drive/TFG/data/Reidentification"

for dirpath1, dirnames1, filenames1 in os.walk(path):
    filenames1 = [f for f in filenames1 if not f[0] == '.']
    for file1 in sorted(filenames1):
        pathWithOutBaseName1, id1 = os.path.split(dirpath1)
        x, place1 = os.path.split(pathWithOutBaseName1)
        timeFile = file1[0: 11]
        fileOutput = open(dirpath1 + "/" + timeFile + "_" + id1 + "_" + "deepFace", "w")
        for dirpath2, dirnames2, filenames2 in os.walk(path):
            filenames2 = [f for f in filenames2 if not f[0] == '.']
            for file2 in sorted(filenames2):
                pathWithOutBaseName2, id2 = os.path.split(dirpath2)
                y, place2 = os.path.split(pathWithOutBaseName2)
                if place1 != place2:
                    result = DeepFace.verify(dirpath1 + "/" + file1, dirpath2 + "/" + file2, model_name="Facenet", enforce_detection=False)
                    fileOutput.write(place1 + " " + id1 + " " + place2 + " " + id2 + " " +  str(result["distance"]) + " \n")
                    print(dirpath1 + "/" + file1 + " ===> " + dirpath2 + "/" + file2 + " ===> " + str(result["distance"]))


