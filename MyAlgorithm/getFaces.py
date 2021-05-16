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
            beginXf, endXf, beginYf, endYf = int(values[2]), int(values[2]) + int(values[4]), int(values[3]), int(values[3]) + int(values[5])
            face_img = img[beginYf:endYf, beginXf:endXf]
            cv2.imwrite("../data/Faces/" + timeFile  + "_" + values[0] + "_" + values[1] + "_face.png ",face_img)
            print("Creada imagen " + timeFile  + "_" + values[0] + "_" + values[1] + "_face.png ")
    fileFace.close()