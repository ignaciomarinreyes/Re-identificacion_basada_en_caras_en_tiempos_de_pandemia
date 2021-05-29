import cv2
import glob

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"

for pathTxtBody in sorted(glob.glob(path + "*bodies.txt")):
    init = pathTxtBody.find("Salida_frame_") + 13
    timeFile = pathTxtBody[init: init + 12]
    fileFace = open(pathTxtBody)
    img = cv2.imread(path + "Salida_frame_" + timeFile + ".png")
    for line in fileFace:
        values = line.split(" ")
        beginX, endX, beginY, endY = int(values[1]), int(values[1]) + int(values[3]), int(values[2]), int(values[2]) + int(values[4])
        body_img = img[beginY:endY, beginX:endX]
        cv2.imwrite("../data/BodiesAndFaces/" + timeFile + "_" + values[0] + "_body.png", body_img)
        print("Creada imagen " + timeFile + "_" + values[0] + "_body.png")
    fileFace.close()

for pathTxtFace in sorted(glob.glob(path + "*faces.txt")):
    init = pathTxtFace.find("Salida_frame_") + 13
    timeFile = pathTxtFace[init: init + 12]
    fileFace = open(pathTxtFace)
    img = cv2.imread(path + "Salida_frame_" + timeFile + ".png")
    for line in fileFace:
        values = line.split(" ")
        if values[1] != 'ND' and  values[1] != "HB":
            beginXf, endXf, beginYf, endYf = int(values[2]), int(values[2]) + int(values[4]), int(values[3]), int(values[3]) + int(values[5])
            face_img = img[beginYf:endYf, beginXf:endXf]
            cv2.imwrite("../data/BodiesAndFaces/" + timeFile  + "_" + values[0] + "_" + values[1] + "_face.png",face_img)
            print("Creada imagen " + timeFile  + "_" + values[0] + "_" + values[1] + "_face.png ")
    fileFace.close()