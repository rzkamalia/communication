import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

import cv2

class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, source_input, **properties):
        super(SensorFactory, self).__init__(**properties)
        self.source_input = source_input
        self.frames = cv2.VideoCapture(self.source_input)
        self.number_frames = 0
        self.fps = frame_rate_rtsp  # depends on FPS input
        self.duration = 1 / self.fps * Gst.SECOND   # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                            'caps=video/x-raw,format=BGR,width={},height={},framerate={}/1 ' \
                            '! videoconvert ! video/x-raw,format=I420 ' \
                            '! x264enc bitrate={} tune=zerolatency speed-preset=ultrafast ' \
                            '! rtph264pay config-interval=1 name=pay0 pt=96 ' \
                            .format(1280, 720, self.fps, max_bitrate_rtsp)  # bitrate (Kbps)
                            # '! video/x-h264,stream-format=byte-stream ' \ # diletakan setelah x264enc
    
    def on_need_data(self, src, _):
        # get some data
        if self.frames.isOpened(): # ini masih bingung kenapa kl diganti while True dia error-nya itu ga ada frame
            ret, frame = self.frames.read()
            if not ret:
                self.frames = cv2.VideoCapture(self.source_input)
            else:
                # start proses AI
                frame = cv2.flip(frame, 0) 
                # end proses AI
                
                resized = cv2.resize(frame, (1280, 720))
                data = resized.tobytes()

                # push to the streaming buffer
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

    def do_create_element(self, _):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)

class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, source_input, port, stream_name, **properties):
        super(GstServer, self).__init__(**properties)
        self.factory = SensorFactory(source_input)
        self.factory.set_shared(True)
        self.set_service(str(port))
        self.get_mount_points().add_factory(stream_name, self.factory)
        self.attach(None)

video_paths = ['./input/superjunior.mp4', './input/shinee.mp4']
portS = ['5001', '5002']
stream_nameS = ['/superjunior', '/shinee']
frame_rate_rtsp = 15
max_bitrate_rtsp = 512

if __name__ == '__main__':
    Gst.init(None)
    for i, video in enumerate(video_paths):
        server = GstServer(video, portS[i], stream_nameS[i])
    serve_client = GLib.MainLoop()
    serve_client.run()