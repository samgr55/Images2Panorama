from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import stitching ,cv2 ,os


parser = ArgumentParser()

parser.add_argument("-v", "--video" ,action="store_true", help="add this argument if you want to stitch images from video")
args = parser.parse_args()




status = False
video = args.video
if (video):
    path = "out_imgs/"
    vidcap = cv2.VideoCapture('Video_1.mov')
    fps = round(vidcap.get(cv2.CAP_PROP_FPS))
    print("Video is "+str(fps)+" FPS")
    if (fps > 50):
        limiter = 40
    else:
        limiter = 15
    success,image = vidcap.read()
    count = 0
    while success:
        if (count % limiter == 0):
            cv2.imwrite(path+"frame%d.jpeg" % count, image)      
        success,image = vidcap.read()
        # print('Read a new frame: ', success)
        count += 1
    myList = os.listdir(path)
    img = cv2.imread(path+myList[0])
    sam = list(map(path.__add__,  myList))
    width = int(img.shape[1])
    height = int(img.shape[0])
    if (width > height):
        print("[INFO]: Video has been taken in Landscape Mode")
        stitcher = stitching.Stitcher()     # taken from CV2 library
        settings = {"detector": "sift", "confidence_threshold": 0.2}
        stitcher = stitching.Stitcher(**settings)
        panorama = stitcher.stitch(sam)
        status = True
    else:
        print("[INFO]: Video has been taken in Portrait Mode")
        stitcher2 = cv2.Stitcher_create()
        images = []
        for samsom in sam:
           image = cv2.imread(samsom)
           images.append(image)
        (status,panorama) = stitcher2.stitch(sam)
        

else:
    path = "imgs_2/"
    myList = os.listdir(path)
    img = cv2.imread(path+myList[0])
    width = int(img.shape[1])
    height = int(img.shape[0])
    if (width > height):
        print("[INFO]: Photos have been taken in Landscape Mode")
        stitcher = stitching.Stitcher()     # taken from CV2 library
        settings = {"detector": "sift", "confidence_threshold": 0.2}
        stitcher = stitching.Stitcher(**settings)
        sam = list(map(path.__add__,  myList))
        panorama = stitcher.stitch(sam)
        status = True
        
    else:
       print("[INFO]: Photos have been taken in Portrait Mode")
       stitcher2 = cv2.Stitcher_create()
       sam = list(map(path.__add__,  myList))
       images = []
       for samsom in sam:
           image = cv2.imread(samsom)
           images.append(image)
       (status,panorama) = stitcher2.stitch(images)
       


if (status):
    print("[INFO]: The panoramic photo has been created successfully") # this is what you want Omar right? if yes, take the status value
else:
    print("[INFO]: Error with the panoramic process")

cv2.imwrite("test1.png", panorama)