import face_model
import argparse
import cv2
import sys
import numpy as np

parser = argparse.ArgumentParser(description='face model test')
# general
parser.add_argument('--image-size', default='112,112', help='')
parser.add_argument('--model', default='/content/gdrive/My Drive/TFG/insightface/models/model-r100-ii/model, 0', help='path to load model.')
parser.add_argument('--gpu', default=0, type=int, help='gpu id')
args = parser.parse_args()

vec = args.model.split(',')
model_prefix = vec[0]
model_epoch = int(vec[1])
model = face_model.FaceModel(args.gpu, model_prefix, model_epoch)
#img = cv2.imread('/content/gdrive/My Drive/TFG/insightface/deploy/yo1.jpeg')
img = cv2.imread('/content/gdrive/My Drive/TFG/insightface/deploy/shakira1.jpeg')
img = cv2.resize(img, (112,112), interpolation=cv2.INTER_LINEAR)
img = model.get_input(img)
f1 = model.get_feature(img)
#img2 = cv2.imread('/content/gdrive/My Drive/TFG/insightface/deploy/yo2.jpeg')
img2 = cv2.imread('/content/gdrive/My Drive/TFG/insightface/deploy/shakira2.jpeg')
img2 = cv2.resize(img2, (112,112), interpolation=cv2.INTER_LINEAR)
f2 = model.get_feature(img2)
sim = np.dot(f2, f1)
print(model_prefix)
print(sim)
assert(sim>=0.99 and sim<1.01)

