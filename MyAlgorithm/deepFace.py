from deepface import DeepFace
import argparse
import glob
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
from deepface.commons import functions, realtime, distance as dst

params = None

def parse_arguments():
    parser = argparse.ArgumentParser(description='DeepFace script')
    parser.add_argument('-path', '-p' ,default="/content/gdrive/My Drive/TFG/data/Reidentification", help='Path to apply DeepFace')
    parser.add_argument('-distInter', '-die', action='store_true')
    parser.add_argument('-distIntra', '-dia', action='store_true')
    parser.add_argument('-vector', '-v', action='store_true')
    args = parser.parse_args()
    return args

def distanceVectorFeature(vImage1, vImage2):
    #metrics = ["cosine", "euclidean", "euclidean_l2"]
    distanceCosine = dst.findCosineDistance(vImage1, vImage2)
    distanceEuclidean = dst.findEuclideanDistance(vImage1, vImage2)
    distanceEuclidean_l2 = dst.findEuclideanDistance(dst.l2_normalize(vImage1), dst.l2_normalize(vImage2))
    distanceCosine = np.float64(distanceCosine)
    distanceEuclidean = np.float64(distanceEuclidean)
    distanceEuclidean_l2 = np.float64(distanceEuclidean_l2)
    return distanceCosine, distanceEuclidean, distanceEuclidean_l2


def distanceDeepFaceInterVideo():
    model_names = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]
    for model in model_names:
        print("============= " + model + " ===================")
        for dirpath1, dirnames1, filenames1 in os.walk(params.path):
            filenames1 = [f for f in filenames1 if not f[0] == '.' and f[-18:] == 'deepFaceVector.txt' and f.split("_")[5] == model]
            for file1 in sorted(filenames1):
                pathWithOutBaseName1, id1 = os.path.split(dirpath1)
                x, place1 = os.path.split(pathWithOutBaseName1)
                timeFile1 = file1[0: 12]
                vectorFeature1 = []
                fileOutput1 = open(dirpath1 + "/" + timeFile1 + "_" + id1 + "_" + model +"_deepFaceVector.txt")
                for line1 in fileOutput1:
                    vectorFeature1.append(float(line1))
                fileOutput = open(dirpath1 + "/" + timeFile1 + "_" + id1 + "_" + model + "_deepFaceInterDistance.txt", "w")
                for dirpath2, dirnames2, filenames2 in os.walk(params.path):
                    filenames2 = [f for f in filenames2 if not f[0] == '.' and f[-18:] == 'deepFaceVector.txt' and f.split("_")[5] == model]
                    for file2 in sorted(filenames2):
                        pathWithOutBaseName2, id2 = os.path.split(dirpath2)
                        y, place2 = os.path.split(pathWithOutBaseName2)
                        timeFile2 = file2[0: 12]
                        if place1 != place2:
                            vectorFeature2 = []
                            fileOutput2 = open(dirpath2 + "/" + timeFile2 + "_" + id2 + "_" + model + "_deepFaceVector.txt")
                            for line2 in fileOutput2:
                                vectorFeature2.append(float(line2))
                            print(dirpath1 + "/" + file1 + " ===> " + dirpath2 + "/" + file2 + " ===> " )
                            distanceCosine, distanceEuclidean, distanceEuclidean_l2 = distanceVectorFeature(vectorFeature1, vectorFeature2)
                            fileOutput.write(place1 + " " + timeFile1 + " " + id1 + " " + place2 + " " + timeFile2 + " " + id2 + " " +  str(distanceCosine) + " " +  str(distanceEuclidean)  + " " +  str(distanceEuclidean_l2)  + " \n")


def distanceDeepFaceIntraVideo():
    for pathPng1 in sorted(glob.glob(params.path + "*.png")):
        for pathPng2 in sorted(glob.glob(params.path + "*.png")):
            result = DeepFace.verify(pathPng1, pathPng2, model_name="Facenet", enforce_detection=False)
            print("png_1 " + pathPng1 + " png_2 " + pathPng2 + "===> " + str(result["distance"]))


def deepFaceVector():
    model_names = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]
    for dirpath, dirnames, filenames in os.walk(params.path):
        filenames = [f for f in filenames if not f[0] == '.' and f[-3:] == 'png']
        for file in sorted(filenames):
            pathWithOutBaseName, id = os.path.split(dirpath)
            timeFile = file[0: 12]
            for modelName in model_names:
                try:
                    print(dirpath + "/" + timeFile + "_" + id + "_body.png" + " ===> " + modelName)
                    result = DeepFace.represent(dirpath + "/" + timeFile + "_" + id + "_body.png", model_name=modelName, enforce_detection=False)
                except:
                    print("No se puede aplicar algoritmo" + dirpath + "/" + timeFile + "_" + id + "_body.png"  + " ===> " + modelName)
                fileOutput = open(dirpath + "/" + timeFile + "_" + id + "_" + modelName + "_deepFaceVector.txt", "w")
                for value in result:
                    fileOutput.write(str(value) + "\n")


if __name__ == '__main__':
    params = parse_arguments()
    if params.vector:
        deepFaceVector()
    if params.distInter:
        distanceDeepFaceInterVideo()
    if params.distIntra:
        distanceDeepFaceIntraVideo()