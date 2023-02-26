import socket
import cv2
import json
import base64
import numpy as np

HOST = '192.168.254.160'
PORT = 9001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

conn, addr = s.accept()

data = b''
while True:
    chunk = conn.recv(4096)
    if not chunk:
        break
    data += chunk
json_data = json.loads(data.decode())
img_str = json_data['image']
img_bytes = base64.b64decode(img_str)
img_array = np.frombuffer(img_bytes, dtype = np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

img = cv2.resize(img, (299, 299)) # prepo for process AI

# process AI
import tensorflow as tf

class_names = ['2nd generation group', '1st generation group']

model = tf.keras.models.load_model('./model50epoch.h5')
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # create a batch
pred = model.predict(img_array)
score = tf.nn.softmax(pred[0])
classes = class_names[np.argmax(score)]
confident =  round(100 * np.max(score), 2)
print(f'Classes = {classes}. Score = {confident}%.')
cv2.imwrite('output.jpg', img)

conn.close()
s.close()