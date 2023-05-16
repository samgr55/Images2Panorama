from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from stitching import *
import cv2 ,os


parser = ArgumentParser()

parser.add_argument("-v", "--video" ,action="store_true", help="add this argument if you want to stitch images from video")
args = parser.parse_args()

video = args.video
if (video):
    path = "C:/Users/samra/Desktop/ImageStitching/TEST/out_imgs/"
    vidcap = cv2.VideoCapture('Video.mov')
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(path+"frame%d.jpeg" % count, image)      
        success,image = vidcap.read()
        # print('Read a new frame: ', success)
        count += 1


else:
    path = "C:/Users/samra/Desktop/ImageStitching/TEST/imgs_1/"

stitcher = stitching.Stitcher()     # taken from CV2 library
settings = {"detector": "sift", "confidence_threshold": 0.2}
stitcher = stitching.Stitcher(**settings)
myList = os.listdir(path)


sam = list(map(path.__add__,  myList))

# print(sam)


panorama = stitcher.stitch(sam) # hopefully it will work bus still I need to do some tuning (WIP)


cv2.imwrite("test1.jpg", panorama)