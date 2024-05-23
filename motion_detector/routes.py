from flask import render_template, Response, jsonify, json, redirect, url_for

from motion_detector import app
from motion_detector.detect import Detect
from motion_detector.forms import TimeFrame_Form

processor = Detect()


@app.route('/')
def index():

    time_frame_form = TimeFrame_Form()
    if time_frame_form.validate_on_submit():
        time_frame = float(time_frame_form.time.data)
        processor.__init__(float(time_frame_form.time.data))
        return render_template("monitoring.html" , time_frame_form=time_frame_form , time_frame=time_frame )
    return render_template("app.html" ,time_frame_form=time_frame_form)


@app.route('/monitoring' , methods=['GET', 'POST'])
def monitoring():
    time_frame = 1
    processor.__init__(time_frame)
    return render_template("monitoring.html" ,time_frame=time_frame )


# @app.route('/video_feed')
# def video_feed():
    # return Response(processor.caputre_image(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
        if i is not None:
            with open('static/scripts/data.json', 'r') as f:
                data = json.load(f)
            data['Body_Angles'] = i
            with open('static/scripts/data.json', 'w') as f:
                json.dump(data, f)


    return Response(processor.get_angle_data())

@app.route('/res_chart_data' ,methods=['GET'])
def res_chart_data():
    for i in processor.get_angle_data_chart_ready():
        if i is not None:
            with open('static/scripts/chart.json', 'r') as f:
                data = json.load(f)
            data.clear()
            data['Body_Angles_Chart'] = i
            with open('static/scripts/chart.json', 'w') as f:
                json.dump(data, f)

    return Response(processor.get_angle_data_chart_ready())

@app.route('/write_and_download' ,methods=['GET'])
def write_and_download():
    return processor.write_and_download()


