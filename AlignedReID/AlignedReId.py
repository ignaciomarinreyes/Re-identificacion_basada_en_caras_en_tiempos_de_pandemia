import torch
from util.FeatureExtractor import FeatureExtractor
from torchvision import transforms
from IPython import embed
import models
from scipy.spatial.distance import cosine, euclidean
from  util.utils import *
from sklearn.preprocessing import normalize
import argparse

params = None

def parse_arguments():
    parser = argparse.ArgumentParser(description='AlignedReId script')
    parser.add_argument('-path', '-p' ,default="/content/gdrive/My Drive/TFG/data/Reidentification", help='Path to apply AlignedReId')
    parser.add_argument('-vector', '-v', action='store_true')
    parser.add_argument('-rank1', '-r1', action='store_true')
    parser.add_argument('-dist', '-d', action='store_true')
    parser.add_argument('-euclidean', '-e', action='store_true')
    args = parser.parse_args()
    return args


def pool2d(tensor, type= 'max'):
    sz = tensor.size()
    if type == 'max':
        x = torch.nn.functional.max_pool2d(tensor, kernel_size=((int(sz[2]/8)), sz[3]))
    if type == 'mean':
        x = torch.nn.functional.mean_pool2d(tensor, kernel_size=((int(sz[2]/8)), sz[3]))
    x = x[0].cpu().data.numpy()
    x = np.transpose(x,(2,1,0))[0]
    return x


def getVectorAlignedReId(pathPng, use_gpu, myexactor, model, img_transform):
    img = read_image(pathPng)
    img = img_to_tensor(img, img_transform)
    if use_gpu:
        model = model.cuda()
        img = img.cuda()
    model.eval()
    f1 = myexactor(img)
    return f1[0] # Usar poold2d ??


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
        filenames = [f for f in filenames if not f[0] == '.']
        for file in sorted(filenames):
            pathWithOutBaseName, id = os.path.split(dirpath)
            timeFile = file[0: 12]
            print(dirpath + "/" + timeFile + "_" + id + "_body.png")
            f1 = getVectorAlignedReId(dirpath + "/" + timeFile + "_" + id + "_body.png", use_gpu, myexactor, model, img_transform)
            fileOutput = open(dirpath + "/" + timeFile + "_" + id + "_" + "AlignedReId.txt", "w")
            for value in f1:
                fileOutput.write(str(value) + "\n")

def calculateAlignedDistAndOriginalDist(dist):
    d, D, sp = dtw(dist)
    origin_dist = np.mean(np.diag(dist))
    print("Aligned distance:" + str(d))
    print("Original distance:" + str(origin_dist))


def alignedReIdVectorDist():
    for dirpath1, dirnames1, filenames1 in os.walk(params.path):
        filenames1 = [f for f in filenames1 if not f[0] == '.']
        for file1 in sorted(filenames1):
            pathWithOutBaseName1, id1 = os.path.split(dirpath1)
            x, place1 = os.path.split(pathWithOutBaseName1)
            fileAlignedReId1 = open(dirpath1 + "/" + file1)
            vAlignedReId1 = []
            for line1 in fileAlignedReId1:
                vAlignedReId1.append(line1)
            for dirpath2, dirnames2, filenames2 in os.walk(params.path):
                filenames2 = [f for f in filenames2 if not f[0] == '.']
                for file2 in sorted(filenames2):
                    pathWithOutBaseName2, id2 = os.path.split(dirpath2)
                    y, place2 = os.path.split(pathWithOutBaseName2)
                    if place1 != place2:
                        print(dirpath1 + "/" + file1 + " ===> " + dirpath2 + "/" + file2 + " ===> " )
                        fileAlignedReId2 = open(dirpath2 + "/" + file2)
                        vAlignedReId2 = []
                        for line2 in fileAlignedReId2:
                            vAlignedReId2.append(line2)
                        if params.euclidean:
                            dist = compute_dist(vAlignedReId1, vAlignedReId2, type='euclidean')
                        if params.dist:
                            calculateAlignedDistAndOriginalDist(dist)
                        if params.rank1:
                            print("CONSTRUCCION")


if __name__ == '__main__':
    params = parse_arguments()
    if params.vector:
        alignedReIdVector()
    if params.dist or params.rank1:
        alignedReIdVectorDist()


