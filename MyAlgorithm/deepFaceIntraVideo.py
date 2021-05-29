from deepface import DeepFace
import glob

path="/content/gdrive/My Drive/TFG/data/Bodies/"
#path="/Users/ignacio/TFG/TFG/data/Faces/"

for pathPng1 in sorted(glob.glob(path + "*.png")):
    for pathPng2 in sorted(glob.glob(path + "*.png")):
        result  = DeepFace.verify(pathPng1, pathPng2, model_name ="Facenet", enforce_detection = False)
        print("png_1 " + pathPng1 + " png_2 " + pathPng2 + "===> " + str(result["distance"]))