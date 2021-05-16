import cv2
import glob

#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_prueba/"
#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_tagged_and_result/"

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"

for pathTxtFace in sorted(glob.glob(path + "*faces.txt")):
    init = pathTxtFace.find("Salida_frame_") + 13
    timeFile = pathTxtFace[init: init + 12]
    fileFace = open(pathTxtFace)
    img = cv2.imread(path + "Salida_frame_" + timeFile + ".jpg")
    for line in fileFace:
        values = line.split(" ")
        if values[1] != 'ND' and  values[1] != "HB":
            beginXf, endXf, beginYf, endYf = int(values[2]), int(values[2]) + int(values[4]), int(values[3]), int(values[3]) + int(values[5])
            face_img = img[beginYf:endYf, beginXf:endXf]
            cv2.imwrite("../data/Faces/" + timeFile  + "_" + values[0] + "_" + values[1] + "_face.jpg",face_img)
            print("Creada imagen " + timeFile  + "_" + values[0] + "_" + values[1] + "_face.jpg ")
    fileFace.close()