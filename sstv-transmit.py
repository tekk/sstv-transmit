import os
import sys
from pysstv.sstv import SSTV
from pysstv.color import Robot36, PD90, PD120
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from playsound import playsound
import subprocess

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))+'/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg','png','JPG','JPEG','PNG'}

application = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# limit upload size upto 8mb
application.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route("/",methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            result = path.split("/")
            filename = result[-1:]
            wav_filename = filename[0].split(".")[0] + '.wav'
            wav_path = os.path.join(UPLOAD_FOLDER, wav_filename)
            im = Image.open(path)
            width, height = im.size
            newsize = (320, 240)
            img = im.resize(newsize)
            sstv = Robot36(img, 44100, 16)
            sstv.vox_enabled = True
            sstv.write_wav(wav_path)
            subprocess.Popen(["play", wav_path])
            return render_template('confirmation.html')
    return render_template('index.html')
 
def main():
    application.debug=True
    application.run(host='0.0.0.0')
 
if __name__ == '__main__':
    main()
