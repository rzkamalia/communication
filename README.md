**flask_form** = folder for "mini" form of sentiment analysis program. running the program:
```
python3 app.py
```
**flask_and_rtsp.py** = rtsp_and_cctv_thread.py + mode flask.

**flask_only.py** = "introduction" streaming one video with flask.

**flask_toggle.py** = flask with toggle.

**rtsp_and_cctv_thread.py** = streaming multi-video with one python file, same process AI for all video, input process AI from queue, and serve streaming from queue of process AI result. 

**rtsp_multiple.py** = streaming multi-video with one python file, same process AI for all video, input process AI direct from video, and serve streaming direct from process AI result.

**rtsp_only.py** = "introduction" streaming one video with rtsp.

**rtsp_thread.py** = streaming multi-video with one python, same process AI fro all video, and using queue for serve frame.

**tcp** = folder for tcp communication. running the server first, then running the client.

**thread_only.py** = "introduction" thread.

**thread_queue.py** = thread with queue.