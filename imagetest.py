import cv2
import numpy as np
from blend_modes import difference

# Read the images
img_in = cv2.imread("RSPN MAIN.png", -1).astype(float)
img_layer = cv2.imread("NEW RSPN Backdrop.png", -1).astype(float)

# Apply the difference blend mode
img_out = difference(img_in, img_layer, 0.5)

# Convert the image back to uint8 for display
img_out = img_out.astype(np.uint8)

# Display the blended image
cv2.imshow('window', img_out)
cv2.waitKey(0)
cv2.destroyAllWindows()

    
def difference(og, inv):
    vid1 = cv.VideoCapture(og)
    vid2 = cv.VideoCapture(inv)
    
    fps = int(vid1.get(cv.CAP_PROP_FPS))
    #h = int(vid1.get(cv.CAP_PROP_FOURCC))
    width = int(vid1.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(vid1.get(cv.CAP_PROP_FRAME_HEIGHT))
    
    # set up out path
    outPath = ""
    splitPath = original.split("/")
    if (len(splitPath[-1])!=0):
        x = splitPath[-1].split(".")
        outPath = "./processedOutputFiles/DIFFERENCE"+ x[0] +".mp4"
        #out = cv.VideoWriter(outPath, int(0x7634706d), fps, (width,height)) 
    else:
        x =splitPath[-2].split(".")
        outPath = outPath = "./processedOutputFiles/DIFFERENCE"+ x[0] +".mp4"
        #out = cv.VideoWriter(outPath, int(0x7634706d), fps, (width,height)) 
        
    count = 0
    while (vid1.isOpened()):
        ret1, frame1 = vid1.read()
        ret2, frame2 = vid2.read()
        if not ret1 or not ret2:
            break
        
        if (len(os.listdir("./tempDuplicates/images")) > 0):
            break
        # Convert to RGBA and float for blending
        
        cv.imwrite("./tempDuplicates/tempframe1.png", frame1.astype(float))
        cv.imwrite("./tempDuplicates/tempframe2.png", frame2.astype(float))
        
        # img_in = cv.imread("./tempDuplicates/tempframe1.png", -1)
        # img_layer = cv.imread("./tempDuplicates/tempframe2.png", -1)

        # Apply the difference blend mode 
        
        img_in= np.asarray(Image.open("./tempDuplicates/tempframe1.png").convert('RGBA')).astype(float)
        img_layer = np.asarray(Image.open("./tempDuplicates/tempframe2.png").convert('RGBA')).astype(float)
        img_out = blend_modes.difference(img_in, img_layer, 0.5)
        
        
        
        # Convert back to uint8, ensure values are within valid range
        compositedFrame = img_out.astype(np.uint8)
        cv.imwrite("./tempDuplicates/images/tmpdiff" + str(count) + ".png", compositedFrame)
        count+=1
        #out.write(compositedFrame)
    
    vid1.release()
    vid2.release()
    #out.release()
    compileImages(outPath, int(0x7634706d), fps, (width,height))
    return(outPath)
 