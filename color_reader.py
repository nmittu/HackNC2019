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
import pickle
from PIL import ImageTk as itk

useWebCam = False
NUM_CLUSTERS = 10
cam = VideoCapture(0)

images = None
with open("img-colors.pkl", "rb") as img_file:
    images = pickle.load(img_file)


def distance(c1, c2):
    return sum((c1[x] - c2[x])**2 for x in range(3))

def closest_file(color):
    min = float("inf")
    val = None
    for c2 in images.keys():
        dist = distance(color, c2)
        if dist < min:
            min = dist
            val = c2

    return images[val],val

with serial.Serial('/dev/ttyACM1') as ser:
    root = Tk()
    imgroot = Toplevel(root)
    image = None
    #C = Canvas(imgroot, bg="black", height=2000, width=3000)
    #C.pack()
    imgLabel = Label(imgroot, height=300, width=600)
    imgLabel.pack(side="bottom", fill="both", expand="yes")

    drawpic = True

    def setbackground(image, color):
        if image != None:
            imgLabel.image = Image.open("/DIV2K_train_HR/%s" % image)
            imgLabel.img = itk.PhotoImage(imgLabel.image)
            imgLabel.configure(image = imgLabel.img, background = color)
    
    def setColor():
        global drawpic
        rgb = [int(x) for x in ser.readline().decode('utf8').strip().split(',')]

        if useWebCam:
            s, img = cam.read()
            if s:
                img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                img = img.resize((150, 150))
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
                rgb = tuple(int(rgbstr[i:i+2], 16) for i in (0, 2, 4))


        if drawpic:
            setbackground(closest_file(rgb)[0], '#%02x%02x%02x' % closest_file(rgb)[1])
            drawpic = False
        
        root.configure(background='#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2]))
        root.after(10, setColor)


    def drawnew(_):
        global drawpic
        drawpic = True
        
    root.after(10, setColor)
    root.bind("<space>", drawnew)
    root.mainloop()
        
