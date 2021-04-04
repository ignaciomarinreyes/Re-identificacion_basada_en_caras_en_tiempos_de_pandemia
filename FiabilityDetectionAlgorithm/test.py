import glob
import numpy as np
import sklearn.metrics as mt

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"

def isInBox(tx, ty, bxi, bxe, byi, bye):
    return bxi < tx < bxe and byi < ty < bye

def isOrNotwearingMask(maskTagged, maskResult):
    return maskTagged == maskResult

def iswearingMask(maskResult):
    return 1 == maskResult

def isNotwearingMask(maskResult):
    return 0 == maskResult

def accuracyInBoxAndWearOrNotMask():
    print("========InBoxAndWearOrNotMask========")
    vPred = []
    vTrue = []
    found = False
    for pathTxtResult, pathTxtTagged in zip(sorted(glob.glob(path + "*result.txt")), sorted(glob.glob(path + "*tagged.txt"))):
        fileTagged = open(pathTxtTagged)
        lineResultV = np.loadtxt(pathTxtResult).astype(int)
        for lineTagged in fileTagged:
            valuesLineTagged = lineTagged.split(" ")
            vTrue.append(int(valuesLineTagged[2]))
            for valuesLineResult in lineResultV:
                #print("---------------------")
                x1 = valuesLineResult[0] + valuesLineResult[2]
                y1 = valuesLineResult[1] + valuesLineResult[3]
                #print("Labed coordenada: x: " + str(valuesLineTagged[0]) + " y: " + str(valuesLineTagged[1]) + " Mask: " + str(valuesLineTagged[2]))
                #print("Result coordenada: x0: " + str(valuesLineResult[0]) + " x1: " + str(x1) + " y0: " + str(valuesLineResult[1]) + " y1: " + str(y1) + " Mask: " + str(valuesLineResult[4]))
                if isInBox(int(valuesLineTagged[0]), int(valuesLineTagged[1]), valuesLineResult[0], x1, valuesLineResult[1], y1) and isOrNotwearingMask(int(valuesLineTagged[2]), valuesLineResult[4]):
                    found = True
                    #print("Success")
                    break
            if found:
                vPred.append(1)
            else:
                vPred.append(0)
            found = False
            #print("-----Change person ------")
        #print("============Change file==================")
    print("vPred:")
    print(vPred)
    print("vTrue:")
    print(vTrue)
    print("======Metrics=====")
    print(mt.accuracy_score(vTrue, vPred))

def accuracyInBox():
    print("========InBox========")
    vPred = []
    vTrue = []
    found = False
    for pathTxtResult, pathTxtTagged in zip(sorted(glob.glob(path + "*result.txt")), sorted(glob.glob(path + "*tagged.txt"))):
        fileTagged = open(pathTxtTagged)
        lineResultV = np.loadtxt(pathTxtResult).astype(int)
        for lineTagged in fileTagged:
            valuesLineTagged = lineTagged.split(" ")
            vTrue.append(int(valuesLineTagged[2]))
            for valuesLineResult in lineResultV:
                #print("---------------------")
                x1 = valuesLineResult[0] + valuesLineResult[2]
                y1 = valuesLineResult[1] + valuesLineResult[3]
                #print("Labed coordenada: x: " + str(valuesLineTagged[0]) + " y: " + str(valuesLineTagged[1]) + " Mask: " + str(valuesLineTagged[2]))
                #print("Result coordenada: x0: " + str(valuesLineResult[0]) + " x1: " + str(x1) + " y0: " + str(valuesLineResult[1]) + " y1: " + str(y1) + " Mask: " + str(valuesLineResult[4]))
                if isInBox(int(valuesLineTagged[0]), int(valuesLineTagged[1]), valuesLineResult[0], x1, valuesLineResult[1], y1):
                    found = True
                    #print("Success")
                    break
            if found:
                vPred.append(1)
            else:
                vPred.append(0)
            found = False
            #print("-----Change person ------")
        #print("============Change file==================")
    print("vPred:")
    print(vPred)
    print("vTrue:")
    print(vTrue)
    print("======Metrics=====")
    print(mt.accuracy_score(vTrue, vPred))


def accuracyInBoxAndWearMask():
    print("========InBoxAndWearMask========")
    vPred = []
    vTrue = []
    found = False
    for pathTxtResult, pathTxtTagged in zip(sorted(glob.glob(path + "*result.txt")), sorted(glob.glob(path + "*tagged.txt"))):
        fileTagged = open(pathTxtTagged)
        lineResultV = np.loadtxt(pathTxtResult).astype(int)
        for lineTagged in fileTagged:
            valuesLineTagged = lineTagged.split(" ")
            if int(valuesLineTagged[2]) != 1:
                continue
            vTrue.append(int(valuesLineTagged[2]))
            for valuesLineResult in lineResultV:
                #print("---------------------")
                x1 = valuesLineResult[0] + valuesLineResult[2]
                y1 = valuesLineResult[1] + valuesLineResult[3]
                #print("Labed coordenada: x: " + str(valuesLineTagged[0]) + " y: " + str(valuesLineTagged[1]) + " Mask: " + str(valuesLineTagged[2]))
                #print("Result coordenada: x0: " + str(valuesLineResult[0]) + " x1: " + str(x1) + " y0: " + str(valuesLineResult[1]) + " y1: " + str(y1) + " Mask: " + str(valuesLineResult[4]))
                if isInBox(int(valuesLineTagged[0]), int(valuesLineTagged[1]), valuesLineResult[0], x1, valuesLineResult[1], y1) and iswearingMask(valuesLineResult[4]):
                    found = True
                    #print("Success")
                    break
            if found:
                vPred.append(1)
            else:
                vPred.append(0)
            found = False
            #print("-----Change person ------")
        #print("============Change file==================")
    print("vPred:")
    print(vPred)
    print("vTrue:")
    print(vTrue)
    print("======Metrics=====")
    print(mt.accuracy_score(vTrue, vPred))

def accuracyInBoxAndNotWearMask():
    print("========InBoxAndNotWearMask========")
    vPred = []
    vTrue = []
    found = False
    for pathTxtResult, pathTxtTagged in zip(sorted(glob.glob(path + "*result.txt")), sorted(glob.glob(path + "*tagged.txt"))):
        fileTagged = open(pathTxtTagged)
        lineResultV = np.loadtxt(pathTxtResult).astype(int)
        for lineTagged in fileTagged:
            valuesLineTagged = lineTagged.split(" ")
            if int(valuesLineTagged[2]) != 0:
                continue
            vTrue.append(int(valuesLineTagged[2]))
            for valuesLineResult in lineResultV:
                #print("---------------------")
                x1 = valuesLineResult[0] + valuesLineResult[2]
                y1 = valuesLineResult[1] + valuesLineResult[3]
                #print("Labed coordenada: x: " + str(valuesLineTagged[0]) + " y: " + str(valuesLineTagged[1]) + " Mask: " + str(valuesLineTagged[2]))
                #print("Result coordenada: x0: " + str(valuesLineResult[0]) + " x1: " + str(x1) + " y0: " + str(valuesLineResult[1]) + " y1: " + str(y1) + " Mask: " + str(valuesLineResult[4]))
                if isInBox(int(valuesLineTagged[0]), int(valuesLineTagged[1]), valuesLineResult[0], x1, valuesLineResult[1], y1) and isNotwearingMask(valuesLineResult[4]):
                    found = True
                    #print("Success")
                    break
            if found:
                vPred.append(1)
            else:
                vPred.append(0)
            found = False
            #print("-----Change person ------")
        #print("============Change file==================")
    print("vPred:")
    print(vPred)
    print("vTrue:")
    print(vTrue)
    print("======Metrics=====")
    print(mt.accuracy_score(vTrue, vPred))


accuracyInBoxAndWearOrNotMask()
accuracyInBox()
accuracyInBoxAndWearMask()
#accuracyInBoxAndNotWearMask() // No hay nadie sin máscara por lo que falla