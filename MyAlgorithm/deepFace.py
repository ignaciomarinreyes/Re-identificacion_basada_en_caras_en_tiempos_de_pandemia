from deepface import DeepFace

path="/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba/"

result  = DeepFace.verify(path + "img1.jpg", path + "img2.jpg")
print("Is verified: ", result["verified"])