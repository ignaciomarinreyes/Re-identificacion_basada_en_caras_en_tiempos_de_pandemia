from deepface import DeepFace
import os

path="/Users/ignacio/dataTFG/Reidentification"

predict = []
real = []
numeradorRank1 = 0
filaActual = 0

for dirpath1, dirnames1, filenames1 in os.walk(path):
    filenames1 = [f for f in filenames1 if not f[0] == '.']
    for file1 in sorted(filenames1):
        pathWithOutBaseName1, id1 = os.path.split(dirpath1)
        x, place1 = os.path.split(pathWithOutBaseName1)
        for dirpath2, dirnames2, filenames2 in os.walk(path):
            filenames2 = [f for f in filenames2 if not f[0] == '.']
            for file2 in sorted(filenames2):
                pathWithOutBaseName2, id2 = os.path.split(dirpath2)
                y, place2 = os.path.split(pathWithOutBaseName2)
                if place1 != place2:
                    real.append(file2.split("_")[4])


for dirpath1, dirnames1, filenames1 in os.walk(path):
    filenames1 = [f for f in filenames1 if not f[0] == '.']
    for file1 in sorted(filenames1):
        pathWithOutBaseName1, id1 = os.path.split(dirpath1)
        x, place1 = os.path.split(pathWithOutBaseName1)
        for dirpath2, dirnames2, filenames2 in os.walk(path):
            filenames2 = [f for f in filenames2 if not f[0] == '.']
            for file2 in sorted(filenames2):
                pathWithOutBaseName2, id2 = os.path.split(dirpath2)
                y, place2 = os.path.split(pathWithOutBaseName2)
                if place1 != place2:
                    result = DeepFace.verify(dirpath1 + "/" + file1, dirpath2 + "/" + file2, model_name="Facenet", enforce_detection=False)
                    predict.append(str(result["distance"]))
                    print(str(result["distance"]))
        positionMinValueRank1List = predict.index(min(predict))
        print("positionMinValue " + str(positionMinValueRank1List))
        if(real[filaActual] == real[positionMinValueRank1List]):
            numeradorRank1+=1
            print("numeradorRank1 " + str(numeradorRank1))
        print(predict)
        predict = []
        filaActual+=1
    rank1 = numeradorRank1/len(real)
    print(rank1)

