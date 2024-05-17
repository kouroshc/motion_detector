from flask import render_template, Response, jsonify, json, redirect, url_for

from motion_detector import app
from motion_detector.detect import Detect
processor = Detect()


@app.route('/')
def index():    return render_template("app.html")


@app.route('/monitoring' ,methods=['GET'])
def monitoring():
    return render_template("monitoring.html")


@app.route('/video_feed')
def video_feed():
    return Response(processor.buffer_image_for_web(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/res_feed_empty')
def res_feed_empty():
    return Response(processor.buffer_res_empty_for_web(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/res_feed_annotated')
def res_feed_annotated():
    return Response(processor.buffer_res_annotated_for_web(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/res_data' ,methods=['GET'])
def res_data():
    for i in processor.get_angle_data():
        with open('static/scripts/data.json', 'r') as f:
            data = json.load(f)
        data['Body_Angles'] = i
        with open('static/scripts/data.json', 'w') as f:
            json.dump(data, f)
    return Response(processor.get_angle_data())

