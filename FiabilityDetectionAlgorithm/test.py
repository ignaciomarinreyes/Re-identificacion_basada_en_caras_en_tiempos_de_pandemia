import glob
import numpy as np
import sklearn.metrics as mt

#path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"
path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_tagged_and_result/"

def accuracyWearOrNotMask():
    print("========WearOrNotMask========")
    vPred = []
    vTrue = []
    for pathTxtResult, pathTxtTagged in zip(sorted(glob.glob(path + "*result.txt")), sorted(glob.glob(path + "*tagged.txt"))):
        fileResult = open(pathTxtResult)
        fileTagged = open(pathTxtTagged)
        for lineResult, lineTagged in zip(fileResult, fileTagged):
            valuesLineResult = lineResult.split(" ")
            valuesLineTagged = lineTagged.split(" ")
            if valuesLineTagged[4] != "ND":
                vTrue.append(int(valuesLineTagged[4]))
                vPred.append(int(valuesLineResult[4]))
    print("vPred:")
    print(vPred)
    print("vTrue:")
    print(vTrue)
    print("======Metrics=====")
    print(mt.accuracy_score(vTrue, vPred))

def accuracyWearMask():
    print("========WearMask========")
    vPred = []
    vTrue = []
    for pathTxtResult, pathTxtTagged in zip(sorted(glob.glob(path + "*result.txt")), sorted(glob.glob(path + "*tagged.txt"))):
        fileResult = open(pathTxtResult)
        fileTagged = open(pathTxtTagged)
        for lineResult, lineTagged in zip(fileResult, fileTagged):
            valuesLineResult = lineResult.split(" ")
            valuesLineTagged = lineTagged.split(" ")
            if valuesLineTagged[4] != "ND" and int(valuesLineTagged[4]) == 1:
                vTrue.append(int(valuesLineTagged[4]))
                vPred.append(int(valuesLineResult[4]))
    print("vPred:")
    print(vPred)
    print("vTrue:")
    print(vTrue)
    print("======Metrics=====")
    print(mt.accuracy_score(vTrue, vPred))

def accuracyNotWearMask():
    print("========NotWearMask========")
    vPred = []
    vTrue = []
    for pathTxtResult, pathTxtTagged in zip(sorted(glob.glob(path + "*result.txt")), sorted(glob.glob(path + "*tagged.txt"))):
        fileResult = open(pathTxtResult)
        fileTagged = open(pathTxtTagged)
        for lineResult, lineTagged in zip(fileResult, fileTagged):
            valuesLineResult = lineResult.split(" ")
            valuesLineTagged = lineTagged.split(" ")
            if valuesLineTagged[4] != "ND" and int(valuesLineTagged[4]) == 0:
                vTrue.append(int(valuesLineTagged[4]))
                vPred.append(int(valuesLineResult[4]))
    print("vPred:")
    print(vPred)
    print("vTrue:")
    print(vTrue)
    print("======Metrics=====")
    print(mt.accuracy_score(vTrue, vPred))


accuracyWearOrNotMask()
accuracyWearMask()
accuracyNotWearMask() # No hay nadie sin máscara por lo que falla