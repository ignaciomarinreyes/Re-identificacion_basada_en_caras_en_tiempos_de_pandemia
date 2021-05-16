from deepface import DeepFace
import glob

path="/content/gdrive/My Drive/TFG/data/Bodies/"
#path="/Users/ignacio/TFG/TFG/data/Faces/"

for pathJpg1 in sorted(glob.glob(path + "*.jpg")):
    for pathJpg2 in sorted(glob.glob(path + "*.jpg")):
        result  = DeepFace.verify(pathJpg1, pathJpg2, model_name ="Facenet", enforce_detection = False)
        print("JPG_1 " + pathJpg1 + " JPG_2 " + pathJpg2 + "===> " + str(result["verified"]))