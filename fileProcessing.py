from cv2 import (
    VideoCapture,
    VideoWriter
)

import os


"""
PROCESS VIDEO FILE AND COMPOSITE
"""



def createDuplicateFile(filepath):
    cap = VideoCapture(filepath)
    
    
    while(cap.isOpened()):
        ret, frame = cap.read()

    