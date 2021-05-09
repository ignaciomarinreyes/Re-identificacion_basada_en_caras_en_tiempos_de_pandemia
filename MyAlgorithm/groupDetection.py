import glob

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"
#path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_tagged_and_result/"
umbral = 10

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
for pathTxtFace in sorted(glob.glob(path + "*faces.txt")):
    init = pathTxtFace.find("Salida_frame_") + 13
    timeFile = pathTxtFace[init: init + 12]
    dIdsFace = getIdsFile(pathTxtFace)
    for id in dIdsFace:
        if id not in dNorepetition:
            dNorepetition[id] = 0
    for id in dNorepetition:
        if id not in dIdsFace:
            dNorepetition[id] = dNorepetition[id] + 1
    for id in dIdsFace:
        if id in dNorepetition:
            if dNorepetition[id] > umbral:
                newId = int(id) + 1000
                newId = str(newId)
                if newId in dGroup:
                    vContent = dGroup[newId].copy()
                    if dIdsFace[id][4] == '1':
                        vContent[8] += 1
                    if dIdsFace[id][4] == '0':
                        vContent[9] += 1
                    if dIdsFace[id][4] == 'ND':
                        vContent[10] += 1
                    vContent[7] = timeFile
                    dGroup[newId] = vContent
                else:
                    dGroup[newId] = [newId, dIdsFace[id][0], dIdsFace[id][1], dIdsFace[id][2], dIdsFace[id][3],0, timeFile, timeFile, 1 if dIdsFace[id][4] == '1' else 0, 1 if dIdsFace[id][4] == '0' else 0, 1 if dIdsFace[id][4] == 'ND' else 0]
            else:
                if id in dGroup:
                    vContent = dGroup[id].copy()
                    if dIdsFace[id][4] == '1':
                        vContent[8] += 1
                    if dIdsFace[id][4] == '0':
                        vContent[9] += 1
                    if dIdsFace[id][4] == 'ND':
                        vContent[10] += 1
                    vContent[7] = timeFile
                    dGroup[id] = vContent
                else:
                    dGroup[id] = [id, dIdsFace[id][0], dIdsFace[id][1], dIdsFace[id][2], dIdsFace[id][3], 0, timeFile, timeFile, 1 if dIdsFace[id][4] == '1' else 0, 1 if dIdsFace[id][4] == '0' else 0, 1 if dIdsFace[id][4] == 'ND' else 0]
print(dGroup)
fileGroupDetection = open(path + "groupDetection.txt", "w")
for id in dGroup:
    fileGroupDetection.write(str(dGroup[id][0]) + " " + str(dGroup[id][1]) + " " + str(dGroup[id][2]) + " " + str(dGroup[id][3]) + " " + str(dGroup[id][4]) + " " + str(dGroup[id][5]) + " " + str(dGroup[id][6]) + " " + str(dGroup[id][7])+ " " + str(dGroup[id][8])+ " " + str(dGroup[id][9])+ " " + str(dGroup[id][10]) + " \n")