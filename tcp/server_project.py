import socket
import cv2
import json
import base64
import pickle
import numpy as np
import tensorflow as tf

class_names = ['2nd generation group', '1st generation group']

def processAI(img):
    model = tf.keras.models.load_model('model50epoch.h5')
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # create a batch
    pred = model.predict(img_array)
    score = tf.nn.softmax(pred[0])
    classes = class_names[np.argmax(score)]
    confident = round(100 * np.max(score), 2)
    return img, classes, confident

HOST = '192.168.177.160'
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

conn, addr = s.accept()

while True:
    # receive from client
    data = conn.recvfrom(1000000000) # kl di bawah ini, error data was truncated
    data = pickle.loads(data[0])
    img = base64.b64decode(data)
    img = np.frombuffer(img, dtype = np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    # process AI
    img, classes, confident = processAI(img)

    # send back to client
    result = {"classes": str(classes), "score": str(confident)}
    result = json.dumps(result)
    conn.sendall(result.encode("utf-8"))

    # to show image
    # cv2.imshow('SERVER', img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
# cv2.destroyAllWindows() # to show image