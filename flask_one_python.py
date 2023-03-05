from flask import Flask, render_template, Response

import cv2

cameras = ['./input/superjunior.mp4', './input/shinee.mp4']
stream_name = ['superjunior', 'shinee']

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

@app.route('/shinee', methods = ['GET'])
def video_shinee():
    return Response(serveStreaming(cameras[1]), mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/superjunior', methods = ['GET'])
def video_superjunior():
    return Response(serveStreaming(cameras[0]), mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()