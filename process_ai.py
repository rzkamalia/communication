import cv2 
from config import *
from queue import Empty

def clearQueue(q):
    try:
        while True:
            q.get_nowait()
    except Empty:
        pass

def processAI(q):
    video = cv2.VideoCapture(source_input)
    while True:
        ret, frame = video.read()
        if not ret:
            video = cv2.VideoCapture(source_input)
        else:
            frame = cv2.flip(frame, 0)    
            q.put(frame)
        if q.qsize() >= 3:
            clearQueue(q)

def processFlip(q):
    video = cv2.VideoCapture(source_input)
    while True:
        ret, frame = video.read()
        if not ret:
            video = cv2.VideoCapture(source_input)
        else:
            frame = cv2.flip(frame, 0)    
            q.put(frame)
        if q.qsize() >= 3:
            clearQueue(q)

def processRotate(q):
    video = cv2.VideoCapture(source_input)
    while True:
        ret, frame = video.read()
        if not ret:
            video = cv2.VideoCapture(source_input)
        else:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)    
            q.put(frame)
        if q.qsize() >= 3:
            clearQueue(q)