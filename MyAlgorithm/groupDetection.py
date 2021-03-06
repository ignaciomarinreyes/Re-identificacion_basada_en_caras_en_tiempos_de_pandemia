import glob
import sys

path = sys.argv[1]

def getIdsFile(pathTxtFace):
    dIdsFace = {}
    fileFace = open(pathTxtFace)
    for line in fileFace:
        values = line.split(" ")
        dIdsFace[values[0]] = values
    fileFace.close()
    return dIdsFace

dGroup = {}

print("Empieza")
for pathTxtFace in sorted(glob.glob(path + "*faces.txt")):
    init = pathTxtFace.find("Salida_frame_") + 13
    timeFile = pathTxtFace[init: init + 12]
    dIdsFace = getIdsFile(pathTxtFace)
    print(pathTxtFace)
    for id in dIdsFace:
        if id in dGroup:
            vContent = dGroup[id].copy()
            if dIdsFace[id][6] == '1':
                vContent[4] += 1
            if dIdsFace[id][6] == '0':
                vContent[5] += 1
            if dIdsFace[id][6] == 'ND':
                vContent[6] += 1
            vContent[3] += 1
            vContent[2] = timeFile
            dGroup[id] = vContent
        else:
            dGroup[id] = [id, timeFile, timeFile, 1, 1 if dIdsFace[id][6] == '1' else 0, 1 if dIdsFace[id][6] == '0' else 0, 1 if dIdsFace[id][6] == 'ND' else 0]

fileGroupDetection = open(path + "groupDetection.txt", "w")
for id in dGroup:
    fileGroupDetection.write(str(dGroup[id][0]) + " " + str(dGroup[id][1]) + " " + str(dGroup[id][2]) + " " + str(dGroup[id][3]) + " " + str(dGroup[id][4]) + " " + str(dGroup[id][5]) + " " + str(dGroup[id][6]) + " \n")

print("Termina")

#python3 "/Users/ignacio/TFG/TFG/MyAlgorithm/groupDetection.py" "/Users/ignacio/VideosTFG/LPATrail_21/"