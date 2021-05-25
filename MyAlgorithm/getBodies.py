import cv2
import glob

#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_prueba/"
#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_tagged_and_result/"

path="/Users/ignacio/TFG/TFG/data/LPATrail19Prueba/"
#pathDestiny = "../data/Bodies/"
pathDestiny = "/Users/ignacio/dataTFG/Bodies/"


for pathTxtBody in sorted(glob.glob(path + "*bodies.txt")):
    init = pathTxtBody.find("Salida_frame_") + 13
    timeFile = pathTxtBody[init: init + 12]
    fileFace = open(pathTxtBody)
    img = cv2.imread(path + "Salida_frame_" + timeFile + ".jpg")
    for line in fileFace:
        values = line.split(" ")
        print(values[1])
        beginX, endX, beginY, endY = int(values[1]), int(values[1]) + int(values[3]), int(values[2]), int(values[2]) + int(values[4])
        body_img = img[beginY:endY, beginX:endX]
        cv2.imwrite(pathDestiny + timeFile + "_" + values[0] + "_body.jpg", body_img)
        print("Creada imagen " + timeFile + "_" + values[0] + "_body.jpg")
    fileFace.close()