import cv2
from flask import Flask, Response, render_template

source_input = 0

app = Flask(__name__)

# OpenCV VideoCapture object
video_capture = cv2.VideoCapture(source_input)

# Variable to store the last frame
last_frame = None

# Define function that generates frames of video
def generate_frames():
    global last_frame
    while True:
        # Read frame from video stream
        ret, frame = video_capture.read()
        if not ret:
            break
            
        # Store the frame in the last_frame variable
        last_frame = frame

        # Convert frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield frame as byte string
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Render index.html template with video stream
    return render_template('index_pause.html')

@app.route('/video_feed')
def get_video():
    # Return processed video stream
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pause_stream')
def get_image():
    
    # Convert the last frame to JPEG format
    _, buffer = cv2.imencode('.jpg', last_frame)
    frame = buffer.tobytes()
        
    return Response(frame, mimetype='image/jpeg')
    
if __name__ == '__main__':
    app.run()
