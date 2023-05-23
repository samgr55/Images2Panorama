import kornia as K
import kornia.feature as KF
import matplotlib.pyplot as plt
import numpy as np
import torch, os
from kornia.contrib import ImageStitcher


# another approach using Deep Learning w/ GPU (WIP)

def load_images(fnames):
    return [K.io.load_image(fn, K.io.ImageLoadType.RGB32)[None, ...] for fn in fnames]
path = "outdoor/"
myList = os.listdir(path)
sam = list(map(path.__add__,  myList))
imgs = load_images(sam)

IS = ImageStitcher(KF.LoFTR(pretrained="outdoor"), estimator="ransac").cuda()

with torch.no_grad():
    out = IS(*imgs)

image = K.tensor_to_image(out)
plt.imsave("test1.png", image)
