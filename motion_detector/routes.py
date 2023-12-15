from flask import render_template

from motion_detector import app

@app.route('/')
def index():
    return render_template("app.html")

@app.route('/monitoring')
def monitoring():
    return render_template("monitoring.html")