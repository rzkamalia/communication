import socket, pickle, cv2, json 
import time



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 8081
s.bind((HOST, PORT))
s.listen() 
conn, addr = s.accept()
with conn: 
    print(f"connected by {addr}")
    i = 0
    while True:
        jsonResult = {"counting":str(i), "second":str(time.time())}
        jsonResult = json.dumps(jsonResult)
        i = i + 1
        x = conn.recvfrom(1000000)
        data = x[0]
        data = pickle.loads(data)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        data = cv2.resize(data,(320,320))
        send = conn.sendall(bytes(jsonResult,encoding="utf-8"))
        cv2.imshow('server', data) #to open image
        if cv2.waitKey(1)==13:
            break
cv2.destroyAllWindows()

        