import cv2
import glob

#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_prueba/"
#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_tagged_and_result/"

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"
i = 0

for pathTxtBody, pathTxtFace, pathJpg in zip(sorted(glob.glob(path + "*bodies.txt")), sorted(glob.glob(path + "*faces.txt")), sorted(glob.glob(path + "*.jpg"))):
    init = pathTxtBody.find("Salida_frame_") + 13
    timeFile = pathTxtBody[init: init + 12]
    fileBody = open(pathTxtBody)
    fileFace = open(pathTxtFace)
    img = cv2.imread(pathJpg)
    for lineBodies, lineFace in zip(fileBody, fileFace):
        valuesBodies = lineBodies.split(" ")
        valuesFace = lineFace.split(" ")
        print("lineBody " + lineBodies)
        print("lineFace " + lineFace)
        beginX, endX, beginY, endY = int(valuesBodies[1]), int(valuesBodies[1]) + int(valuesBodies[3]), int(valuesBodies[2]), int(valuesBodies[2]) + int(valuesBodies[4])
        body_img = img[beginY:endY, beginX:endX]
        cv2.imwrite("../data/BodiesAndFaces/" + str(i) + "_" + timeFile  + "_" + valuesBodies[0] + "_body_.png ",body_img)
        i+=1
        if valuesFace[1] != 'ND':
            beginXf, endXf, beginYf, endYf = int(valuesFace[1]), int(valuesFace[1]) + int(valuesFace[3]), int(valuesFace[2]), int(valuesFace[2]) + int(valuesFace[4])
            face_img = img[beginYf:endYf, beginXf:endXf]
            cv2.imwrite("../data/BodiesAndFaces/" + str(i) + "_" + timeFile  + " " + valuesFace[0] + "_face_.png ", face_img)
        else:
            fileFaceNull = open("../data/BodiesAndFaces/"+ str(i) + "_" + timeFile  + " " + valuesFace[0] +  "_FaceNoEncontrada", "w")
            fileFaceNull.close()
        i += 1
    fileBody.close()
    fileFace.close()
