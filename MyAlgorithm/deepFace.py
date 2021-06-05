from deepface import DeepFace
import argparse
import glob
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
from deepface.commons import functions, realtime, distance as dst
from sklearn.metrics import average_precision_score, precision_recall_curve, auc

params = None

def parse_arguments():
    parser = argparse.ArgumentParser(description='DeepFace script')
    parser.add_argument('-path', '-p' ,default="/content/gdrive/My Drive/TFG/data/Reidentification", help='Path to apply DeepFace')
    parser.add_argument('-distInter', '-die', action='store_true')
    parser.add_argument('-distIntra', '-dia', action='store_true')
    parser.add_argument('-vector', '-v', action='store_true')
    parser.add_argument('-rank1', '-r1', action='store_true')
    parser.add_argument('-averagePrecision', '-ap', action='store_true')
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

#distanceCosine, distanceEuclidean, distanceEuclidean_l2
# -r1 -p "/Users/ignacio/TFG/TFG/data/Reidentification"
def rank1DeepFace():
    model_names = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]
    for model in model_names:
        numeradorRank1Cosine = 0
        numeradorRank1Euclidean = 0
        numeradorRank1Euclidean_l2 = 0
        denominadorRank1 = 0
        print("============= " + model + " ===================")
        for dirpath1, dirnames1, filenames1 in os.walk(params.path):
            filenames1 = [f for f in filenames1 if not f[0] == '.' and f[-25:] == 'deepFaceInterDistance.txt' and f.split("_")[5] == model]
            for file1 in sorted(filenames1):
                distCosineList = []
                distEuclideanList = []
                distEuclidean_l2List = []
                id2List = []
                fileOutput = open(dirpath1 + "/" + file1)
                id1 = file1.split("_")[4]
                for line in fileOutput:
                    id2List.append(line.split(" ")[5])
                    distCosineList.append(line.split(" ")[6])
                    distEuclideanList.append(line.split(" ")[7])
                    distEuclidean_l2List.append(line.split(" ")[8])
                positionMinValueRank1CosineList = distCosineList.index(min(distCosineList))
                positionMinValueRank1EuclideanList = distEuclideanList.index(min(distEuclideanList))
                positionMinValueRank1Euclidean_l2List = distEuclidean_l2List.index(min(distEuclidean_l2List))
                #print(file1)
                #print("positionMinValue " + str(positionMinValueRank1CosineList))
                if(id1 == id2List[positionMinValueRank1CosineList]):
                    numeradorRank1Cosine+=1
                    #print("numeradorRank1 " + str(numeradorRank1Cosine))
                if(id1 == id2List[positionMinValueRank1EuclideanList]):
                    numeradorRank1Euclidean+=1
                if(id1 == id2List[positionMinValueRank1Euclidean_l2List]):
                    numeradorRank1Euclidean_l2+=1
                denominadorRank1+=1
        rank1Cosine = numeradorRank1Cosine/denominadorRank1
        rank1Euclidean = numeradorRank1Euclidean / denominadorRank1
        rank1Euclidean_l2 = numeradorRank1Euclidean_l2 / denominadorRank1
        print("========= RANK1 " + model + " =============")
        print("Cosine " + str(rank1Cosine))
        print("Euclidean " + str(rank1Euclidean))
        print("Euclidean_l2 " + str(rank1Euclidean_l2))

def distanceDeepFaceInterVideo():
    model_names = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]
    for model in model_names:
        print("============= " + model + " ===================")
        for dirpath1, dirnames1, filenames1 in os.walk(params.path):
            filenames1 = [f for f in filenames1 if not f[0] == '.' and f[-18:] == 'deepFaceVector.npy' and f.split("_")[5] == model]
            for file1 in sorted(filenames1):
                pathWithOutBaseName1, id1 = os.path.split(dirpath1)
                x, place1 = os.path.split(pathWithOutBaseName1)
                timeFile1 = file1[0: 12]
                vectorFeature1 = np.load(dirpath1 + "/" + timeFile1 + "_" + id1 + "_" + model +"_deepFaceVector.npy")
                fileOutput = open(dirpath1 + "/" + timeFile1 + "_" + id1 + "_" + model + "_deepFaceInterDistance.txt", "w")
                for dirpath2, dirnames2, filenames2 in os.walk(params.path):
                    filenames2 = [f for f in filenames2 if not f[0] == '.' and f[-18:] == 'deepFaceVector.npy' and f.split("_")[5] == model]
                    for file2 in sorted(filenames2):
                        pathWithOutBaseName2, id2 = os.path.split(dirpath2)
                        y, place2 = os.path.split(pathWithOutBaseName2)
                        timeFile2 = file2[0: 12]
                        if place1 != place2:
                            vectorFeature2 = np.load(dirpath2 + "/" + timeFile2 + "_" + id2 + "_" + model + "_deepFaceVector.npy")
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
                np.save(dirpath + "/" + timeFile + "_" + id + "_" + modelName + "_deepFaceVector", result)


def getParameterAveragePrecision(dirpath1, file1):
    gallery_coincidences = []
    distQueryGalleryCosine = []
    distanceEuclidean = []
    distanceEuclidean_l2 = []
    fileOutput = open(dirpath1 + "/" + file1)
    for line in fileOutput:
        if line.split(" ")[2] == line.split(" ")[5]:
            gallery_coincidences.append(1)
        else:
            gallery_coincidences.append(0)
        distQueryGalleryCosine.append(float(line.split(" ")[6]))
        distanceEuclidean.append(float(line.split(" ")[7]))
        distanceEuclidean_l2.append(float(line.split(" ")[8]))
    similarityQueryGalleryCosine = 1 - distQueryGalleryCosine / np.amax(distQueryGalleryCosine)
    similarityQueryGalleryEuclidean = 1 - distanceEuclidean / np.amax(distanceEuclidean)
    similarityQueryGalleryEuclidean_l2 = 1 - distanceEuclidean_l2 / np.amax(distanceEuclidean_l2)
    return gallery_coincidences, similarityQueryGalleryCosine, similarityQueryGalleryEuclidean, similarityQueryGalleryEuclidean_l2

def averagePrecisionDeepFace():
    model_names = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]
    for model in model_names:
        allAPCosine = []
        allAPEuclidean = []
        allAPEuclidean_l2 = []
        for dirpath1, dirnames1, filenames1 in os.walk(params.path):
            filenames1 = [f for f in filenames1 if not f[0] == '.' and f[-25:] == 'deepFaceInterDistance.txt' and f.split("_")[5] == model]
            for file1 in sorted(filenames1):
                gallery_coincidences, similarityQueryGalleryCosine, similarityQueryGalleryEuclidean, similarityQueryGalleryEuclidean_l2  = getParameterAveragePrecision(dirpath1, file1)
                apCosine = average_precision_score(gallery_coincidences, similarityQueryGalleryCosine, average='macro', pos_label=1)
                apEuclidean = average_precision_score(gallery_coincidences, similarityQueryGalleryEuclidean, average='macro', pos_label=1)
                apEuclidean_l2 = average_precision_score(gallery_coincidences, similarityQueryGalleryEuclidean_l2, average='macro', pos_label=1)
                allAPCosine.append(apCosine)
                allAPEuclidean.append(apEuclidean)
                allAPEuclidean_l2.append(apEuclidean_l2)
        mAPCosine = np.mean(allAPCosine)
        mAPEuclidean = np.mean(allAPEuclidean)
        mAPEuclidean_l2 = np.mean(allAPEuclidean_l2)
        print("============ mAP " + model + " ====================")
        print("mAP Coseno " + str(mAPCosine))
        print("mAP Euclidea " + str(mAPEuclidean))
        print("mAP Euclidea_l2 " + str(mAPEuclidean_l2))
        print("===================================================")


if __name__ == '__main__':
    params = parse_arguments()
    if params.vector:
        deepFaceVector()
    if params.distInter:
        distanceDeepFaceInterVideo()
    if params.distIntra:
        distanceDeepFaceIntraVideo()
    if params.rank1:
        rank1DeepFace()
    if params.averagePrecision:
        averagePrecisionDeepFace()