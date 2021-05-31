from deepface import DeepFace
import argparse
import glob
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
import numpy as np
from tqdm import tqdm
from deepface.basemodels import VGGFace, OpenFace, Facenet, FbDeepFace, DeepID, DlibWrapper, ArcFace, Boosting
from deepface.commons import functions, realtime, distance as dst


params = None

def parse_arguments():
    parser = argparse.ArgumentParser(description='DeepFace script')
    parser.add_argument('-path', '-p' ,default="/content/gdrive/My Drive/TFG/data/Reidentification", help='Path to apply DeepFace')
    parser.add_argument('-inter', '-ie', action='store_true')
    parser.add_argument('-intra', '-ir', action='store_true')
    parser.add_argument('-vector', '-v', action='store_true')
    args = parser.parse_args()
    return args

def verifyVectorFeature(vImage1, vImage2, img1_path, img2_path, model_name = 'VGG-Face', distance_metric = 'cosine', model = None, enforce_detection = True, detector_backend = 'mtcnn', align = True):
	tic = time.time()
	img_list, bulkProcess = functions.initialize_input(img1_path, img2_path)
	functions.initialize_detector(detector_backend = detector_backend)
	resp_objects = []
	#--------------------------------
	if model_name == 'Ensemble':
		model_names = ["VGG-Face", "Facenet", "OpenFace", "DeepFace"]
		metrics = ["cosine", "euclidean", "euclidean_l2"]
	else:
		model_names = []; metrics = []
		model_names.append(model_name)
		metrics.append(distance_metric)
	#--------------------------------
	if model == None:
		if model_name == 'Ensemble':
			models = Boosting.loadModel()
		else:
			model = DeepFace.build_model(model_name)
			models = {}
			models[model_name] = model
	else:
		if model_name == 'Ensemble':
			Boosting.validate_model(model)
			models = model.copy()
		else:
			models = {}
			models[model_name] = model
	#------------------------------
	#calling deepface in a for loop causes lots of progress bars. this prevents it.
	disable_option = False if len(img_list) > 1 else True
	pbar = tqdm(range(0,len(img_list)), desc='Verification', disable = disable_option)
	for index in pbar:
		instance = img_list[index]
		if type(instance) == list and len(instance) >= 2:
			img1_path = instance[0]; img2_path = instance[1]
			ensemble_features = []
			for i in  model_names:
				custom_model = models[i]
				#img_path, model_name = 'VGG-Face', model = None, enforce_detection = True, detector_backend = 'mtcnn'
				img1_representation = vImage1
				img2_representation = vImage2
				#----------------------
				#find distances between embeddings
				for j in metrics:
					if j == 'cosine':
						distance = dst.findCosineDistance(img1_representation, img2_representation)
					elif j == 'euclidean':
						distance = dst.findEuclideanDistance(img1_representation, img2_representation)
					elif j == 'euclidean_l2':
						distance = dst.findEuclideanDistance(dst.l2_normalize(img1_representation), dst.l2_normalize(img2_representation))
					else:
						raise ValueError("Invalid distance_metric passed - ", distance_metric)
					distance = np.float64(distance) #causes trobule for euclideans in api calls if this is not set (issue #175)
					#----------------------
					#decision
					if model_name != 'Ensemble':
						threshold = dst.findThreshold(i, j)
						if distance <= threshold:
							identified = True
						else:
							identified = False
						resp_obj = {
							"verified": identified
							, "distance": distance
							, "max_threshold_to_verify": threshold
							, "model": model_name
							, "similarity_metric": distance_metric
						}
						if bulkProcess == True:
							resp_objects.append(resp_obj)
						else:
							return resp_obj
					else: #Ensemble
						#this returns same with OpenFace - euclidean_l2
						if i == 'OpenFace' and j == 'euclidean':
							continue
						else:
							ensemble_features.append(distance)
			#----------------------
			if model_name == 'Ensemble':
				boosted_tree = Boosting.build_gbm()
				prediction = boosted_tree.predict(np.expand_dims(np.array(ensemble_features), axis=0))[0]
				verified = np.argmax(prediction) == 1
				score = prediction[np.argmax(prediction)]
				resp_obj = {
					"verified": verified
					, "score": score
					, "distance": ensemble_features
					, "model": ["VGG-Face", "Facenet", "OpenFace", "DeepFace"]
					, "similarity_metric": ["cosine", "euclidean", "euclidean_l2"]
				}
				if bulkProcess == True:
					resp_objects.append(resp_obj)
				else:
					return resp_obj
		else:
			raise ValueError("Invalid arguments passed to verify function: ", instance)
	toc = time.time()
	if bulkProcess == True:
		resp_obj = {}
		for i in range(0, len(resp_objects)):
			resp_item = resp_objects[i]
			resp_obj["pair_%d" % (i+1)] = resp_item
		return resp_obj


def deepFaceInterVideo():
    for dirpath1, dirnames1, filenames1 in os.walk(params.path):
        filenames1 = [f for f in filenames1 if not f[0] == '.' and f[-18:] == 'deepFaceVector.txt']
        for file1 in sorted(filenames1):
            pathWithOutBaseName1, id1 = os.path.split(dirpath1)
            x, place1 = os.path.split(pathWithOutBaseName1)
            timeFile1 = file1[0: 12]
            vectorFeature1 = []
            fileOutput1 = open(dirpath1 + "/" + timeFile1 + "_" + id1 + "_" + "deepFaceVector.txt")
            for line1 in fileOutput1:
                vectorFeature1.append(float(line1))
            fileOutput = open(dirpath1 + "/" + timeFile1 + "_" + id1 + "_" + "deepFaceInterResult.txt", "w")
            for dirpath2, dirnames2, filenames2 in os.walk(params.path):
                filenames2 = [f for f in filenames2 if not f[0] == '.' and f[-18:] == 'deepFaceVector.txt']
                for file2 in sorted(filenames2):
                    pathWithOutBaseName2, id2 = os.path.split(dirpath2)
                    y, place2 = os.path.split(pathWithOutBaseName2)
                    timeFile2 = file2[0: 12]
                    if place1 != place2:
                        vectorFeature2 = []
                        fileOutput2 = open(dirpath2 + "/" + timeFile2 + "_" + id2 + "_" + "deepFaceVector.txt")
                        for line2 in fileOutput2:
                            vectorFeature2.append(float(line2))
                        print(dirpath1 + "/" + file1 + " ===> " + dirpath2 + "/" + file2 + " ===> " )
                        result = verifyVectorFeature(vectorFeature1, vectorFeature2,dirpath1 + "/" + file1[0:-18] + "body.png",dirpath2 + "/" + file2[0:-18] + "body.png", model_name="Facenet", enforce_detection=False)
                        fileOutput.write(place1 + " " + id1 + " " + place2 + " " + id2 + " " +  str(result["distance"]) + " \n")


def deepFaceIntraVideo():
    for pathPng1 in sorted(glob.glob(params.path + "*.png")):
        for pathPng2 in sorted(glob.glob(params.path + "*.png")):
            result = DeepFace.verify(pathPng1, pathPng2, model_name="Facenet", enforce_detection=False)
            print("png_1 " + pathPng1 + " png_2 " + pathPng2 + "===> " + str(result["distance"]))


def deepFaceVector():
    for dirpath, dirnames, filenames in os.walk(params.path):
        filenames = [f for f in filenames if not f[0] == '.']
        for file in sorted(filenames):
            pathWithOutBaseName, id = os.path.split(dirpath)
            timeFile = file[0: 12]
            print(dirpath + "/" + timeFile + "_" + id + "_body.png")
            try:
                result = DeepFace.represent(dirpath + "/" + timeFile + "_" + id + "_body.png", model_name="Facenet", enforce_detection=False)
            except:
                print("No se puede aplicar algoritmo" + dirpath + "/" + timeFile + "_" + id + "_body.png")
            fileOutput = open(dirpath + "/" + timeFile + "_" + id + "_" + "deepFaceVector.txt", "w")
            for value in result:
                fileOutput.write(str(value) + "\n")



if __name__ == '__main__':
    params = parse_arguments()
    if params.vector:
        deepFaceVector()
    if params.inter:
        deepFaceInterVideo()
    if params.intra:
        deepFaceIntraVideo()