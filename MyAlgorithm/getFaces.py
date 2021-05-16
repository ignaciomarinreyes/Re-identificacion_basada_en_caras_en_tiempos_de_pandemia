import cv2
import glob

#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_prueba/"
#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_tagged_and_result/"

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"

for pathTxtFace, pathJpg in zip(sorted(glob.glob(path + "*faces.txt")), sorted(glob.glob(path + "*.jpg"))):
    init = pathTxtFace.find("Salida_frame_") + 13
    timeFile = pathTxtFace[init: init + 12]
    fileFace = open(pathTxtFace)
    img = cv2.imread(pathJpg)
    for line in fileFace:
        values = line.split(" ")
        if values[1] != 'ND':
            beginX, endX, beginY, endY = int(values[1]), int(values[1]) + int(values[3]), int(values[2]), int(values[2]) + int(values[4])
            print(values[1] + " "  + values[2] + " " + values[3] + " " + values[4])
            face_img = img[beginY:endY, beginX:endX]
            cv2.imwrite("../data/Faces/" + values[0] + "_" + timeFile  + ".png ",face_img)
            print("Creada imagen " +  values[0] + "_" + timeFile  + ".png ")
    fileFace.close()