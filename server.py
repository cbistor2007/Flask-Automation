from flask import Flask, request
from flask import render_template
# Import Class
from communicator_functions import comm_functions as cmf
# import webview
from flaskwebgui import FlaskUI
import os
import sys
import configparser
from flask_bootstrap import Bootstrap
from waitress import serve
base_dir = '.'

# Setup the Configuration Parser
user_Settings = configparser.ConfigParser()
user_Settings.sections()
[]


file_to_open = os.path.join(os.path.abspath(
    os.sep), "\\Automation Controller\\user_settings.ini")
print(file_to_open)
user_Settings.read(file_to_open)
# total_theaters = 10
total_theaters = user_Settings['DEFAULT']['total_theaters']
# print(total_theaters)

app = Flask(__name__)
# window = webview.create_window('Hello', app)

ui = FlaskUI(app, width=800, height=800)


@app.route('/')
@app.route('/index/')
def home():
    return render_template('index.html', total_theater_val=total_theaters)


@app.post("/sound_change")
def sound_change():
    theater_num = request.form.get('theater_number')
    exe_command = "non_sync"
    cmf.sound_processor(theater_num, exe_command)
    return render_template('index.html', total_theater_val=total_theaters)


if __name__ == "__main__":
    app.run(debug=False)
    # serve(app, host="0.0.0.0", port=6000)
    # webview.start()
    # ui.run()
    # FlaskUI(app=app, server="flask").run()
