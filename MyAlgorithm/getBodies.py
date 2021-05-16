import cv2
import glob

#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_prueba/"
#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_tagged_and_result/"

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"

for pathTxtBody, pathJpg in zip(sorted(glob.glob(path + "*bodies.txt")), sorted(glob.glob(path + "*.jpg"))):
    init = pathTxtBody.find("Salida_frame_") + 13
    timeFile = pathTxtBody[init: init + 12]
    fileFace = open(pathTxtBody)
    img = cv2.imread(pathJpg)
    for line in fileFace:
        values = line.split(" ")
        beginX, endX, beginY, endY = int(values[1]), int(values[1]) + int(values[3]), int(values[2]), int(values[2]) + int(values[4])
        print(values[1] + " " + int(values[1]) + int(values[3]) + " " + int(values[2]) + " " + int(values[2]) + int(values[4]))
        body_img = img[beginY:endY, beginX:endX]
        cv2.imwrite("../data/Bodies/" + values[0] + "_" + timeFile  + ".png ",body_img)
        print("Creada imagen " +  values[0] + "_" + timeFile  + ".png ")
    fileFace.close()
