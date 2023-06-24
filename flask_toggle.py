import cv2
import datetime
import os

directory = './output/'

if not os.path.exists(directory):
    os.makedirs(directory)

from flask import Flask, Response, render_template
from queue import Queue, Empty
from threading import Thread

from config_database import *

source_input = 0

app = Flask(__name__)

last_frame = None
save_frame = None

def clearQueue(q):
    try:
        while True:
            q.get_nowait()
    except Empty:
        pass

def processGetFrame(source_input, q):
    video = cv2.VideoCapture(source_input)
    while True:
        ret, frame = video.read()
        if not ret:
            video = cv2.VideoCapture(source_input)
        else:
            q.put(frame)

        if q.qsize() >= 3:
            clearQueue(q) 

def generate_frames(frame_queue):
    global last_frame
    while True:
        frame = frame_queue.get()
            
        last_frame = frame

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        frame_queue.task_done()

@app.route('/')
def index():
    return render_template('button.html')

@app.route('/video_feed')
def get_video():
    return Response(generate_frames(frame_queue), mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/pause_stream')
def get_image():
    global save_frame
    save_frame = last_frame

    _, buffer = cv2.imencode('.jpg', last_frame)
    frame = buffer.tobytes()
    return Response(frame, mimetype = 'image/jpeg')

@app.route('/tidak_absen')
def tidak_absen():
    # ini insert data yang dengan status ga OK
    status = 'tidak absen'

    date_time = datetime.datetime.now()
    str_date_time = str(date_time.strftime('%d-%b-%Y %H:%M:%S') + ' WIB')

    filename = directory + 'tidak_absen_' + str_date_time + '.jpg'
    cv2.imwrite(filename, save_frame)
    read_img = open(filename, 'rb').read()

    data_log = [str_date_time, status, read_img]
    insert_to_database(database_name, variable_name, variable_value, data_log)
    
    return Response(status=204)

@app.route('/absen')
def absen():
    # ini insert data yang dengan status OK
    status = 'absen'

    date_time = datetime.datetime.now()
    str_date_time = str(date_time.strftime('%d-%b-%Y %H:%M:%S') + ' WIB')

    filename = directory + 'absen_' + str_date_time + '.jpg'
    cv2.imwrite(filename, save_frame)
    read_img = open(filename, 'rb').read()

    data_log = [str_date_time, status, read_img]
    insert_to_database(database_name, variable_name, variable_value, data_log)
    
    return Response(status=204)

if __name__ == '__main__':
    database_name = 'absen'
    create_table(database_name)

    variable_name = ['time', 'status', 'image']
    variable_value = ["%s", "%s", "%s"]
    variable_name = ', '.join(variable_name)
    variable_value = ', '.join(variable_value)

    frame_queue = Queue()
    thread_frame = Thread(target = processGetFrame, args = (source_input, frame_queue, ), daemon = True)
    thread_frame.start()
    
    thread_output = Thread(target = generate_frames, args = (frame_queue, ), daemon = True)
    thread_output.start()
    app.run()
