import torch
from util.FeatureExtractor import FeatureExtractor
from torchvision import transforms
import models
from scipy.spatial.distance import cosine, euclidean
from  util.utils import *
from sklearn.preprocessing import normalize
import argparse
import numpy as np

params = None

def parse_arguments():
    parser = argparse.ArgumentParser(description='AlignedReId script')
    parser.add_argument('-path', '-p' ,default="/content/gdrive/My Drive/TFG/data/Reidentification", help='Path to apply AlignedReId')
    parser.add_argument('-vector', '-v', action='store_true')
    parser.add_argument('-rank1', '-r1', action='store_true')
    parser.add_argument('-dist', '-d', action='store_true')
    args = parser.parse_args()
    return args


# -r1 -p "/Users/ignacio/TFG/TFG/data/Reidentification"
def rank1AlignedReId():
    numeradorAlignRank1 = 0
    numeradorOriginRank1 = 0
    denominadorRank1 = 0
    for dirpath1, dirnames1, filenames1 in os.walk(params.path):
        filenames1 = [f for f in filenames1 if not f[0] == '.' and f[-23:] == 'AlignedReIdDistance.txt']
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
            #print(file1)
            #print("positionMinValue " + str(positionMinValueAlignRank1List))
            if(id1 == id2List[positionMinValueAlignRank1List]):
                numeradorAlignRank1+=1
                #print("numeradorRank1 " + str(numeradorAlignRank1))
            if(id1 == id2List[positionMinValueOriginRank1List]):
                numeradorOriginRank1+=1
            denominadorRank1+=1
    rank1Align = numeradorAlignRank1/denominadorRank1
    rank1Origin = numeradorOriginRank1/denominadorRank1
    print("========= RANK1 =============")
    print("Aligned " + str(rank1Align))
    print("Original " + str(rank1Origin))


def pool2d(tensor, type= 'max'):
    sz = tensor.size()
    if type == 'max':
        x = torch.nn.functional.max_pool2d(tensor, kernel_size=((int(sz[2]/8)), sz[3]))
    if type == 'mean':
        x = torch.nn.functional.mean_pool2d(tensor, kernel_size=((int(sz[2]/8)), sz[3]))
    x = x[0].cpu().data.numpy()
    x = np.transpose(x,(2,1,0))[0]
    return x


def alignedReIdVector():
    os.environ['CUDA_VISIBLE_DEVICES'] = "0"
    use_gpu = torch.cuda.is_available()
    model = models.init_model(name='resnet50', num_classes=1041, loss={'softmax', 'metric'}, use_gpu=use_gpu,aligned=True)
    checkpoint = torch.load("/content/gdrive/My Drive/TFG/AlignedReID/data/MSMT17_Resnet50_Alignedreid_LS.tar", encoding = "ISO-8859-1", )
    model.load_state_dict(checkpoint['state_dict'])
    img_transform = transforms.Compose([
        transforms.Resize((256, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    exact_list = ['7']
    myexactor = FeatureExtractor(model, exact_list)
    for dirpath, dirnames, filenames in os.walk(params.path):
        filenames = [f for f in filenames if not f[0] == '.' and f[-8:] == 'body.png']
        for file in sorted(filenames):
            pathWithOutBaseName, id = os.path.split(dirpath)
            timeFile = file[0: 12]
            pathImage = dirpath + "/" + timeFile + "_" + id + "_body.png"
            print(pathImage)
            img1 = read_image(pathImage)
            img1 = img_to_tensor(img1, img_transform)
            if use_gpu:
                model = model.cuda()
                img1 = img1.cuda()
            model.eval()
            f1 = myexactor(img1)
            a1 = normalize(pool2d(f1[0], type='max'))
            np.savez(dirpath + "/" + timeFile + "_" + id + "_" + "AlignedReId",a1[0],a1[1],a1[2],a1[3],a1[4],a1[5],a1[6],a1[7])


def calculateAlignedAndOriginalDistance(dist):
    d, D, sp = dtw(dist)
    origin_dist = np.mean(np.diag(dist))
    return str(d), str(origin_dist)


def distanceAlignedReIdVector():
    for dirpath1, dirnames1, filenames1 in os.walk(params.path):
        filenames1 = [f for f in filenames1 if not f[0] == '.' and f[-15:] == 'AlignedReId.npz']
        for file1 in sorted(filenames1):
            pathWithOutBaseName1, id1 = os.path.split(dirpath1)
            x, place1 = os.path.split(pathWithOutBaseName1)
            timeFile1 = file1[0: 12]
            arrays1 = np.load(dirpath1 + "/" + timeFile1 + "_" + id1 +  "_AlignedReId.npz")
            fileOutput = open(dirpath1 + "/" + timeFile1 + "_" + id1 + "_AlignedReIdDistance.txt", "w")
            for dirpath2, dirnames2, filenames2 in os.walk(params.path):
                filenames2 = [f for f in filenames2 if not f[0] == '.' and f[-15:] == 'AlignedReId.npz']
                for file2 in sorted(filenames2):
                    pathWithOutBaseName2, id2 = os.path.split(dirpath2)
                    y, place2 = os.path.split(pathWithOutBaseName2)
                    timeFile2 = file2[0: 12]
                    if place1 != place2:
                        arrays2 = np.load(dirpath2 + "/" + timeFile2 + "_" + id2 + "_AlignedReId.npz")
                        print(dirpath1 + "/" + file1 + " ===> " + dirpath2 + "/" + file2 + " ===> " )
                        dist = np.zeros((8, 8))
                        for i in range(8):
                            temp_feat1 = arrays1["arr_" + str(i)]
                            for j in range(8):
                                temp_feat2 = arrays2["arr_" + str(j)]
                                dist[i][j] = euclidean(temp_feat1, temp_feat2)
                        alignDistance, originalDistance = calculateAlignedAndOriginalDistance(dist)
                        fileOutput.write(place1 + " " + timeFile1 + " " + id1 + " " + place2 + " " + timeFile2 + " " + id2 + " " +  alignDistance + " " +  originalDistance + " \n")

if __name__ == '__main__':
    params = parse_arguments()
    if params.vector:
        alignedReIdVector()
    if params.dist:
        distanceAlignedReIdVector()
    if params.rank1:
        rank1AlignedReId()


