import torch
from util.FeatureExtractor import FeatureExtractor
from torchvision import transforms
import models
from scipy.spatial.distance import cosine, euclidean
from util.utils import *
from sklearn.preprocessing import normalize
import argparse
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve, auc
from pathlib import Path

params = None


def parse_arguments():
    parser = argparse.ArgumentParser(description='AlignedReId script')
    parser.add_argument('-path', '-p', default="/content/gdrive/My Drive/TFG/data/Reidentification",
                        help='Path to apply AlignedReId')
    parser.add_argument('-vector', '-v', action='store_true')
    parser.add_argument('-rank1', '-r1', action='store_true')
    parser.add_argument('-dist', '-d', action='store_true')
    parser.add_argument('-averagePrecision', '-ap', action='store_true')
    args = parser.parse_args()
    return args


def getParameterAveragePrecision(dirpath1, file1):
    gallery_coincidences = []
    distQueryGalleryAlign = []
    distanceQueryGalleryOriginal = []
    print(dirpath1 + "/" + file1)
    fileOutput = open(dirpath1 + "/" + file1)
    for line in fileOutput:
        if line.split(" ")[2] == line.split(" ")[5]:
            gallery_coincidences.append(1)
        else:
            gallery_coincidences.append(0)
        distQueryGalleryAlign.append(float(line.split(" ")[6]))
        distanceQueryGalleryOriginal.append(float(line.split(" ")[7]))
    similarityQueryGalleryAlign = 1 - distQueryGalleryAlign / np.amax(distQueryGalleryAlign)
    similarityQueryGalleryOriginal = 1 - distanceQueryGalleryOriginal / np.amax(distanceQueryGalleryOriginal)
    return gallery_coincidences, similarityQueryGalleryAlign, similarityQueryGalleryOriginal


def averagePrecisionAlignedReId():
    model_names = ["Cuhk03_Resnet50", "DukeMTMCReID_Resnet50", "Market1501_Resnet50"]
    for model in model_names:
        allAPAlign = []
        allAPOriginal = []
        for dirpath1, dirnames1, filenames1 in os.walk(params.path):
            filenames1 = [f for f in filenames1 if
                          not f[0] == '.' and f[-23:] == 'AlignedReIdDistance.txt' and f.split("_")[5] ==
                          model.split("_")[0]]
            for file1 in sorted(filenames1):
                gallery_coincidences, similarityQueryGalleryAlign, similarityQueryGalleryOriginal = getParameterAveragePrecision(
                    dirpath1, file1)
                apAlign = average_precision_score(gallery_coincidences, similarityQueryGalleryAlign, average='macro',
                                                  pos_label=1)
                apOriginal = average_precision_score(gallery_coincidences, similarityQueryGalleryOriginal,
                                                     average='macro', pos_label=1)
                if str(apAlign) == "nan" or str(apOriginal) == "nan":
                    print("Existen nan: " + dirpath1 + "/" + file1)
                else:
                    allAPAlign.append(apAlign)
                    allAPOriginal.append(apOriginal)
        mAPAlign = np.mean(allAPAlign)
        mAPOriginal = np.mean(allAPOriginal)
        print("============ mAP " + model + " ====================")
        print("mAP Align " + str(mAPAlign))
        print("mAP Original " + str(mAPOriginal))
        print("===================================================")


# -r1 -p "/Users/ignacio/TFG/TFG/data/Reidentification"
def rank1AlignedReId():
    model_names = ["Cuhk03_Resnet50", "DukeMTMCReID_Resnet50", "Market1501_Resnet50"]
    for modelName in model_names:
        print("======= " + modelName + " ==========")
        numeradorAlignRank1 = 0
        numeradorOriginRank1 = 0
        denominadorRank1 = 0
        for dirpath1, dirnames1, filenames1 in os.walk(params.path):
            filenames1 = [f for f in filenames1 if
                          not f[0] == '.' and f[-23:] == 'AlignedReIdDistance.txt' and f.split("_")[5] ==
                          modelName.split("_")[0]]
            for file1 in sorted(filenames1):
                distAlignList = []
                distOriginList = []
                id2List = []
                fileOutput = open(dirpath1 + "/" + file1)
                id1 = file1.split("_")[4]
                for line in fileOutput:
                    id2List.append(line.split(" ")[5])
                    distAlignList.append(line.split(" ")[6])
                    distOriginList.append(line.split(" ")[7])
                positionMinValueAlignRank1List = distAlignList.index(min(distAlignList))
                positionMinValueOriginRank1List = distOriginList.index(min(distOriginList))
                if (id1 == id2List[positionMinValueAlignRank1List]):
                    numeradorAlignRank1 += 1
                if (id1 == id2List[positionMinValueOriginRank1List]):
                    numeradorOriginRank1 += 1
                denominadorRank1 += 1
        rank1Align = numeradorAlignRank1 / denominadorRank1
        rank1Origin = numeradorOriginRank1 / denominadorRank1
        print("========= RANK1 " + modelName + " =============")
        print("Aligned " + str(rank1Align))
        print("Original " + str(rank1Origin))


def pool2d(tensor, type='max'):
    sz = tensor.size()
    if type == 'max':
        x = torch.nn.functional.max_pool2d(tensor, kernel_size=((int(sz[2] / 8)), sz[3]))
    if type == 'mean':
        x = torch.nn.functional.mean_pool2d(tensor, kernel_size=((int(sz[2] / 8)), sz[3]))
    x = x[0].cpu().data.numpy()
    x = np.transpose(x, (2, 1, 0))[0]
    return x


def alignedReIdVector():
    pathModel = "/content/gdrive/My Drive/TFG/AlignedReID/data/"
    model_names = ["Cuhk03_Resnet50", "DukeMTMCReID_Resnet50", "Market1501_Resnet50"]
    num_classes_models = [767, 702, 751]
    for modelName, num_classes in zip(model_names, num_classes_models):
        print("======= " + modelName + " ==========")
        os.environ['CUDA_VISIBLE_DEVICES'] = "0"
        use_gpu = torch.cuda.is_available()
        model = models.init_model(name='resnet50', num_classes=num_classes, loss={'softmax', 'metric'}, use_gpu=use_gpu,
                                  aligned=True)
        checkpoint = torch.load(pathModel + modelName + ".tar", encoding="ISO-8859-1", )
        model.load_state_dict(checkpoint['state_dict'])
        img_transform = transforms.Compose([
            transforms.Resize((256, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        exact_list = ['7']
        myexactor = FeatureExtractor(model, exact_list)
        for dirpath, dirnames, filenames in os.walk(params.path):
            filenames = [f for f in filenames if not f[0] == '.' and f[-8:] == 'body.jpg']
            for file in sorted(filenames):
                pathWithOutBaseName, id = os.path.split(dirpath)
                timeFile = file[0: 12]
                fileObj = Path(dirpath + "/" + timeFile + "_" + id + "_" + modelName + "_deepFaceVector.npy")
                if not fileObj.exists():
                    pathImage = dirpath + "/" + timeFile + "_" + id + "_body.jpg"
                    print(pathImage)
                    img1 = read_image(pathImage)
                    img1 = img_to_tensor(img1, img_transform)
                    if use_gpu:
                        model = model.cuda()
                        img1 = img1.cuda()
                    model.eval()
                    f1 = myexactor(img1)
                    a1 = normalize(pool2d(f1[0], type='max'))
                    np.savez(dirpath + "/" + timeFile + "_" + id + "_" + modelName + "_AlignedReId", a1[0], a1[1],
                             a1[2], a1[3], a1[4], a1[5], a1[6], a1[7])
                else:
                    print("Existe " + dirpath + "/" + timeFile + "_" + id + "_" + modelName + "_AlignedReId.npz")


def calculateAlignedAndOriginalDistance(dist):
    d, D, sp = dtw(dist)
    origin_dist = np.mean(np.diag(dist))
    return str(d), str(origin_dist)


def distanceAlignedReIdVector():
    model_names = ["Cuhk03_Resnet50", "DukeMTMCReID_Resnet50", "Market1501_Resnet50"]
    for modelName in model_names:
        print("======= " + modelName + " ==========")
        for dirpath1, dirnames1, filenames1 in os.walk(params.path):
            filenames1 = [f for f in filenames1 if
                          not f[0] == '.' and f[-15:] == 'AlignedReId.npz' and f.split("_")[5] == modelName.split("_")[
                              0]]
            for file1 in sorted(filenames1):
                pathWithOutBaseName1, id1 = os.path.split(dirpath1)
                x, place1 = os.path.split(pathWithOutBaseName1)
                timeFile1 = file1[0: 12]
                fileObj = Path(dirpath1 + "/" + timeFile1 + "_" + id1 + "_" + modelName + "_AlignedReIdDistance.txt")
                if not fileObj.exists():
                    arrays1 = np.load(dirpath1 + "/" + timeFile1 + "_" + id1 + "_" + modelName + "_AlignedReId.npz")
                    fileOutput = open(
                        dirpath1 + "/" + timeFile1 + "_" + id1 + "_" + modelName + "_AlignedReIdDistance.txt", "w")
                    for dirpath2, dirnames2, filenames2 in os.walk(params.path):
                        filenames2 = [f for f in filenames2 if
                                      not f[0] == '.' and f[-15:] == 'AlignedReId.npz' and f.split("_")[5] ==
                                      modelName.split("_")[0]]
                        for file2 in sorted(filenames2):
                            pathWithOutBaseName2, id2 = os.path.split(dirpath2)
                            y, place2 = os.path.split(pathWithOutBaseName2)
                            timeFile2 = file2[0: 12]
                            if place1 != place2:
                                arrays2 = np.load(
                                    dirpath2 + "/" + timeFile2 + "_" + id2 + "_" + modelName + "_AlignedReId.npz")
                                print(dirpath1 + "/" + file1 + " ===> " + dirpath2 + "/" + file2 + " ===> ")
                                dist = np.zeros((8, 8))
                                for i in range(8):
                                    temp_feat1 = arrays1["arr_" + str(i)]
                                    for j in range(8):
                                        temp_feat2 = arrays2["arr_" + str(j)]
                                        dist[i][j] = euclidean(temp_feat1, temp_feat2)
                                alignDistance, originalDistance = calculateAlignedAndOriginalDistance(dist)
                                fileOutput.write(
                                    place1 + " " + timeFile1 + " " + id1 + " " + place2 + " " + timeFile2 + " " + id2 + " " + alignDistance + " " + originalDistance + " \n")
                else:
                    print(
                        "Existe " + dirpath1 + "/" + timeFile1 + "_" + id1 + "_" + modelName + "_AlignedReIdDistance.txt")


if __name__ == '__main__':
    params = parse_arguments()
    if params.vector:
        alignedReIdVector()
    if params.dist:
        distanceAlignedReIdVector()
    if params.rank1:
        rank1AlignedReId()
    if params.averagePrecision:
        averagePrecisionAlignedReId()

