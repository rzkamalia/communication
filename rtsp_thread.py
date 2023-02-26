from threading import Thread
from queue import Queue, Empty

import cv2

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, q, **properties):
        super(SensorFactory, self).__init__(**properties)
        self.q = q
        self.number_frames = 0
        self.fps = frame_rate_rtsp  # depends on FPS input (15 FPS)
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

def processAI(source_input, q):
    video = cv2.VideoCapture(source_input)
    while True:
        # print('source_input', source_input)
        ret, frame = video.read()
        if not ret:
            video = cv2.VideoCapture(source_input)
        else:
            frame = cv2.flip(frame, 0)    
            frame = cv2.resize(frame, (1280, 720))
            frame = frame.tobytes()
            q.put(frame)

        if q.qsize() >= 3:
            clearQueue(q) 

video_paths = ['./input/superjunior.mp4', './input/shinee.mp4']
portS = ['5001', '5002']
stream_nameS = ['/superjunior', '/shinee']
input_queueS = []
threadS = []
frame_rate_rtsp = 15
max_bitrate_rtsp = 512

if __name__ == '__main__':
    for video in video_paths:
        input_queue = Queue()
        input_queueS.append(input_queue)
        
        thread = Thread(target = processAI, args = (video, input_queue, ), daemon = True)
        thread.start()
        threadS.append(thread)
        input_queue.join()

    Gst.init(None)
    for i, queue in enumerate(input_queueS):
        server = GstServer(queue, portS[i], stream_nameS[i])
    serve_client = GLib.MainLoop()
    serve_client.run()

    for thread in threadS:
        thread.join()
