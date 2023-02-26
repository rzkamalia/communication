from flask import Flask, render_template, Response
from waitress import serve

import cv2 
from config import *

def serveStreaming(source_input):
    video = cv2.VideoCapture(source_input)
    while True:
        ret, frame = video.read()
        if not ret:
            video = cv2.VideoCapture(source_input)
        else:
            frame = cv2.flip(frame, 0)    
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

app = Flask(__name__)

@app.route(stream_name)
def get_image():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(serveStreaming(source_input), mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print(f'http://0.0.0.0:{port_artis}{stream_name}')
    serve(app, host = '0.0.0.0', port = port_artis, threads = 4)