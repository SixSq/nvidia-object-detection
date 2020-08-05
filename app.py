#!/usr/bin/env python
# coding: utf-8

import os
import sys
import argparse
import time
from flask import Flask, render_template, Response
from video_analysis import VideoAnalysis
import cv2

app = Flask(__name__)
parameters = {}


def mjpeg_generator():
    """Video streaming generator function."""

    while True:
        time.sleep(5)
        cap = cv2.VideoCapture(0);    # open the video stream from a file a device or

        ret, frame = cap.read()

        print("PUSHING NEW IMAGE")

        inputImage = cv2.imwrite("input.jpg",  frame)

        run = ['./darknet','detect', 'cfg/yolov3-tiny.cfg', 'weights/yolov3-tiny.weights', "input.jpg"]
        
        prog = subprocess.run(run, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(prog.stdout)
        
        # image = self.request_image()
        image = cv2.imread("predictions.jpg")
        ret, jpeg = cv2.imencode('.jpg', image,
                                (cv2.IMWRITE_JPEG_QUALITY, self.quality))
        image = jpeg.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


@app.route('/')
def index():
    """Video streaming home page which makes use of /mjpeg."""
    return render_template('index.html')

@app.route('/video')
def video():
    """Video streaming home page which makes use of /jpeg."""
    return render_template('video.html')

# @app.route('/mjpeg')
# def mjpeg():
#     """Video streaming route. Put this in the src attribute of an img tag."""
#     return Response(VideoAnalysis(**parameters).mjpeg_generator(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame',
#                     direct_passthrough=True)

@app.route('/mjpeg')
def mjpeg():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(mjpeg_generator())


# @app.route('/jpeg')
# def jpeg():
#     return Response(VideoAnalysis(**parameters).request_image(),
#                     mimetype='image/jpeg',
#                     direct_passthrough=True)


@app.route('/jpeg')
def jpeg():
    return Response(mjpeg_generator())

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

def main():
    global parameters

    argument_parser = get_argument_parser()
    args = argument_parser.parse_args()
    parameters = dict(args._get_kwargs())
    for k,v in parameters.items():
        print('{}: {}'.format(k, v))

    app.run(host='0.0.0.0', port='8000', debug=False, threaded=True)

if __name__ == '__main__':
    main()