import socket
import cv2
import json
import base64

HOST = '192.168.254.160'
PORT = 9001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

img = cv2.imread('./input/20230106_084342.jpg')
img_str = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
data = {'image': img_str}
json_data = json.dumps(data) # convert dta to a JSON string
s.sendall(json_data.encode())

s.close()