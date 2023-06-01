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

# OpenCV VideoCapture object
# video_capture = cv2.VideoCapture(source_input)

# Variable to store the last frame
last_frame = None

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

# Define function that generates frames of video
def generate_frames(frame_queue):
    global last_frame
    while True:
        # # Read frame from video stream
        # ret, frame = video_capture.read()
        # if not ret:
        #     break
        frame = frame_queue.get()
            
        # Store the frame in the last_frame variable
        last_frame = frame

        # Convert frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield frame as byte string
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        frame_queue.task_done()

@app.route('/')
def index():
    # Render index.html template with video stream
    return render_template('button.html')

@app.route('/video_feed')
def get_video():
    # Return processed video stream
    return Response(generate_frames(frame_queue), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pause_stream')
def get_image():
    # Convert the last frame to JPEG format
    _, buffer = cv2.imencode('.jpg', last_frame)
    frame = buffer.tobytes()
        
    return Response(frame, mimetype='image/jpeg')

@app.route('/tidak_absen')
def tidak_absen():
    # ini insert data yang dengan status ga OK
    status = 'tidak absen'

    date_time = datetime.datetime.now()
    str_date_time = str(date_time.strftime('%d-%b-%Y %H:%M:%S') + ' WIB')
    print(str_date_time)

    filename = directory + 'absen_' + str_date_time + '.jpg'
    cv2.imwrite(filename, last_frame)
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
    print(str_date_time)

    filename = directory + 'absen_' + str_date_time + '.jpg'
    cv2.imwrite(filename, last_frame)
    read_img = open(filename, 'rb').read()

    data_log = [str_date_time, status, read_img]
    insert_to_database(database_name, variable_name, variable_value, data_log)
    
    return Response(status=204)

if __name__ == '__main__':
    # Save to database
    database_name = 'absen'
    create_table(database_name)

    variable_name = ['time', 'status', 'image']
    variable_value = ["%s", "%s", "%s"]
    variable_name = ', '.join(variable_name)
    variable_value = ', '.join(variable_value)

    frame_queue = Queue()
    thread_frame = Thread(target = processGetFrame, args = (source_input, frame_queue, ), daemon = True)
    thread_frame.start()
    
    # output_queue = Queue()
    thread_output = Thread(target = generate_frames, args = (frame_queue, ), daemon = True)
    thread_output.start()
    app.run()
