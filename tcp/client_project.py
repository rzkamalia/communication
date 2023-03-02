import socket
import cv2
import base64
import pickle

HOST = '192.168.115.160'
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    # load image in client
    img = cv2.imread('../input/20230106_084342.jpg')
    img = cv2.resize(img, (299, 299))
    # cv2.imshow('CLIENT', img) # to show image

    # send to server
    img_str = base64.b64encode(cv2.imencode('.jpg', img)[1])
    data = pickle.dumps(img_str)
    s.sendto(data, (HOST, PORT))

    # receive message from client
    received = s.recv(1024)
    received = received.decode("utf-8")
    print(received)
    
    # to show image
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
# cv2.destroyAllWindows() # to show image