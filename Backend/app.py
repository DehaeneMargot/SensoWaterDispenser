# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from subprocess import check_output

import time
import threading
from helpers.HCSR05 import HCSR05
from helpers.DS18B20 import DS18B20
from helpers.lcd import LCD
from helpers.lcd import I2C
from RPi import GPIO
import statistics

#RFID library
from mfrc522 import SimpleMFRC522

#setup
temperature_sensor = DS18B20('28-032197790819')

ultrasonic1 = HCSR05(5,6)
ultrasonic2 = HCSR05(22,27)

motor = 12

knop = 20

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
    
GPIO.setup(motor, GPIO.OUT)
GPIO.output(motor, GPIO.LOW)

GPIO.setup(knop,GPIO.IN,GPIO.PUD_UP)

lcd = LCD()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret!'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
#end_dist = 0

reader = SimpleMFRC522()

user = ""
userid = ""
rfid = ""

#code pump
def control_motor(pin):
    global start_distArray
    start_distArray = []
    global end_distArray
    end_distArray = []
    global dist_diff
    global start_dist
    global end_dist
    global start_liter
    global end_liter
    global liter
    time.sleep(1)
    global distance_bottle
    distance_bottle = ultrasonic1.get_distance()
    DataRepository.add_history(2, userid, distance_bottle)
    if distance_bottle < 10:
        if GPIO.input(knop) == 0:
            print("start")
            i=0
            while (i<5):
                start_distArray.append(ultrasonic2.get_distance())
                i+=1
            start_dist = min(start_distArray)
            DataRepository.add_history(3, userid, start_dist)
            
            start_liter = (start_dist - 14.62)/(-2.27)
            GPIO.output(motor, 1)
            lcd.cursor_line(1)
            lcd.write_message("Water running...")
            print("motor aan")
        else:
            GPIO.output(motor, 0)
            time.sleep(5)
            i=0
            while (i<5):
                end_distArray.append(ultrasonic2.get_distance())
                i+=1
            end_dist = min(end_distArray)
            DataRepository.add_history(3, userid, end_dist)

            end_liter = (end_dist - 14.62)/(-2.27)
            liter = (start_liter - end_liter)*1000
            if liter > 0:
                DataRepository.add_history(4, userid, liter)
            print("motor uit")
            lcd.clear_screen()
            lcd.write_message(str(ip_pi()))
            dist_diff = end_dist - start_dist
            print(dist_diff)
            
    else:
        GPIO.output(motor, 0)
        lcd.clear_screen()
        time.sleep(0.01)
        lcd.write_message(str(ip_pi()))
        lcd.cursor_line(1)
        lcd.write_message("No bottle nearby")
        time.sleep(5)
        lcd.clear_screen()
        lcd.write_message(str(ip_pi()))

GPIO.add_event_detect(knop, GPIO.BOTH, control_motor, bouncetime=300)


def ip_pi():
    ips = check_output(['hostname', '--all-ip-addresses'])
    ips = str(ips)
    ip = ips.strip("b'").split(" ")
    return ip[1]

def get_temp():
    try:
        temperature = temperature_sensor.get_temperature()
        print(temperature)
        DataRepository.add_history(1, userid, temperature)
        socketio.emit('B2F_update_temperature', {"waarde":temperature}, broadcast=False)
        
    except Exception as ex:
        print(f"Fout bij het inlezen: {ex}")


def get_user():
    global user
    global userid
    global rfid
    id = reader.read()
    rfid = id[0]
    print(rfid)
    try:
        connected_user = DataRepository.get_userid_by_rfid(rfid)
        user = connected_user['Nickname']
        userid = connected_user['UserID']
        socketio.emit('B2F_update_user', {"waarde":userid}, broadcast=False)
    
    except Exception as ex:
        print("You must add this user to the system")
        socketio.emit('B2F_new_user', {"waarde":rfid}, broadcast=False)

def get_total_water():
    total_water = DataRepository.read_total_water_consumption(userid)
    total = total_water['Total']
    socketio.emit('B2F_update_total', {"waarde":total, "userid":userid}, broadcast=False)

def get_average_water():
    average_water = DataRepository.read_average_water_consumption(userid)
    average = average_water['Average']
    socketio.emit('B2F_update_average', {"waarde":average}, broadcast=False)

def water_level():
    container_full = 8.4
    container_empty = 22.8
    current_value = ultrasonic2.get_distance()
    DataRepository.add_history(3, userid, current_value)
    water_level = round(((container_empty - current_value)/14.4)*100,0)
    socketio.emit('B2F_update_waterlevel', {"waarde":water_level}, broadcast=False)
    if water_level < 10:
        lcd.cursor_line(1)
        lcd.write_message("Refill tank")
        time.sleep(5)
        lcd.clear_screen()
        time.sleep(0.01)
        lcd.write_message(str(ip_pi()))

def consumption_per_day():
    consumption_day = DataRepository.read_total_consumption_per_user(userid)
    consumption = consumption_day['Value']
    if consumption is None:
        consumption = 0
    socketio.emit('B2F_update_consumption', {"waarde":consumption, "userid":userid}, broadcast=False)

def get_daily_goal():
    daily_goal = DataRepository.read_goal(userid)
    goal = daily_goal['DailyGoal']
    socketio.emit('B2F_update_goal', {"waarde":goal}, broadcast=False)

# API ENDPOINTS

@app.route('/hallo')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route('/progress', methods=['GET'])
def get_progress():
    data = DataRepository.read_logging()
    return jsonify(data), 200

@app.route('/<deviceid>/progress', methods=['GET'])
def get_progress_per_device(deviceid):
    data = DataRepository.read_logging_per_device(deviceid)
    return jsonify(data), 200

@app.route('/<deviceid>/<userid>/progress', methods=['GET'])
def get_progress_per_user(deviceid, userid):
    data = DataRepository.read_logging_per_user(deviceid, userid)
    return jsonify(data), 200

@app.route('/<userid>/consumption', methods=['GET'])
def get_consumption_logs(userid):
    data = DataRepository.read_consumption_logs(userid)
    return jsonify(data), 200

@app.route('/<userid>/goal', methods=['GET'])
def get_goal(userid):
    data = DataRepository.read_goal(userid)
    return jsonify(data), 200

@app.route('/<userid>/goals', methods=['GET'])
def get_all_goals(userid):
    data = DataRepository.read_all_goals(userid)
    return jsonify(data), 200

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

@socketio.on('F2B_onboarding')
def read_rfid():
    lcd.clear_screen()
    time.sleep(0.01)
    lcd.write_message(str(ip_pi()))
    get_user()
    socketio.emit('B2F_user', {"waarde":user}, broadcast=False)

@socketio.on('F2B_container')
def read_container():
    get_temp()
    water_level()

@socketio.on('F2B_dashboard')
def read_dashboard():
    get_daily_goal()
    consumption_per_day()
    socketio.emit('B2F_update_user', {"waarde":user}, broadcast=False)

@socketio.on('F2B_statistics')
def read_statistics():
    get_total_water()
    get_average_water()

@socketio.on('F2B_editgoal')
def read_goal():
    get_daily_goal()

@socketio.on('F2B_change_goal')
def change_goal(jsonObject):
    new_goal = jsonObject['goal']
    DataRepository.add_goal(new_goal, userid)

@socketio.on('F2B_add_user')
def add_new_user(jsonObject):
    new_nickname = jsonObject['nickname']
    new_firstname = jsonObject['firstname']
    new_lastname = jsonObject['lastname']
    new_password = jsonObject['password']
    new_container = jsonObject['container']
    DataRepository.add_user(new_nickname, new_firstname, new_lastname, new_password, rfid, new_container)
    lcd.cursor_line(1)
    lcd.write_message(f"Welcome {new_firstname}")
    time.sleep(5)
    lcd.clear_screen()


@socketio.on('F2B_Check')
def check():
    return 0

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
