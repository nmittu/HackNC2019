from cv2 import *
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import pickle
import os

NUM_CLUSTERS = 10

def getColor(img):
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    img = img.resize((300, 300))
    ar = np.asarray(img)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))

    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    color = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    rgbstr = "%s" % color
    return tuple(int(rgbstr[i:i+2], 16) for i in (0, 2, 4))

images = {}

for filename in os.listdir("DIV2K_train_HR"):
    image = cv2.imread("DIV2K_train_HR/%s" % filename)
    color = getColor(image)

    images[color] = filename
    print(color, filename)

with open("img-colors.pkl", "wb") as f:
    pickle.dump(images, f)
