#!/usr/bin/python3
import time
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from model import AIModel
import sys
import os

UPLOAD_FOLDER = "/code"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("if file and allowed_file(file.filename) ".format(file.filename), file=sys.stdout)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("predict(file.filename): ".format(file.filename), file = sys.stdout)
            inf = predict(file.filename)
            return {"label": inf["label"], "confidence": float("{:.4}".format(inf["confidence"])) }
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
    <input type=file name=file>
    <input type=submit value=Upload>
    </form>
   '''
def predict(img):
    model = AIModel()
    return model.predict(img)

if __name__ == "__main__":
    app.run(debug=True, port = 9191, host="0.0.0.0")

