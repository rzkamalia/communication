from threading import Thread
from queue import Queue, Empty

import cv2

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

from flask import Flask, render_template, Response
from waitress import serve

video_paths = ['./input/superjunior.mp4', './input/shinee.mp4']
portS = ['5001', '5002']
stream_nameS = ['/superjunior', '/shinee']
frame_queueS = []
output_queueS = []
frame_threadS = []
output_threadS = []
frame_rate_rtsp = 15
max_bitrate_rtsp = 512

# MODE = 0 flask / 1 rtsp
MODE = 1

def serveStreaming(q):
    while True:
        frame = q.get()
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        q.task_done()

if MODE == 0:
    app = Flask(__name__)

    @app.route('/kpop'+'/<i>', methods = ['GET'])
    def get_stream(i):
        return render_template('index_with_endpoint.html', endpoint = i)

    @app.route('/<int:i>')
    def video_feed(i):
        return Response(serveStreaming(output_queueS[i]), mimetype = 'multipart/x-mixed-replace; boundary=frame')

class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, q, **properties):
        super(SensorFactory, self).__init__(**properties)
        self.q = q
        self.number_frames = 0
        self.fps = frame_rate_rtsp  # depends on FPS input
        self.duration = 1 / self.fps * Gst.SECOND   # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                            'caps=video/x-raw,format=BGR,width={},height={},framerate={}/1 ' \
                            '! videoconvert ! video/x-raw,format=I420 ' \
                            '! x264enc bitrate={} tune=zerolatency speed-preset=ultrafast ' \
                            '! rtph264pay config-interval=1 name=pay0 pt=96 ' \
                            .format(1280, 720, self.fps, max_bitrate_rtsp)  # bitrate (kbps)
                            # '! video/x-h264,stream-format=byte-stream ' \ # diletakan setelah x264enc
    
    def on_need_data(self, src, _):
        data = self.q.get()
        buf = Gst.Buffer.new_allocate(None, len(data), None)
        buf.fill(0, data)
        buf.duration = self.duration
        timestamp = self.number_frames * self.duration
        buf.pts = buf.dts = int(timestamp)
        buf.offset = timestamp
        self.number_frames += 1
        retval = src.emit('push-buffer', buf)
        if retval != Gst.FlowReturn.OK:
            print("retval != Gst.FlowReturn.OK | retval:", retval)
        self.q.task_done()

    def do_create_element(self, _):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)

class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, q, port, stream_name, **properties):
        super(GstServer, self).__init__(**properties)
        self.factory = SensorFactory(q)
        self.factory.set_shared(True)
        self.set_service(str(port))
        self.get_mount_points().add_factory(stream_name, self.factory)
        self.attach(None)

def clearQueue(q):
    try:
        while True:
            q.get_nowait()
    except Empty:
        pass

def processAI(input_q, output_q):
    while True:
        frame = input_q.get()
        frame = cv2.flip(frame, 0)    
        frame = cv2.resize(frame, (1280, 720))
        if MODE == 1:
            frame = frame.tobytes()
        output_q.put(frame)
        input_q.task_done()

        if output_q.qsize() >= 3:
            clearQueue(output_q) 

def processGetFrame(source_input, q):
    print(source_input)
    video = cv2.VideoCapture(source_input)
    while True:
        ret, frame = video.read()
        if not ret:
            video = cv2.VideoCapture(source_input)
        else:
            q.put(frame)

        if q.qsize() >= 3:
            clearQueue(q) 

if __name__ == '__main__':
    for i, video in enumerate(video_paths):
        frame_queue = Queue()
        frame_queueS.append(frame_queue)

        output_queue = Queue()
        output_queueS.append(output_queue)
        
        thread_frame = Thread(target = processGetFrame, args = (video, frame_queue, ), daemon = True)
        thread_frame.start()
        frame_threadS.append(thread_frame)

        thread_output = Thread(target = processAI, args = (frame_queue, output_queue, ), daemon = True)
        thread_output.start()
        output_threadS.append(thread_output)
        
        output_queue.join()

    if MODE == 0:
        serve(app, host = '0.0.0.0', port = '5000', threads = 4)
    else:
        Gst.init(None)
        for j, queue in enumerate(output_queueS):
            server = GstServer(queue, portS[j], stream_nameS[j])
        serve_client = GLib.MainLoop()
        serve_client.run()

    for thread in frame_threadS:
        thread.join()

    for thread in output_threadS:
        thread.join()    