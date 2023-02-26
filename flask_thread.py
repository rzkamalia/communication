from flask import Flask, render_template, Response
from waitress import serve

from queue import Queue
from threading import Thread

from config import *
from process_ai import *

def serveStreaming(q):
    while True:
        frame = q.get()
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        q.task_done()

app = Flask(__name__)

@app.route(stream_name)
def get_image():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(serveStreaming(q), mimetype = 'multipart/x-mixed-replace; boundary=frame')

# MAIN > CONFIG BANYAK, PROCESS AI SAMA SEMUA, RUN PYTHON SEBANYAK CONFIG
# note: run pake run.sh
# if __name__ == '__main__':
#     q = Queue()

#     process_ai = Thread(target = processAI, args = (q, ), daemon = True)
#     process_ai.start()

#     print(f'http://0.0.0.0:{port_artis}{stream_name}')
#     serve(app, host = '0.0.0.0', port = port_artis, threads = 4)
    
#     q.join() # wait for the queue to empty

# MAIN > CONFIG BANYAK, PROCESS AI BEDA SEMUA, RUN PYTHON SEBANYAK CONFIG
# note: run pake run.sh
if __name__ == '__main__':
    q = Queue()

    if stream_name == '/superjunior':
        process_ai = Thread(target = processFlip, args = (q, ), daemon = True)   
    elif stream_name == '/shinee':
        process_ai = Thread(target = processRotate, args = (q, ), daemon = True)
    process_ai.start()

    print(f'http://0.0.0.0:{port_artis}{stream_name}')
    serve(app, host = '0.0.0.0', port = port_artis, threads = 4)
    
    q.join() # wait for the queue to empty