import cv2
import numpy as np
import scipy
from scipy.misc import imread
import pickle
import random
import os
import matplotlib.pyplot as plt


# Feature extractor
def extract_features(image_path, vector_size=24):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = image[0:300, 0:300]
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        alg = cv2.KAZE_create()
        # Dinding image keypoints
        kps = alg.detect(image)
        # Getting first 32 of them. 
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        kps, dsc = alg.compute(image, kps)
        # Flatten all of them in one big vector - our feature vector
        dsc = dsc.flatten()
        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print('Error: ', e)
        return None

    return dsc


def batch_extractor(images_path, pickled_db_path="features.pck"):
    files = []

    folders = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    for subfolder in folders:
        files += [os.path.join(subfolder, p) for p in sorted(os.listdir(subfolder))]

    result = {}
    i = 1
    for f in files:
        # print('Extracting features from image %s' % f)
        print(str(100*i/len(files))[:5]+'%')
        i += 1
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)
    
    # saving all our feature vectors in pickled file
    with open(pickled_db_path, 'wb') as fp:
        pickle.dump(result, fp)


class Matcher(object):

    def __init__(self, pickled_db_path="features.pck"):
        with open(pickled_db_path, "rb") as fp:
            self.data = pickle.load(fp)
        self.names = []
        self.matrix = []
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    def cos_cdist(self, vector):
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        # print(self.matrix)

        cos_distances = np.array([])

        for vec in self.matrix:
            # print(len(vec))
            cosdis = np.dot(v, vec) / (np.linalg.norm(vec) * np.linalg.norm(vec))
            cos_distances = np.append(cos_distances, (1-cosdis))

        return cos_distances

    def euc_dist(self, vector):
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        # print(self.matrix)

        euc_distances = np.array([])

        for vec in self.matrix:
            # print(len(vec))
            edis = np.linalg.norm(v-vec)
            euc_distances = np.append(euc_distances, (edis))
            
        return euc_distances

    def match(self, image_path, topn=5):
        features = extract_features(image_path)
        img_distances = self.cos_cdist(features)
        img_distances = self.euc_dist(features)
        # getting top 5 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()

def show_img(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    img = img[0:300, 0:300]
    cv2.imshow(path,img)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # plt.imshow(img)
    # plt.show()

def pic_name(path):
    return path.split('\\')[0].split('/')[-1][5:]

def run():
    images_path = 'resources/PINS/'

    files = []

    folders = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    for subfolder in folders:
        files += [os.path.join(subfolder, p) for p in sorted(os.listdir(subfolder))]
    # files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    # getting 3 random images 
    sample = random.sample(files, 1)
    # sample = ['resources/saya.jpg'];
    
    batch_extractor(images_path)

    # print(sample)
    
    ma = Matcher('features.pck')
    
    for s in sample:
        print()
        # print('Query image ==========================================')
        show_img(s)
        names, match = ma.match(s, topn=2)
        print(pic_name(s).lower())
        # print('Result images ========================================')
        for i in range(1,2):
            # we got cosine distance, less cosine distance between vectors
            # more they similar, thus we subtruct it from 1 to get match value
            # print(i)
            # if(os.path.join(images_path, names[i]) == 'resources/images/saya2.jpg'):
            print('Match %s' % (1-match[i]))
            print(pic_name(os.path.join(images_path, names[i])).lower())
            show_img(os.path.join(images_path, names[i]))
                # break;    

    
run()