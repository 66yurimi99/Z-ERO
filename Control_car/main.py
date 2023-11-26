import sys
import threading
import time
from flask import Flask, render_template, Response
from send_vid import Send_vid
from Autodrive_control import AutoDrive
import RPi.GPIO as GPIO
import requests

app = Flask(__name__)
streaming = Send_vid()
mutex = threading.Lock()

# 사용자로부터 입력 받기
isCar = 0
Driver_state = 0
obj = 3
theta = 20.0

# 받아오셈
drive_control = AutoDrive(isCar, Driver_state, obj, theta)

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 일으킵니다.
        return response.text
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        return None

@app.route('/video_feed')
def video_feed():
    return streaming.get_response()

@app.route('/')
def index():
    return render_template('index.html')  # HTML 페이지 렌더링
	
def send_vid():
    print("flask..")
    app.run(host='0.0.0.0', debug=True, use_reloader=False,threaded=True)

def self_drive():
    print("control..")
    while True:
        mutex.acquire()
        state, theta = drive_control.get_Direction()
        drive_control.Cal_velocity()
        mutex.release()
        time.sleep(1)

def data_fetcher():
    global isCar, Driver_state, obj, theta

    while True:
        url = "http://54.175.8.12/db_get.php?car&driver&speed&direction"
        data = fetch_data(url)

        if data:
            print(f"The data is: {data}")
            tem = data.split(',')
            with mutex:
                isCar = int(tem[0])
                Driver_state = int(tem[1])
                obj = int(tem[2])
                if len(tem) > 3:
                    theta = float(tem[3])
                else:
                    theta = 20.0
        else:
            print("Can't read")

        time.sleep(1)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO_Right = 12
    GPIO_Left = 13
    GPIO.setup(GPIO_Right, GPIO.OUT)  # PwM_R
    GPIO.setup(GPIO_Left, GPIO.OUT)  # PwM_L
    try:
        drive_control.Set_GPIO()

        flask_thread = threading.Thread(target=send_vid)
        control_thread = threading.Thread(target=self_drive)
        fetch_thread = threading.Thread(target=data_fetcher)

        flask_thread.start()
        control_thread.start()
        fetch_thread.start()

        flask_thread.join()
        control_thread.join()
        fetch_thread.join()

    except KeyboardInterrupt:
        drive_control.stop_motor()
    finally:
        drive_control.stop_motor()
        # Clean up GPIO
        GPIO.cleanup()
        sys.exit(0)
