from flask import  Flask, request, redirect, render_template, flash
import time
import os
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.secret_key = 'thisissecret'
UPLOAD_FOLDER = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
model_path = 'E:/College/Semester 7/prak ketuprak/model/VGG19.h5'

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
def index():
    return render_template('/index.html', )

def predict_result(run_time, probs, img):
    class_list = {'Paper': 0, 'Rock': 1, 'Scissors:' :2}
    idx_pred = probs.index(max(probs))
    labels = list(class_list.keys())
    return render_template('/result.html', labels=labels,
                            probs=probs, pred=idx_pred,
                            run_time=run_time, img=img)


@app.route('/predict', methods=['POST'])
def predict():
    model = load_model(model_path)
    file = request.files.get("file")  
    if file is None or file.filename == '':
        flash('No image file selected. Please choose an image.', 'error')
        return redirect('/')

    file.save(os.path.join('static', 'temp.jpg'))
    img = cv2.cvtColor(np.array(Image.open('./static/temp.jpg')), cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = np.expand_dims(img.astype('float32') / 255, axis=0)
    
    start = time.time()
    pred = model.predict(img)[0]
    runtimes = round(time.time() - start, 4)
    respon_model = [round(elem * 100, 2) for elem in pred]

    return predict_result(runtimes, respon_model, 'temp.jpg')

if __name__ == "__main__":
        app.run(debug=True, host='0.0.0.0', port=2000)