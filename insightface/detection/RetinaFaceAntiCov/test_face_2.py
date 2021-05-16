import cv2
import sys
import numpy as np
import datetime
import os
import glob
from retinaface_cov import RetinaFaceCoV

thresh = 0.8
mask_thresh = 0.2
gpuid = 0
path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_prueba/"
#path="/content/gdrive/My Drive/TFG/data/LPATrail20-Salida_faces_tagged_and_result/"

detector = RetinaFaceCoV("/content/gdrive/My Drive/TFG/insightface/detection/RetinaFaceAntiCov/model/mnet_cov2", 0, gpuid, 'net3l')
for pathTxtBody, pathJpg in zip(sorted(glob.glob(path + "*bodies.txt")), sorted(glob.glob(path + "*.jpg"))):
    print("###################################")
    print("Leyendo:" + pathTxtBody)
    init = pathTxtBody.find("Salida_frame_") + 13
    timeFile = pathTxtBody[init: init + 12]
    fileBody = open(pathTxtBody)
    img = cv2.imread(pathJpg)
    fileOutput = open(path + "Salida_frame_" + timeFile + "_faces.txt", "w")
    for line in fileBody:
        scales = [640, 1080]
        values = line.split(" ")
        print("===========================================")
        print(values[0] + " " + values[1] + " " + values[2] + " " + values[3] + " " + values[4])
        beginXBody, endXBody, beginYBody, endYBody = int(values[1]), int(values[1]) + int(values[3]), int(values[2]), int(
            values[2]) + int(values[4])
        #if beginX < 0:
        #    beginX = 0
        #if beginY < 0:
        #    beginY = 0
        heihtImageBody = int(endYBody) - int(beginYBody)
        endYBodyHead = int(beginYBody) + int((1 / 3 * heihtImageBody)) #BeginYBody es la parte superior, el 0 de y está arriba
        crop_imgBodyHead = img[beginYBody:endYBodyHead, beginXBody:endXBody]
        im_shape = crop_imgBodyHead.shape
        target_size = scales[0]
        max_size = scales[1]
        im_size_min = np.min(im_shape[0:2])
        im_size_max = np.max(im_shape[0:2])
        im_scale = float(target_size) / float(im_size_min)
        if np.round(im_scale * im_size_max) > max_size:
            im_scale = float(max_size) / float(im_size_max)
        scales = [im_scale]
        flip = False
        if (heihtImageBody > 30):
            faces, landmarks = detector.detect(crop_imgBodyHead,
                                               thresh,
                                               scales=scales,
                                               do_flip=flip)
            if faces is not None:
                print('find', faces.shape[0], 'faces')
                if faces.shape[0] == 0:
                    fileOutput.write(values[0] + " ND ND ND ND ND ND ND ND ND ND ND ND ND ND ND ND \n")
                else:
                    areaBoxFace = []
                    for i in range(faces.shape[0]):
                        face = faces[i]
                        boxFace = face[0:4].astype(np.int)
                        widthXBoxFace = boxFace[2] - boxFace[0]
                        heightYBoxFace = boxFace[3] - boxFace[1]
                        areaBoxFaceValue = widthXBoxFace * heightYBoxFace
                        areaBoxFace.append(areaBoxFaceValue)
                    maxValue = max(areaBoxFace)
                    j = areaBoxFace.index(maxValue)
                    landmark5 = landmarks[j].astype(np.int)
                    faceMax = faces[j]
                    boxFace = faceMax[0:4].astype(np.int)
                    mask = faceMax[5]
                    colorBox = 0
                    if mask >= mask_thresh:
                        color = (0, 0, 255) # Black color in BGR, red
                        colorBox = 1
                    else:
                        color = (0, 255, 0) # green
                        colorBox = 0
                    beginXBoxFace = beginXBody + boxFace[0]
                    widthXBoxFace = boxFace[2] - boxFace[0]
                    beginYBoxFace = beginYBody + boxFace[1]
                    heightYBoxFace = boxFace[3] - boxFace[1]
                    print("Limit box: " + str(beginXBoxFace) + " " + str(beginYBoxFace) + " " + str(widthXBoxFace) + " " + str(heightYBoxFace) + "--->" + str(colorBox) + " " + str(values[0]))
                    fileOutput.write(str(values[0]) + " " + str(j) + " " + str(beginXBoxFace) + " " + str(beginYBoxFace) + " " + str(widthXBoxFace) + " " + str(heightYBoxFace) + " " + str(colorBox) + " " + str(landmark5[0][0]) + " " + str(landmark5[0][1]) + " " + str(landmark5[1][0]) + " " + str(landmark5[1][1]) + " " + str(landmark5[2][0]) + " " + str(landmark5[2][1]) + " " + str(landmark5[3][0]) + " " + str(landmark5[3][1]) + " " + str(landmark5[4][0]) + " " + str(landmark5[4][1]) + " \n")
        else:
            fileOutput.write(values[0] + " ND ND ND ND ND ND ND ND ND ND ND ND ND ND ND HB \n")
            print("Box ready: "  + path + "Salida_frame_" + timeFile + "_faces.txt")
    fileOutput.close()
    sizefile = os.stat(path + "Salida_frame_" + timeFile + "_faces.txt").st_size
    if(sizefile == 0):
        os.remove(path + "Salida_frame_" + timeFile + "_faces.txt")
    fileBody.close()
