import cv2 as cv

import os
import numpy as np


"""
PROCESS VIDEO FILE AND COMPOSITE
"""



def createInvertedFile(filepath):
    cap = cv.VideoCapture(filepath)
    h = int(cap.get(cv.CAP_PROP_FOURCC))
    fourcc = chr(h&0xff) + chr((h>>8)&0xff) + chr((h>>16)&0xff) + chr((h>>24)&0xff)
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv.CAP_PROP_FPS)) 
    
    pathVALUES = filepath.split("/")
    
    outFilePath = ""
    # out file
    if (len(pathVALUES[-1])!=0):
        x = pathVALUES[-1].split(".")
        outFilePath = "./tempDuplicates/DUPLCIATEDTEMP"+ x[0] +".mp4"
        out = cv.VideoWriter(outFilePath, h, fps, (width,height)) 
    else:
        x = pathVALUES[-2].split(".")
        outFilePath = "./tempDuplicates/DUPLCIATEDTEMP"+ x[0] +".mp4"
        out = cv.VideoWriter(outFilePath, h, fps, (width,height)) 
    
     
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        
        inverted_image = cv.bitwise_not(frame)
        out.write(inverted_image)
        
    cap.release
    out.release()
    return(outFilePath)
    print("inverted video file")
    

def offsetFile(filepath):
    cap = cv.VideoCapture(filepath)
    
    fps = int(cap.get(cv.CAP_PROP_FPS))
    
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    
    # CREATE BLACK FRAME
    blackFrame = np.zeros((height,width), dtype= np.uint8)


def compositeVideos(original, inverted, frameOffset):
    vid1 = cv.VideoCapture(original)
    vid2 = cv.VideoCapture(inverted)
    
    fps = int(vid1.get(cv.CAP_PROP_FPS)) 
    
    
    h1 = int(vid1.get(cv.CAP_PROP_FOURCC))
    width1 = int(vid1.get(cv.CAP_PROP_FRAME_WIDTH))
    height1 = int(vid1.get(cv.CAP_PROP_FRAME_HEIGHT))
    
    h2 = int(vid2.get(cv.CAP_PROP_FOURCC))
    width2 = int(vid2.get(cv.CAP_PROP_FRAME_WIDTH))
    height2 = int(vid2.get(cv.CAP_PROP_FRAME_HEIGHT))
    
    
    
    
    

print("Created Inverted Video at: " + createInvertedFile("./testVideoAssets/2342260-hd_1920_1080_30fps.mp4"))
