import glob
import numpy as np

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"

def isInBox(tx, ty, bxi, bxe, byi, bye):
    return bxi < tx < bxe and byi < ty < bye

def iswearingMask(maskTagged, maskResult):
    return maskTagged == maskResult

totalPeople = 0
totalSuccess = 0
for pathTxtResult, pathTxtTagged in zip(sorted(glob.glob(path + "*result.txt")), sorted(glob.glob(path + "*tagged.txt"))):
    fileTagged = open(pathTxtTagged)
    lineResultV = np.loadtxt(pathTxtResult).astype(int)
    numberPeople = 0
    numberSuccess = 0
    for lineTagged in fileTagged:
        valuesLineTagged = lineTagged.split(" ")
        numberPeople += 1
        for valuesLineResult in lineResultV:
            x1 = valuesLineResult[0] + valuesLineResult[2]
            y1 = valuesLineResult[1] + valuesLineResult[3]
            print("Labed coordenada: x: " + str(valuesLineTagged[0]) + " y: " + str(valuesLineTagged[1]) + " Mask: " + str(valuesLineTagged[2]))
            print("Result coordenada: x0: " + str(valuesLineResult[0]) + " x1: " + str(x1) + " y0: " + str(valuesLineResult[1]) + " y1: " + str(y1) + " Mask: " + str(valuesLineResult[4]))
            if isInBox(int(valuesLineTagged[0]), int(valuesLineTagged[1]), valuesLineResult[0], x1, valuesLineResult[1], y1) and iswearingMask(int(valuesLineTagged[2]), valuesLineResult[4]):
                numberSuccess+=1
                print("Success")
            print("Number success: " + str(numberSuccess))
            print("Number people: " + str(numberPeople))
            print("---------------------")
        print("-----Change person ------")
    totalPeople += numberPeople
    totalSuccess += numberSuccess
    print("============Change file==================")
print("Number total success: " + str(totalSuccess))
print("Number total people: " + str(totalPeople))
print("Hit rate: " + str((totalSuccess/totalPeople)*100))


