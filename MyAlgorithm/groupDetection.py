import glob

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"
#path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_tagged_and_result/"
umbral = 2

def getIdsFile(pathTxtFace):
    dIdsFace = {}
    fileFace = open(pathTxtFace)
    for line in fileFace:
        values = line.split(" ")
        dIdsFace[values[5]] = values
    fileFace.close()
    return dIdsFace

dGroup = {}
dNorepetition = {}
dIncrement = {}
idNew = 0

for pathTxtFace in sorted(glob.glob(path + "*faces.txt")):
    init = pathTxtFace.find("Salida_frame_") + 13
    timeFile = pathTxtFace[init: init + 12]
    dIdsFace = getIdsFile(pathTxtFace)
    for id in dIdsFace:
        if id not in dIncrement:
            dIncrement[id] = 0
        idNew = str(int(id) + dIncrement[id])
        if idNew not in dNorepetition:
            dNorepetition[idNew] = 0
    for id in dNorepetition:
        if id not in dIdsFace:
            dNorepetition[id] = dNorepetition[id] + 1
        else:
            dNorepetition[id] = 0
    for id in dIdsFace:
        idNew = str(int(id) + dIncrement[id])
        if idNew not in dIncrement:
            dIncrement[idNew] = 0
        if idNew in dNorepetition:
            if dNorepetition[idNew] > umbral:
                dIncrement[idNew] = dIncrement[idNew] + 1000
            else:
                if idNew in dGroup:
                    vContent = dGroup[idNew].copy()
                    if dIdsFace[id][4] == '1':
                        vContent[8] += 1
                    if dIdsFace[id][4] == '0':
                        vContent[9] += 1
                    if dIdsFace[id][4] == 'ND':
                        vContent[10] += 1
                    vContent[7] = timeFile
                    dGroup[idNew] = vContent
                else:
                    dGroup[idNew] = [idNew, dIdsFace[id][0], dIdsFace[id][1], dIdsFace[id][2], dIdsFace[id][3], 0, timeFile, timeFile, 1 if dIdsFace[id][4] == '1' else 0, 1 if dIdsFace[id][4] == '0' else 0, 1 if dIdsFace[id][4] == 'ND' else 0]

print(dGroup)
fileGroupDetection = open(path + "groupDetection.txt", "w")
for id in dGroup:
    fileGroupDetection.write(str(dGroup[id][0]) + " " + str(dGroup[id][1]) + " " + str(dGroup[id][2]) + " " + str(dGroup[id][3]) + " " + str(dGroup[id][4]) + " " + str(dGroup[id][5]) + " " + str(dGroup[id][6]) + " " + str(dGroup[id][7])+ " " + str(dGroup[id][8])+ " " + str(dGroup[id][9])+ " " + str(dGroup[id][10]) + " \n")