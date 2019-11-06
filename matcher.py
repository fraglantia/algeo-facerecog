import cv2
import numpy as np
import scipy
from matplotlib.pyplot import imread
# from scipy.misc import imread
from tkinter import *
from PIL import ImageTk, Image
import pickle
import random
import os
import matplotlib.pyplot as plt


def extract_features(image_path, vector_size=24):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # crop img 300x300
    image = image[0:300, 0:300]

    alg = cv2.KAZE_create()
    # keypoints
    keypoints = alg.detect(image)
    keypoints = sorted(keypoints, key=lambda x: -x.response)[:vector_size]
    keypoints, dsc = alg.compute(image, keypoints)
    dsc = dsc.flatten()

    needed_size = (vector_size * 64)
    if dsc.size < needed_size:
        # if vectornya kurang besar (keypoints detectednya sedikit, fill w/ 0's)
        dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])

    return dsc


def batch_extractor(images_path, pickled_db_path="features.pck"):
    files = []

    folders = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    for subfolder in folders:
        files += [os.path.join(subfolder, p) for p in sorted(os.listdir(subfolder))]

    result = {}
    i = 1
    for f in files:
        print(str(100*i/len(files))[:5]+'%')
        i += 1
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)

    # simpan data hasil ekstraksi ke file pickle external
    with open(pickled_db_path, 'wb') as fp:
        pickle.dump(result, fp)

def show_img(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    img = img[0:300, 0:300]
    cv2.imshow(path,img)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # plt.imshow(img)
    # plt.show()

def cosdist(v1, v2):
    dotpro = np.sum(np.multiply(v1,v2))

    norm1 = np.sum(np.square(v1))
    norm1 = np.sqrt(norm1)

    norm2 = np.sum(np.square(v2))
    norm2 = np.sqrt(norm2)

    cosdis = 1-dotpro/(norm1*norm2)

    return cosdis

def eucdist(v1, v2):
    # v1 = [(x1-y1)^2, (x2-y2)^2, (x3-y3)^2, (x4-y4)^2]
    v1 = np.square(np.subtract(v2,v1))
    edis = np.sum(v1)
    edis = np.sqrt(edis)

    return edis


def load_database(pickled_db_path="features.pck"):
    with open(pickled_db_path, "rb") as fp:
        data = pickle.load(fp)
    # return a dictionary
    return data.items()

def matching(imgpath, db, cosine=True, top=5):
    imgvec = extract_features(imgpath)
    tuplearr = []

    for k, v in db:
        if(cosine):
            dist = cosdist(imgvec, v)
        else:
            dist = eucdist(imgvec, v)

        tuplearr.append((k,dist))

    return sorted(tuplearr, key=lambda x: x[1])[:top]


def pic_name(path):
    return path.split('\\')[0].split('/')[-1][5:]


# UNCOMMENT kalo mau buat db baru
# batch_extractor('resources/REF/')