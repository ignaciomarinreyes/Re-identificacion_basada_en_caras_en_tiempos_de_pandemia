import cv2
import glob

#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_prueba/"
#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_tagged_and_result/"

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"

for pathTxtBody, pathTxtFace, pathJpg in zip(sorted(glob.glob(path + "*bodies.txt")), sorted(glob.glob(path + "*faces.txt")), sorted(glob.glob(path + "*.jpg"))):
    init = pathTxtBody.find("Salida_frame_") + 13
    timeFile = pathTxtBody[init: init + 12]
    fileBody = open(pathTxtBody)
    fileFace = open(pathTxtFace)
    img = cv2.imread(pathJpg)
    for lineBodies in fileBody:
        valuesBodies = lineBodies.split(" ")
        print("lineBody " + lineBodies)
        beginX, endX, beginY, endY = int(valuesBodies[1]), int(valuesBodies[1]) + int(valuesBodies[3]), int(valuesBodies[2]), int(valuesBodies[2]) + int(valuesBodies[4])
        body_img = img[beginY:endY, beginX:endX]
        cv2.imwrite("../data/BodiesAndFaces/" + timeFile  + "_" + valuesBodies[0] + "_body.png ",body_img)
    for lineFace in fileFace:
        valuesFace = lineFace.split(" ")
        print("lineFace " + lineFace)
        if valuesFace[2] != 'ND':
            beginXf, endXf, beginYf, endYf = int(valuesFace[2]), int(valuesFace[2]) + int(valuesFace[4]), int(valuesFace[3]), int(valuesFace[3]) + int(valuesFace[5])
            face_img = img[beginYf:endYf, beginXf:endXf]
            cv2.imwrite("../data/BodiesAndFaces/" + timeFile  + "_" + valuesFace[0] + "_" + valuesFace[1] + "_face.png ", face_img)
        else:
            fileFaceNull = open("../data/BodiesAndFaces/" + timeFile  + "_" + valuesFace[0] + "_" + valuesFace[1] + "_FaceNoEncontrada", "w")
            fileFaceNull.close()
    fileBody.close()
    fileFace.close()
