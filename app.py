#!/usr/bin/env python
# coding: utf-8

import os
import sys
import argparse
import subprocess

from flask import Flask, render_template, Response, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from camera2 import imageGenerator

app = Flask(__name__)
parameters = {}

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    """Video streaming home page which makes use of /mjpeg."""
    return render_template('index.html')

@app.route('/video')
def video():
    """Video streaming home page which makes use of /jpeg."""
    return render_template('video.html')

@app.route('/mjpeg')
def mjpeg():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(imageGenerator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame',
                    direct_passthrough=True)

@app.route('/jpeg')
def jpeg():
    return Response(imageGenerator(),
                    mimetype='image/jpeg',
                    direct_passthrough=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            run = ['./darknet/darknet','detect' ,'/darknet/cfg/yolov3-tiny.cfg', '/darknet/weights/yolov3-tiny.weights', filepath]
            print('Starting YOLO')
            prog = subprocess.run(run, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            prog.wait()
            print('YOLO FINISHED')
            print(prog)
            return redirect(url_for('upload',
                                    filename=filename))

    return 'Not valid'

def get_argument_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('-i', '--input_source', default=os.environ.get('INPUT_SOURCE', 0),       help='Video input source')
    parser.add_argument('-q', '--quality',      default=os.environ.get('QUALITY', 80), type=int, help='Quality of the output stream [0-100]')
    parser.add_argument('-w', '--width',        default=os.environ.get('WIDTH', 1280), type=int, help='Width of the output stream')
    parser.add_argument('-h', '--height',       default=os.environ.get('HEIGHT', 720), type=int, help='Height of the output stream')
    parser.add_argument('-t', '--threads',      default=os.environ.get('THREADS',  1), type=int, help='Number of thread to run analysis')
    parser.add_argument('--mqtt_broker', default=os.environ.get('MQTT_BROKER'), help='MQTT Broker TCP endpoint')
    parser.add_argument('--mqtt_topic',  default=os.environ.get('MQTT_TOPIC', 'video_analysis/message'), help='MQTT Topic')
    # TODO
    #parser.add_argument('-d', '--debug', dest='debug', help='Show debug log level (all log messages).', action='store_true', default=False)
    #parser.add_argument('-q', '--quiet', dest='quiet', help='Show less log messages. Add more to get less details.', action='count', default=0)
    return parser

def main():
    global parameters

    argument_parser = get_argument_parser()
    args = argument_parser.parse_args()
    parameters = dict(args._get_kwargs())
    for k,v in parameters.items():
        print('{}: {}'.format(k, v))

    app.run(host='0.0.0.0', debug=False, threaded=True)

if __name__ == '__main__':
    main()