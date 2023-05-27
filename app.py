import cv2
import numpy as np
import io
import base64

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
    stitcher = cv2.Stitcher_create()
    
    status, stitched = stitcher.stitch(images)

    _, buffer = cv2.imencode('.jpg', stitched)
    img_str = base64.b64encode(buffer).decode()

    return render_template('result.html', img_data=img_str)

if __name__ == '__main__':
    app.run(debug=True)