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
        outFilePath = "./tempDuplicates/INVERTED"+ x[0] +".mp4"
        out = cv.VideoWriter(outFilePath, h, fps, (width,height)) 
    else:
        x = pathVALUES[-2].split(".")
        outFilePath = "./tempDuplicates/INVERTED"+ x[0] +".mp4"
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
    

def offsetFile(filepath, order, offsetVal):
    cap = cv.VideoCapture(filepath)
    
    fps = int(cap.get(cv.CAP_PROP_FPS))
    
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    h = int(cap.get(cv.CAP_PROP_FOURCC))
    
    # CREATE BLACK FRAME
    blackFrame = np.zeros((height,width), dtype= np.uint8)
    
    
    # file path normalization
    outPath = ""
    splitPath = filepath.split("/")
    if (len(splitPath[-1])!=0):
        x = splitPath[-1].split(".")
        outPath = "./tempDuplicates/OFFSET"+ x[0] +".mp4"
        out = cv.VideoWriter(outPath, h, fps, (width,height)) 
    else:
        x =splitPath[-2].split(".")
        outPath = outPath = "./tempDuplicates/OFFSET"+ x[0] +".mp4"
        out = cv.VideoWriter(outPath, h, fps, (width,height)) 
    
    
    # IF STATEMETNS TO OFFSET BASED OFF OFFSET FUNCTION BY SIMPLY ADDING BLACK FRAMES
    if (order == "BEFORE"):
        # Add black frames beforehand
        for i in range(offsetVal):
            out.write(blackFrame)

        # Add rest of the video
        while(cap.isOpened()):
            ret, frame = cap.read()
            
            if not ret:
                break
            
            inverted_image = cv.bitwise_not(frame)
            out.write(inverted_image)
    elif (order == "AFTER"):

        # Add rest of the video
        while(cap.isOpened()):
            ret, frame = cap.read()
            
            if not ret:
                break
        
            inverted_image = cv.bitwise_not(frame)
            out.write(inverted_image)
        
        # Add black frames afterwards
        for i in range(offsetVal):
            out.write(blackFrame)
            
    cap.release
    out.release()
    return(outPath)
    print("Offset video file")


def compositeAlpha(original, inverted, frameOffset):
    
    # Offset files to have same length based off how long the user wants to offset
    offsetOriginal = offsetFile(original, "AFTER", frameOffset)
    offsetInverted = offsetFile(inverted,"BEFORE", frameOffset)
    
    vid1 = cv.VideoCapture(offsetOriginal)
    vid2 = cv.VideoCapture(offsetInverted)
    
    fps = int(vid1.get(cv.CAP_PROP_FPS)) 
    
    
    h1 = int(vid1.get(cv.CAP_PROP_FOURCC))
    width1 = int(vid1.get(cv.CAP_PROP_FRAME_WIDTH))
    height1 = int(vid1.get(cv.CAP_PROP_FRAME_HEIGHT))
    
    h2 = int(vid2.get(cv.CAP_PROP_FOURCC))
    width2 = int(vid2.get(cv.CAP_PROP_FRAME_WIDTH))
    height2 = int(vid2.get(cv.CAP_PROP_FRAME_HEIGHT))
    
    
    while (vid1.isOpened()):
        print()
        
    
    
    

print("Created Inverted Video at: " + createInvertedFile("./testVideoAssets/2342260-hd_1920_1080_30fps.mp4"))
