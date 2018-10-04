import sys, random, argparse
import numpy as np
import math as maths
import matplotlib as mpl
from PIL import Image

#70 shades of greyx
#it's way better then 50 shades of them
gscale1 =  "$@B%8&WM#*oahldbpqwmZOoOLCJUYXzcvunxrjft\/|()1{}[]?-_+~<>i!lI;:,\"^."

#10 levels of grey
gscale2 = '@%#*+=-:. '

def getAverage(image):
    #given an image, return the greyscale values of it
    im = np.array(image)

    w,h = im.shape
    return np.average(im.reshape(w*h))

def convertToAscii(filename, cols, scale, moreLevels):
    global gscale1, gscale2

    #gettig the image and findout out the size of it
    image = Image.open(filename).convert('LA')
    W, H = image.size[0], image.size[1]
    print("Das image is of size %d x %d" % (W,H))

    #getting the size of the new image
    w = W/cols
    h = w/scale
    rows = int(H/h)

    #check to make sure that the image is a goof size
    if cols > W or rows > H:
        print("FIX YOUR SHIT, this image is too small for this program")
        exit(0)

    #this is what the ascii image will be stored in
    asciiImg = []

    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        #case when we get to the end of our rows
        if j == rows -1:
            y2 = H

        asciiImg.append("")

        for i in range(cols):
            x1 = int(i*w)
            x2 = int((i+1)*w)

            #case when we get to the end of our cols
            if i == cols-1:
                x2 = W

            #get the value a region of image we be looking at
            img = image.crop((x1,x2,y1,y2))
            avg = int(getAverage(img))

            #finding which thing to add to the thing
            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]

            #adding the thing to the picture
            asciiImg[j] += gsval

    return asciiImg

#My mane squeeze
def main():

    perkele = "This is a thing that makes ascii images"
    parser = argparse.ArgumentParser(description = perkele)

    parser.add_argument('--file', dest = 'imgFile', required = True)
    parser.add_argument('--scale', dest = 'scale', required = False)
    parser.add_argument('--out', dest = 'outFile', required = False)
    parser.add_argument('--cols', dest='cols', required = False )
    parser.add_argument('--moreLevels', dest='moreLevels', action='store_true')

    args = parser.parse_args()

    #setting up in and out files
    imgFile = args.imgFile
    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile

    #setting up scales
    scale = 0.43
    if args.scale:
        scale = float(args.scale)

    #set cols
    cols = 80
    if args.cols:
        cols = int(args.cols)

    #calling the magical function that does all the things
    asciiImg = convertToAscii(imgFile, cols, scale, args.moreLevels)

    #writing the asciiImg to a file
    f = open(outFile, 'w')
    for rows in asciiImg:
        f.write(row + '\n')
    f.close()

    print("Your thing is in %s" % outFile)

main()
