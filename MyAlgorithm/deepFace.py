from deepface import DeepFace
import glob

path="/content/gdrive/My Drive/TFG/data/Bodies/"
#path="/Users/ignacio/TFG/TFG/data/Faces/"

for pathPng1 in sorted(glob.glob(path + "*.jpg")):
    for pathPng2 in sorted(glob.glob(path + "*.jpg")):
        result  = DeepFace.verify(pathPng1, pathPng2)
        print("JPG_1 " + pathPng1  + " JPG_2 " +  pathPng2 +  "===> " + str(result["verified"]))