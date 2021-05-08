import glob

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"
#path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_tagged_and_result/"

def readFile(pathTxtFace):
    vIdBeforeFile = []
    fileFaceTemp = open(pathTxtFace)
    for line in fileFaceTemp:
        values = line.split(" ")
        vIdBeforeFile.append(values[5])
    fileFaceTemp.close()
    return vIdBeforeFile


vGeneralId = [None] * 500
i = 0
pathTxtFaceBefore = ""
for pathTxtFace in sorted(glob.glob(path + "*faces.txt")):
    init = pathTxtFace.find("Salida_frame_") + 13
    timeFile = pathTxtFace[init: init + 12]
    if i == 0:
        pathTxtFaceBefore = pathTxtFace
    if i > 0:
        vIdsBeforeFile = readFile(pathTxtFaceBefore)
        fileFace = open(pathTxtFace)
        for line in fileFace:
            fields = line.split(" ")
            vContent = []
            if vGeneralId[int(fields[5])] is not None:
                vContent = vGeneralId[int(fields[5])].copy()
                vContent[1] += 1
                if fields[4] == '1':
                    vContent[4] += 1
                if fields[4] == '0':
                    vContent[5] += 1
                if fields[4] == 'ND':
                    vContent[6] += 1
                if fields[5] not in vIdsBeforeFile:
                    vContent[3] = timeFile
            else:
                vContent = [str(fields[5]),0,timeFile,None,0,0,0]
            vGeneralId[int(fields[5])] = vContent
        pathTxtFaceBefore = pathTxtFace
    i+=1

print(vGeneralId)
fileGroupDetection = open(path + "groupDetection.txt", "w")
for values in vGeneralId:
    if values is not None:
        fileGroupDetection.write(str(values[0]) + " " + str(values[1]) + " " + str(values[2]) + " " + str(values[3]) + " " + str(values[4]) + " " + str(values[5]) + " " + str(values[6]) + "\n")


