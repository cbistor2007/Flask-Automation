from flask import Flask, request, redirect
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
import json
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
theater_name = user_Settings['DEFAULT']['theater_name']

template_dir = os.path.join(os.path.abspath(
    os.sep), "\\Automation Controller\\templates\\")

static_dir = os.path.join(os.path.abspath(
    os.sep), "\\Automation Controller\\static\\")

print("Template Directory:" + template_dir)
print("Static Directory:" + static_dir)

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
app.config["TEMPLATES_AUTO_RELOAD"] = True
# window = webview.create_window('Hello', app)

ui = FlaskUI(app, width=800, height=800)


@app.route('/')
def home():
    return render_template('index.html', total_theater_val=total_theaters)


@app.post('/sound_change')
def sound_change():
    success = "true"
    theater_num = int(request.form.get('theater_id'))
    exe_command = request.form.get("exe_command")
    # exe_command = "non_sync"
    print("Theater: " + str(theater_num) + " - Command: " + str(exe_command))
    cmf.sound_processor(str(theater_num), exe_command)
    return success


@app.post('/projector_execute')
def projector_execute():
    success = "true"
    theater_num = int(request.form.get('theater_id'))
    exe_command = request.form.get('exe_command')
    if exe_command == "bulb_on":
        print(exe_command)
        cmf.lamp_on(str(theater_num))
    elif exe_command == "bulb_off":
        print(exe_command)
        cmf.lamp_off(str(theater_num))
    elif exe_command == "dowser_open":
        print(exe_command)
        cmf.dowser_open(str(theater_num))
    elif exe_command == "dowser_close":
        print(exe_command)
        cmf.dowser_close(str(theater_num))
    elif exe_command == "power_on":
        print(exe_command)
        cmf.projector_on(str(theater_num))
    elif exe_command == "power_off":
        print(exe_command)
        cmf.projector_off(str(theater_num))
    elif exe_command == "projector_status":
        print(exe_command)

    # exe_command = "non_sync"
    print("Theater: " + str(theater_num) + " - Comand: " + str(exe_command))
    # return render_template('index.html', bulb_state=bulb_state)
    return success


@app.post('/get_all_bulb_states')
def bulb_state_execute():
    print("BULB STATE EXECUTED BY AJAX")
    bulb_state_json = ""
    bulb_state_json = cmf.lamp_request()
    # bulb_state_json = json.dumps(bulb_state_json)
    print(bulb_state_json)
    return bulb_state_json


@app.post('/get_all_projector_states')
def projector_state_execute():
    print("PROJECTOR STATE EXECUTED BY AJAX")
    power_status_json = ""
    power_status_json = cmf.projector_power_state_request()
    # bulb_state_json = json.dumps(bulb_state_json)
    print(power_status_json)
    return power_status_json


@app.post('/thunderstorm')
def thunderstorm():
    success = "true"
    print("Thunderstorm Executed")
    action_state = "pause_film"
    cmf.all_functions(action_state)
    return success


@app.post('/bulb_on_all')
def all_bulb_on():
    success = "true"
    print("BULB ON PYTHON CALLED")
    cmf.all_bulb_on()
    return success


@app.post('/bulb_off_all')
def all_bulb_off():
    success = "true"
    print("BULB OFF PYTHON CALLED")
    # action_state = "Pause"
    cmf.all_bulb_off()
    return success


@app.post('/power_restored')
def power_restored():
    success = "true"
    print("Power Restored Executed")
    action_state = "restore_film"
    cmf.all_functions(action_state)
    return success


@app.post('/server_execute')
def server_command():
    success = "true"
    theater_num = int(request.form.get('theater_id'))
    exe_command = request.form.get('exe_command')

    if exe_command == "pause_film":
        print(exe_command)
        cmf.server_automation(str(theater_num), exe_command)
    elif exe_command == "play_film":
        print(exe_command)
        cmf.server_automation(str(theater_num), exe_command)
    elif exe_command == "restore_film":
        print(exe_command)
        cmf.server_automation(str(theater_num), exe_command)
    elif exe_command == "shutdown":
        print(exe_command)
        cmf.server_shutdown(str(theater_num))
    print("SERVER PYTHON CALLED")

    return success


if __name__ == "__main__":
    app.run(debug=False)
    # serve(app, host="0.0.0.0", port=6000)
    # webview.start()
    # ui.run()
    # FlaskUI(app=app, server="flask").run()
