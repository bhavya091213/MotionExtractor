import cv2 as cv
import blend_modes
from PIL import Image

import numpy as np
import videotest as vt


"""
PROCESS VIDEO FILE AND COMPOSITE
"""


def createInvertedFile(filepath):
    cap = cv.VideoCapture(filepath)
    h = int(cap.get(cv.CAP_PROP_FOURCC))
    fourcc = (
        chr(h & 0xFF)
        + chr((h >> 8) & 0xFF)
        + chr((h >> 16) & 0xFF)
        + chr((h >> 24) & 0xFF)
    )
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv.CAP_PROP_FPS))

    pathVALUES = filepath.split("/")

    outFilePath = ""
    # out file
    if len(pathVALUES[-1]) != 0:
        x = pathVALUES[-1].split(".")
        outFilePath = "./tempDuplicates/INVERTED" + x[0] + ".mp4"
        out = cv.VideoWriter(outFilePath, h, fps, (width, height))
    else:
        x = pathVALUES[-2].split(".")
        outFilePath = "./tempDuplicates/INVERTED" + x[0] + ".mp4"
        out = cv.VideoWriter(outFilePath, h, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        inverted_image = cv.bitwise_not(frame)
        out.write(inverted_image)

    cap.release
    out.release()
    return outFilePath


def offsetFile(filepath, order, offsetVal):
    cap = cv.VideoCapture(filepath)

    fps = int(cap.get(cv.CAP_PROP_FPS))

    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    h = int(cap.get(cv.CAP_PROP_FOURCC))

    # CREATE BLACK FRAME
    blackFrame = np.zeros((height, width, 3), dtype=np.uint8)

    # file path normalization
    outPath = ""
    splitPath = filepath.split("/")
    if len(splitPath[-1]) != 0:
        x = splitPath[-1].split(".")
        outPath = "./tempDuplicates/OFFSET" + x[0] + ".mp4"
        out = cv.VideoWriter(outPath, h, fps, (width, height))
    else:
        x = splitPath[-2].split(".")
        outPath = "./tempDuplicates/OFFSET" + x[0] + ".mp4"
        out = cv.VideoWriter(outPath, h, fps, (width, height))

    # IF STATEMETNS TO OFFSET BASED OFF OFFSET FUNCTION BY SIMPLY ADDING BLACK FRAMES
    if order == "BEFORE":
        # Add black frames beforehand
        for i in range(offsetVal):
            out.write(blackFrame)

        # Add rest of the video
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            out.write(frame)
    elif order == "AFTER":

        # Add rest of the video
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            out.write(frame)

        # Add black frames afterwards
        for i in range(offsetVal):
            out.write(blackFrame)

    cap.release
    out.release()
    return outPath


def compileImages(path, fourcc, fps, sizeTuple):
    folder_dir = "./tempDuplicates/images"
    out = cv.VideoWriter(path, fourcc, fps, sizeTuple)
    for image in os.listdir(folder_dir):
        file_name = os.path.join(os.path.dirname(__file__), image)
        assert os.path.exists(file_name)
        out.write(cv.imread(file_name, -1))

    out.release()


def composite(original, inverted, frameOffset, blendType):

    # Offset files to have same length based off how long the user wants to offset
    offsetOriginalAFTER = offsetFile(original, "AFTER", frameOffset)

    if blendType == "ALPHA":
        offsetInverted = offsetFile(inverted, "BEFORE", frameOffset)
        return alphaComposite(offsetOriginalAFTER, offsetInverted)
    elif blendType == "DIFFERENCE":
        offsetOriginalBEFORE = offsetFile(original, "BEFORE", frameOffset)
        return difference(offsetOriginalAFTER, offsetOriginalBEFORE)


def difference(og, inv):
    vid1 = cv.VideoCapture(og)
    vid2 = vid1

    fps = int(vid1.get(cv.CAP_PROP_FPS))
    # h = int(vid1.get(cv.CAP_PROP_FOURCC))
    width = int(vid1.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(vid1.get(cv.CAP_PROP_FRAME_HEIGHT))

    # set up out path
    outPath = ""
    splitPath = original.split("/")
    if len(splitPath[-1]) != 0:
        x = splitPath[-1].split(".")
        outPath = "./processedOutputFiles/DIFFERENCE" + x[0] + ".mp4"
        # out = cv.VideoWriter(outPath,  cv.VideoWriter_fourcc(*'v264'), fps, (width,height))
    else:
        x = splitPath[-2].split(".")
        outPath = outPath = "./processedOutputFiles/DIFFERENCE" + x[0] + ".mp4"
        # out = cv.VideoWriter(outPath, cv.VideoWriter_fourcc(*'v264'), fps, (width,height))

    tempImagePath = "./tempDuplicates/images"
    os.makedirs(tempImagePath)
    count = 0
    while vid1.isOpened():
        ret1, frame1 = vid1.read()
        ret2, frame2 = vid2.read()
        if not ret1 or not ret2:
            break
        # Convert to RGBA and float for blending

        cv.imwrite("./tempDuplicates/tempframe1.png", frame1.astype(float))
        cv.imwrite("./tempDuplicates/tempframe2.png", frame2.astype(float))

        # img_in = cv.imread("./tempDuplicates/tempframe1.png", -1)
        # img_layer = cv.imread("./tempDuplicates/tempframe2.png", -1)

        # Apply the difference blend mode

        img_in = np.asarray(
            Image.open("./tempDuplicates/tempframe1.png").convert("RGBA")
        ).astype(float)
        img_layer = np.asarray(
            Image.open("./tempDuplicates/tempframe2.png").convert("RGBA")
        ).astype(float)
        img_out = blend_modes.difference(img_in, img_layer, 1.0)

        # Convert back to uint8, ensure values are within valid range
        compositedFrame = img_out.astype(np.uint8)
        cv.imwrite(tempImagePath + "/tmpdiff" + str(count) + ".png", compositedFrame)
        count += 1
        # out.write(compositedFrame)

    vid1.release()
    vid2.release()

    vt.compileFromImages(tempImagePath, outPath)
    out.release()
    compileImages(outPath, int(0x7634706D), fps, (width, height))
    return outPath


def alphaComposite(og, inv):

    vid1 = cv.VideoCapture(og)
    vid2 = cv.VideoCapture(inv)

    fps = int(vid1.get(cv.CAP_PROP_FPS))
    h = int(vid1.get(cv.CAP_PROP_FOURCC))
    width = int(vid1.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(vid1.get(cv.CAP_PROP_FRAME_HEIGHT))

    # set up out path
    outPath = ""
    splitPath = original.split("/")
    if len(splitPath[-1]) != 0:
        x = splitPath[-1].split(".")
        outPath = "./processedOutputFiles/ALPHACOMPOSITE" + x[0] + ".mp4"
        out = cv.VideoWriter(outPath, h, fps, (width, height))
    else:
        x = splitPath[-2].split(".")
        outPath = outPath = "./processedOutputFiles/ALPHACOMPOSITE" + x[0] + ".mp4"
        out = cv.VideoWriter(outPath, h, fps, (width, height))

    while vid1.isOpened():
        ret1, frame1 = vid1.read()
        ret2, frame2 = vid2.read()
        if not ret1 or not ret2:
            break

        compositedFrame = cv.addWeighted(frame1, 0.5, frame2, 0.5, 0.0)  # set alphas

        out.write(compositedFrame)

    # release
    vid1.release()
    vid2.release()
    out.release()
    return outPath


# original = "./testVideoAssets/2342260-hd_1920_1080_30fps.mp4"
# original = "./testVideoAssets/151744-801455851_tiny.mp4"
# original = "./testVideoAssets/istockphoto-1130731523-640_adpp_is.mp4"
# original = "./testVideoAssets/75376-555532001_small.mp4"
# inverted = createInvertedFile(original)
# print("Created Composited Video at: " + composite(original,inverted,1,"ALPHA"))

# print("Created Composited Video at: " + composite(original, original, 1, "DIFFERENCE"))

# fileslst = [
#     "./testVideoAssets/2342260-hd_1920_1080_30fps.mp4}",
#     "./testVideoAssets/151744-801455851_tiny.mp4",
#     "./testVideoAssets/istockphoto-1130731523-640_adpp_is.mp4",
#     "./testVideoAssets/75376-555532001_small.mp4",
# ]

fileslst = ["out5.mp4", "tire.mov"]

for file in fileslst:
    original = "./testVideoAssets/" + file
    inverted = createInvertedFile(original)
    print(
        "Created Composited Video at: " + composite(original, inverted, 20, "ALPHA")
    )  # doesnt seem to work with avi files
    # print(
    #    "Created Composited Video at: " + composite(original, original, 1, "DIFFERENCE")
    # )
