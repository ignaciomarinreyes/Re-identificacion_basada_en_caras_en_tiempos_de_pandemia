import glob
import sklearn.metrics as mt
import sys

path = sys.argv[1]

def accuracyWearOrNotMask():
    print("========WearOrNotMask========")
    vPred = []
    vTrue = []
    for pathTxtFace, pathTxtTagged in zip(sorted(glob.glob(path + "*faces.txt")), sorted(glob.glob(path + "*tagged.txt"))):
        fileResult = open(pathTxtFace)
        fileTagged = open(pathTxtTagged)
        for lineResult, lineTagged in zip(fileResult, fileTagged):
            valuesLineFaces = lineResult.split(" ")
            valuesLineTagged = lineTagged.split(" ")
            if valuesLineTagged[6] != "ND" and valuesLineFaces[6] != "ND":
                vTrue.append(int(valuesLineTagged[6]))
                vPred.append(int(valuesLineFaces[6]))
    print("======Metrics=====")
    print(mt.accuracy_score(vTrue, vPred))
    print("===Confusion matrix =====")
    print(mt.confusion_matrix(vTrue,vPred))

def accuracyWearMask():
    print("========WearMask========")
    vPred = []
    vTrue = []
    for pathTxtFace, pathTxtTagged in zip(sorted(glob.glob(path + "*faces.txt")), sorted(glob.glob(path + "*tagged.txt"))):
        fileResult = open(pathTxtFace)
        fileTagged = open(pathTxtTagged)
        for lineResult, lineTagged in zip(fileResult, fileTagged):
            valuesLineFaces = lineResult.split(" ")
            valuesLineTagged = lineTagged.split(" ")
            if valuesLineTagged[6] != "ND" and valuesLineFaces[6] != "ND" and int(valuesLineTagged[6]) == 1:
                vTrue.append(int(valuesLineTagged[6]))
                vPred.append(int(valuesLineFaces[6]))
    print("======Metrics=====")
    print(mt.accuracy_score(vTrue, vPred))
    print("===Confusion matrix =====")
    print(mt.confusion_matrix(vTrue,vPred))

def accuracyNotWearMask():
    print("========NotWearMask========")
    vPred = []
    vTrue = []
    for pathTxtFace, pathTxtTagged in zip(sorted(glob.glob(path + "*faces.txt")), sorted(glob.glob(path + "*tagged.txt"))):
        fileFaces = open(pathTxtFace)
        fileTagged = open(pathTxtTagged)
        for lineResult, lineTagged in zip(fileFaces, fileTagged):
            valuesLineFaces = lineResult.split(" ")
            valuesLineTagged = lineTagged.split(" ")
            if valuesLineTagged[6] != "ND" and valuesLineFaces[6] != "ND" and int(valuesLineTagged[6]) == 0:
                vTrue.append(int(valuesLineTagged[6]))
                vPred.append(int(valuesLineFaces[6]))
    print("======Metrics=====")
    print(mt.accuracy_score(vTrue, vPred))
    print("===Confusion matrix =====")
    print(mt.confusion_matrix(vTrue,vPred))

accuracyWearOrNotMask()
accuracyWearMask()
accuracyNotWearMask()

# python3 /Users/ignacio/TFG/TFG/MyAlgorithm/fiabilityDetection.py  "/Users/ignacio/VideosTFG/LPATrail_21/"
