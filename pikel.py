import cv2
import numpy as np
import scipy
from scipy.misc import imread
import pickle
import random
import os
import matplotlib.pyplot as plt


def load_database(pickled_db_path="features.pck"):
    with open(pickled_db_path, "rb") as fp:
        data = pickle.load(fp)
    return data


db = load_database()
for k,v in db.items():
	print(k)
	break
