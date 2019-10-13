import serial
from tkinter import *
from cv2 import *
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster

useWebCam = True
NUM_CLUSTERS = 5

with serial.Serial('COM3') as ser:
    root = Tk()

    def setColor():
        rgb = [int(x) for x in ser.readline().decode('utf8').strip().split(',')]
        rgbstr = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

        if useWebCam:
            cam = VideoCapture(0)
            s, img = cam.read()
            if s:
                img = Image.fromarray(img)
                img = img.resize((150, 150))
                ar = np.asarray(img)
                shape = ar.shape
                ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

                codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

                vecs, dist = scipy.cluster.vq.vq(ar, codes)
                counts, bins = scipy.histogram(vecs, len(codes))

                index_max = scipy.argmax(counts)
                peak = codes[int_max]
                color = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
                rgbstr = "$%s" % color

        root.configure(background=rgbstr)
        root.after(10, setColor)

    root.after(10, setColor)
    root.mainloop()
        