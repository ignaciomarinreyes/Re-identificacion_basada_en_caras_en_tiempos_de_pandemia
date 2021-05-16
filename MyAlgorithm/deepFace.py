from deepface import DeepFace

result  = DeepFace.verify(path + "img1.jpg", path + "img2.jpg")
print("Is verified: ", result["verified"])