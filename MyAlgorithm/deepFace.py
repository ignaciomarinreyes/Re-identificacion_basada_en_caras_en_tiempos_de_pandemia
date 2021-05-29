from deepface import DeepFace
import os
import argparse
import glob

params = None

def parse_arguments():
    parser = argparse.ArgumentParser(description='DeepFace script')
    parser.add_argument('-path', '-p' ,default="/content/gdrive/My Drive/TFG/data/Reidentification", help='Path to apply DeepFace')
    parser.add_argument('-inter', '-ie', action='store_true')
    parser.add_argument('-intra', '-ir', action='store_true')
    parser.add_argument('-vector', '-v', action='store_true')
    args = parser.parse_args()
    return args

def deepFaceInterVideo():
    for dirpath1, dirnames1, filenames1 in os.walk(params.path):
        filenames1 = [f for f in filenames1 if not f[0] == '.']
        for file1 in sorted(filenames1):
            pathWithOutBaseName1, id1 = os.path.split(dirpath1)
            x, place1 = os.path.split(pathWithOutBaseName1)
            timeFile = file1[0: 11]
            fileOutput = open(dirpath1 + "/" + timeFile + "_" + id1 + "_" + "deepFace", "w")
            for dirpath2, dirnames2, filenames2 in os.walk(params.path):
                filenames2 = [f for f in filenames2 if not f[0] == '.']
                for file2 in sorted(filenames2):
                    pathWithOutBaseName2, id2 = os.path.split(dirpath2)
                    y, place2 = os.path.split(pathWithOutBaseName2)
                    if place1 != place2:
                        print(dirpath1 + "/" + file1 + " ===> " + dirpath2 + "/" + file2 + " ===> " )
                        result = DeepFace.verify(dirpath1 + "/" + file1, dirpath2 + "/" + file2, model_name="Facenet", enforce_detection=False)
                        fileOutput.write(place1 + " " + id1 + " " + place2 + " " + id2 + " " +  str(result["distance"]) + " \n")


def deepFaceIntraVideo():
    for pathJpg1 in sorted(glob.glob(params.path + "*.jpg")):
        for pathJpg2 in sorted(glob.glob(params.path + "*.jpg")):
            result = DeepFace.verify(pathJpg1, pathJpg2, model_name="Facenet", enforce_detection=False)
            print("JPG_1 " + pathJpg1 + " JPG_2 " + pathJpg2 + "===> " + str(result["distance"]))


def deepFaceVector():
    for dirpath, dirnames, filenames in os.walk(params.path):
        filenames = [f for f in filenames if not f[0] == '.']
        for file in sorted(filenames):
            pathWithOutBaseName, id = os.path.split(dirpath)
            timeFile = file[0: 12]
            print(dirpath + "/" + timeFile + "_" + id + "_body.png")
            try:
                result = DeepFace.represent(dirpath + "/" + timeFile + "_" + id + "_body.png", model_name="Facenet", enforce_detection=False)
            except:
                print("No se puede aplicar algoritmo" + dirpath + "/" + timeFile + "_" + id + "_body.png")
            fileOutput = open(dirpath + "/" + timeFile + "_" + id + "_" + "deepFace.txt", "w")
            for value in result:
                fileOutput.write(str(value) + "\n")



if __name__ == '__main__':
    params = parse_arguments()
    if params.vector:
        deepFaceVector()
    if params.inter:
        deepFaceInterVideo()
    if params.intra:
        deepFaceIntraVideo()