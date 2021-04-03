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
detector = RetinaFaceCoV("/content/gdrive/My Drive/TFG/insightface/detection/RetinaFaceAntiCov/model/mnet_cov2", 0, gpuid, 'net3l')
for pathTxtBody, pathJpg in zip(sorted(glob.glob(path + "*bodies.txt")), sorted(glob.glob(path + "*.jpg"))):
    print("###################################")
    print("Leyendo:" + pathTxtBody)
    init = pathTxtBody.find("Salida_frame_") + 13
    timeFile = pathTxtBody[init: init + 12]
    fileBody = open(pathTxtBody)
    img = cv2.imread(pathJpg)
    j = 1
    for line in fileBody:
        scales = [640, 1080]
        values = line.split(" ")
        if (len(values) == 6 and values[4] == '1'):
            print("===========================================")
            print(values[0] + " " + values[1] + " " + values[2] + " " + values[3] + " " + values[4] + " " + values[5])
            beginX, endX, beginY, endY = int(values[0]), int(values[0]) + int(values[2]), int(values[1]), int(
                values[1]) + int(values[3])
            heihtCropImage = int(endY) - int(beginY)
            endYFace = int(beginY) + int((1/3 * heihtCropImage))
            crop_img = img[beginY:endYFace, beginX:endX]
            print(beginY)
            print(endYFace)
            im_shape = crop_img.shape
            target_size = scales[0]
            max_size = scales[1]
            im_size_min = np.min(im_shape[0:2])
            im_size_max = np.max(im_shape[0:2])
            im_scale = float(target_size) / float(im_size_min)
            if np.round(im_scale * im_size_max) > max_size:
                im_scale = float(max_size) / float(im_size_max)
            scales = [im_scale]
            flip = False
            faces, landmarks = detector.detect(crop_img,
                                               thresh,
                                               scales=scales,
                                               do_flip=flip)
            if faces is not None:
                tempImg = crop_img.copy() # Los círculos no se borran, pueden haber dos imagenes con el mismo círculo
                print('find', faces.shape[0], 'faces')
                for i in range(faces.shape[0]):
                    face = faces[i]
                    box = face[0:4].astype(np.int)
                    mask = face[5]
                    print(i, box, mask)
                    if mask >= mask_thresh:
                        color = (0, 0, 255)
                    else:
                        color = (0, 255, 0)
                    cv2.rectangle(tempImg, (box[0], box[1]), (box[2], box[3]), color, 2)
                    landmark5 = landmarks[i].astype(np.int)
                    for l in range(landmark5.shape[0]): # Los cinco círculos azules
                        color = (255, 0, 0)
                        cv2.circle(tempImg, (landmark5[l][0], landmark5[l][1]), 1, color, 2)
                cv2.imwrite(path + "Salida_frame_" + timeFile + "_result_" + str(j) + ".jpg", tempImg)
                print("Image ready: "  + path + "Salida_frame_" + timeFile + "_result_" + str(j) + ".jpg")
            j += 1
    fileBody.close()