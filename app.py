import cv2, stitching, shutil
import numpy as np
import io, os
import base64
from pathlib import Path
import secrets


from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])


def upload():
    files = request.files.getlist('images')
    print(files)
    images = [cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR) for file in files]
    stitcher = stitching.Stitcher()
    settings = {"detector": "akaze", "confidence_threshold": 0.2}
    stitcher = stitching.Stitcher(**settings)
    scalar = 0.7
    tempCount = 0
    tempPath = "cache/" + secrets.token_urlsafe(30)
    os.mkdir(tempPath)
    tempPath = tempPath+"/"
    for image in images:
        resized = cv2.resize(image,(int(image.shape[1]*scalar),int(image.shape[0]*scalar)),interpolation = cv2.INTER_AREA)
        cv2.imwrite(tempPath+str(tempCount)+".jpg", resized)
        tempCount +=1
    myList2 = os.listdir(tempPath)
    sam = list(map(tempPath.__add__,  myList2))
    panorama = stitcher.stitch(sam)
    _, buffer = cv2.imencode('.jpg', panorama)
    img_str = base64.b64encode(buffer).decode()
    
    [f.unlink() for f in Path(tempPath).glob("*") if f.is_file()]
    return render_template('result.html', img_data=img_str)

if __name__ == '__main__':
    app.run(debug=True,port=80)
    
    